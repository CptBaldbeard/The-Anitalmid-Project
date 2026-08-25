"""Tests for the Career Pivot engine (backend/pivot.py)."""

import unittest
from collections import Counter

from backend.pivot import compute_pivot

CATS = [
    "Technology", "Healthcare", "Science", "Business & Finance", "Engineering",
    "Creative & Media", "Education", "Legal", "Public Safety", "Operations",
    "Arts & Entertainment", "Social Services", "Aviation", "Energy & Utilities",
    "Government & Nonprofit", "Agriculture & Environment", "Transportation",
    "Sports & Fitness", "Manufacturing & Production", "Hospitality & Tourism",
    "Architecture & Construction", "Veterinary", "Real Estate", "Skilled Trades",
]


def role(title, category, composite):
    return {
        "title": title,
        "category": category,
        "composite_score": composite,
        "keyword_score": 40,
        "framework_score": 40,
        "experience_boost": 0,
    }


def ranking_150():
    """150 fake roles spread across all 24 categories, scores descending."""
    return [role(f"R{i:03d}", CATS[i % len(CATS)], 100.0 - i * 0.5) for i in range(150)]


class PivotEngineTests(unittest.TestCase):
    def test_excludes_top_matches(self):
        ranking = ranking_150()
        pool = compute_pivot(ranking)
        top6 = {f"R{i:03d}" for i in range(6)}
        self.assertFalse(top6 & {r["title"] for r in pool})

    def test_pool_is_25(self):
        self.assertEqual(len(compute_pivot(ranking_150())), 25)

    def test_strictly_balanced_one_per_field(self):
        # Every field gets ~one role; no field dominates.
        pool = compute_pivot(ranking_150())
        counts = Counter(r["category"] for r in pool)
        self.assertEqual(len(counts), 24)          # all 24 fields represented
        self.assertLessEqual(max(counts.values()), 2)  # at most 2 in any field

    def test_no_technology_skew(self):
        # An INTJ/tech-flavored profile must NOT stack Technology in the pivot.
        pool = compute_pivot(ranking_150(), education_interests=["MS in Computer Science"])
        counts = Counter(r["category"] for r in pool)
        self.assertLessEqual(counts.get("Technology", 0), 2)

    def test_relevant_fields_ordered_first(self):
        pool = compute_pivot(
            ranking_150(),
            education_interests=["MS in Data Science"],
            hobbies=["woodworking"],
        )
        relevant = {"Technology", "Skilled Trades", "Manufacturing & Production", "Arts & Entertainment"}
        # The one-per-field portion (everything before the bonus slot) orders relevant first.
        primary = pool[:24]
        idx_relevant = [i for i, r in enumerate(primary) if r["category"] in relevant]
        idx_other = [i for i, r in enumerate(primary) if r["category"] not in relevant]
        self.assertTrue(idx_relevant and idx_other)
        self.assertLess(max(idx_relevant), min(idx_other))

    def test_education_match_flag(self):
        pool = compute_pivot(ranking_150(), education_interests=["MS in Data Science"])
        tech = [r for r in pool if r["category"] == "Technology"]
        self.assertTrue(tech)
        self.assertTrue(all(r["education_match"] for r in tech))

    def test_hobby_match_flag(self):
        pool = compute_pivot(ranking_150(), hobbies=["woodworking"])
        wood = [r for r in pool if r["category"] == "Skilled Trades"]
        self.assertTrue(wood)
        self.assertTrue(all(r["hobby_match"] for r in wood))

    def test_hobbies_do_not_break_balance(self):
        pool = compute_pivot(ranking_150(), hobbies=["drone flying", "gaming"])
        counts = Counter(r["category"] for r in pool)
        self.assertLessEqual(max(counts.values()), 2)

    def test_short_ranking_returns_empty(self):
        self.assertEqual(compute_pivot([role("A", "Science", 90.0)]), [])

    def test_empty_ranking_returns_empty(self):
        self.assertEqual(compute_pivot([]), [])

    def test_unknown_education_is_ignored(self):
        ranking = ranking_150()
        base = compute_pivot(ranking)
        bogus = compute_pivot(ranking, education_interests=["totally made up"])
        self.assertEqual([r["title"] for r in base], [r["title"] for r in bogus])


if __name__ == "__main__":
    unittest.main()
