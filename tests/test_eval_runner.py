import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))


def load_runner():
    spec = importlib.util.spec_from_file_location("shared_eval_runner", ROOT / "evals" / "runner.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load_runner()


class EvalRunnerSuiteTests(unittest.TestCase):
    def test_debug_and_tdd_are_explicit_suites(self):
        debug = runner.suite_runs("claude", reps=1, suite="debug")
        self.assertEqual(len(debug), 4)
        self.assertEqual({run["workspace"] for run in debug}, {"debug-workspace"})

        tdd = runner.suite_runs("pi", reps=1, suite="tdd")
        self.assertEqual(len(tdd), 4)
        self.assertEqual({run["workspace"] for run in tdd}, {"tdd-workspace"})

    def test_claude_tdd_keeps_the_frozen_baseline_arm(self):
        runs = runner.suite_runs("claude", reps=1, suite="tdd")
        self.assertEqual(len(runs), 6)
        self.assertEqual(
            {run["arm"] for run in runs},
            {"without_skill", "old_skill", "with_skill"},
        )

    def test_only_the_current_review_feedback_comparison_is_supported(self):
        runs = runner.suite_runs(
            "codex", reps=1, suite="review-feedback-structural-compression"
        )
        self.assertEqual(len(runs), 24)
        self.assertEqual(len({run["eval"] for run in runs}), 12)

        with self.assertRaisesRegex(ValueError, "unsupported suite"):
            runner.suite_runs("codex", reps=1, suite="all")


if __name__ == "__main__":
    unittest.main()
