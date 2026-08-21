# Anitalmid Web App

FastAPI backend + static frontend for the Anitalmid career-matching engine.

## Run

```bash
cd webapp
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8300
```

Then open http://127.0.0.1:8300/.

## Config (env vars)

- `ANITALMID_DATABASE_URL` — Postgres URL (defaults to local SQLite).
- `ANITALMID_SECRET` — JWT signing secret (auto-generated + persisted if unset).

## Stack

- **FastAPI** + **SQLAlchemy** (Postgres-ready, SQLite fallback)
- **JWT auth** (PyJWT + bcrypt)
- **pymupdf** — PDF resume parsing
- **Camoufox web search** — career expansion beyond the core role profiles (Holland/MBTI queries)

## Endpoints

- `POST /auth/register` · `POST /auth/login` · `GET /auth/me`
- `POST /analyze` (multipart resume upload) · `POST /analyze-text` (JSON)
- `GET /analyses` · `GET /analyses/{id}`
