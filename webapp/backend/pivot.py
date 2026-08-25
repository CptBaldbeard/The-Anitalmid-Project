"""Career Pivot engine — strictly balanced field selection.

Unlike the main matcher (which ranks by profile fit), the pivot returns ONE career
per field across the catalog so no single field dominates. Education + hobbies mark
fields *relevant* (used for ordering and the bonus slots) but every field is weighted
equally: the pivot never skews toward Technology or the user's home field.

Deterministic, no LLM.
"""

from __future__ import annotations

from .degrees import map_degrees_to_categories
from .hobbies import map_hobbies_to_categories

TOP_N_EXCLUDE: int = 6
POOL_SIZE: int = 25

HOBBIES_NOTE: str = "Hobbies are matched against the frameworks and the career fields they point to."


def compute_pivot(
    full_ranking: list[dict],
    education_experience: list[str] | None = None,
    education_interests: list[str] | None = None,
    hobbies: list[str] | None = None,
    top_n_exclude: int = TOP_N_EXCLUDE,
    pool_size: int = POOL_SIZE,
) -> list[dict]:
    """Return a strictly balanced pool: ~one role per career field.

    Each returned role is annotated with ``pivot_score`` (its profile-alignment
    score, unchanged), ``education_match`` (its field matches the user's education)
    and ``hobby_match`` (its field matches a hobby). No field is weighted above
    another.
    """
    ranking = list(full_ranking or [])
    ranking.sort(key=lambda r: r.get("composite_score", 0.0), reverse=True)

    # The "basic Top matches" are excluded — the pivot is about what's *beyond* them.
    rest = ranking[top_n_exclude:]

    ed_cats = map_degrees_to_categories((education_experience or []) + (education_interests or []))
    hobby_cats = map_hobbies_to_categories(hobbies or [])  # {category: summed strength}

    # Relevance per field = education flag + hobby strength. Used only for ordering
    # and bonus slots — NOT for scoring a field above another.
    relevance: dict[str, float] = {}
    for cat in set(ed_cats) | set(hobby_cats):
        relevance[cat] = (1.0 if cat in ed_cats else 0.0) + hobby_cats.get(cat, 0.0)

    # One best role per field (rest is already composite-sorted, so first wins).
    best_by_cat: dict[str, dict] = {}
    for r in rest:
        cat = r.get("category", "Other")
        best_by_cat.setdefault(cat, r)

    def annotate(r: dict) -> dict:
        cat = r.get("category", "")
        r["pivot_score"] = float(r.get("composite_score", 0.0))
        r["education_match"] = cat in ed_cats
        r["hobby_match"] = cat in hobby_cats
        return r

    # Order fields: relevant first (relevance desc, then alignment desc), then the rest.
    def field_sort_key(cat: str) -> tuple:
        role = best_by_cat[cat]
        return (-relevance.get(cat, 0.0), -role.get("composite_score", 0.0))

    ordered_cats = sorted(best_by_cat, key=field_sort_key)
    pool = [annotate(best_by_cat[cat]) for cat in ordered_cats]

    # Top up to pool_size with extra roles, preferring relevant fields (bonus slots).
    if len(pool) < pool_size:
        used = {r["title"] for r in pool}
        extras = [r for r in rest if r["title"] not in used]
        extras.sort(
            key=lambda r: (
                -relevance.get(r.get("category", ""), 0.0),
                -r.get("composite_score", 0.0),
            )
        )
        for r in extras:
            if len(pool) >= pool_size:
                break
            pool.append(annotate(r))

    return pool[:pool_size]
