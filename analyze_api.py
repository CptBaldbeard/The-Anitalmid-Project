#!/usr/bin/env python3
"""
Phase 0 Spike — Anitalmid Career-Matching API

A thin FastAPI wrapper around the existing resume_matcher.py to prove the
"thin service over the existing engine" hypothesis. Accepts a resume upload
(txt / md / rtf / pdf) and returns the top-6 career matches + detected
framework signals as JSON.

Run:  uvicorn analyze_api:app --host 127.0.0.1 --port 8300
"""
import sys
import tempfile
import os
from dataclasses import asdict
from pathlib import Path

# Make resume_matcher importable (it lives in this same directory).
VAULT = Path(__file__).resolve().parent
if str(VAULT) not in sys.path:
    sys.path.insert(0, str(VAULT))

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

import resume_matcher as rm

app = FastAPI(
    title="Anitalmid Career-Matching API",
    description="Phase 0 spike: thin FastAPI wrapper over resume_matcher.py",
    version="0.1.0-spike",
)


def _serialize_results(results):
    """Convert the matcher's output (RoleProfile dataclasses) to JSON-safe dicts."""
    ranking = []
    for r in results:
        role = asdict(r["role"])
        ranking.append(
            {
                "role": role,
                "composite_score": r["composite_score"],
                "keyword_score": r["keyword_score"],
                "framework_score": r["framework_score"],
                "experience_boost": r["experience_boost"],
                "category": r["category"],
                "pivot_cost": r["pivot_cost"],
            }
        )
    for i, item in enumerate(ranking, 1):
        item["rank"] = i
    return ranking


def _analyze_text(text: str) -> dict:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text to analyze")
    results, mbti, holland, big_five = rm.match_resume_to_roles(text)
    ranking = _serialize_results(results)
    return {
        "signals": {
            "mbti": mbti,
            "holland": holland,
            "big_five": big_five,
        },
        "top_matches": ranking[:6],
        "full_ranking": ranking,
    }


class TextPayload(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "anitalmid-analyze", "phase": "0-spike"}


@app.post("/analyze")
async def analyze(resume: UploadFile = File(...)):
    """Upload a resume file (.txt / .md / .rtf / .pdf) and get ranked matches."""
    raw = await resume.read()
    filename = resume.filename or "resume.txt"
    suffix = Path(filename).suffix.lower()

    # Write to a temp file and reuse the existing load_resume() auto-detection.
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name
    try:
        text = rm.load_resume(tmp_path)
    finally:
        os.unlink(tmp_path)

    return _analyze_text(text)


@app.post("/analyze-text")
def analyze_text(payload: TextPayload):
    """Analyze raw resume text passed as JSON (useful for testing / integrations)."""
    return _analyze_text(payload.text)
