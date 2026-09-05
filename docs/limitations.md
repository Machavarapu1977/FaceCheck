# Known Limitations & Security Considerations

## Limitations

1. **Reverse Image Search Rate Limits & Coverage**:
   - External reverse image search providers (e.g. SerpAPI Google Lens, TinEye) impose API rate limits and free-tier quotas.
   - Public search engines only index publicly available web pages. Private or restricted social media accounts cannot be indexed or retrieved.

2. **Facial Recognition Scenarios**:
   - Face similarity scores rely on optical clarity, lighting, pose alignment, and resolution.
   - Facial similarity scores represent mathematical distance between vector embeddings and **do NOT claim absolute real-world human identity verification**.

3. **Blockchain Testnets**:
   - Smart contracts deployed to EVM testnets (Sepolia, Amoy, Hardhat) demonstrate tamper-evident data integrity but are subject to testnet faucet availability and RPC latency.

## Privacy & Security

- **No Raw Biometrics On-Chain**: Raw facial photographs and full biometric embedding vectors are NEVER saved to the blockchain.
- **Cryptographic Hashes**: Only one-way SHA-256 hashes (`image_hash`, `match_data_hash`, `record_hash`) are stored on-chain.
- **Key Safety**: Private keys are managed strictly via local environment variables `.env` and never logged or committed to source control.
