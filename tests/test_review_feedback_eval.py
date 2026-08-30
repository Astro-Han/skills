import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


grader = load_module("eval_grader", ROOT / "evals" / "grader.py")
runner = load_module("eval_runner", ROOT / "evals" / "runner.py")


class ReviewFeedbackEvalTests(unittest.TestCase):
    def test_codex_transcript_preserves_messages_before_file_changes(self):
        rows = [
            {"type": "thread.started", "thread_id": "t"},
            {"type": "item.completed", "item": {
                "id": "m1", "type": "agent_message",
                "text": "C1 + C2 Verified P2 root cause invariant natural owner LineItem; "
                        "C3 No finding because sum([]) is zero.",
            }},
            {"type": "item.completed", "item": {
                "id": "f1", "type": "file_change",
                "changes": [{"path": "quoteview/model.py", "kind": "update"}],
            }},
        ]
        with tempfile.TemporaryDirectory() as directory:
            transcript = Path(directory) / "transcript.jsonl"
            transcript.write_text("\n".join(json.dumps(row) for row in rows))
            events, final = grader.load_events(transcript)

        ledger_index, _ = grader.adjudication_before(events, 1)
        self.assertEqual(ledger_index, 0)
        self.assertEqual(grader.first_production_edit(events, ("quoteview/model.py",)), 1)
        self.assertIn("C3 No finding", final)

    def test_scope_rebase_case_starts_from_an_existing_pr_diff(self):
        case = runner.REVIEW_FEEDBACK_CASES["rebase-cumulative-diff"]
        self.assertEqual(case["fixture"], "mediathread")
        self.assertEqual(case["seed_patch"], "mediathread-pr.patch")
        self.assertTrue((ROOT / "evals" / "seeds" / case["seed_patch"]).is_file())

    def test_causal_synthesis_case_scores_contracts_not_prescribed_slices(self):
        case = runner.REVIEW_FEEDBACK_CASES["synthesize-digest-flows"]
        self.assertEqual(case["kind"], "causal_synthesis")
        self.assertEqual(len(case["comments"]), 12)
        self.assertNotIn("slices", case)
        self.assertNotIn("expected_production_paths", case)
        self.assertNotIn("false_comment", case)

    def test_causal_design_suite_freezes_current_v3_as_baseline(self):
        runs = runner.suite_runs("codex", reps=2, suite="review-feedback-causal-design")
        self.assertEqual(len(runs), 4)
        self.assertEqual({run["eval"] for run in runs}, {"synthesize-digest-flows"})
        self.assertEqual(
            {run["skill_arm"] for run in runs},
            {"git:" + runner.REVIEW_FEEDBACK_CAUSAL_BASELINE_REF, runner.SHIPPED},
        )

    def test_entropy_helpers_measure_authority_growth_without_naming_the_solution(self):
        fixture = ROOT / "evals" / "fixtures" / "shipmentflow"
        self.assertEqual(grader.module_mutable_bindings(fixture, "shipmentflow/"), 0)
        self.assertEqual(grader.annotated_class_fields(fixture, "shipmentflow/"), 4)

    def test_causal_holdout_has_opposite_grouping_and_compatibility_pressure(self):
        case = runner.REVIEW_FEEDBACK_CASES["synthesize-shipment-flows"]
        self.assertEqual(case["cohort"], "holdout")
        self.assertEqual(case["fixture"], "shipmentflow")
        self.assertEqual(len(case["comments"]), 8)
        self.assertIn("legacy_route", case["prompt"])
        self.assertIn("normalize_text", case["prompt"])
        self.assertNotIn("slices", case)

    def test_fresh_holdouts_cover_mixed_and_independent_repair_shapes(self):
        subscription = runner.REVIEW_FEEDBACK_CASES["synthesize-subscription-flows"]
        policy = runner.REVIEW_FEEDBACK_CASES["synthesize-policy-flows"]
        self.assertEqual(subscription["cohort"], "fresh_holdout")
        self.assertEqual(policy["cohort"], "fresh_holdout")
        self.assertEqual(len(subscription["comments"]), 9)
        self.assertEqual(len(policy["comments"]), 10)
        self.assertIn("transition", subscription["authority_terms"])
        self.assertIn("bucket", policy["authority_terms"])
        self.assertIn("legacy_route", policy["prompt"])

    def test_structural_compression_pairs_twelve_cases_with_current_full_skill(self):
        runs = runner.suite_runs(
            "codex", reps=2, suite="review-feedback-structural-compression"
        )
        self.assertEqual(len(runs), 48)
        self.assertEqual(len({run["eval"] for run in runs}), 12)
        self.assertEqual({run["arm"] for run in runs}, {"baseline_skill", "candidate_skill"})
        self.assertEqual(
            {run["skill_arm"] for run in runs},
            {"git:" + runner.REVIEW_FEEDBACK_STRUCTURAL_BASELINE_REF, runner.SHIPPED},
        )

    def test_codex_command_uses_requested_model_and_high_effort(self):
        command = runner.codex_command("gpt-5.6-luna", "prompt", [])
        self.assertIn("gpt-5.6-luna", command)
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertEqual(command[-1], "prompt")

    def test_severity_uses_the_ledger_occurrence_not_the_preamble(self):
        text = (
            "I will inspect B1 and B2 first.\n"
            "| B1 + B2 | Verified | P2 | Fix at owner |\n"
        )
        self.assertTrue(grader.comments_have_severity(text, ("B1", "B2"), "P2"))


if __name__ == "__main__":
    unittest.main()
