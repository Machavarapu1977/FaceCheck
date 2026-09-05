# Architecture Overview

```
             INPUT IMAGE
                  |
                  v
          FACE DETECTION (OpenCV)
                  |
                  v
       FACE EMBEDDING (512-d L2)
                  |
                  |
                  +------------------+
                  |                  |
                  v                  v
     REVERSE IMAGE SEARCH        IMAGE HASH
      (SerpAPI / Lens)           (SHA-256)
                  |
                  v
          SEARCH CANDIDATES
                  |
                  v
      CANDIDATE FACE DETECTION
                  |
                  v
      FACE EMBEDDING COMPARISON
       (Cosine Similarity)
                  |
                  v
           MATCH RANKING
      (0.6*Face + 0.4*Search)
                  |
                  v
           MATCH METADATA
                  |
                  v
         CANONICAL DATA HASH
             (SHA-256)
                  |
                  v
             BLOCKCHAIN
    (FaceVerificationRegistry.sol)
                  |
                  v
         TAMPER VERIFICATION
```

## System Components

1. **Face Detection & Embedding Engine**:
   - `detector.py`: Detects single/multiple faces returning bounding box coordinates `(x, y, w, h)`.
   - `embedding.py`: Extracts 512-dimensional normalized face vectors and calculates cosine similarity scores.

2. **Reverse Image Search Provider Abstraction**:
   - `base.py`: Defines standard `BaseReverseImageSearchProvider` interface.
   - `serpapi_provider.py`: Connects directly to SerpAPI Google Lens API.
   - `provider.py`: Provides factory to instantiate real vs mock fallback providers.

3. **Candidate Matching & Ranking Engine**:
   - `matcher.py`: Evaluates reverse search candidates, downloads public thumbnails, runs face detection/similarity on candidate crops, and computes transparent `combined_score = 0.6 * face_similarity + 0.4 * reverse_search_relevance`.

4. **Canonical Hashing**:
   - `hasher.py`: Computes deterministic SHA-256 hashes for raw input image bytes and canonicalized JSON data.

5. **Blockchain Smart Contract**:
   - `FaceVerificationRegistry.sol`: EVM smart contract storing tamper-evident hashes on Sepolia / Polygon Amoy / Hardhat testnet.
