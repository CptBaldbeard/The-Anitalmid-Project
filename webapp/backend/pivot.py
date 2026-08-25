"""Career Pivot engine.

Turns the main analysis' full role ranking into a pool of 25 related-but-different
careers: it excludes the top matches (already shown to the user), boosts fields the
user's education points at, and enforces per-field diversity so the pool spans
different career fields rather than re-listing the same field.

Deterministic, no LLM — consistent with the rest of the pipeline.
"""

from __future__ import annotations

from .degrees import map_degrees_to_categories

BOOST_EXPERIENCE: float = 5.0
BOOST_INTERESTS: float = 10.0
TOP_N_EXCLUDE: int = 6
POOL_SIZE: int = 25
MAX_PER_CATEGORY: int = 5

HOBBIES_NOTE: str = "Hobbies are noted for future refinement and do not affect this ranking."


def compute_pivot(
    full_ranking: list[dict],
    education_experience: list[str] | None = None,
    education_interests: list[str] | None = None,
    hobbies: list[str] | None = None,
    top_n_exclude: int = TOP_N_EXCLUDE,
    pool_size: int = POOL_SIZE,
    max_per_category: int = MAX_PER_CATEGORY,
    boost_experience: float = BOOST_EXPERIENCE,
    boost_interests: float = BOOST_INTERESTS,
) -> list[dict]:
    """Return the pivot pool of at most ``pool_size`` roles (usually 25).

    Each returned role dict is annotated with ``pivot_score`` (composite + education
    boost) and ``education_boost`` (True when its field matched the user's education).
    Hobbies are intentionally not scored in v1.
    """
    del hobbies  # reserved for a future scoring pass

    ranking = list(full_ranking or [])
    # Stable, deterministic baseline order (matches the main analysis' sort).
    ranking.sort(key=lambda r: r.get("composite_score", 0.0), reverse=True)

    # The "basic Top matches" are excluded — the pivot is about what's *beyond* them.
    rest = ranking[top_n_exclude:]

    exp_cats = map_degrees_to_categories(education_experience or [])
    int_cats = map_degrees_to_categories(education_interests or [])

    for r in rest:
        category = r.get("category", "")
        boost = 0.0
        if category in exp_cats:
            boost += boost_experience
        if category in int_cats:
            boost += boost_interests
        r["pivot_score"] = float(r.get("composite_score", 0.0)) + boost
        r["education_boost"] = boost > 0

    # Re-rank by pivot score, then walk with a per-category diversity cap.
    rest.sort(key=lambda r: r["pivot_score"], reverse=True)

    pool: list[dict] = []
    seen: dict[str, int] = {}
    for r in rest:
        category = r.get("category", "Other")
        if seen.get(category, 0) >= max_per_category:
            continue
        pool.append(r)
        seen[category] = seen.get(category, 0) + 1
        if len(pool) >= pool_size:
            break

    return pool
