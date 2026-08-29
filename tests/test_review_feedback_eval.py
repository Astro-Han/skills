import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
        self.assertEqual(len(runs), 2)
        self.assertEqual({run["fixture"] for run in runs}, {"seatmap"})
        self.assertEqual({run["eval"] for run in runs}, {"remove-mirrored-state"})

    def test_codex_command_uses_requested_model_and_high_effort(self):
        command = runner.codex_command("gpt-5.6-luna", "prompt", [])
        self.assertIn("gpt-5.6-luna", command)
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertEqual(command[-1], "prompt")


if __name__ == "__main__":
    unittest.main()
