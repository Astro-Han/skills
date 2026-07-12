import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CLI = ROOT / "skills" / "craft-skill" / "scripts" / "eval.py"


class EvalCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["uv", "run", "python", str(CLI), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validate_rejects_an_eval_without_a_decision(self) -> None:
        manifest = {
            "comparison": {"baseline": "baseline", "candidate": "candidate"},
            "metric": {"name": "task score", "direction": "higher"},
            "runs": [
                {"case_id": "case-1", "variant": "baseline", "value": 0},
                {"case_id": "case-1", "variant": "candidate", "value": 1},
            ],
        }

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eval.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_cli("summarize", str(path))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("decision", result.stderr)

    def test_validate_rejects_unpaired_variants(self) -> None:
        manifest = {
            "decision": "Adopt the candidate only if it improves task score.",
            "comparison": {"baseline": "baseline", "candidate": "candidate"},
            "metric": {"name": "task score", "direction": "higher"},
            "runs": [
                {"case_id": "case-1", "variant": "baseline", "value": 0},
                {"case_id": "case-1", "variant": "candidate", "value": 1},
                {"case_id": "case-2", "variant": "candidate", "value": 1},
            ],
        }

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eval.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_cli("summarize", str(path))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("same variants", result.stderr)

    def test_blind_creates_an_anonymous_review_pack_and_separate_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline.txt"
            candidate = root / "candidate.txt"
            review_dir = root / "review"
            key_path = root / "private" / "answer-key.json"
            baseline.write_text("old output", encoding="utf-8")
            candidate.write_text("new output", encoding="utf-8")

            result = self.run_cli(
                "blind",
                str(baseline),
                str(candidate),
                "--review-dir",
                str(review_dir),
                "--key",
                str(key_path),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path.name for path in review_dir.iterdir()}, {"A.txt", "B.txt"})
            self.assertFalse(key_path.is_relative_to(review_dir))
            key = json.loads(key_path.read_text(encoding="utf-8"))
            self.assertEqual(set(key), {"A", "B"})
            self.assertEqual({entry["input"] for entry in key.values()}, {"left", "right"})
            self.assertEqual(
                {entry["path"] for entry in key.values()},
                {str(baseline.resolve()), str(candidate.resolve())},
            )
            reviewed = {
                (review_dir / "A.txt").read_text(encoding="utf-8"),
                (review_dir / "B.txt").read_text(encoding="utf-8"),
            }
            self.assertEqual(reviewed, {"old output", "new output"})

    def test_blind_key_distinguishes_inputs_with_the_same_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline" / "output.md"
            candidate = root / "candidate" / "output.md"
            baseline.parent.mkdir()
            candidate.parent.mkdir()
            baseline.write_text("old", encoding="utf-8")
            candidate.write_text("new", encoding="utf-8")
            key_path = root / "private" / "answer-key.json"

            result = self.run_cli(
                "blind",
                str(baseline),
                str(candidate),
                "--review-dir",
                str(root / "review"),
                "--key",
                str(key_path),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            key = json.loads(key_path.read_text(encoding="utf-8"))
            self.assertEqual({entry["input"] for entry in key.values()}, {"left", "right"})
            self.assertEqual(
                {entry["path"] for entry in key.values()},
                {str(baseline.resolve()), str(candidate.resolve())},
            )

    def test_summarize_reports_only_predeclared_paired_statistics(self) -> None:
        manifest = {
            "decision": "Adopt the candidate only if it improves task score.",
            "comparison": {"baseline": "baseline", "candidate": "candidate"},
            "metric": {"name": "task score", "direction": "higher"},
            "runs": [
                {"case_id": "case-1", "variant": "baseline", "value": 1},
                {"case_id": "case-1", "variant": "candidate", "value": 2},
                {"case_id": "case-2", "variant": "baseline", "value": 2},
                {"case_id": "case-2", "variant": "candidate", "value": 4},
                {"case_id": "case-3", "variant": "baseline", "value": 3},
                {"case_id": "case-3", "variant": "candidate", "value": 6},
            ],
        }

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eval.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_cli("summarize", str(path))

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["decision"], manifest["decision"])
        self.assertEqual(summary["metric"], manifest["metric"])
        self.assertEqual(summary["baseline"], {"mean": 2, "sample_stdev": 1})
        self.assertEqual(summary["candidate"], {"mean": 4, "sample_stdev": 2})
        self.assertEqual(summary["paired_improvement"], {"mean": 2, "sample_stdev": 1})
        self.assertNotIn("winner", summary)


if __name__ == "__main__":
    unittest.main()
