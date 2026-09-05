from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int

class FaceDetectionResult(BaseModel):
    faces_detected_count: int
    primary_face_bbox: Optional[BoundingBox] = None
    all_faces: List[BoundingBox] = []
    selected_face_index: int = 0
    embedding_generated: bool
    embedding_preview: Optional[List[float]] = None

class CandidateResult(BaseModel):
    url: str
    source_domain: str
    title: str
    platform: str = "Web Result"
    image_url: Optional[str] = None
    thumbnail: Optional[str] = None
    face_similarity: float = 0.0
    reverse_search_relevance: float = 0.0
    combined_score: float = 0.0
    similarity_calc_status: str = "CALCULATED"  # "CALCULATED" or "UNAVAILABLE_MEDIA"
    cosine_similarity: Optional[float] = None
    match: bool = False

class HashInfo(BaseModel):
    image_hash: str
    match_data_hash: str
    record_hash: str
    canonical_data: Dict[str, Any]

class BlockchainInfo(BaseModel):
    transaction_hash: str
    block_number: Optional[int] = None
    record_id: str
    contract_address: str
    chain_id: int
    network_name: str = "Local Hardhat Testnet"
    submitter_address: str
    timestamp: int
    explorer_url: Optional[str] = None

class VerificationResponse(BaseModel):
    status: str  # "MATCH_FOUND" or "NO_MATCH_FOUND"
    face: FaceDetectionResult
    reverse_search: Dict[str, Any]
    best_match: Optional[CandidateResult] = None
    top_candidates: List[CandidateResult] = []
    hashes: HashInfo
    blockchain: Optional[BlockchainInfo] = None

class VerificationLookupResponse(BaseModel):
    record_id: str
    image_hash: str
    match_data_hash: str
    record_hash: str
    match_status: str
    result_url: str
    timestamp: int
    submitter: str
    is_valid: bool

class VerificationCheckRequest(BaseModel):
    record_id: str
    image_hash: str
    match_data_hash: str
    record_hash: str

class VerificationCheckResponse(BaseModel):
    record_id: str
    is_valid: bool
    message: str
