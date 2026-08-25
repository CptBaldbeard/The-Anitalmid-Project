"""Pydantic schemas for the Anitalmid career-matching API."""
from typing import Any, Dict, List

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
    job_url: str = ""   # optional — if set, the analysis also matches this job posting


class SignalsPayload(BaseModel):
    mbti: str = ""       # optional, e.g. "INFP"
    holland: str = ""    # 3-letter RIASEC code, e.g. "RIS"
    major: str = ""      # college major name, optional
    job_url: str = ""    # optional — if set, also match this job posting


class JobAnalysisRequest(BaseModel):
    url: str
    text: str = ""       # resume text (optional — drives keyword + signal inference)
    mbti: str = ""       # user MBTI (optional — used when no resume text, signals mode)
    holland: str = ""    # user Holland code (optional — same)


class EmailResultsRequest(BaseModel):
    signals: Dict[str, Any] = Field(default_factory=dict)
    top_matches: List[Dict[str, Any]] = Field(default_factory=list)


class ApplyPilotExportRequest(BaseModel):
    top_matches: List[Dict[str, Any]] = Field(default_factory=list)
    location: str = ""


class PivotRequest(BaseModel):
    full_ranking: List[Dict[str, Any]] = Field(default_factory=list)
    education_experience: List[str] = Field(default_factory=list)
    education_interests: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)


class PivotResponse(BaseModel):
    pivot_matches: List[Dict[str, Any]] = Field(default_factory=list)
    education_categories: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
    hobbies_note: str = ""


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
