from typing import List, Dict, Any
from urllib.parse import urlparse
from backend.services.reverse_image_search.base import BaseReverseImageSearchProvider
from backend.services.reverse_image_search.serpapi_provider import SerpApiLensProvider

class MockReverseSearchProvider(BaseReverseImageSearchProvider):
    """
    Mock reverse search provider for development & DEMO_MODE testing.
    Provides realistic candidates with valid public avatar image URLs for dynamic extraction.
    """
    def search(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        candidates = [
            {
                "title": "Alex Morgan - Senior Software Engineer | LinkedIn",
                "url": "https://www.linkedin.com/in/alex-morgan-tech",
                "source_domain": "linkedin.com",
                "image_url": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg",
                "reverse_search_relevance": 0.92
            },
            {
                "title": "Alex Morgan (@alexm_tech) / X",
                "url": "https://x.com/alexm_tech",
                "source_domain": "x.com",
                "image_url": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/albert.jpg",
                "reverse_search_relevance": 0.88
            },
            {
                "title": "Global Tech Summit Speakers 2026",
                "url": "https://techsummit2026.org/speakers/alex-morgan",
                "source_domain": "techsummit2026.org",
                "image_url": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/facedetect_results.jpg",
                "reverse_search_relevance": 0.75
            }
        ]
        return candidates

import logging
logger = logging.getLogger("reverse_search")

class ReverseSearchProviderFactory:
    @staticmethod
    def get_provider(provider_name: str, api_key: str = "", demo_mode: bool = False) -> BaseReverseImageSearchProvider:
        if demo_mode:
            logger.info("[REVERSE_SEARCH] DEMO_MODE is True. Using MockReverseSearchProvider.")
            return MockReverseSearchProvider()
        
        if not api_key:
            logger.warning("[REVERSE_SEARCH] SERPAPI_KEY is empty in .env. Falling back to MockReverseSearchProvider.")
            return MockReverseSearchProvider()
        
        provider_name = provider_name.lower()
        if provider_name == "serpapi":
            logger.info("[REVERSE_SEARCH] Using genuine SerpApiLensProvider with provided API key.")
            return SerpApiLensProvider(api_key=api_key)
        else:
            logger.warning(f"[REVERSE_SEARCH] Provider '{provider_name}' unrecognized. Falling back to MockReverseSearchProvider.")
            return MockReverseSearchProvider()
