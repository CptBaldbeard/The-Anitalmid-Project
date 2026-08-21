"""Shared paths + config for the Anitalmid webapp backend."""
import os
import secrets
from pathlib import Path

# Backend dir = .../webapp/backend ; vault lives one level up under "The Anitalmid Project".
BACKEND_DIR = Path(__file__).resolve().parent
VAULT = BACKEND_DIR.parents[1] / "The Anitalmid Project"
DB_PATH = BACKEND_DIR / "anitalmid.db"

# Database: Postgres via env var, else local SQLite (dev fallback).
#   Postgres: ANITALMID_DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/anitalmid
DATABASE_URL = os.environ.get("ANITALMID_DATABASE_URL") or f"sqlite:///{DB_PATH}"


def _secret() -> str:
    env = os.environ.get("ANITALMID_SECRET")
    if env:
        return env
    secret_file = BACKEND_DIR / ".secret"
    if secret_file.exists():
        return secret_file.read_text().strip()
    s = secrets.token_hex(32)
    secret_file.write_text(s)
    return s


SECRET = _secret()
