"""OSKG-style validation — flags each role as experience- vs aptitude-validated.

The full OSKG uses typed claim edges (Depends on / Supports / Contradicts).
For the web product this is the lightweight convergence rule from the pipeline:
a role is EXPERIENCE-validated when keyword evidence is strong, APTITUDE-validated
when framework compatibility is strong, and weak otherwise.
"""


def validate_roles(ranking: list) -> list:
    """Annotate each role with a validation tag and assign rank.

    Thresholds mirror the resume_matcher scoring semantics:
      - keyword_score >= 40  -> strong experience evidence
      - framework_score >= 40 -> strong aptitude evidence
    """
    EXPERIENCE_THRESHOLD = 40.0
    APTITUDE_THRESHOLD = 40.0

    for i, role in enumerate(ranking, 1):
        role["rank"] = i
        kw = role["keyword_score"]
        fw = role["framework_score"]

        if kw >= EXPERIENCE_THRESHOLD:
            role["validation"] = "experience-validated"
        elif fw >= APTITUDE_THRESHOLD:
            role["validation"] = "aptitude-validated"
        else:
            role["validation"] = "weak"

    return ranking
