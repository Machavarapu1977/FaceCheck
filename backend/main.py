import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import upload, verification, blockchain, health
from backend.config import settings

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("main")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Pipeline for Face ID, Reverse Image Search, Canonical SHA-256 Hashing, and Blockchain Record Verification."
)

# Enable CORS for frontend interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(upload.router, prefix="/api", tags=["Verification"])
app.include_router(verification.router, prefix="/api/verification", tags=["Verification Lookup"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["Blockchain"])
app.include_router(health.router, prefix="/api", tags=["Health"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"DEMO_MODE: {settings.DEMO_MODE}")
    logger.info(f"REVERSE_SEARCH_PROVIDER: {settings.REVERSE_SEARCH_PROVIDER}")
    logger.info(f"BLOCKCHAIN_RPC_URL: {settings.BLOCKCHAIN_RPC_URL}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
