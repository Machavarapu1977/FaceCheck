import hashlib
import json
from typing import Dict, Any, Tuple

class CanonicalHasher:
    @staticmethod
    def hash_image_bytes(image_bytes: bytes) -> str:
        """
        Computes SHA-256 hash of raw input photograph bytes.
        Returns 0x-prefixed hex string.
        """
        hasher = hashlib.sha256()
        hasher.update(image_bytes)
        return "0x" + hasher.hexdigest()

    @staticmethod
    def hash_canonical_json(data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Creates deterministic canonical JSON string with sorted keys,
        compact separators (',', ':'), and UTF-8 encoding before hashing with SHA-256.
        Returns (0x-prefixed hex string, canonical_data_dict).
        """
        canonical_json_str = json.dumps(
            data,
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=False
        )
        hasher = hashlib.sha256()
        hasher.update(canonical_json_str.encode('utf-8'))
        return "0x" + hasher.hexdigest(), data

    @staticmethod
    def compute_record_hash(
        image_hash: str,
        match_data_hash: str,
        timestamp: int,
        result_url: str
    ) -> str:
        """
        Computes combined verification record hash over image_hash, match_data_hash, timestamp, and result_url.
        """
        combined = f"{image_hash}:{match_data_hash}:{timestamp}:{result_url}"
        hasher = hashlib.sha256()
        hasher.update(combined.encode('utf-8'))
        return "0x" + hasher.hexdigest()
