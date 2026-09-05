import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application configuration
    APP_NAME: str = "Face ID + Blockchain Verification"
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    # Reverse Image Search Configuration
    REVERSE_SEARCH_PROVIDER: str = os.getenv("REVERSE_SEARCH_PROVIDER", "serpapi")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    TINEYE_API_KEY: str = os.getenv("TINEYE_API_KEY", "")
    
    # Matching Thresholds & Weights
    FACE_SIMILARITY_THRESHOLD: float = float(os.getenv("FACE_SIMILARITY_THRESHOLD", "0.65"))
    REVERSE_SEARCH_THRESHOLD: float = float(os.getenv("REVERSE_SEARCH_THRESHOLD", "0.50"))
    FACE_WEIGHT: float = float(os.getenv("FACE_WEIGHT", "0.70"))
    IMAGE_SEARCH_WEIGHT: float = float(os.getenv("IMAGE_SEARCH_WEIGHT", "0.30"))
    
    # Blockchain Network Configuration
    BLOCKCHAIN_RPC_URL: str = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
    BLOCKCHAIN_PRIVATE_KEY: str = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", "1337"))
    EXPLORER_URL: str = os.getenv("EXPLORER_URL", "https://sepolia.etherscan.io")

    class Config:
        env_file = ".env"

settings = Settings()
