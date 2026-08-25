"""Shared paths + config for the Anitalmid webapp backend."""
import os
import secrets
from pathlib import Path

# Backend dir = .../webapp/backend.
BACKEND_DIR = Path(__file__).resolve().parent
DB_PATH = BACKEND_DIR / "anitalmid.db"


def _load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from webapp/.env into os.environ (no overrides).

    Real environment variables always win over .env values (python-dotenv
    semantics). A missing .env is fine — this is a local-dev convenience; in
    production Render injects the real variables.
    """
    env_path = path or (BACKEND_DIR.parent / ".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# Database: Postgres via env var, else local SQLite (dev fallback).
#   Postgres: ANITALMID_DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/anitalmid
DATABASE_URL = os.environ.get("ANITALMID_DATABASE_URL") or f"sqlite:///{DB_PATH}"


def _secret() -> str:
    env = os.environ.get("ANITALMID_SECRET")
    if env:
        return env
    if os.environ.get("ANITALMID_DATABASE_URL"):
        # Production (Postgres configured) — a missing JWT secret is a
        # misconfiguration. Fail loudly rather than minting an ephemeral key
        # (Render's filesystem is ephemeral, so a generated key would not even
        # survive a restart, silently invalidating every session).
        raise RuntimeError(
            "ANITALMID_SECRET is not set. Production requires an explicit JWT "
            "signing secret via the ANITALMID_SECRET environment variable."
        )
    # Local dev only: reuse or generate a persisted secret.
    secret_file = BACKEND_DIR / ".secret"
    if secret_file.exists():
        return secret_file.read_text().strip()
    s = secrets.token_hex(32)
    secret_file.write_text(s)
    return s


SECRET = _secret()

# Public base URL for building verification links (set in production).
BASE_URL = os.environ.get("ANITALMID_BASE_URL", "http://localhost:8300").rstrip("/")

# Admin metrics digest (secret-key-protected /admin/metrics/email endpoint).
# Both must be set in production for the admin digest to work.
ADMIN_KEY = os.environ.get("ANITALMID_ADMIN_KEY", "")
ADMIN_EMAIL = os.environ.get("ANITALMID_ADMIN_EMAIL", "")
