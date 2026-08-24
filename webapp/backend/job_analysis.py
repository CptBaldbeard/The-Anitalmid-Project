"""Job-posting alignment — fetch a job URL, map it to MBTI/Holland/Big Five, and
compare it against a user's resume (keywords/experience) and signals.

Deterministic (no LLM): keyword matching reuses the role-catalog vocabulary plus a
curated cross-domain skills lexicon, and the framework mapping reuses the same
`signal_detection` detectors used on resumes. Explanations are template-generated
from the match data so the whole thing stays explainable and token-free.
"""
import json
import re
import urllib.error
import urllib.request

from .signal_detection import (
    detect_big_five_signals,
    detect_holland_signals,
    detect_mbti_signals,
)
from .roles import ROLE_PROFILES

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

# Curated cross-domain skills/terms that may not appear in the role catalog —
# supplements the aggregated role keywords. Keep these lowercase.
_CURATED_SKILLS = [
    # tech
    "python", "javascript", "typescript", "sql", "html", "css", "java", "c++",
    "rust", "react", "node", "aws", "azure", "gcp", "kubernetes", "docker", "linux",
    "machine learning", "artificial intelligence", "data analysis", "data science",
    "api", "database", "devops", "ci/cd", "cloud", "microservices", "cybersecurity",
    "observability", "monitoring", "logging", "metrics", "infrastructure", "saas",
    "open source", "sdk", "cli", "terraform", "git",
    # marketing / growth
    "marketing", "growth", "growth marketing", "seo", "sem", "content marketing",
    "copywriting", "copy", "social media", "email marketing", "campaign", "funnel",
    "conversion", "a/b testing", "experimentation", "kpi", "analytics", "b2b",
    "b2c", "product-led growth", "plg", "demand generation", "brand", "positioning",
    "landing page", "distribution", "community", "go-to-market", "crm", "lifecycle",
    "onboarding", "retention", "paid acquisition", "organic",
    # business / general
    "sales", "leadership", "management", "strategy", "operations", "finance",
    "accounting", "customer success", "project management", "agile", "scrum",
    "stakeholder", "communication", "collaboration", "research", "writing", "writer",
    "presentation", "budget", "forecasting", "reporting", "documentation",
    "cross-functional", "startup", "remote", "equity",
]


def _build_skills_lexicon() -> list[str]:
    """Aggregate the role catalog's STRONG keywords + curated terms, filtered for noise.

    Strong (weight-3) keywords are the most specific; moderate/weak are too generic.
    Multi-word phrases are kept as-is (they're specific); single words must be >= 4
    chars and pass a generic stoplist, which drops high-frequency words ("analysis",
    "design", "creative"…) that would otherwise create false "you're missing X" gaps.
    """
    terms = set(_CURATED_SKILLS)
    for role in ROLE_PROFILES:
        for kw in role.keywords_strong or []:
            t = str(kw).strip().lower()
            if not t or len(t) > 40 or t in _GENERIC_STOP:
                continue
            if " " in t:
                terms.add(t)
            elif len(t) >= 4:
                terms.add(t)
    return sorted(terms)


_GENERIC_STOP = {
    "analysis", "design", "creative", "culture", "color", "engineering", "architecture",
    "architect", "asset", "distribution", "community", "campaign", "flavor", "language",
    "engine", "process", "system", "team", "project", "service", "solution", "product",
    "development", "management", "support", "quality", "standard", "build", "work",
    "people", "customer", "client", "business", "company", "market", "content", "brand",
    "strategy", "plan", "model", "tool", "technology", "technical", "experience",
    "skill", "knowledge", "environment", "information", "training", "education", "care",
    "treatment", "patient", "food", "water", "energy", "legal", "government", "policy",
    "program", "resource", "testing", "maintenance", "operation", "production",
    "manufacturing", "communication", "presentation", "leadership", "documentation",
    "reporting", "writing", "reading", "data", "research", "report", "network",
    "software", "application", "platform", "cloud", "security", "job", "role", "position",
}


SKILLS_LEXICON = _build_skills_lexicon()


