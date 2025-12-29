"""
llms2 - A Python package for managing multiple LLM profiles and API interactions.
"""

from .llms import LLMS
from .utils import encode_image, decode_image, extract_code_block

__version__ = "0.1.0"

__all__ = [
    "LLMS",
    "encode_image",
    "decode_image",
    "extract_code_block",
]
