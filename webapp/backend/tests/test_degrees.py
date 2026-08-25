"""Tests for the degree catalog (backend/degrees.py)."""

import unittest

from backend import degrees
from backend.degrees import CATEGORIES, DEGREES, Degree, LEVELS


class DegreeCatalogTests(unittest.TestCase):
    def test_catalog_is_comprehensive(self):
        # Undergrad (~250) + Masters + Doctoral.
        self.assertGreaterEqual(len(DEGREES), 700)

    def test_undergrad_roughly_250(self):
        undergrad = [d for d in DEGREES if d.level == "Undergraduate"]
        self.assertGreaterEqual(len(undergrad), 220)

    def test_names_are_unique(self):
        names = [d.name.lower() for d in DEGREES]
        self.assertEqual(len(names), len(set(names)))

    def test_every_degree_has_level_and_category(self):
        for d in DEGREES:
            self.assertIsInstance(d, Degree)
            self.assertIn(d.level, LEVELS, f"{d.name} has bad level {d.level}")
            self.assertTrue(d.categories, f"{d.name} missing category")

    def test_categories_are_canonical(self):
        for d in DEGREES:
            for cat in d.categories:
                self.assertIn(cat, CATEGORIES, f"{d.name} maps to unknown category {cat}")

    def test_degrees_by_level_is_grouped(self):
        grouped = degrees.degrees_by_level()
        self.assertEqual(set(grouped), set(LEVELS))
        total = sum(len(v) for v in grouped.values())
        self.assertEqual(total, len(DEGREES))

    def test_degree_names_is_sorted_and_matches_catalog(self):
        names = degrees.degree_names()
        self.assertEqual(len(names), len(DEGREES))
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_resolve_degree_exact(self):
        self.assertEqual(degrees.resolve_degree("MBA").name, "MBA")

    def test_resolve_degree_undergrad(self):
        d = degrees.resolve_degree("B.S. in Computer Science")
        self.assertIsNotNone(d)
        self.assertEqual(d.level, "Undergraduate")

    def test_resolve_degree_case_insensitive(self):
        d = degrees.resolve_degree("ms in computer science")
        self.assertIsNotNone(d)
        self.assertEqual(d.name, "MS in Computer Science")

    def test_resolve_degree_unknown(self):
        self.assertIsNone(degrees.resolve_degree("zzz not a degree"))

    def test_map_catalog_degrees(self):
        cats = degrees.map_degrees_to_categories(["MS in Data Science", "MFA Creative Writing"])
        self.assertEqual(cats, {"Technology", "Arts & Entertainment"})

    def test_map_undergrad_degree(self):
        cats = degrees.map_degrees_to_categories(["B.S. in Nursing"])
        self.assertEqual(cats, {"Healthcare"})

    def test_map_free_text_degree(self):
        cats = degrees.map_degrees_to_categories(["Master of Science in Nursing"])
        self.assertIn("Healthcare", cats)

    def test_map_garbage_is_ignored(self):
        cats = degrees.map_degrees_to_categories(["totally made up thing"])
        self.assertEqual(cats, set())

    def test_map_empty_list(self):
        self.assertEqual(degrees.map_degrees_to_categories([]), set())


if __name__ == "__main__":
    unittest.main()
