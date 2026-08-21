"""Resume parsing — reuses the existing resume_matcher.load_resume()."""
import os
import sys
import tempfile
from pathlib import Path

from .config import VAULT

if str(VAULT) not in sys.path:
    sys.path.insert(0, str(VAULT))

import resume_matcher as rm  # noqa: E402


def extract_text_from_upload(filename: str, raw: bytes) -> str:
    """Extract text from an uploaded resume (txt / md / rtf / pdf)."""
    suffix = Path(filename or "resume.txt").suffix.lower() or ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name
    try:
        return rm.load_resume(tmp_path)
    finally:
        os.unlink(tmp_path)


def pdf_supported() -> bool:
    return bool(getattr(rm, "HAS_PYMUPDF", False))
