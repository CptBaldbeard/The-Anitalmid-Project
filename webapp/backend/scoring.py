"""Role scoring — reuses the bundled resume_matcher.match_resume_to_roles()."""
from dataclasses import asdict

from . import resume_matcher as rm


def score_roles(text: str) -> tuple[list, dict]:
    """Score resume text against all role profiles.

    Returns (ranking, signals) where ranking is a list of JSON-safe dicts and
    signals is the {mbti, holland, big_five} dict.
    """
    results, mbti, holland, big_five = rm.match_resume_to_roles(text)

    ranking = []
    for r in results:
        role = asdict(r["role"])
        ranking.append(
            {
                "title": role["title"],
                "category": role["category"],
                "composite_score": r["composite_score"],
                "keyword_score": r["keyword_score"],
                "framework_score": r["framework_score"],
                "experience_boost": r["experience_boost"],
                "holland_code": role["holland_code"],
                "o_net_code": role["o_net_code"],
                "mbti_type": role["mbti_type"],
                "salary_range": role["salary_range"],
                "pivot_cost": role["pivot_cost"],
                "experience_required": role["experience_required"],
                "description": role["description"],
                "keywords_strong": role["keywords_strong"],
            }
        )

    signals = {"mbti": mbti, "holland": holland, "big_five": big_five}
    return ranking, signals