def _has(text_lower: str, kw: str) -> bool:
    """Word-boundary prefix match (stem 'collaborat' catches collaborate/collaboration)."""
    return re.search(rf"\b{re.escape(kw)}", text_lower) is not None


def _strip_html(raw: str) -> str:
    import html as _html

    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    return re.sub(r"[ \t]+", " ", txt).strip()


def fetch_job(url: str) -> dict:
    """Fetch a job posting and extract title / company / description.

    Prefers the embedded schema.org `JobPosting` JSON-LD (present on Ashby, Greenhouse,
    Lever, Workday, etc.); falls back to `<title>` + stripped body HTML.
    """
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": BROWSER_UA,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        src = resp.read().decode("utf-8", errors="ignore")

    m = re.search(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', src, re.S | re.I
    )
    if m:
        for block in re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', src, re.S | re.I
        ):
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict) and data.get("@type") == "JobPosting":
                org = data.get("hiringOrganization") or {}
                return {
                    "title": data.get("title", ""),
                    "company": org.get("name", "") if isinstance(org, dict) else "",
                    "description": _strip_html(data.get("description", "")),
                    "url": url,
                }

    title = re.search(r"<title>([^<]*)</title>", src, re.S | re.I)
    body = _strip_html(src)
    return {
        "title": title.group(1).strip() if title else "",
        "company": "",
        "description": body,
        "url": url,
    }


def _years_required(job_text: str) -> str:
    """Best-effort extraction of a stated years-of-experience requirement."""
    m = re.search(
        r"(\d+)\s*(?:\+|\s*(?:-|to)\s*\d+)?\s*(?:\+?\s*)?years?",
        job_text,
        re.I,
    )
    if m:
        return m.group(0)
    return ""


def analyze_keywords(resume_text: str, job_text: str) -> dict:
    """Compare resume vs job vocabulary using the skills lexicon."""
    resume_l = (resume_text or "").lower()
    job_l = (job_text or "").lower()

    aligned, gaps, extra = [], [], []
    for kw in SKILLS_LEXICON:
        in_job = _has(job_l, kw)
        in_resume = _has(resume_l, kw)
        if in_job and in_resume:
            aligned.append(kw)
        elif in_job and not in_resume:
            gaps.append(kw)
        elif in_resume and not in_job:
            extra.append(kw)

    covered = len(aligned)
    missing = len(gaps)
    score = round(covered / (covered + missing) * 100, 1) if (covered + missing) else None

    return {
        "aligned": aligned,
        "gaps": gaps,
        "extra": extra,
        "aligned_count": covered,
        "gap_count": missing,
        "extra_count": len(extra),
        "score": score,
    }


def map_job_signals(job_text: str) -> dict:
    """Map the job description to MBTI / Holland / Big Five (same detectors as resumes)."""
    return {
        "mbti": detect_mbti_signals(job_text),
        "holland": detect_holland_signals(job_text),
        "big_five": detect_big_five_signals(job_text),
    }


def _mbti_match(user_type: str, job_type: str) -> tuple[int, int]:
    matched = known = 0
    for u, j in zip(user_type, job_type):
        if u == "X" or not j:
            continue
        known += 1
        if u == j:
            matched += 1
    return matched, known


def _holland_overlap(user_code: str, job_code: str) -> list[str]:
    return [c for c in (user_code or "")[:3] if c and c in (job_code or "")]


def _level_key(v: str) -> str:
    if not v:
        return ""
    if "High" in v:
        return "High"
    if "Medium" in v:
        return "Medium"
    return "Low"


