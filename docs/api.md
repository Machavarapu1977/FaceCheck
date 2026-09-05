# API Documentation

## Endpoints

### 1. Upload & Execute Verification Pipeline
`POST /api/verify`

**Request:** `multipart/form-data` with `file` (JPG, JPEG, PNG).

**Response (JSON):**
```json
{
  "status": "MATCH_FOUND",
  "face": {
    "faces_detected_count": 1,
    "primary_face_bbox": { "x": 10, "y": 20, "width": 100, "height": 100 },
    "embedding_generated": true,
    "embedding_preview": [0.123, -0.456, 0.789, 0.012, -0.345]
  },
  "reverse_search": {
    "provider": "serpapi",
    "candidates_found_count": 3
  },
  "best_match": {
    "url": "https://www.linkedin.com/in/sample",
    "source_domain": "linkedin.com",
    "title": "Sample Profile | LinkedIn",
    "face_similarity": 0.87,
    "reverse_search_relevance": 0.92,
    "combined_score": 0.89,
    "match": true
  },
  "top_candidates": [...],
  "hashes": {
    "image_hash": "0x...",
    "match_data_hash": "0x...",
    "record_hash": "0x...",
    "canonical_data": {...}
  },
  "blockchain": {
    "transaction_hash": "0x...",
    "block_number": 104250,
    "record_id": "0x...",
    "contract_address": "0x...",
    "chain_id": 1337,
    "submitter_address": "0x...",
    "timestamp": 1756800000
  }
}
```

### 2. Retrieve Blockchain Verification Record
`GET /api/verification/{record_id}`

### 3. Verify Local Hashes Against Blockchain Record
`POST /api/verification/verify`

**Request Body:**
```json
{
  "record_id": "0x...",
  "image_hash": "0x...",
  "match_data_hash": "0x...",
  "record_hash": "0x..."
}
```

### 4. Health Check
`GET /api/health`
