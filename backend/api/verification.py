from fastapi import APIRouter, HTTPException
from backend.services.blockchain.web3_client import Web3Client
from backend.services.hashing.hasher import CanonicalHasher
from backend.models.schemas import (
    VerificationLookupResponse, VerificationCheckRequest, VerificationCheckResponse
)

router = APIRouter()

@router.get("/{record_id}", response_model=VerificationLookupResponse)
async def get_verification_record(record_id: str):
    try:
        web3_client = Web3Client()
        record = web3_client.get_verification_record(record_id)
        return VerificationLookupResponse(
            record_id=record["record_id"],
            image_hash=record["image_hash"],
            match_data_hash=record["match_data_hash"],
            record_hash=record["record_hash"],
            match_status=record["match_status"],
            result_url=record["result_url"],
            timestamp=record["timestamp"],
            submitter=record["submitter"],
            is_valid=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=444 if "not found" in str(e).lower() else 500,
            detail={"error": "RECORD_NOT_FOUND", "message": str(e)}
        )

@router.post("/verify", response_model=VerificationCheckResponse)
async def verify_local_record(request: VerificationCheckRequest):
    try:
        web3_client = Web3Client()
        is_valid = web3_client.verify_record_on_chain(
            record_id_hex=request.record_id,
            image_hash=request.image_hash,
            match_data_hash=request.match_data_hash,
            record_hash=request.record_hash
        )
        
        msg = "Verification SUCCESS: Local image and match metadata match the tamper-evident blockchain record." if is_valid else "Verification FAILED: Local data does not match recorded blockchain hashes. Data may be tampered!"

        return VerificationCheckResponse(
            record_id=request.record_id,
            is_valid=is_valid,
            message=msg
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "VERIFICATION_ERROR", "message": str(e)}
        )
