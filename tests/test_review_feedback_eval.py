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

    def test_review_feedback_suite_pairs_old_and_shipped_skills(self):
        runs = runner.suite_runs("codex", reps=2, suite="review-feedback")
        self.assertEqual(len(runs), 4)
        self.assertEqual({run["arm"] for run in runs}, {"old_skill", "with_skill"})
        self.assertEqual({run["fixture"] for run in runs}, {"quoteview"})

    def test_holdout_suite_uses_a_distinct_fixture(self):
        runs = runner.suite_runs("codex", reps=1, suite="review-feedback-holdout")
        self.assertEqual(len(runs), 8)
        self.assertEqual(
            {run["fixture"] for run in runs},
            {"seatmap", "handlekit", "profilefmt", "jobflow"},
        )

    def test_matrix_runs_nine_cases_for_both_arms(self):
        runs = runner.suite_runs("codex", reps=5, suite="review-feedback-matrix")
        self.assertEqual(len(runs), 90)
        self.assertEqual({run["arm"] for run in runs}, {"old_skill", "with_skill"})
        self.assertEqual(len({run["eval"] for run in runs}), 9)

    def test_compression_suite_pairs_frozen_full_and_shipped_skills(self):
        runs = runner.suite_runs("codex", reps=3, suite="review-feedback-compression")
        self.assertEqual(len(runs), 54)
        self.assertEqual({run["arm"] for run in runs}, {"full_skill", "compressed_skill"})
        self.assertEqual(
            {run["skill_arm"] for run in runs},
            {"git:" + runner.REVIEW_FEEDBACK_FULL_REF, runner.SHIPPED},
        )

    def test_compression_holdout_uses_two_unseen_fixtures(self):
        runs = runner.suite_runs("codex", reps=5, suite="review-feedback-compression-holdout")
        self.assertEqual(len(runs), 20)
        self.assertEqual({run["fixture"] for run in runs}, {"transferlog", "credrotate"})
        self.assertEqual({run["arm"] for run in runs}, {"full_skill", "compressed_skill"})

    def test_second_holdout_is_new_and_pairs_both_arms(self):
        runs = runner.suite_runs("codex", reps=6, suite="review-feedback-second-holdout")
        self.assertEqual(len(runs), 36)
        self.assertEqual(
            {run["fixture"] for run in runs},
            {"batchplan", "wireview", "launchmode"},
        )
        self.assertEqual({run["arm"] for run in runs}, {"old_skill", "with_skill"})

    def test_final_holdout_runs_eight_pairs_on_a_new_fixture(self):
        runs = runner.suite_runs("codex", reps=8, suite="review-feedback-final-holdout")
        self.assertEqual(len(runs), 16)
        self.assertEqual({run["fixture"] for run in runs}, {"cartsummary"})

    def test_scope_rebase_suite_pairs_frozen_baseline_and_candidate(self):
        runs = runner.suite_runs("codex", reps=10, suite="review-feedback-scope-rebase")
        self.assertEqual(len(runs), 20)
        self.assertEqual({run["fixture"] for run in runs}, {"mediathread"})
        self.assertEqual({run["arm"] for run in runs}, {"baseline_skill", "candidate_skill"})
        self.assertEqual(
            {run["skill_arm"] for run in runs},
            {"git:" + runner.REVIEW_FEEDBACK_SCOPE_BASELINE_REF, runner.SHIPPED},
        )

    def test_scope_rebase_case_starts_from_an_existing_pr_diff(self):
        case = runner.REVIEW_FEEDBACK_CASES["rebase-cumulative-diff"]
        self.assertEqual(case["fixture"], "mediathread")
        self.assertEqual(case["seed_patch"], "mediathread-pr.patch")
        self.assertTrue((ROOT / "evals" / "seeds" / case["seed_patch"]).is_file())

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
