import requests
from typing import List, Dict, Any
from urllib.parse import urlparse
from backend.services.reverse_image_search.base import BaseReverseImageSearchProvider

class SerpApiLensProvider(BaseReverseImageSearchProvider):
    """
    Genuine reverse image search implementation using SerpAPI Google Lens API engine.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://serpapi.com/search.json"

    def search(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        if not self.api_key:
            raise ValueError("SERPAPI_KEY is not configured.")

        # Step 1: Temporarily host image bytes to get a public direct URL for SerpAPI Google Lens
        image_url = None

        # Primary host: uguu.se (direct raw public image URL)
        if not image_url:
            try:
                r = requests.post(
                    'https://uguu.se/upload',
                    files={'files[]': ('image.jpg', image_bytes, 'image/jpeg')},
                    timeout=8
                )
                if r.status_code == 200:
                    d = r.json()
                    files = d.get('files', [])
                    if files and 'url' in files[0]:
                        image_url = files[0]['url']
            except Exception:
                pass

        # Fallback 1: litterbox.catbox.moe
        if not image_url:
            try:
                r = requests.post(
                    'https://litterbox.catbox.moe/resources/internals/api.php',
                    data={'reqtype': 'fileupload', 'time': '1h'},
                    files={'fileToUpload': ('image.jpg', image_bytes, 'image/jpeg')},
                    timeout=8,
                    verify=False
                )
                if r.status_code == 200 and r.text.startswith('http'):
                    image_url = r.text.strip()
            except Exception:
                pass

        # Fallback 2: tmpfiles.org
        if not image_url:
            try:
                r = requests.post(
                    'https://tmpfiles.org/api/v1/upload',
                    files={'file': ('image.jpg', image_bytes, 'image/jpeg')},
                    timeout=8
                )
                if r.status_code == 200:
                    data = r.json()
                    raw = data.get('data', {}).get('url', '')
                    if raw:
                        image_url = raw.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
            except Exception:
                pass

        if not image_url:
            raise RuntimeError("Failed to host temporary image for SerpAPI Google Lens reverse image search.")

        # Step 2: Query SerpAPI Google Lens with the image URL via GET
        params = {
            "engine": "google_lens",
            "url": image_url,
            "api_key": self.api_key
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            exact_matches = data.get("exact_matches", [])
            visual_matches = data.get("visual_matches", [])
            organic_results = data.get("organic_results", [])

            raw_items = []
            if isinstance(exact_matches, list):
                raw_items.extend(exact_matches)
            if isinstance(visual_matches, list):
                raw_items.extend(visual_matches)
            if isinstance(organic_results, list):
                raw_items.extend(organic_results)

            for idx, item in enumerate(raw_items[:12]):
                link = item.get("link", "")
                domain = urlparse(link).netloc if link else "web"
                # Rank relevance decays gracefully from 0.85 (top visual match) to 0.35
                rank_relevance = max(0.35, round(0.85 - (idx * 0.04), 2))
                img_src = item.get("thumbnail") or item.get("source") or item.get("image") or item.get("original")
                results.append({
                    "title": item.get("title", "Visual Match"),
                    "url": link,
                    "source_domain": domain,
                    "image_url": img_src,
                    "reverse_search_relevance": rank_relevance
                })
            return results
        except Exception as e:
            raise RuntimeError(f"SerpAPI Google Lens reverse image search failed: {str(e)}")
