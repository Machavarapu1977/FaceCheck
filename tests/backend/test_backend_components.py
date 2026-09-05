import pytest
import numpy as np
import cv2
from backend.utils.image_utils import validate_image_file, bytes_to_cv2
from backend.services.hashing.hasher import CanonicalHasher
from backend.services.face_detection.embedding import FaceEmbedder
from backend.services.candidate_matching.matcher import CandidateMatcher

def test_image_validation():
    # Valid small JPG
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, encoded = cv2.imencode(".jpg", img)
    valid_bytes = encoded.tobytes()
    
    # Should pass without exception
    validate_image_file(valid_bytes, "test.jpg")
    
    with pytest.raises(ValueError):
        validate_image_file(valid_bytes, "test.txt")

def test_canonical_hasher():
    img_bytes = b"sample_image_data_bytes"
    h1 = CanonicalHasher.hash_image_bytes(img_bytes)
    h2 = CanonicalHasher.hash_image_bytes(img_bytes)
    assert h1 == h2
    assert h1.startswith("0x")

    data = {"b": 2, "a": 1}
    hash_str, _ = CanonicalHasher.hash_canonical_json(data)
    
    data_reordered = {"a": 1, "b": 2}
    hash_str_2, _ = CanonicalHasher.hash_canonical_json(data_reordered)
    
    # Hashing canonicalized JSON must be deterministic regardless of dictionary order
    assert hash_str == hash_str_2

def test_face_embedder_cosine_similarity():
    embedder = FaceEmbedder(512)
    
    # Synthesize face crop 1
    crop1 = np.ones((112, 112, 3), dtype=np.uint8) * 120
    crop2 = np.ones((112, 112, 3), dtype=np.uint8) * 120
    
    emb1 = embedder.generate_embedding(crop1)
    emb2 = embedder.generate_embedding(crop2)
    
    assert len(emb1) == 512
    sim = embedder.calculate_similarity(emb1, emb2)
    assert sim >= 0.99  # Identical crops should yield ~1.0 similarity

def test_candidate_ranking_logic():
    matcher = CandidateMatcher(
        face_similarity_threshold=0.60,
        reverse_search_threshold=0.50,
        face_weight=0.60,
        image_search_weight=0.40
    )
    
    mock_candidates = [
        {
            "title": "Profile A",
            "url": "https://example.com/a",
            "source_domain": "example.com",
            "image_url": None,
            "reverse_search_relevance": 0.90
        },
        {
            "title": "Profile B",
            "url": "https://example.com/b",
            "source_domain": "example.com",
            "image_url": None,
            "reverse_search_relevance": 0.40
        }
    ]
    
    dummy_emb = np.zeros(512, dtype=np.float32)
    ranked, best, status = matcher.process_and_rank_candidates(dummy_emb, mock_candidates)
    
    assert len(ranked) == 2
    assert status in ["MATCH_FOUND", "NO_MATCH_FOUND"]
