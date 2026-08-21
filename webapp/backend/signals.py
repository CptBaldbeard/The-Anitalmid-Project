"""Framework signal detection — reuses resume_matcher's detectors."""
import sys

from .config import VAULT

if str(VAULT) not in sys.path:
    sys.path.insert(0, str(VAULT))

import resume_matcher as rm  # noqa: E402


def detect_signals(text: str) -> dict:
    """Return MBTI / Holland / Big Five signals inferred from resume text."""
    return {
        "mbti": rm.detect_mbti_signals(text),
        "holland": rm.detect_holland_signals(text),
        "big_five": rm.detect_big_five_signals(text),
    }
