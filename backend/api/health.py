from fastapi import APIRouter
from backend.services.blockchain.web3_client import Web3Client
from backend.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    web3_client = Web3Client()
    blockchain_ok = web3_client.is_connected()
    
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "demo_mode": settings.DEMO_MODE,
        "services": {
            "face_detection": "operational",
            "reverse_image_search_provider": settings.REVERSE_SEARCH_PROVIDER,
            "blockchain_rpc": "operational" if blockchain_ok else "offline_or_fallback"
        }
    }
