"""Pydantic schemas for the Anitalmid career-matching API."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SignalResult(BaseModel):
    mbti: Dict[str, Any]
    holland: Dict[str, Any]
    big_five: Dict[str, Any]


class RoleMatch(BaseModel):
    rank: int
    title: str
    category: str
    composite_score: float
    keyword_score: float
    framework_score: float
    experience_boost: float
    holland_code: str
    o_net_code: str
    salary_range: str
    pivot_cost: str
    experience_required: str
    description: str
    validation: str  # "experience-validated" | "aptitude-validated" | "weak"


class MapNode(BaseModel):
    id: str
    label: str
    type: str  # profile | signal | role | path | expanded
    data: Dict[str, Any] = Field(default_factory=dict)


class MapEdge(BaseModel):
    source: str
    target: str
    label: str = ""
    weight: float = 1.0


class CareerMap(BaseModel):
    nodes: List[MapNode]
    edges: List[MapEdge]


class AnalysisResult(BaseModel):
    id: str
    signals: SignalResult
    top_matches: List[RoleMatch]
    full_ranking: List[RoleMatch]
    career_map: CareerMap
    created_at: float


class TextPayload(BaseModel):
    text: str


# ---- Auth ----

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    email_verified: bool = False


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    dev_verify_link: Optional[str] = None
