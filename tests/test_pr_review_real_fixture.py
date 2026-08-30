import importlib.util
import json
import contextlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "evals/pr-review/real_fixture.py"
    spec = importlib.util.spec_from_file_location("real_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fixture = load_module()


def pr(number, *, state="MERGED", merged=True, files=1, additions=10, deletions=2, title="fix: x"):
    return {
        "number": number,
        "state": state,
        "mergedAt": "2026-08-01T00:00:00Z" if merged else None,
        "isDraft": False,
        "author": {"login": "human"},
        "title": title,
        "url": f"https://example.test/{number}",
        "changedFiles": files,
        "additions": additions,
        "deletions": deletions,
    }


class RealFixtureTests(unittest.TestCase):
    def test_capture_pool_respects_the_frozen_query_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "pool.json"
            with mock.patch.object(fixture, "run", return_value="[]") as call:
                fixture.capture_pool(
                    "o/r", "2026-05-30", "2026-08-29", output, limit=200
                )

        command = call.call_args.args[0]
        self.assertEqual(command[command.index("--limit") + 1], "200")

    def test_diverse_candidate_selection_is_deterministic_and_respects_repo_quotas(self):
        pools = [
            {
                "schema_version": 1,
                "repo": "a/one",
                "pull_requests": [
                    pr(1, title="fix: reachable bug", additions=30),
                    pr(2, title="feat: useful path", additions=40),
                    pr(3, title="chore(deps): bump library", additions=20),
                    {**pr(4, title="fix: drafted", additions=20), "isDraft": True},
                    pr(5, title="fix: replacement case", additions=35),
                ],
            },
            {
                "schema_version": 1,
                "repo": "b/two",
                "pull_requests": [
                    pr(10, title="fix: state transition", additions=50),
                    pr(11, title="refactor: one owner", additions=60),
                    pr(12, title="fix: enormous", additions=600),
                ],
            },
        ]
        policy = {
            "schema_version": 1,
            "seed": "diverse-fixed",
            "eligibility": {
                "minimum_churn": 20,
                "maximum_churn": 500,
                "maximum_changed_files": 20,
                "excluded_title_patterns": ["^chore\\(deps\\):"],
            },
            "repositories": [
                {
                    "repo": "a/one",
                    "candidate_count": 2,
                    "final_case_count": 1,
                    "exclude_numbers": [2],
                },
                {"repo": "b/two", "candidate_count": 2, "final_case_count": 1},
            ],
        }

        first = fixture.select_diverse_candidates(pools, policy)
        second = fixture.select_diverse_candidates(pools, policy)

        self.assertEqual(first, second)
        self.assertEqual(first["candidate_count"], 4)
        self.assertEqual(first["planned_final_case_count"], 2)
        selected = {(case["repo"], case["number"]) for case in first["cases"]}
        self.assertEqual(selected, {("a/one", 1), ("a/one", 5), ("b/two", 10), ("b/two", 11)})

    def test_select_diverse_cli_records_each_frozen_pool_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pools = []
            repositories = []
            for repo, number in (("a/one", 1), ("b/two", 2)):
                path = root / f"{repo.replace('/', '--')}.json"
                fixture.write_json(
                    path,
                    {
                        "schema_version": 1,
                        "repo": repo,
                        "pull_requests": [pr(number, additions=30)],
                    },
                )
                pools.append(path)
                repositories.append(
                    {"repo": repo, "candidate_count": 1, "final_case_count": 1}
                )
            policy = root / "policy.json"
            fixture.write_json(
                policy,
                {
                    "schema_version": 1,
                    "seed": "fixed",
                    "eligibility": {
                        "minimum_churn": 20,
                        "maximum_churn": 500,
                        "maximum_changed_files": 20,
                        "excluded_title_patterns": [],
                    },
                    "repositories": repositories,
                },
            )
            output = root / "selection.json"

            subprocess.run(
                [
                    "python",
                    str(ROOT / "evals/pr-review/real_fixture.py"),
                    "select-diverse",
                    *sum((["--pool", str(path)] for path in pools), []),
                    "--policy",
                    str(policy),
                    "--output",
                    str(output),
                ],
                check=True,
            )

            result = fixture.read_json(output)
            self.assertEqual(result["candidate_count"], 2)
            self.assertEqual(
                result["pool_digests"],
                {path.name: fixture.digest(path) for path in pools},
            )
            self.assertEqual(result["policy_digest"], fixture.digest(policy))

    def test_diverse_selection_verifier_accepts_exact_repo_quotas(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            policy = root / "policy.json"
            candidates = root / "candidates.json"
            fixture.write_json(
                policy,
                {
                    "repositories": [
                        {"repo": "a/one", "final_case_count": 1},
                        {"repo": "b/two", "final_case_count": 1},
                    ]
                },
            )
            fixture.write_json(
                candidates,
                {
                    "cases": [
                        {"repo": "a/one", "number": 1},
                        {"repo": "b/two", "number": 2},
                    ]
                },
            )
            selection = root / "selection.json"
            fixture.write_json(
                selection,
                {
                    "policy_digest": fixture.digest(policy),
                    "candidates_digest": fixture.digest(candidates),
                    "cases": ["a/one#1", "b/two#2"],
                },
            )

            self.assertEqual(
                fixture.verify_diverse_selection(candidates, policy, selection), 2
            )

    def test_capture_patch_routes_through_gh(self):
        with mock.patch.object(fixture, "run", return_value="patch") as call:
            self.assertEqual(fixture.capture_patch("o/r", 42), "patch")
        call.assert_called_once_with(["gh", "pr", "diff", "42", "--repo", "o/r", "--patch"])

    def test_comparison_base_comes_from_github_compare(self):
        response = {"merge_base_commit": {"sha": "c" * 40}}
        with mock.patch.object(fixture, "github_json", return_value=response) as call:
            actual = fixture.comparison_base("o/r", "a" * 40, "b" * 40)
        self.assertEqual(actual, "c" * 40)
        call.assert_called_once_with(
            ["api", f"repos/o/r/compare/{'a' * 40}...{'b' * 40}"]
        )

    def test_issue_references_are_hydrated_from_their_repository(self):
        reference = {
            "number": 7,
            "repository": {"name": "other", "owner": {"login": "org"}},
        }
        response = {"number": 7, "url": "https://example.test/7", "title": "Issue", "body": "Body"}
        with mock.patch.object(fixture, "github_json", return_value=response) as call:
            issues = fixture.hydrate_issues([reference], "fallback/repo")
        self.assertEqual(issues[0]["title"], "Issue")
        call.assert_called_once_with(
            ["issue", "view", "7", "--repo", "org/other", "--json", "number,url,title,body"]
        )

    def test_selection_is_deterministic_disjoint_and_excludes_known_cases(self):
        pulls = [
            pr(1, state="CLOSED", merged=False, files=8, additions=400),
            pr(2, state="CLOSED", merged=False, files=9, additions=500),
            pr(3, title="test: focused", files=2),
            pr(4, title="docs: focused", files=2),
            pr(5, files=1),
            pr(6, files=2),
            pr(7, files=7, additions=400),
            pr(8, files=8, additions=500),
            pr(9, files=9, additions=600),
            pr(10, files=30, additions=3000),
            pr(11, files=31, additions=3100),
            pr(12, files=32, additions=3200),
            pr(99, files=33, additions=3300),
        ]
        pool = {"schema_version": 1, "repo": "o/r", "pull_requests": pulls}
        policy = {
            "schema_version": 1,
            "repo": "o/r",
            "seed": "fixed",
            "exclude_numbers": [99],
            "repeat_numbers": [1, 3, 5, 7],
            "strata": [
                {"name": "closed_unmerged", "count": 2},
                {"name": "test_docs_ci", "count": 2},
                {"name": "small", "count": 2},
                {"name": "medium", "count": 3},
                {"name": "large", "count": 3},
            ],
        }
        first = fixture.select_cases(pool, policy)
        second = fixture.select_cases(pool, policy)
        self.assertEqual(first, second)
        numbers = [case["number"] for case in first["cases"]]
        self.assertEqual(len(numbers), 12)
        self.assertEqual(len(set(numbers)), 12)
        self.assertNotIn(99, numbers)
        self.assertEqual(first["repeat_numbers"], [1, 3, 5, 7])
        selected_by_stratum = {case["number"]: case["stratum"] for case in first["cases"]}
        self.assertEqual(selected_by_stratum[3], "test_docs_ci")
        self.assertEqual(selected_by_stratum[4], "test_docs_ci")

    def test_repeat_cases_must_come_from_selection(self):
        pool = {
            "schema_version": 1,
            "repo": "o/r",
            "pull_requests": [pr(1), pr(2)],
        }
        policy = {
            "schema_version": 1,
            "repo": "o/r",
            "seed": "fixed",
            "repeat_numbers": [99],
            "strata": [{"name": "small", "count": 1}],
        }
        with self.assertRaisesRegex(ValueError, "must be selected"):
            fixture.select_cases(pool, policy)

    def test_manifest_rejects_outcome_leakage(self):
        manifest = {
            "schema_version": 1,
            "case_id": "case",
            "repo": "o/r",
            "pr_number": 1,
            "url": "https://example.test/1",
            "title": "x",
            "base_sha": "a" * 40,
            "comparison_base_sha": "a" * 40,
            "head_sha": "b" * 40,
            "additions": 1,
            "deletions": 0,
            "changed_files": 1,
            "files": [{"path": "x", "additions": 1, "deletions": 0}],
            "checks": [],
            "issues": [],
            "patch_sha256": "c" * 64,
            "review_decision": "approved",
        }
        with self.assertRaisesRegex(ValueError, "leaks outcome"):
            fixture.validate_manifest(manifest)

    def test_materialize_applies_patch_to_real_base_without_copying_gold(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            (repo / "owned.py").write_text("value = 1\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(
                ["git", "-c", "user.name=eval", "-c", "user.email=e@e.co", "commit", "-qm", "base"],
                cwd=repo,
                check=True,
            )
            base = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
            ).stdout.strip()
            (repo / "owned.py").write_text("value = 2\n")
            patch = subprocess.run(
                ["git", "diff"], cwd=repo, check=True, capture_output=True, text=True
            ).stdout
            subprocess.run(["git", "checkout", "--", "owned.py"], cwd=repo, check=True)
            (repo / "future.py").write_text("future = True\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(
                ["git", "-c", "user.name=eval", "-c", "user.email=e@e.co", "commit", "-qm", "future"],
                cwd=repo,
                check=True,
            )
            future = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
            ).stdout.strip()
            case = root / "case"
            case.mkdir()
            (case / "PATCH.diff").write_text(patch)
            manifest = {
                "schema_version": 1,
                "case_id": "real-1",
                "repo": "o/r",
                "pr_number": 1,
                "url": "https://example.test/1",
                "title": "fix",
                "body": "",
                "author": "author",
                "base_sha": base,
                "comparison_base_sha": base,
                "head_sha": "b" * 40,
                "additions": 1,
                "deletions": 1,
                "changed_files": 1,
                "files": [{"path": "owned.py", "additions": 1, "deletions": 1}],
                "checks": [],
                "issues": [],
                "patch_sha256": fixture.digest(case / "PATCH.diff"),
            }
            fixture.write_json(case / "manifest.json", manifest)
            (case / "PR_SNAPSHOT.md").write_text(fixture.markdown_snapshot(manifest))
            (case / "gold.json").write_text(json.dumps({"answer": "must remain private"}))
            selection_path = root / "selection.json"
            fixture.write_json(
                selection_path,
                {
                    "cases": [
                        {
                            "number": 1,
                            "title": "fix",
                            "url": "https://example.test/1",
                            "changed_files": 1,
                            "additions": 1,
                            "deletions": 1,
                        }
                    ]
                },
            )
            self.assertEqual(fixture.verify_all(root, selection_path), 1)
            output = root / "work"
            with contextlib.chdir(root):
                fixture.materialize(Path("case"), Path("repo"), Path("work"))
            self.assertEqual((output / "owned.py").read_text(), "value = 2\n")
            self.assertFalse((output / "gold.json").exists())
            self.assertFalse((output / ".pr-review-eval/gold.json").exists())
            self.assertFalse((output / "future.py").exists())
            self.assertNotEqual(
                subprocess.run(
                    ["git", "cat-file", "-e", future], cwd=output, capture_output=True
                ).returncode,
                0,
            )

    def test_mail_patch_series_is_applied_in_commit_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            (repo / "value.txt").write_text("one\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            commit = ["git", "-c", "user.name=eval", "-c", "user.email=e@e.co", "commit", "-qm"]
            subprocess.run([*commit, "base"], cwd=repo, check=True)
            base = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
            ).stdout.strip()
            (repo / "value.txt").write_text("two\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run([*commit, "first"], cwd=repo, check=True)
            (repo / "value.txt").write_text("three\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run([*commit, "second"], cwd=repo, check=True)
            patch = subprocess.run(
                ["git", "format-patch", "--stdout", f"{base}..HEAD"],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            output = root / "work"
            subprocess.run(["git", "clone", "-q", "--shared", str(repo), str(output)], check=True)
            subprocess.run(["git", "checkout", "-q", "--detach", base], cwd=output, check=True)
            patch_path = root / "series.patch"
            patch_path.write_text(patch)
            fixture.apply_captured_patch(output, patch_path, base)
            self.assertEqual((output / "value.txt").read_text(), "three\n")
            self.assertEqual(
                subprocess.run(
                    ["git", "rev-parse", "HEAD"], cwd=output, check=True, capture_output=True, text=True
                ).stdout.strip(),
                base,
            )
            self.assertEqual(
                subprocess.run(
                    ["git", "diff", "--cached", "--numstat"],
                    cwd=output,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                "1\t1\tvalue.txt",
            )


if __name__ == "__main__":
    unittest.main()
