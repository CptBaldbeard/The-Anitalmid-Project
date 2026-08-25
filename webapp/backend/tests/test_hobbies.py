"""Tests for the hobby catalog + signal mapping (backend/hobbies.py)."""

import unittest

from backend import hobbies
from backend.hobbies import HOBBIES, Hobby, STRENGTH_WEIGHT


class HobbyCatalogTests(unittest.TestCase):
    def test_catalog_has_many_hobbies(self):
        self.assertGreaterEqual(len(HOBBIES), 150)

    def test_names_are_unique(self):
        names = [h.name.lower() for h in HOBBIES]
        self.assertEqual(len(names), len(set(names)))

    def test_every_hobby_has_categories_and_strength(self):
        for h in HOBBIES:
            self.assertIsInstance(h, Hobby)
            self.assertTrue(h.categories, f"{h.name} missing categories")
            self.assertIn(h.strength, STRENGTH_WEIGHT, f"{h.name} bad strength")

    def test_holland_hints_are_valid(self):
        for h in HOBBIES:
            for letter in h.holland:
                self.assertIn(letter, "RIASEC", f"{h.name} bad holland letter {letter}")

    def test_hobby_names_is_sorted(self):
        names = hobbies.hobby_names()
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_resolve_hobby_exact(self):
        self.assertEqual(hobbies.resolve_hobby("drone flying").name, "drone flying")

    def test_resolve_hobby_case_insensitive(self):
        self.assertEqual(hobbies.resolve_hobby("Drone Flying").name, "drone flying")

    def test_resolve_hobby_fuzzy(self):
        self.assertIsNotNone(hobbies.resolve_hobby("photography"))

    def test_resolve_hobby_unknown(self):
        self.assertIsNone(hobbies.resolve_hobby("zzz not a hobby"))

    def test_map_hobby_to_categories(self):
        cats = hobbies.map_hobbies_to_categories(["drone flying"])
        self.assertIn("Creative & Media", cats)
        self.assertIn("Real Estate", cats)
        self.assertIn("Aviation", cats)

    def test_map_unknown_hobby_is_ignored(self):
        self.assertEqual(hobbies.map_hobbies_to_categories(["zzz"]), {})

    def test_hobby_signals_aggregate(self):
        sig = hobbies.hobby_signals(["drone flying", "woodworking"])
        self.assertIn("R", sig["holland"])   # both Realistic-ish
        self.assertEqual(sig["big_five"].get("O"), "High")

    def test_hobby_signals_empty(self):
        self.assertEqual(hobbies.hobby_signals([]), {"holland": "", "big_five": {}, "mbti": ""})


if __name__ == "__main__":
    unittest.main()
