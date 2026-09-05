import time
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.utils.image_utils import validate_image_file, bytes_to_cv2, crop_face, cv2_to_bytes
from backend.services.face_detection.detector import OpenCVFaceDetector
from backend.services.face_detection.embedding import FaceEmbedder
from backend.services.reverse_image_search.provider import ReverseSearchProviderFactory
from backend.services.candidate_matching.matcher import CandidateMatcher
from backend.services.hashing.hasher import CanonicalHasher
from backend.services.blockchain.web3_client import Web3Client
from backend.config import settings
from backend.models.schemas import (
    VerificationResponse, FaceDetectionResult, BoundingBox, HashInfo,
    CandidateResult, BlockchainInfo
)

router = APIRouter()
logger = logging.getLogger("upload_api")


@router.post("/verify", response_model=VerificationResponse)
async def process_verification(
    file: UploadFile = File(...),
    selected_face_index: Optional[int] = Form(0)
):
    try:
        contents = await file.read()
        validate_image_file(contents, file.filename)

        logger.info(f"[INPUT] Received image file '{file.filename}' ({len(contents)} bytes)")

        # Step 1: Compute SHA-256 Image Hash
        image_hash = CanonicalHasher.hash_image_bytes(contents)
        logger.info(f"[HASH] Input image SHA-256: {image_hash}")

        # Step 2: Detect ALL faces
        img_cv2 = bytes_to_cv2(contents)
        detector = OpenCVFaceDetector()
        faces = detector.detect_faces(img_cv2)

        faces_count = len(faces)
        logger.info(f"[FACE] Detected {faces_count} face(s) in input photograph")

        if faces_count == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "NO_FACE_DETECTED",
                    "message": "Face detection failed — no face found in the uploaded photograph. Please upload a clear image containing a facial portrait."
                }
            )

        # Build bounding box objects for all detected faces
        all_face_bboxes = [
            BoundingBox(x=f[0], y=f[1], width=f[2], height=f[3])
            for f in faces
        ]

        # Validate and clamp selected_face_index
        if selected_face_index is None or selected_face_index < 0:
            selected_face_index = 0
        if selected_face_index >= faces_count:
            selected_face_index = 0

        selected_bbox_tuple = faces[selected_face_index]
        primary_bbox_obj = all_face_bboxes[selected_face_index]

        # Crop selected face
        face_crop = crop_face(img_cv2, selected_bbox_tuple)

        # Step 3: Face Embedding Generation
        embedder = FaceEmbedder()
        embedding = embedder.generate_embedding(face_crop)
        logger.info(f"[FACE] Generated normalized 512-d face embedding vector for face #{selected_face_index}.")

        # Step 4: Genuine Reverse Image Search
        search_provider = ReverseSearchProviderFactory.get_provider(
            provider_name=settings.REVERSE_SEARCH_PROVIDER,
            api_key=settings.SERPAPI_KEY,
            demo_mode=settings.DEMO_MODE
        )

        # Pass the full source image bytes to reverse image search so Google Lens
        # matches the actual full profile photo and context on the web (e.g., LinkedIn)
        # rather than searching tight cropped faces against random portrait galleries.
        raw_candidates = search_provider.search(contents)

        # If full image search returned 0 results, fall back to searching the face crop
        if not raw_candidates:
            logger.info("[SEARCH] Full image search returned 0 candidates; trying face crop fallback...")
            face_crop_bytes = cv2_to_bytes(face_crop)
            raw_candidates = search_provider.search(face_crop_bytes)

        logger.info(f"[SEARCH] Reverse image search returned {len(raw_candidates)} candidate results.")

        # Step 5: Candidate Matching & Social Platform Identification
        matcher = CandidateMatcher(
            face_similarity_threshold=settings.FACE_SIMILARITY_THRESHOLD,
            reverse_search_threshold=settings.REVERSE_SEARCH_THRESHOLD,
            face_weight=settings.FACE_WEIGHT,
            image_search_weight=settings.IMAGE_SEARCH_WEIGHT
        )

        candidates_list, best_match_dict, match_status = matcher.process_and_rank_candidates(
            embedding, raw_candidates
        )
        logger.info(f"[MATCH] Candidate evaluation status: {match_status}")

        # Count social media matches
        social_platforms = {"Instagram", "Facebook", "X (Twitter)", "LinkedIn", "TikTok", "YouTube", "Reddit", "Pinterest"}
        social_media_count = sum(
            1 for c in candidates_list
            if c.get("platform", "Web Result") in social_platforms
        )

        # Format candidates
        top_candidates = [CandidateResult(**c) for c in candidates_list]
        best_match = CandidateResult(**best_match_dict) if best_match_dict else None

        # Step 6: Canonical Data & Cryptographic Hash Generation
        timestamp = int(time.time())
        result_url = best_match.url if best_match else "N/A"

        match_data_payload = {
            "match_status": match_status,
            "best_match_url": result_url,
            "best_match_title": best_match.title if best_match else "N/A",
            "platform": best_match.platform if best_match else "N/A",
            "combined_score": best_match.combined_score if best_match else 0.0,
            "cosine_similarity": best_match.cosine_similarity if best_match else None,
            "timestamp": timestamp
        }

        match_data_hash, canonical_data = CanonicalHasher.hash_canonical_json(match_data_payload)
        record_hash = CanonicalHasher.compute_record_hash(image_hash, match_data_hash, timestamp, result_url)
        logger.info(f"[HASH] Canonical Match Data Hash: {match_data_hash}")
        logger.info(f"[HASH] Combined Verification Record Hash: {record_hash}")

        # Step 7: Blockchain Record Submission
        web3_client = Web3Client()
        bc_receipt = web3_client.submit_verification_record(
            image_hash=image_hash,
            match_data_hash=match_data_hash,
            record_hash=record_hash,
            match_status=match_status,
            result_url=result_url
        )

        blockchain_info = BlockchainInfo(**bc_receipt) if bc_receipt else None

        return VerificationResponse(
            status=match_status,
            face=FaceDetectionResult(
                faces_detected_count=faces_count,
                primary_face_bbox=primary_bbox_obj,
                all_faces=all_face_bboxes,
                selected_face_index=selected_face_index,
                embedding_generated=True,
                embedding_preview=embedding[:5].tolist()
            ),
            reverse_search={
                "provider": settings.REVERSE_SEARCH_PROVIDER,
                "candidates_found_count": len(candidates_list),
                "social_media_matches": social_media_count,
            },
            best_match=best_match,
            top_candidates=top_candidates,
            hashes=HashInfo(
                image_hash=image_hash,
                match_data_hash=match_data_hash,
                record_hash=record_hash,
                canonical_data=canonical_data
            ),
            blockchain=blockchain_info
        )

    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"[ERROR] Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail={"error": "INVALID_INPUT", "message": str(ve)})
    except Exception as e:
        logger.error(f"[ERROR] Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "PIPELINE_FAILURE", "message": str(e)})
