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

    def test_accepts_a_minimal_goal_without_section_headings(self) -> None:
        result = self.run_stdin(
            "/goal 修复登录超时后的错误跳转；回归测试证明超时会返回登录页，且正常登录仍通过。"
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_a_plain_text_goal(self) -> None:
        result = self.run_stdin(
            "Goal: Remove the obsolete cache path; the focused regression test and full suite must pass."
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_an_empty_goal(self) -> None:
        result = self.run_stdin("/goal")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Goal outcome is empty", result.stderr)

    def test_rejects_an_unresolved_placeholder(self) -> None:
        result = self.run_stdin("/goal Fix [one issue] and prove the regression test passes.")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unresolved placeholder", result.stderr)

    def test_rejects_an_explicitly_vague_instruction(self) -> None:
        result = self.run_stdin("/goal Fix everything until the full test suite passes.")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Dangerous vague instruction", result.stderr)

    def test_file_mode_accepts_a_complete_legacy_contract(self) -> None:
        goal = """/goal Repair the login timeout redirect without changing normal login behavior.
Context: Read the failing route test and current authentication handler.
Scope: Correct the redirect at the lowest responsible layer.
Non-goals: Do not redesign unrelated authentication screens.
Constraints: Preserve the public session contract and existing route ownership.
Verification: Run the focused regression test and the full authentication suite.
Iteration: Use each failing assertion to revisit the current root-cause hypothesis.
Stop when: The timeout regression and full authentication suite pass.
Pause if: Production credentials or a destructive data migration becomes necessary.
Final report: Summarize the changed files and test results.
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
