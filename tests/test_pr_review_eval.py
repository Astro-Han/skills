import importlib.util
import json
import re
import subprocess
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

    def test_evidence_reconciliation_diagnostic_is_16_pairs(self):
        runs = runner.suite_runs(
            "codex", reps=2, suite="pr-review-evidence-reconciliation"
        )
        self.assertEqual(len(runs), 32)
        self.assertEqual(len(runs) // 2, 16)
        self.assertEqual(
            {run["arm"] for run in runs},
            {"baseline_skill", "candidate_skill"},
        )
        self.assertEqual(len({run["eval"] for run in runs}), 8)

    def test_evidence_reconciliation_selection_balances_roles(self):
        selection = json.loads(
            (
                ROOT
                / "evals/pr-review/evidence-reconciliation/selection.json"
            ).read_text()
        )
        roles = selection["roles"]
        self.assertEqual(len(roles["positive"]), 4)
        self.assertEqual(len(roles["clean_or_intentional_tradeoff_control"]), 4)
        self.assertEqual(
            set(selection["cases"]),
            set(roles["positive"])
            | set(roles["clean_or_intentional_tradeoff_control"]),
        )

    def test_reachability_regression_compares_frozen_and_shipped_skills(self):
        runs = runner.suite_runs("codex", reps=4, suite="pr-review-reachability")
        self.assertEqual(len(runs), 8)
        self.assertEqual({run["arm"] for run in runs}, {"pre_reachability", "with_skill"})
        self.assertEqual({run["eval"] for run in runs}, {"review-downstream-guard-blocks-path"})

    def test_partial_facts_suite_compares_frozen_and_shipped_skills(self):
        runs = runner.suite_runs("codex", reps=4, suite="pr-review-partial-facts")
        self.assertEqual(len(runs), 16)
        self.assertEqual({run["arm"] for run in runs}, {"complete_facts", "with_skill"})
        self.assertEqual(
            {run["eval"] for run in runs},
            {"review-offline-pr-patch", "review-exported-snapshot-before-approval"},
        )

    def test_no_status_suite_is_eight_ab_pairs(self):
        runs = runner.suite_runs("codex", reps=4, suite="pr-review-no-statuses")
        self.assertEqual(len(runs), 16)
        self.assertEqual({run["arm"] for run in runs}, {"three_states", "with_skill"})
        self.assertEqual(
            {run["eval"] for run in runs},
            {"review-parallel-authority-ux", "review-exported-snapshot-before-approval"},
        )

    def test_partial_fact_patches_match_their_base_sources(self):
        for fixture in ("prreview-offline-patch", "prreview-stale-approval"):
            subprocess.run(
                [
                    "git", "apply", "--check", "--directory=evals/fixtures/" + fixture,
                    "evals/fixtures/" + fixture + "/PATCH.diff",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

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

    def test_skill_uses_plain_review_terms(self):
        skill = (ROOT / "skills" / "pr-review" / "SKILL.md").read_text().lower()
        for invented_label in (
            "human confirmation required",
            "entropy delta",
            "witness chain",
            "decision packet",
            "production composition",
            "coherent entropy",
        ):
            self.assertNotIn(invented_label, skill)
        self.assertNotIn("approve/comment/wait", skill)
        self.assertNotIn("**wait**", skill)
        self.assertIn("name gaps, which do not block analysis", skill)
        self.assertIn("keep findings separate from merge and publication conditions", skill)
        self.assertIn("never call it approvable", skill)
        self.assertIn("**next step**", skill)

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

    def test_formal_state_parser_distinguishes_state_from_plain_action(self):
        self.assertEqual(
            grader.formal_review_state("## Recommendation\n**Wait** — manual UI check\n"),
            "wait",
        )
        self.assertEqual(
            grader.formal_review_state("## Recommendation: Approve\n"),
            "approve",
        )
        self.assertEqual(grader.formal_review_state("结论：Approve\n"), "approve")
        self.assertIsNone(
            grader.formal_review_state("## Next step\nRefresh the current head before approval.\n")
        )

    def test_approval_detector_allows_negative_guidance(self):
        self.assertTrue(grader.recommends_approval("The PR is ready to approve."))
        self.assertTrue(grader.recommends_approval("代码层面可以批准。"))
        self.assertTrue(grader.recommends_approval("This snapshot can be approved."))
        self.assertFalse(grader.recommends_approval("Do not approve before refreshing CI."))
        self.assertFalse(grader.recommends_approval("当前 PR 不能直接批准。"))
        self.assertFalse(grader.recommends_approval("不能把这个快照视为可批准的 PR。"))


if __name__ == "__main__":
    unittest.main()
