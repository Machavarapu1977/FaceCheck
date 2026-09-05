import cv2
import numpy as np
from PIL import Image
import io
from typing import Tuple, List, Optional
import os

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def validate_image_file(file_bytes: bytes, filename: str) -> None:
    if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"Image file size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB.")
    
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
    except Exception as e:
        raise ValueError(f"Invalid or corrupted image format: {str(e)}")

def bytes_to_cv2(file_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image into OpenCV format.")
    return img

def crop_face(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = bbox
    height, width = img.shape[:2]
    
    # Add small padding safely
    pad_x = int(w * 0.1)
    pad_y = int(h * 0.1)
    
    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(width, x + w + pad_x)
    y2 = min(height, y + h + pad_y)
    
    return img[y1:y2, x1:x2]

def cv2_to_bytes(img: np.ndarray, ext: str = ".jpg") -> bytes:
    success, encoded_image = cv2.imencode(ext, img)
    if not success:
        raise ValueError(f"Failed to encode image with extension {ext}.")
    return encoded_image.tobytes()
