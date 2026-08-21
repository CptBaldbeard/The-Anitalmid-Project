"""SQLAlchemy persistence — Postgres-ready (DATABASE_URL) with SQLite fallback."""
import json
import time
import uuid
from datetime import datetime

from sqlalchemy import Column, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(80), nullable=False)
    password_hash = Column(String(255), nullable=False)
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
        return s.query(User).get(user_id)
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
