"""SQLAlchemy persistence — Postgres-ready (DATABASE_URL) with SQLite fallback."""
import json
import time
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Float, Integer, String, Text, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(80), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(Float, default=lambda: datetime.now().timestamp())


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(String(32), primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)
    resume_text = Column(Text, nullable=True)
    signals_json = Column(Text, nullable=True)
    results_json = Column(Text, nullable=True)
    map_json = Column(Text, nullable=True)
    created_at = Column(Float, default=lambda: datetime.now().timestamp())


engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)
    _migrate()


def _migrate() -> None:
    """Lightweight auto-migration for columns added after the initial deploy."""
    with engine.connect() as conn:
        if engine.dialect.name == "postgresql":
            rows = conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
            ))
            cols = {r[0] for r in rows}
        else:
            rows = conn.execute(text("PRAGMA table_info(users)"))
            cols = {r[1] for r in rows}
    if "email_verified" not in cols:
        with engine.begin() as conn:
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE"
            ))


def get_session():
    return SessionLocal()


# ---- Users ----

def create_user(email: str, username: str, password_hash: str) -> User:
    s = get_session()
    try:
        u = User(email=email.lower().strip(), username=username.strip(), password_hash=password_hash)
        s.add(u)
        s.commit()
        s.refresh(u)
        return u
    finally:
        s.close()


def get_user_by_email(email: str) -> User | None:
    s = get_session()
    try:
        return s.query(User).filter(User.email == email.lower().strip()).first()
    finally:
        s.close()


def get_user(user_id: int) -> User | None:
    s = get_session()
    try:
        return s.get(User, user_id)
    finally:
        s.close()


def set_email_verified(user_id: int) -> None:
    s = get_session()
    try:
        u = s.get(User, user_id)
        if u:
            u.email_verified = True
            s.commit()
    finally:
        s.close()


# ---- Analyses ----

def save_analysis(user_id: int | None, resume_text: str, signals: dict, results: list, career_map: dict) -> str:
    aid = uuid.uuid4().hex[:12]
    s = get_session()
    try:
        s.add(
            Analysis(
                id=aid,
                user_id=user_id,
                resume_text=resume_text,
                signals_json=json.dumps(signals),
                results_json=json.dumps(results),
                map_json=json.dumps(career_map),
                created_at=time.time(),
            )
        )
        s.commit()
        return aid
    finally:
        s.close()


def get_analysis(aid: str) -> dict | None:
    s = get_session()
    try:
        row = s.query(Analysis).filter(Analysis.id == aid).first()
        if not row:
            return None
        return {
            "id": row.id,
            "user_id": row.user_id,
            "signals": json.loads(row.signals_json or "{}"),
            "results": json.loads(row.results_json or "[]"),
            "career_map": json.loads(row.map_json or "{}"),
            "created_at": row.created_at,
        }
    finally:
        s.close()


def list_analyses(user_id: int | None = None, limit: int = 50) -> list:
    s = get_session()
    try:
        q = s.query(Analysis)
        if user_id is not None:
            q = q.filter(Analysis.user_id == user_id)
        rows = q.order_by(Analysis.created_at.desc()).limit(limit).all()
        return [{"id": r.id, "created_at": r.created_at} for r in rows]
    finally:
        s.close()


# ---- Admin metrics ----


def get_admin_metrics() -> dict:
    """Aggregate admin metrics: totals + last-24h activity + 7-day analyses trend."""
    from datetime import datetime

    s = get_session()
    try:
        now = time.time()
        day = 86400.0

        total_users = s.query(User).count()
        total_analyses = s.query(Analysis).count()

        new_users = (
            s.query(User)
            .filter(User.created_at >= now - day)
            .order_by(User.created_at.desc())
            .all()
        )
        analyses_24h = s.query(Analysis).filter(Analysis.created_at >= now - day).count()

        per_day = []
        for i in range(7):
            end = now - i * day
            start = end - day
            cnt = (
                s.query(Analysis)
                .filter(Analysis.created_at >= start, Analysis.created_at < end)
                .count()
            )
            per_day.append(
                {"date": datetime.fromtimestamp(end).strftime("%Y-%m-%d"), "count": cnt}
            )

        return {
            "total_users": total_users,
            "total_analyses": total_analyses,
            "new_users_24h": [
                {"email": u.email, "username": u.username, "created_at": u.created_at}
                for u in new_users
            ],
            "analyses_24h": analyses_24h,
            "analyses_per_day": per_day,
        }
    finally:
        s.close()
