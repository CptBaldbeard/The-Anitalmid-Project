"""Camoufox-powered career expansion — structured role entries beyond the core 10.

Searches Camoufox for career fields matching the user's Holland (RIASEC) code and
MBTI type, then structures each hit into an "expanded role" entry with a cleaned
career title, Holland code, field category, and a best-effort salary / pivot-cost.
"""
import asyncio
import json
import random
import re
import time
import urllib.parse
import urllib.request

CAMOUFOX_URL = "http://localhost:8000/search"

# In-memory cache: Holland code -> (entries, timestamp). TTL avoids stale results
# and unbounded growth while still preventing re-bursting the scraper.
_CACHE: dict = {}
_CACHE_TTL = 3600  # seconds

# Site-name suffixes to strip from result titles ("... — Truity").
_SITE_STRIP = re.compile(r"\s*[—–-]\s*[^—–-]{0,60}$")
# Salary figures: $65,000 / $65k / $45k–$80k / $52,000 - $78,000
_SALARY_RE = re.compile(
    r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*[kK]?(?:\s*(?:[-–—]|to)\s*\$?\s?\d{1,3}(?:,\d{3})*\s*[kK]?)?"
)

_TECH = ("engineer", "developer", "software", "data", "analyst", "security", "network",
         "system", "cloud", "it ", "administrator", "specialist", "technician", "devops")
_BUSINESS = ("accountant", "auditor", "finance", "bank", "bookkeep", "compliance", "actuary")
_CREATIVE = ("writer", "design", "artist", "media", "music", "illustrat", "photograph", "author")
_SCIENCE = ("research", "scientist", "laborator", "academic", "biolog", "chemist", "geolog")
_HEALTH = ("nurse", "doctor", "health", "therap", "physician", "dental", "counsel")


def _search(query: str, max_results: int = 6) -> list:
    q = urllib.parse.quote(query)
    url = f"{CAMOUFOX_URL}?q={q}&max={max_results}"
    req = urllib.request.Request(url, headers={"User-Agent": "anitalmid/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        return data.get("results", [])
    except Exception as e:
        print(f"[expansion] Camoufox search failed for '{query}': {e}")
        return []


def _build_queries(holland_code: str, signals: dict) -> list:
    queries = []
    if holland_code:
        queries.append(f"careers for Holland code {holland_code}")
        queries.append(f"jobs for {holland_code} RIASEC personality type")
    mbti = (signals.get("mbti") or {}).get("inferred_type")
    if mbti:
        queries.append(f"best careers for {mbti} personality")
    return queries


def _clean_title(title: str) -> str:
    t = _SITE_STRIP.sub("", title or "").strip()
    # "Holland Code CRI (The Technical Auditor)" -> "The Technical Auditor"
    m = re.search(r"\(the\s+([^)]+)\)", t, flags=re.I)
    if m:
        return m.group(1).strip()
    # Drop remaining parentheticals and leading labels.
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"^(search|list of|holland code [A-Z]{2,3}|top \d+|best|\d+ best)\s*[-—:–]?\s*", "", t, flags=re.I)
    return t.strip()


def _extract_salary(text: str) -> str | None:
    m = _SALARY_RE.search(text or "")
    return re.sub(r"\s+", " ", m.group(0)).strip() if m else None


def _classify(title: str) -> str:
    t = title.lower()
    if any(k in t for k in _TECH):
        return "Technology"
    if any(k in t for k in _BUSINESS):
        return "Business & Finance"
    if any(k in t for k in _CREATIVE):
        return "Creative & Media"
    if any(k in t for k in _SCIENCE):
        return "Science & Research"
    if any(k in t for k in _HEALTH):
        return "Healthcare"
    return "Other"


def _estimate_pivot(title: str, category: str) -> str:
    t = title.lower()
    if category == "Technology":
        return "Low"
    if any(k in t for k in ("professor", "physician", "doctor", "lawyer", "scientist", "nurse")):
        return "High"
    if any(k in t for k in ("writer", "analyst", "researcher", "design", "consultant")):
        return "Medium"
    return "Medium"


async def search_expanded_roles(holland_code: str, signals: dict) -> list:
    """Return structured expanded-role entries (deduped, capped, cached)."""
    key = holland_code or ""
    cached = _CACHE.get(key)
    if cached and time.time() - cached[1] < _CACHE_TTL:
        return cached[0]

    queries = _build_queries(holland_code, signals)
    batches = []
    for i, q in enumerate(queries):
        if i > 0:
            await asyncio.sleep(random.uniform(1.0, 2.5))  # jitter to dodge DDG burst rate-limiting
        batches.append(await asyncio.to_thread(_search, q, 6))

    raw = []
    for batch in batches:
        for r in batch:
            url = (r.get("url") or "").strip()
            if not url or not url.startswith("http"):
                continue
            raw.append({"title": r.get("title", ""), "url": url, "snippet": r.get("snippet", "")})

    seen = set()
    entries = []
    for r in raw:
        if r["url"] in seen:
            continue
        seen.add(r["url"])

        title = _clean_title(r["title"])
        if not title:
            continue
        category = _classify(title)
        salary = _extract_salary(r["snippet"]) or _extract_salary(title)
        entries.append(
            {
                "title": title,
                "holland_code": holland_code or "",
                "category": category,
                "salary_range": salary,
                "pivot_cost": _estimate_pivot(title, category),
                "source_url": r["url"],
                "snippet": (r.get("snippet") or "")[:240],
            }
        )

    _CACHE[key] = (entries[:10], time.time())
    return entries[:10]
