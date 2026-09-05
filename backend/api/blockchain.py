from fastapi import APIRouter, HTTPException
from backend.services.blockchain.web3_client import Web3Client
from backend.config import settings

router = APIRouter()


@router.get("/status")
async def get_blockchain_status():
    web3_client = Web3Client()
    connected = web3_client.is_connected()
    return {
        "connected": connected,
        "rpc_url": settings.BLOCKCHAIN_RPC_URL,
        "chain_id": settings.CHAIN_ID,
        "network_name": web3_client.network_name,
        "contract_address": web3_client.contract_address,
        "explorer_url": web3_client.explorer_base_url,
        "account": web3_client.account.address if web3_client.account else None
    }


@router.post("/verify")
async def verify_on_chain_record(payload: dict):
    """
    Performs a REAL on-chain verification by querying the smart contract.
    Expected payload: { record_id, image_hash, match_data_hash, record_hash }
    """
    record_id = payload.get("record_id", "")
    image_hash = payload.get("image_hash", "")
    match_data_hash = payload.get("match_data_hash", "")
    record_hash = payload.get("record_hash", "")

    if not all([record_id, image_hash, match_data_hash, record_hash]):
        raise HTTPException(status_code=400, detail="Missing required verification fields.")

    try:
        web3_client = Web3Client()
        if not web3_client.is_connected() or not web3_client.contract:
            raise HTTPException(
                status_code=503,
                detail="Blockchain RPC node or contract is not available. Cannot verify on-chain record."
            )

        is_valid = web3_client.verify_record_on_chain(
            record_id_hex=record_id,
            image_hash=image_hash,
            match_data_hash=match_data_hash,
            record_hash=record_hash
        )

        return {
            "record_id": record_id,
            "is_valid": is_valid,
            "network_name": web3_client.network_name,
            "chain_id": web3_client.chain_id,
            "contract_address": web3_client.contract_address,
            "message": "ON-CHAIN RECORD VERIFIED" if is_valid else "VERIFICATION FAILED — hash mismatch on-chain."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"On-chain verification error: {str(e)}")
