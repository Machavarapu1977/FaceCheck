from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import numpy as np

class BaseFaceDetector(ABC):
    @abstractmethod
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detects faces in an OpenCV image.
        Returns a list of bounding boxes [(x, y, width, height), ...]
        """
        pass

class BaseFaceEmbedder(ABC):
    @abstractmethod
    def generate_embedding(self, face_crop: np.ndarray) -> np.ndarray:
        """
        Generates a 512-dimensional normalized face embedding vector.
        """
        pass

    @abstractmethod
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Computes cosine similarity score between two normalized face embeddings (0.0 to 1.0).
        """
        pass
