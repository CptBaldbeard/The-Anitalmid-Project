"""Anitalmid Career-Matching API — FastAPI entrypoint (auth + Postgres-ready).

Run:
    cd .../webapp && uvicorn backend.main:app --host 127.0.0.1 --port 8300
"""
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from . import auth, config, db, emailer, export, job_analysis, majors, map_gen, oskg, parser, scoring
from .rate_limit import ip_limiter, user_limiter
from .models import (
    AnalysisResult,
    ApplyPilotExportRequest,
    EmailResultsRequest,
    JobAnalysisRequest,
    LoginRequest,
    RegisterRequest,
    SignalsPayload,
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


@app.middleware("http")
async def rate_limit(request, call_next):
    """Per-IP throttle on the analysis endpoints (blocks scripted abuse)."""
    if request.url.path in ("/analyze", "/analyze-text", "/analyze-signals", "/analyze/job"):
        ip = request.client.host if request.client else "unknown"
        if not ip_limiter.allow(f"ip:{ip}", limit=10, window=3600):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many analyses — please wait a while and try again."},
            )
    return await call_next(request)


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


# ---- Auth endpoints ----

@app.post("/auth/register", response_model=TokenResponse)
def register(payload: RegisterRequest):
    if db.get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    user = db.create_user(payload.email, payload.username, auth.hash_password(payload.password))
    token = auth.create_token(user.id)
    return {"access_token": token, "user": _user_response(user)}


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


# ---- Health ----

@app.get("/health")
def health():
    return {"status": "ok", "service": "anitalmid-analyze", "pdf_supported": parser.pdf_supported()}


@app.get("/majors")
def list_majors():
    return {"majors": majors.major_names()}


# ---- Analysis pipeline ----

async def _run_pipeline(text: str, user_id: int | None, job_url: str = "") -> dict:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text to analyze")

    if user_id is not None and not user_limiter.allow(f"user:{user_id}", limit=25, window=86400):
        raise HTTPException(status_code=429, detail="Daily analysis limit reached — try again tomorrow.")

    ranking, signals = scoring.score_roles(text)
    ranking = oskg.validate_roles(ranking)

    career_map = map_gen.build_career_map(ranking, signals)

    results_meta = [{k: v for k, v in r.items() if k != "rank"} for r in ranking]
    aid = db.save_analysis(user_id, text, signals, results_meta, career_map)

    result = {
        "id": aid,
        "signals": signals,
        "top_matches": ranking[:6],
        "full_ranking": ranking,
        "career_map": career_map,
    }
    if job_url:
        try:
            result["job_alignment"] = job_analysis.analyze_job(job_url.strip(), text)
        except Exception:
            result["job_alignment"] = {"error": "Couldn't fetch that job posting."}
    return result


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_url: str = Form(""),
    user: db.User = Depends(get_current_user),
):
    raw = await resume.read()
    text = parser.extract_text_from_upload(resume.filename or "resume.txt", raw)
    return await _run_pipeline(text, user.id, job_url)


@app.post("/analyze-text")
async def analyze_text(payload: TextPayload, user: db.User = Depends(get_current_user)):
    return await _run_pipeline(payload.text, user.id, payload.job_url)


async def _run_signals_pipeline(mbti: str, holland: str, major: str, user_id: int | None, job_url: str = "") -> dict:
    holland = (holland or "").strip().upper()
    if not holland:
        raise HTTPException(status_code=400, detail="Pick at least one interest (Holland code).")

    if user_id is not None and not user_limiter.allow(f"user:{user_id}", limit=25, window=86400):
        raise HTTPException(status_code=429, detail="Daily analysis limit reached — try again tomorrow.")

    ranking, signals = scoring.score_signals(mbti, holland, major)
    ranking = oskg.validate_roles(ranking)

    career_map = map_gen.build_career_map(ranking, signals)

    results_meta = [{k: v for k, v in r.items() if k != "rank"} for r in ranking]
    summary = f"signals: MBTI={mbti or '-'} Holland={holland} Major={major or '-'}"
    aid = db.save_analysis(user_id, summary, signals, results_meta, career_map)

    result = {
        "id": aid,
        "signals": signals,
        "top_matches": ranking[:6],
        "full_ranking": ranking,
        "career_map": career_map,
    }
    if job_url:
        try:
            result["job_alignment"] = job_analysis.analyze_job(job_url.strip(), "", mbti, holland)
        except Exception:
            result["job_alignment"] = {"error": "Couldn't fetch that job posting."}
    return result


