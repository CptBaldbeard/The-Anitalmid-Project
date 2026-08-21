"""Framework signal detection — reuses the bundled resume_matcher detectors."""
from . import resume_matcher as rm


def detect_signals(text: str) -> dict:
    """Return MBTI / Holland / Big Five signals inferred from resume text."""
    return {
        "mbti": rm.detect_mbti_signals(text),
        "holland": rm.detect_holland_signals(text),
        "big_five": rm.detect_big_five_signals(text),
    }
