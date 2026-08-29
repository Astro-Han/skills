import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


grader = load_module("pr_review_eval_grader", ROOT / "evals" / "grader.py")
runner = load_module("pr_review_eval_runner", ROOT / "evals" / "runner.py")


class PrReviewEvalTests(unittest.TestCase):
    def test_suite_pairs_no_skill_and_shipped_skill(self):
        runs = runner.suite_runs("codex", reps=1, suite="pr-review")
        self.assertEqual(len(runs), 8)
        self.assertEqual({run["arm"] for run in runs}, {"without_skill", "with_skill"})
        self.assertEqual(len({run["eval"] for run in runs}), 4)

    def test_holdout_is_separate_from_design_cases(self):
        design = runner.suite_runs("codex", reps=1, suite="pr-review")
        holdout = runner.suite_runs("codex", reps=1, suite="pr-review-holdout")
        self.assertEqual(len(holdout), 2)
        self.assertTrue({run["eval"] for run in design}.isdisjoint(
            {run["eval"] for run in holdout}
        ))

    def test_section_position_accepts_english_and_chinese_headings(self):
        self.assertEqual(grader.section_position("intro\n## Problem\nbody", "problem", "问题"), 6)
        self.assertEqual(grader.section_position("# 问题与真实性\nbody", "problem", "问题"), 0)
        self.assertEqual(grader.section_position("## 方案与生产组合\nbody", "solution", "方案"), 0)


if __name__ == "__main__":
    unittest.main()
