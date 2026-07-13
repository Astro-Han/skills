import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CLI = ROOT / "skills" / "goal-writer" / "scripts" / "lint_goal.py"


class GoalLintCliTests(unittest.TestCase):
    def run_stdin(self, goal: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["uv", "run", "python", str(CLI), "-"],
            cwd=ROOT,
            input=goal,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_a_goal_without_transport_syntax(self) -> None:
        result = self.run_stdin(
            "修复登录超时后的错误跳转；回归测试证明超时会返回登录页，且正常登录仍通过。"
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_a_plain_text_goal(self) -> None:
        result = self.run_stdin(
            "Goal: Remove the obsolete cache path; the focused regression test and full suite must pass."
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_warns_when_a_goal_exceeds_2000_characters(self) -> None:
        result = self.run_stdin("x" * 2001)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("warning", result.stderr)
        self.assertIn("2001", result.stderr)

    def test_rejects_a_goal_over_4000_characters(self) -> None:
        result = self.run_stdin("x" * 4001)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("4001", result.stderr)
        self.assertIn("hard limit", result.stderr)

    def test_rejects_an_empty_goal(self) -> None:
        result = self.run_stdin("  \n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Goal contract is empty", result.stderr)

    def test_allows_a_concrete_bracketed_reference(self) -> None:
        result = self.run_stdin("修复 [issue #123]；对应回归测试通过。")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_an_explicit_placeholder(self) -> None:
        result = self.run_stdin("修复 TODO；对应回归测试通过。")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unresolved placeholder", result.stderr)

    def test_does_not_guess_whether_goal_language_is_vague(self) -> None:
        result = self.run_stdin(
            "Fix everything reported in issues #1–#3; all three regression tests and the full suite pass."
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_file_mode_accepts_a_multiline_contract(self) -> None:
        goal = """Repair the login timeout redirect without changing normal login behavior.
Completion requires the focused regression test and full authentication suite to pass.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "goal.md"
            path.write_text(goal, encoding="utf-8")
            result = subprocess.run(
                ["uv", "run", "python", str(CLI), str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