@app.post("/analyze-signals")
async def analyze_signals(payload: SignalsPayload, user: db.User = Depends(get_current_user)):
    return await _run_signals_pipeline(payload.mbti, payload.holland, payload.major, user.id, payload.job_url)


@app.post("/analyze/job")
def analyze_job(payload: JobAnalysisRequest, user: db.User = Depends(get_current_user)):
    url = (payload.url or "").strip()
    if not url:
        raise HTTPException(status_code=400, detail="Paste a job posting URL.")
    if not user_limiter.allow(f"job:{user.id}", limit=25, window=86400):
        raise HTTPException(status_code=429, detail="Daily job-analysis limit reached — try again tomorrow.")
    try:
        return job_analysis.analyze_job(url, payload.text, payload.mbti, payload.holland)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Couldn't fetch that job posting: {e}")


@app.get("/analyses")
def list_analyses(limit: int = 50, user: db.User = Depends(get_current_user)):
    return {"analyses": db.list_analyses(user_id=user.id, limit=limit)}


@app.get("/analyses/{aid}")
def get_analysis(aid: str, user: db.User = Depends(get_current_user)):
    record = db.get_analysis(aid)
    if not record or record.get("user_id") != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record


# ---- Email results ----

@app.post("/analyze/email")
def email_results(payload: EmailResultsRequest, user: db.User = Depends(get_current_user)):
    if not user.email:
        raise HTTPException(status_code=400, detail="No email address is associated with this account")
    if not user_limiter.allow(f"email:{user.id}", limit=10, window=86400):
        raise HTTPException(status_code=429, detail="You've hit the daily email limit, try again tomorrow")
    html = emailer.build_results_email(user.username, payload.signals, payload.top_matches)
    sent = emailer.send_email(user.email, "Your Anitalmid career map", html)
    if not sent:
        raise HTTPException(status_code=502, detail="We couldn't send the email right now, please try again")
    return {"sent": True, "to": user.email}


# ---- Admin metrics digest ----


@app.post("/admin/metrics/email")
def admin_metrics_email(x_admin_key: str | None = Header(None)):
    if not config.ADMIN_KEY:
        raise HTTPException(status_code=503, detail="Admin metrics not configured (ANITALMID_ADMIN_KEY)")
    if not x_admin_key or x_admin_key != config.ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not config.ADMIN_EMAIL:
        raise HTTPException(status_code=503, detail="Admin email not configured (ANITALMID_ADMIN_EMAIL)")
    metrics = db.get_admin_metrics()
    html = emailer.build_metrics_email(metrics)
    sent = emailer.send_email(config.ADMIN_EMAIL, "Anitalmid — daily metrics", html)
    if not sent:
        raise HTTPException(status_code=502, detail="Couldn't send the metrics email")
    return {"sent": True, "to": config.ADMIN_EMAIL}


# ---- ApplyPilot export ----


@app.post("/export/applypilot")
def export_applypilot(payload: ApplyPilotExportRequest, user: db.User = Depends(get_current_user)):
    if not payload.top_matches:
        raise HTTPException(status_code=400, detail="No matches to export — run an analysis first.")
    zip_bytes = export.build_applypilot_zip(payload.top_matches, payload.location)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="applypilot_config.zip"'},
    )


# ---- Frontend static SPA ----

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

# Ensure schema exists before first request.
db.init_db()
