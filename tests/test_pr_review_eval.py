import importlib.util
import re
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
        self.assertEqual(len(runs), 20)
        self.assertEqual({run["arm"] for run in runs}, {"without_skill", "with_skill"})
        self.assertEqual(len({run["eval"] for run in runs}), 10)

    def test_full_matrix_is_48_ab_pairs_and_96_model_runs(self):
        design = runner.suite_runs("codex", reps=4, suite="pr-review")
        holdout = runner.suite_runs("codex", reps=4, suite="pr-review-holdout")
        runs = design + holdout
        self.assertEqual(len(runs), 96)
        self.assertEqual(len(runs) // 2, 48)
        self.assertEqual(len({run["eval"] for run in runs}), 12)

    def test_matrix_has_declared_trigger_boundary(self):
        design_cases = [runner.PR_REVIEW_CASES[name] for name in runner.PR_REVIEW_DESIGN_CASES]
        self.assertEqual(sum(case["should_trigger"] for case in design_cases), 8)
        self.assertEqual(sum(not case["should_trigger"] for case in design_cases), 2)
        self.assertEqual(len(runner.PR_REVIEW_HOLDOUT_CASES), 2)

    def test_skill_is_english_only_and_within_direct_context_budget(self):
        skill = (ROOT / "skills" / "pr-review" / "SKILL.md").read_text()
        reference = (
            ROOT / "skills" / "pr-review" / "references" / "queue-and-publication.md"
        ).read_text()
        self.assertFalse(re.search(r"[\u4e00-\u9fff]", skill))
        self.assertLessEqual(len(skill.split()), 750)
        self.assertLessEqual(len(skill.split()) + len(reference.split()), 1000)

    def test_holdout_is_separate_from_design_cases(self):
        design = runner.suite_runs("codex", reps=1, suite="pr-review")
        holdout = runner.suite_runs("codex", reps=1, suite="pr-review-holdout")
        self.assertEqual(len(holdout), 4)
        self.assertTrue({run["eval"] for run in design}.isdisjoint(
            {run["eval"] for run in holdout}
        ))

    def test_section_position_accepts_english_and_chinese_headings(self):
        self.assertEqual(grader.section_position("intro\n## Problem\nbody", "problem", "问题"), 6)
        self.assertEqual(grader.section_position("# 问题与真实性\nbody", "problem", "问题"), 0)
        self.assertEqual(grader.section_position("## 方案与生产组合\nbody", "solution", "方案"), 0)

    def test_split_parser_accepts_verbose_and_compact_forms(self):
        self.assertTrue(grader.component_split_present(
            "Production: 12 additions, 3 deletions", "production", 12, 3
        ))
        self.assertTrue(grader.component_split_present(
            "Tests +15/-0", "tests", 15, 0
        ))

    def test_recommendation_parser_reads_heading_then_choice(self):
        self.assertEqual(
            grader.recommendation_choice("## Recommendation\n**Human confirmation required**\n"),
            "human confirmation required",
        )
        self.assertEqual(
            grader.recommendation_choice("## Recommendation: Approve\n"),
            "approve",
        )


if __name__ == "__main__":
    unittest.main()
