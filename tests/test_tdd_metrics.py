import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals" / "tdd"))

import metrics


CART = (ROOT / "evals" / "fixtures" / "cartlib" / "cartlib" / "cart.py").read_text()


class MutantGenerationTests(unittest.TestCase):
    def test_generates_deterministic_compilable_mutants(self):
        first = metrics.generate_mutants(CART)
        second = metrics.generate_mutants(CART)
        self.assertEqual(first, second)
        self.assertGreater(len(first), 5)
        for mutant in first:
            compile(mutant, "<mutant>", "exec")
            self.assertNotEqual(mutant, CART)


class SuiteMetricsTests(unittest.TestCase):
    def test_clean_fixture_has_no_meaningful_excess(self):
        result = metrics.suite_metrics(ROOT / "evals" / "fixtures" / "cartlib")
        self.assertEqual(result["tests_passing"], 5)
        self.assertGreater(result["kill_rate"], 0.3)
        self.assertLessEqual(result["excess_tests"], 1)

    def test_cluttered_fixture_reports_redundant_and_dead_weight_tests(self):
        result = metrics.suite_metrics(ROOT / "evals" / "fixtures" / "cartlib-cluttered")
        self.assertEqual(result["tests_passing"], 12)
        self.assertGreaterEqual(result["excess_tests"], 4)
        cover = set(result["minimal_cover"])
        self.assertNotIn("tests.test_cart.TestCart.test_subtotal_is_float", cover)
        self.assertNotIn("tests.test_cart.TestCart.test_add_many_items_nonempty", cover)


if __name__ == "__main__":
    unittest.main()
