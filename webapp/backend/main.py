"""Anitalmid Career-Matching API — FastAPI entrypoint (auth + Postgres-ready).

Run:
    cd .../webapp && uvicorn backend.main:app --host 127.0.0.1 --port 8300
"""
from pathlib import Path

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import auth, db, emailer, expansion, map_gen, oskg, parser, scoring
from .config import BASE_URL
from .models import (
    AnalysisResult,
    LoginRequest,
    RegisterRequest,
    TextPayload,
    TokenResponse,
    UserResponse,
)

app = FastAPI(
    title="Anitalmid Career-Matching API",
    description="WebUI backend: resume + certs + experience -> career map (JWT auth).",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_cache_static(request, call_next):
    """Don't long-cache static assets so redeploys are visible immediately."""
    response = await call_next(request)
    path = request.url.path
    if path.endswith((".html", ".css", ".js")) or path in ("/", "/index.html"):
        response.headers["Cache-Control"] = "no-cache"
    return response


# ---- Auth dependency ----

def get_current_user(authorization: str = Header(None)) -> db.User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    user_id = auth.decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def _user_response(user: db.User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "email_verified": bool(user.email_verified),
    }


def _require_verified(user: db.User) -> None:
    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before analyzing.")


# ---- Auth endpoints ----

@app.post("/auth/register", response_model=TokenResponse)
def register(payload: RegisterRequest):
    if db.get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    user = db.create_user(payload.email, payload.username, auth.hash_password(payload.password))
    token = auth.create_token(user.id)

    verify_token = auth.create_verify_token(user.email)
    link = f"{BASE_URL}/auth/verify?token={verify_token}"
    sent = emailer.send_verification_email(user.email, user.username, link)

    resp = {"access_token": token, "user": _user_response(user)}
    if not sent:
        resp["dev_verify_link"] = link
    return resp


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = db.get_user_by_email(payload.email)
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.create_token(user.id)
    return {"access_token": token, "user": _user_response(user)}


@app.get("/auth/me", response_model=UserResponse)
def me(user: db.User = Depends(get_current_user)):
    return _user_response(user)


@app.get("/auth/verify", response_class=HTMLResponse)
def verify_email(token: str = ""):
    email = auth.decode_verify_token(token)
    if not email:
        return _verify_page(False, "Invalid or expired verification link.")
    user = db.get_user_by_email(email)
    if not user:
        return _verify_page(False, "Account not found.")
    if user.email_verified:
        return _verify_page(True, "Email already verified.")
    db.set_email_verified(user.id)
    return _verify_page(True, "Email verified! You can now sign in.")


@app.post("/auth/resend-verification")
def resend_verification(user: db.User = Depends(get_current_user)):
    if user.email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    verify_token = auth.create_verify_token(user.email)
    link = f"{BASE_URL}/auth/verify?token={verify_token}"
    sent = emailer.send_verification_email(user.email, user.username, link)
    resp = {"sent": sent}
    if not sent:
        resp["dev_verify_link"] = link
    return resp


def _verify_page(success: bool, message: str) -> str:
    color = "#4ade80" if success else "#f87171"
    glyph = "&#10003;" if success else "&#10007;"
    sub = (
        "Head back to the app and sign in to get your career map."
        if success
        else "Try registering again or request a new verification link."
    )
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Anitalmid — Email Verification</title></head>
<body style="background:#0b0f1a;color:#e9eef7;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
<div style="text-align:center;max-width:420px;padding:40px;border:1px solid #2a3450;border-radius:12px">
<div style="font-size:48px;color:{color}">{glyph}</div>
<h2 style="color:{color};margin:12px 0 8px">{message}</h2>
<p style="color:#93a0b8">{sub}</p>
<a href="/" style="display:inline-block;margin-top:16px;background:#2dd4bf;color:#061018;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold">Go to Anitalmid</a>
</div></body></html>"""


# ---- Health ----

@app.get("/health")
def health():
    return {"status": "ok", "service": "anitalmid-analyze", "pdf_supported": parser.pdf_supported()}


# ---- Analysis pipeline ----

async def _run_pipeline(text: str, user_id: int | None) -> dict:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text to analyze")

    ranking, signals = scoring.score_roles(text)
    ranking = oskg.validate_roles(ranking)

    # Camoufox web expansion — additional career fields beyond the core roles.
    holland_code = (signals.get("holland") or {}).get("inferred_code")
    expanded = await expansion.search_expanded_roles(holland_code, signals)

    career_map = map_gen.build_career_map(ranking, signals, expanded)

    results_meta = [{k: v for k, v in r.items() if k != "rank"} for r in ranking]
    aid = db.save_analysis(user_id, text, signals, results_meta, career_map)

    return {
        "id": aid,
        "signals": signals,
        "top_matches": ranking[:6],
        "full_ranking": ranking,
        "career_map": career_map,
        "expanded_matches": expanded,
    }


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    user: db.User = Depends(get_current_user),
):
    _require_verified(user)
    raw = await resume.read()
    text = parser.extract_text_from_upload(resume.filename or "resume.txt", raw)
    return await _run_pipeline(text, user.id)


@app.post("/analyze-text")
async def analyze_text(payload: TextPayload, user: db.User = Depends(get_current_user)):
    _require_verified(user)
    return await _run_pipeline(payload.text, user.id)


@app.get("/analyses")
def list_analyses(limit: int = 50, user: db.User = Depends(get_current_user)):
    return {"analyses": db.list_analyses(user_id=user.id, limit=limit)}


@app.get("/analyses/{aid}")
def get_analysis(aid: str, user: db.User = Depends(get_current_user)):
    record = db.get_analysis(aid)
    if not record or record.get("user_id") != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record


# ---- Frontend static SPA ----

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

# Ensure schema exists before first request.
db.init_db()
