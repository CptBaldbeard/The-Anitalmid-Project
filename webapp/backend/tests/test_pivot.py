"""Tests for the Career Pivot engine (backend/pivot.py)."""

import unittest

from backend.pivot import compute_pivot

# A few canonical categories for test data.
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
    out = []
    for i in range(150):
        out.append(role(f"R{i:03d}", CATS[i % len(CATS)], 100.0 - i * 0.5))
    return out


class PivotEngineTests(unittest.TestCase):
    def test_excludes_top_matches(self):
        ranking = ranking_150()
        pool = compute_pivot(ranking)
        top6 = {f"R{i:03d}" for i in range(6)}
        self.assertFalse(top6 & {r["title"] for r in pool})

    def test_pool_is_25_with_diverse_catalog(self):
        pool = compute_pivot(ranking_150())
        self.assertEqual(len(pool), 25)

    def test_diversity_cap(self):
        ranking = [role(f"T{i}", "Technology", 100 - i) for i in range(12)]
        ranking += [role(f"S{i}", "Science", 60 - i) for i in range(20)]
        pool = compute_pivot(ranking, top_n_exclude=0, max_per_category=5)
        self.assertLessEqual(sum(1 for r in pool if r["category"] == "Technology"), 5)

    def test_interests_outrank_experience(self):
        # interests boost (+10) should beat experience boost (+5), both beat no boost.
        ranking = [
            role("A", "Science", 90.0),
            role("B", "Technology", 89.0),
            role("C", "Arts & Entertainment", 88.0),
        ]
        pool = compute_pivot(
            ranking,
            education_experience=["MS in Computer Science"],   # Technology +5
            education_interests=["MFA Creative Writing"],       # Arts & Entertainment +10
            top_n_exclude=0,
        )
        self.assertEqual([r["title"] for r in pool], ["C", "B", "A"])
        self.assertTrue(pool[0]["education_boost"])
        self.assertEqual(pool[0]["pivot_score"], 98.0)
        self.assertFalse(pool[2]["education_boost"])
        self.assertEqual(pool[2]["pivot_score"], 90.0)

    def test_education_boost_flag(self):
        ranking = ranking_150()
        pool = compute_pivot(ranking, education_interests=["MS in Data Science"])  # Technology
        tech = [r for r in pool if r["category"] == "Technology"]
        self.assertTrue(tech, "expected some Technology roles in the pool")
        self.assertTrue(all(r["education_boost"] for r in tech))
        self.assertTrue(all(r["pivot_score"] > r["composite_score"] for r in tech))

    def test_hobbies_do_not_change_ranking(self):
        ranking = ranking_150()
        p1 = compute_pivot(ranking, [], [], ["woodworking", "gaming"])
        p2 = compute_pivot(ranking, [], [], [])
        self.assertEqual([r["title"] for r in p1], [r["title"] for r in p2])

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
