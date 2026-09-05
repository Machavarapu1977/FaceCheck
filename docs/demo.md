# Face ID + Blockchain Verification Step-by-Step Demo Walkthrough

This document outlines the step-by-step verification procedure for executing an end-to-end demo of the **Face ID + Blockchain Verification Pipeline**.

---

## Step 1: Launch Local EVM Testnet Node

Open Terminal 1:
```bash
cd contracts
npx hardhat node
```
*Output displays local RPC endpoint `http://127.0.0.1:8545` and test accounts.*

---

## Step 2: Deploy FaceVerificationRegistry Contract

Open Terminal 2:
```bash
cd contracts
npx hardhat run scripts/deploy.js --network hardhat
```
*Output:*
`FaceVerificationRegistry deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3`

---

## Step 3: Launch FastAPI Backend Server

Open Terminal 3:
```bash
# Ensure virtualenv is activated and requirements installed
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*FastAPI server initializes and connects to Web3 client on port 8000.*

---

## Step 4: Launch Vite React Frontend

Open Terminal 4:
```bash
cd frontend
npm run dev
```
*Vite development server serves UI at `http://localhost:3000`.*

---

## Step 5: Execute End-to-End Pipeline in Web Interface

1. Navigate to `http://localhost:3000` in Google Chrome or Microsoft Edge.
2. Drag and drop a facial photograph (e.g. `portrait.jpg`).
3. Click **"Run Face Verification Pipeline"**.
4. Observe step-by-step execution:
   - **Face Detection**: Highlights primary face bounding box `(x, y, w, h)`.
   - **Embedding Generation**: Displays first 5 normalized dimensions of 512-d facial embedding.
   - **Genuine Reverse Image Search**: Queries search provider and lists candidate web & social media matches with similarity scores.
   - **Combined Ranking**: Ranks candidates transparently.
   - **SHA-256 Hashes**: Calculates `image_hash`, `match_data_hash`, and combined `record_hash`.
   - **Blockchain Confirmation**: Returns transaction receipt, block number, and `record_id`.
5. Click **"Verify On-Chain Record"** to execute the tamper-evident validation modal.
