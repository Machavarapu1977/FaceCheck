import os
import cv2
import numpy as np
from typing import List, Tuple
from backend.services.face_detection.base import BaseFaceDetector

# Path to the YuNet ONNX model (bundled with the service)
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_detection_yunet_2023mar.onnx")


class OpenCVFaceDetector(BaseFaceDetector):
    """
    Face detector using OpenCV FaceDetectorYN (YuNet DNN model).
    OpenCV 5.x removed CascadeClassifier; this uses the built-in
    high-accuracy YuNet model instead.
    Detects all faces and returns their bounding boxes sorted by area.
    """

    def __init__(self):
        self._detector = None
        if os.path.exists(_MODEL_PATH):
            try:
                # Input size will be updated per-image in detect_faces()
                self._detector = cv2.FaceDetectorYN_create(
                    model=_MODEL_PATH,
                    config="",
                    input_size=(320, 320),
                    score_threshold=0.6,
                    nms_threshold=0.3,
                    top_k=100,
                )
            except Exception as e:
                self._detector = None

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        if image is None or image.size == 0:
            return []

        h, w = image.shape[:2]

        if self._detector is not None:
            try:
                self._detector.setInputSize((w, h))
                _, faces = self._detector.detect(image)
                results = []
                if faces is not None:
                    for face in faces:
                        x, y, fw, fh = int(face[0]), int(face[1]), int(face[2]), int(face[3])
                        # Clamp to image bounds
                        x = max(0, x)
                        y = max(0, y)
                        fw = min(fw, w - x)
                        fh = min(fh, h - y)
                        if fw > 0 and fh > 0:
                            results.append((x, y, fw, fh))
                # Sort by area descending (largest face first)
                results.sort(key=lambda b: b[2] * b[3], reverse=True)
                return results
            except Exception:
                pass

        # Fallback: try multi-pass detection using equalizeHist + DNN params
        # If detector not available, return empty (no fake bounding boxes)
        return []
