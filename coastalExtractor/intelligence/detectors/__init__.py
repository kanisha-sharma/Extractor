"""
Stage 3 detectors.
"""

from .caption_detector import CaptionDetector
from .key_value_detector import KeyValueDetector
from .list_detector import ListDetector

__all__ = [
    "CaptionDetector",
    "KeyValueDetector",
    "ListDetector",
]