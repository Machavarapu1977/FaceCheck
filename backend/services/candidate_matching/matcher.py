import requests
import numpy as np
import cv2
from typing import List, Dict, Any, Tuple, Optional
from backend.services.face_detection.detector import OpenCVFaceDetector
from backend.services.face_detection.embedding import FaceEmbedder
from backend.utils.image_utils import bytes_to_cv2, crop_face

class CandidateMatcher:
    def __init__(
        self,
        face_similarity_threshold: float = 0.65,
        reverse_search_threshold: float = 0.50,
        face_weight: float = 0.70,
        image_search_weight: float = 0.30
    ):
        self.face_similarity_threshold = face_similarity_threshold
        self.reverse_search_threshold = reverse_search_threshold
        self.face_weight = face_weight
        self.image_search_weight = image_search_weight
        
        self.detector = OpenCVFaceDetector()
        self.embedder = FaceEmbedder()

    def download_candidate_image(self, image_url: str) -> Optional[np.ndarray]:
        if not image_url:
            return None
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(image_url, headers=headers, timeout=6)
            if resp.status_code == 200 and len(resp.content) > 0:
                return bytes_to_cv2(resp.content)
        except Exception:
            pass
        return None

    def detect_platform(self, url: str, domain: str) -> str:
        u = (url or "").lower()
        d = (domain or "").lower()
        if "instagram.com" in u or "instagram.com" in d:
            return "Instagram"
        if "facebook.com" in u or "fb.com" in u or "facebook.com" in d:
            return "Facebook"
        if "x.com" in u or "twitter.com" in u or "x.com" in d or "twitter.com" in d:
            return "X (Twitter)"
        if "linkedin.com" in u or "linkedin.com" in d:
            return "LinkedIn"
        if "tiktok.com" in u or "tiktok.com" in d:
            return "TikTok"
        if "youtube.com" in u or "youtu.be" in u or "youtube.com" in d:
            return "YouTube"
        if "reddit.com" in u or "reddit.com" in d:
            return "Reddit"
        if "pinterest.com" in u or "pinterest.com" in d:
            return "Pinterest"
        if "github.com" in u or "github.com" in d:
            return "GitHub"
        return "Web Result"

    def match_candidate(
        self,
        input_embedding: np.ndarray,
        candidate_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = candidate_item.get("url", "")
        source_domain = candidate_item.get("source_domain", "")
        platform = self.detect_platform(url, source_domain)
        
        image_url = candidate_item.get("image_url")
        reverse_relevance = float(candidate_item.get("reverse_search_relevance", 0.50))
        
        face_sim = 0.0
        similarity_calc_status = "UNAVAILABLE_MEDIA"
        cosine_similarity = None
        
        candidate_img = self.download_candidate_image(image_url)
        
        if candidate_img is not None:
            faces = self.detector.detect_faces(candidate_img)
            if len(faces) > 0:
                # Compare against all detected faces in the candidate image (e.g. group photos, band posters)
                best_sim = 0.0
                for face_bbox in faces:
                    face_crop = crop_face(candidate_img, face_bbox)
                    cand_embedding = self.embedder.generate_embedding(face_crop)
                    sim_val = self.embedder.calculate_similarity(input_embedding, cand_embedding)
                    if sim_val > best_sim:
                        best_sim = sim_val
                
                face_sim = round(float(best_sim), 4)
                cosine_similarity = face_sim
                similarity_calc_status = "CALCULATED"

        if similarity_calc_status == "CALCULATED":
            combined_score = round(
                (self.face_weight * face_sim) + (self.image_search_weight * reverse_relevance),
                4
            )
            # Biometric verification strictly requires face_similarity to meet threshold
            is_match = (face_sim >= self.face_similarity_threshold)
        else:
            combined_score = round(reverse_relevance * 0.40, 4)
            is_match = False

        return {
            "url": url,
            "source_domain": source_domain,
            "title": candidate_item.get("title", ""),
            "platform": platform,
            "image_url": image_url,
            "thumbnail": image_url,
            "face_similarity": face_sim,
            "reverse_search_relevance": reverse_relevance,
            "combined_score": combined_score,
            "similarity_calc_status": similarity_calc_status,
            "cosine_similarity": cosine_similarity,
            "match": is_match
        }

    def process_and_rank_candidates(
        self,
        input_embedding: np.ndarray,
        raw_candidates: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]], str]:
        processed_candidates = []
        for cand in raw_candidates:
            result = self.match_candidate(input_embedding, cand)
            processed_candidates.append(result)

        # Sort candidates: genuine matches first, then descending by combined_score
        processed_candidates.sort(
            key=lambda x: (1 if x["match"] else 0, x["face_similarity"], x["combined_score"]),
            reverse=True
        )

        best_match = None
        status = "NO_MATCH_FOUND"

        matching_candidates = [c for c in processed_candidates if c["match"]]
        if matching_candidates:
            best_match = matching_candidates[0]
            status = "MATCH_FOUND"

        return processed_candidates, best_match, status