def compare_signals(user_signals: dict, job_signals: dict) -> dict:
    """Psychometric alignment: how well the user's signals match the job's language."""
    user_mbti = (user_signals.get("mbti", {}) or {}).get("inferred_type", "")
    job_mbti = (job_signals.get("mbti", {}) or {}).get("inferred_type", "")
    user_holland = (user_signals.get("holland", {}) or {}).get("inferred_code", "")
    job_holland = (job_signals.get("holland", {}) or {}).get("inferred_code", "")

    m_matched, m_known = _mbti_match(user_mbti, job_mbti)
    mbti_pct = round(m_matched / m_known * 100, 1) if m_known else None

    h_overlap = _holland_overlap(user_holland, job_holland)
    holland_pct = round(len(h_overlap) / 3 * 100, 1) if job_holland else None

    # Big Five: count traits where the user's level matches the job's inferred level.
    user_bf = (user_signals.get("big_five", {}) or {}).get("inferred_profile", {})
    job_bf = (job_signals.get("big_five", {}) or {}).get("inferred_profile", {})
    bf = {}
    for t in ("O", "C", "E", "A", "N"):
        u = _level_key(user_bf.get(t, ""))
        j = _level_key(job_bf.get(t, ""))
        bf[t] = {"user": user_bf.get(t, ""), "job": job_bf.get(t, ""), "match": bool(u and j and u == j)}
    bf_matches = sum(1 for v in bf.values() if v["match"])
    bf_known = sum(1 for v in bf.values() if v["job"])
    bf_pct = round(bf_matches / bf_known * 100, 1) if bf_known else None

    # Overall: average of the available framework scores.
    parts = [p for p in (mbti_pct, holland_pct, bf_pct) if p is not None]
    overall = round(sum(parts) / len(parts), 1) if parts else None

    return {
        "mbti": {"user": user_mbti, "job": job_mbti, "match_pct": mbti_pct},
        "holland": {
            "user": user_holland,
            "job": job_holland,
            "overlap": h_overlap,
            "match_pct": holland_pct,
        },
        "big_five": {"traits": bf, "match_pct": bf_pct},
        "overall": overall,
    }


def _keyword_explanation(kw: dict, years: str) -> str:
    lines = []
    if kw["aligned"]:
        sample = ", ".join(kw["aligned"][:12])
        lines.append(
            f"Your background aligns on {kw['aligned_count']} keyword(s) the posting calls for "
            f"(e.g. {sample})."
        )
    if kw["gaps"]:
        sample = ", ".join(kw["gaps"][:12])
        lines.append(
            f"You're missing {kw['gap_count']} keyword(s) the posting emphasizes "
            f"(e.g. {sample}) — the job mentions these but your resume doesn't."
        )
    if kw["extra"]:
        sample = ", ".join(kw["extra"][:12])
        lines.append(
            f"Your resume carries {kw['extra_count']} skill(s) beyond the posting's vocabulary "
            f"(e.g. {sample}) — relevant experience, but not what this role prioritizes."
        )
    if years:
        lines.append(f"The posting asks for around {years} of experience.")
    if kw["score"] is not None:
        lines.append(f"Keyword coverage: {kw['score']}% of the posting's signal terms appear in your resume.")
    return " ".join(lines)


def analyze_job(url: str, resume_text: str = "", mbti: str = "", holland: str = "") -> dict:
    """Full job-alignment analysis. resume_text drives keyword + signal inference;
    mbti/holland override the user's signals when resume_text is absent (signals mode)."""
    job = fetch_job(url)
    job_text = job["description"]

    job_signals = map_job_signals(job_text)
    years = _years_required(job_text)

    # User signals: prefer resume inference; fall back to explicit mbti/holland.
    user_signals = {}
    if resume_text and resume_text.strip():
        user_signals = map_job_signals(resume_text)
        kw = analyze_keywords(resume_text, job_text)
    else:
        user_signals = {
            "mbti": {"inferred_type": (mbti or "").strip().upper()},
            "holland": {"inferred_code": (holland or "").strip().upper()},
            "big_five": {"inferred_profile": {}},
        }
        kw = {
            "aligned": [], "gaps": [], "extra": [],
            "aligned_count": 0, "gap_count": 0, "extra_count": 0, "score": None,
        }

    psych = compare_signals(user_signals, job_signals)

    return {
        "job": {
            "title": job["title"],
            "company": job["company"],
            "url": job["url"],
            "years_required": years,
            "description": job_text,
        },
        "job_signals": job_signals,
        "user_signals": user_signals,
        "keyword_alignment": kw,
        "psychometric_alignment": psych,
        "explanation": _keyword_explanation(kw, years),
    }
