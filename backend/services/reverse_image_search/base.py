from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseReverseImageSearchProvider(ABC):
    @abstractmethod
    def search(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Submits an image to a reverse image search engine/API.
        Returns a list of candidate dictionary objects containing:
        - title: Page or image title
        - url: Web page URL
        - source_domain: Domain name
        - image_url: Direct image/thumbnail URL
        - reverse_search_relevance: Relevance confidence score [0.0 - 1.0]
        """
        pass
