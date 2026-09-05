# Face ID + Blockchain Verification

A full-stack AI/ML + blockchain pipeline that detects faces in an uploaded photograph, performs **genuine reverse image search** via Google Lens (SerpAPI), identifies social-media matches, computes cryptographic SHA-256 hashes of the verification record, and stores a tamper-evident record on an **EVM-compatible blockchain** (local Hardhat or Ethereum Sepolia testnet).

---

## Architecture

```
Frontend (React/Vite)
    │  POST /api/verify (multipart: image + selected_face_index)
    ▼
Backend (FastAPI / Python)
    ├── 1. Validate & hash input image (SHA-256)
    ├── 2. Detect ALL faces (OpenCV Haar Cascade)
    ├── 3. Crop selected face → generate 512-d L2-normalized embedding (FaceNet-style)
    ├── 4. Genuine reverse image search → SerpAPI Google Lens (uploads image to tmpfiles.org → GET url=)
    ├── 5. Social platform detection (Instagram, Facebook, X, LinkedIn, TikTok, YouTube, Reddit …)
    ├── 6. Honest facial similarity: cosine similarity if candidate face extractable, else "UNAVAILABLE_MEDIA"
    ├── 7. Canonical SHA-256 hashing (deterministic JSON → match_data_hash, record_hash)
    └── 8. EVM smart contract → FaceVerificationRegistry.createVerificationRecord(...)
            └── Returns: real tx_hash, block_number, network_name, explorer_url
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Axios, Lucide-React |
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Face Detection | OpenCV Haar Cascade (`haarcascade_frontalface_default.xml`) |
| Face Embedding | FaceEmbedder — 512-dimensional L2-normalized vector |
| Reverse Image Search | SerpAPI Google Lens (`engine=google_lens`, GET with `url=`) |
| Hashing | Python `hashlib` SHA-256 (canonical JSON, sorted keys) |
| Smart Contract | Solidity 0.8.20 — `FaceVerificationRegistry` |
| Blockchain (Dev) | Hardhat local node — Chain ID 1337 |
| Blockchain (Production) | Ethereum Sepolia Testnet — Chain ID 11155111 |
| Web3 Library | web3.py |

---

## Face Detection Method

OpenCV Haar Cascade frontal face detector (`haarcascade_frontalface_default.xml`) detects all faces in the input photograph. Results are sorted by face area descending (largest face first). The user can select which detected face to use for the search.

- **Zero faces** → pipeline halts with `"Face detection failed — no face found."`
- **One face** → automatically selected
- **Multiple faces** → UI shows `[Face #1] [Face #2] …` selection buttons

---

## Face Embedding Model

A 512-dimensional L2-normalized face embedding vector is generated from the cropped face region using the `FaceEmbedder` service. This embedding is used for **local cosine similarity computation only** — it is **never stored on-chain** (only SHA-256 hashes are stored).

---

## Reverse Image Search Provider

**SerpAPI Google Lens** (`engine=google_lens`)

1. The uploaded image is temporarily hosted at `https://tmpfiles.org` to generate a direct public URL.
2. A `GET https://serpapi.com/search.json?engine=google_lens&url=<image_url>&api_key=<key>` request is made.
3. Real `visual_matches` results are returned (title, URL, source domain, thumbnail, relevance score).
4. Results are **never hardcoded** — every result comes from the live Google Lens index.

**Sign up**: https://serpapi.com — Free plan includes **250 searches/month**.

---

## Social Media Result Handling

Each returned URL is classified by domain pattern:

| Platform | Pattern matched |
|---|---|
| Instagram | `instagram.com` |
| Facebook | `facebook.com`, `fb.com` |
| X (Twitter) | `x.com`, `twitter.com` |
| LinkedIn | `linkedin.com` |
| TikTok | `tiktok.com` |
| YouTube | `youtube.com`, `youtu.be` |
| Reddit | `reddit.com` |
| Pinterest | `pinterest.com` |

The UI displays a **Platform badge** per result, and counts total social media matches separately.

---

## Facial Similarity Calculation

The system **does not fabricate similarity scores**. For each reverse-image-search result:

1. **If a candidate thumbnail image is accessible and contains a detectable face:**
   - Download thumbnail → detect face → generate 512-d embedding → compute **cosine similarity** with the input face embedding.
   - Displayed as: `"Face Cosine Similarity: XX%"` with threshold `60%`.

2. **If no usable face is found in the thumbnail (no face detected or download failed):**
   - Displayed as: `"Reverse-image result found; facial similarity could not be independently calculated from the returned media."`

**No estimated or fabricated scores are ever displayed.**

---

## Hashing Mechanism

Three cryptographic SHA-256 hashes are generated:

| Hash | Source |
|---|---|
| `image_hash` | SHA-256 of raw input image bytes |
| `match_data_hash` | SHA-256 of canonicalized JSON match data (sorted keys, deterministic) |
| `record_hash` | SHA-256 of `image_hash + match_data_hash + timestamp + result_url` |

Canonical match data JSON (sorted, deterministic):
```json
{
  "best_match_title": "...",
  "best_match_url": "...",
  "combined_score": 0.0,
  "cosine_similarity": null,
  "match_status": "...",
  "platform": "...",
  "timestamp": 1234567890
}
```

Raw biometric embeddings are **never stored** on-chain.

---

## Smart Contract

**Contract**: `FaceVerificationRegistry.sol`  
**Language**: Solidity 0.8.20

Key function:
```solidity
function createVerificationRecord(
    bytes32 imageHash,
    bytes32 matchDataHash,
    bytes32 recordHash,
    string calldata matchStatus,
    string calldata resultUrl
) external returns (bytes32 recordId)
```

Event emitted:
```solidity
event VerificationRecorded(
    bytes32 indexed recordId,
    bytes32 indexed imageHash,
    bytes32 matchDataHash,
    bytes32 recordHash,
    string matchStatus,
    string resultUrl,
    uint256 timestamp,
    address indexed submitter
);
```

On-chain verification:
```solidity
function verifyRecord(bytes32 recordId, bytes32 imageHash, bytes32 matchDataHash, bytes32 recordHash) external view returns (bool)
```

---

## Blockchain Network

| Environment | Network | Chain ID | RPC |
|---|---|---|---|
| Development | Local Hardhat | 1337 | `http://127.0.0.1:8545` |
| Production | Ethereum Sepolia | 11155111 | Infura / Alchemy |

### Switching to Ethereum Sepolia (Recommended for judges)

1. **Create a testnet wallet** — use MetaMask, never your mainnet wallet.
2. **Get Sepolia ETH** from https://sepoliafaucet.com
3. **Get an RPC endpoint** from https://infura.io or https://alchemy.com (free tier)
4. **Deploy the contract** to Sepolia:
   ```bash
   cd contracts
   npx hardhat run scripts/deploy.js --network sepolia
   ```
5. **Update `.env`**:
   ```env
   BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
   BLOCKCHAIN_PRIVATE_KEY=0xYOUR_TESTNET_PRIVATE_KEY
   CONTRACT_ADDRESS=0xDEPLOYED_CONTRACT_ADDRESS
   CHAIN_ID=11155111
   EXPLORER_URL=https://sepolia.etherscan.io
   ```

---

## Contract Deployment

### Local Hardhat (Development)
```bash
# Terminal 1 — start local blockchain node
cd contracts
npx hardhat node

# Terminal 2 — deploy contract
npx hardhat run scripts/deploy.js --network localhost
```
Contract address is automatically saved to `contracts/deployment.json` and auto-loaded by the backend.

### Ethereum Sepolia (Production)
Add `sepolia` network to `contracts/hardhat.config.js`, then:
```bash
npx hardhat run scripts/deploy.js --network sepolia
```
Copy the deployed contract address to `.env` as `CONTRACT_ADDRESS`.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `SERPAPI_KEY` | Yes (real mode) | SerpAPI key for Google Lens search |
| `DEMO_MODE` | No | `true` = mock results, `false` = real search |
| `BLOCKCHAIN_RPC_URL` | Yes | JSON-RPC endpoint |
| `BLOCKCHAIN_PRIVATE_KEY` | Yes | Testnet wallet private key (never mainnet!) |
| `CONTRACT_ADDRESS` | Yes | Deployed `FaceVerificationRegistry` address |
| `CHAIN_ID` | Yes | `1337` (local) or `11155111` (Sepolia) |
| `EXPLORER_URL` | No | Base URL for blockchain explorer (e.g. `https://sepolia.etherscan.io`) |

---

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup
```bash
cd FaceCheck
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Contracts Setup
```bash
cd contracts
npm install
```

---

## How to Run

### Step 1 — Start local blockchain node (development only)
```bash
cd contracts
npx hardhat node
```

### Step 2 — Deploy contract (first time or after node restart)
```bash
# In a new terminal, from contracts/
npx hardhat run scripts/deploy.js --network localhost
```

### Step 3 — Configure .env
```bash
# Root of project
cp .env.example .env
# Edit .env — add SERPAPI_KEY and set DEMO_MODE=false
```

### Step 4 — Start Backend
```bash
# From project root
python -m uvicorn backend.main:app --reload --port 8000
```

### Step 5 — Start Frontend
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## How to Execute the Complete Pipeline

1. Open http://localhost:5173
2. **Upload** a portrait photograph (JPG/PNG, max 10MB)
3. If **multiple faces** are detected, click `[Face #1]`, `[Face #2]` etc. to select the target face
4. Click **Run Face Verification Pipeline**
5. Watch the pipeline progress bar: `UPLOAD → FACE DETECTION → EMBEDDING → REVERSE IMAGE SEARCH → MATCH VALIDATION → BLOCKCHAIN → VERIFIED`
6. Review results:
   - **Section 2**: Face count, bounding box, 512-d embedding status
   - **Section 3**: Reverse image search results with platform badges, thumbnails, honest similarity
   - **Section 4**: SHA-256 hashes, blockchain receipt (tx hash, block number, network, record ID)
7. Click **Verify On-Chain Record** to perform a live blockchain query
8. Click **View Transaction on Blockchain Explorer** to open Etherscan (Sepolia) or local explorer

---

## How to Verify the Blockchain Transaction

### Via the UI
Click **"Verify On-Chain Record"** — the backend calls `FaceVerificationRegistry.verifyRecord(...)` via Web3 and displays `✓ ON-CHAIN RECORD VERIFIED` or `✗ VERIFICATION FAILED`.

### Manually (Sepolia)
1. Copy the **Tx Hash** from the UI
2. Go to https://sepolia.etherscan.io
3. Paste the Tx Hash in the search bar
4. Verify: correct contract address, event logs, timestamp, and hash values

---

## Known Limitations

1. **Face detection**: OpenCV Haar Cascade is a classical detector — it may miss faces in non-frontal poses, low resolution, or heavy occlusion. A deep-learning model (e.g. MTCNN, RetinaFace) would be more robust.
2. **Facial similarity**: Cosine similarity is only computed when a candidate thumbnail contains a detectable face. Many web thumbnails do not contain usable face images — in these cases similarity is reported as unavailable rather than fabricated.
3. **Reverse image search**: Google Lens does not always return social-media profile URLs directly — it returns URLs where the image appears on the web. Social-media platforms (e.g. Instagram) often block crawling.
4. **Testnet**: This uses a public EVM testnet (Sepolia). Testnet ETH has no real value. Do not use mainnet.
5. **Temporary image hosting**: The uploaded image is temporarily hosted on `tmpfiles.org` to generate a public URL for Google Lens. The image is not permanently stored.
6. **SerpAPI credits**: The free tier includes 250 searches/month. High usage requires a paid plan.

---

## Privacy Considerations

- **No biometric data is stored on-chain** — only SHA-256 hashes of match data.
- Raw face embeddings are computed in-memory only and are never persisted.
- The uploaded photograph is never permanently stored — it is processed in-memory.
- A temporary public URL is generated for the image (via `tmpfiles.org`) for Google Lens only — this URL is ephemeral.
- Face recognition and reverse image search can produce **false positives** and **false negatives**. Results should be treated as investigative leads, not definitive identifications.
- This application is a **testnet demonstration** and should not be used for real identity verification without proper legal, ethical, and technical review.

---

## License

MIT
