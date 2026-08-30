#!/usr/bin/env python3
"""Capture, select, verify, and materialize frozen real-PR evaluation cases."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


SCHEMA_VERSION = 1
FORBIDDEN_EXECUTOR_KEYS = {
    "gold",
    "expected_findings",
    "mergeability",
    "merged_at",
    "review_decision",
    "reviews",
    "state",
}


def read_json(path: Path):
    return json.loads(path.read_text())


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, *, cwd=None, text=True):
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=text,
        ).stdout
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else error.stderr
        raise RuntimeError(
            "command failed: {}\n{}".format(" ".join(command), (stderr or "").strip())
        ) from error


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def capture_pool(repo: str, created_from: str, created_to: str, output: Path, limit: int = 500):
    fields = (
        "number,title,state,isDraft,createdAt,closedAt,mergedAt,additions,deletions,"
        "changedFiles,url,author,headRefOid,baseRefOid"
    )
    raw = run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--limit",
            str(limit),
            "--search",
            f"created:{created_from}..{created_to}",
            "--json",
            fields,
        ]
    )
    pulls = json.loads(raw)
    write_json(
        output,
        {
            "schema_version": SCHEMA_VERSION,
            "repo": repo,
            "captured_at": utc_now(),
            "created_from": created_from,
            "created_to": created_to,
            "query_limit": limit,
            "pull_requests": pulls,
        },
    )


def stable_rank(seed: str, number: int):
    return hashlib.sha256(f"{seed}:{number}".encode()).hexdigest()


def is_bot(pr):
    if (pr.get("author") or {}).get("is_bot"):
        return True
    login = ((pr.get("author") or {}).get("login") or "").lower()
    return any(name in login for name in ("dependabot", "renovate", "github-actions"))


def select_diverse_candidates(pools, policy):
    if policy["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported schema version")
    pools_by_repo = {pool["repo"]: pool for pool in pools}
    rules = policy["eligibility"]
    excluded_titles = [re.compile(pattern, re.IGNORECASE) for pattern in rules["excluded_title_patterns"]]
    selected = []
    planned_final = 0
    for repository in policy["repositories"]:
        repo = repository["repo"]
        if repo not in pools_by_repo:
            raise ValueError(f"missing pool for {repo}")
        pool = pools_by_repo[repo]
        if pool["schema_version"] != SCHEMA_VERSION:
            raise ValueError("unsupported schema version")
        excluded_numbers = set(repository.get("exclude_numbers", []))
        eligible = []
        for pull in pool["pull_requests"]:
            churn = int(pull["additions"]) + int(pull["deletions"])
            if pull["state"] != "MERGED" or pull.get("isDraft") or is_bot(pull):
                continue
            if pull["number"] in excluded_numbers:
                continue
            if not rules["minimum_churn"] <= churn <= rules["maximum_churn"]:
                continue
            if int(pull["changedFiles"]) > rules["maximum_changed_files"]:
                continue
            if any(pattern.search(pull["title"]) for pattern in excluded_titles):
                continue
            eligible.append(pull)
        eligible.sort(
            key=lambda pull: hashlib.sha256(
                f"{policy['seed']}:{repo}:{pull['number']}".encode()
            ).hexdigest()
        )
        count = int(repository["candidate_count"])
        if len(eligible) < count:
            raise ValueError(f"repository {repo} has {len(eligible)} candidates, needs {count}")
        for pull in eligible[:count]:
            selected.append(
                {
                    "repo": repo,
                    "number": pull["number"],
                    "title": pull["title"],
                    "url": pull["url"],
                    "changed_files": pull["changedFiles"],
                    "additions": pull["additions"],
                    "deletions": pull["deletions"],
                }
            )
        planned_final += int(repository["final_case_count"])
    return {
        "schema_version": SCHEMA_VERSION,
        "seed": policy["seed"],
        "candidate_count": len(selected),
        "planned_final_case_count": planned_final,
        "cases": selected,
    }


def matches_stratum(pr, name: str):
    churn = int(pr["additions"]) + int(pr["deletions"])
    files = int(pr["changedFiles"])
    title = pr["title"].lower()
    closed_unmerged = pr["state"] == "CLOSED" and not pr.get("mergedAt")
    test_docs_ci = bool(re.match(r"^(test|docs|ci)(?:\(|:)", title))
    if name == "closed_unmerged":
        return closed_unmerged
    if name == "test_docs_ci":
        return not closed_unmerged and test_docs_ci
    if closed_unmerged or test_docs_ci:
        return False
    if name == "small":
        return files <= 5 and churn <= 300
    if name == "medium":
        return 6 <= files <= 20 and churn <= 2000
    if name == "large":
        return files > 20 or churn > 2000
    raise ValueError(f"unknown stratum: {name}")


def select_cases(pool, policy):
    if pool["schema_version"] != SCHEMA_VERSION or policy["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported schema version")
    if pool["repo"] != policy["repo"]:
        raise ValueError("pool and policy repos differ")
    excluded = set(policy.get("exclude_numbers", []))
    eligible = [
        pr
        for pr in pool["pull_requests"]
        if pr["number"] not in excluded and not pr.get("isDraft") and not is_bot(pr)
    ]
    selected = []
    used = set()
    for stratum in policy["strata"]:
        candidates = [
            pr
            for pr in eligible
            if pr["number"] not in used and matches_stratum(pr, stratum["name"])
        ]
        candidates.sort(key=lambda pr: stable_rank(policy["seed"], pr["number"]))
        count = int(stratum["count"])
        if len(candidates) < count:
            raise ValueError(f"stratum {stratum['name']} has {len(candidates)} candidates, needs {count}")
        for pr in candidates[:count]:
            used.add(pr["number"])
            selected.append(
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                    "changed_files": pr["changedFiles"],
                    "additions": pr["additions"],
                    "deletions": pr["deletions"],
                    "stratum": stratum["name"],
                }
            )
    selected_numbers = {case["number"] for case in selected}
    repeat_numbers = policy.get("repeat_numbers", [])
    if len(repeat_numbers) != len(set(repeat_numbers)):
        raise ValueError("repeat_numbers contains duplicates")
    if not set(repeat_numbers).issubset(selected_numbers):
        raise ValueError("repeat_numbers must be selected cases")
    return {
        "schema_version": SCHEMA_VERSION,
        "repo": policy["repo"],
        "seed": policy["seed"],
        "repeat_numbers": repeat_numbers,
        "pool_digest": hashlib.sha256(
            json.dumps(pool, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "cases": selected,
    }


def capture_selected(pool_path: Path, policy_path: Path, output: Path):
    selection = select_cases(read_json(pool_path), read_json(policy_path))
    write_json(output, selection)


def capture_diverse_selection(pool_paths, policy_path: Path, output: Path):
    selection = select_diverse_candidates(
        [read_json(path) for path in pool_paths], read_json(policy_path)
    )
    selection["pool_digests"] = {path.name: digest(path) for path in pool_paths}
    selection["policy_digest"] = digest(policy_path)
    write_json(output, selection)


def verify_diverse_selection(candidates_path: Path, policy_path: Path, selection_path: Path):
    selection = read_json(selection_path)
    if selection["policy_digest"] != digest(policy_path):
        raise ValueError("diverse selection policy digest mismatch")
    if selection["candidates_digest"] != digest(candidates_path):
        raise ValueError("diverse candidate digest mismatch")
    selected_ids = selection["cases"]
    if len(selected_ids) != len(set(selected_ids)):
        raise ValueError("diverse selection contains duplicate cases")
    candidates = read_json(candidates_path)
    candidate_ids = {f"{case['repo']}#{case['number']}" for case in candidates["cases"]}
    unknown = set(selected_ids) - candidate_ids
    if unknown:
        raise ValueError(f"diverse selection contains unknown cases: {sorted(unknown)}")
    actual_counts = {}
    for case_id in selected_ids:
        repo, _ = case_id.rsplit("#", 1)
        actual_counts[repo] = actual_counts.get(repo, 0) + 1
    policy = read_json(policy_path)
    expected_counts = {
        item["repo"]: int(item["final_case_count"]) for item in policy["repositories"]
    }
    if actual_counts != expected_counts:
        raise ValueError(
            f"diverse selection repo quotas differ: expected {expected_counts}, got {actual_counts}"
        )
    return len(selected_ids)


def github_json(args):
    return json.loads(run(["gh", *args]))


def capture_patch(repo: str, number: int):
    return run(["gh", "pr", "diff", str(number), "--repo", repo, "--patch"])


def comparison_base(repo: str, base_sha: str, head_sha: str):
    comparison = github_json(
        ["api", f"repos/{repo}/compare/{base_sha}...{head_sha}"]
    )
    return comparison["merge_base_commit"]["sha"]


def hydrate_issues(references, default_repo: str):
    issues = []
    for reference in references or []:
        repository = reference.get("repository") or {}
        owner = (repository.get("owner") or {}).get("login")
        name = repository.get("name")
        issue_repo = f"{owner}/{name}" if owner and name else default_repo
        issue = github_json(
            ["issue", "view", str(reference["number"]), "--repo", issue_repo, "--json", "number,url,title,body"]
        )
        issues.append(
            {
                "number": issue["number"],
                "url": issue["url"],
                "title": issue["title"],
                "body": issue.get("body") or "",
            }
        )
    return issues


def markdown_snapshot(manifest):
    def normalized(value):
        return (value or "").replace("\r\n", "\n").replace("\r", "\n")

    lines = [
        "# Frozen pull request snapshot",
        "",
        f"- PR: {manifest['url']} — `{manifest['title']}`",
        f"- Author: {manifest['author']}",
        f"- Target base head: `{manifest['base_sha']}`",
        f"- Comparison base: `{manifest['comparison_base_sha']}`",
        f"- Exact source head: `{manifest['head_sha']}`",
        (
            f"- Diff: {manifest['additions']} additions, {manifest['deletions']} deletions, "
            f"{manifest['changed_files']} files"
        ),
        "- Live mergeability and review state: intentionally unavailable in this historical fixture",
        "",
        "## Pull request body",
        "",
        normalized(manifest["body"]) or "(empty)",
        "",
        "## Linked issues",
        "",
    ]
    if manifest["issues"]:
        for issue in manifest["issues"]:
            lines.extend(
                [
                    f"### {issue['url']} — {issue['title']}",
                    "",
                    normalized(issue["body"]) or "(empty)",
                    "",
                ]
            )
    else:
        lines.extend(["No closing Issue was linked in the frozen PR metadata.", ""])
    lines.extend(["## Exact-head checks", ""])
    if manifest["checks"]:
        for check in manifest["checks"]:
            conclusion = check.get("conclusion") or check.get("state") or "UNKNOWN"
            lines.append(f"- {check.get('name', 'unnamed')}: {conclusion}")
    else:
        lines.append("No exact-head checks were present in the captured metadata.")
    lines.extend(["", "## Changed files", ""])
    for changed in manifest["files"]:
        lines.append(
            f"- `{changed['path']}`: +{changed.get('additions', 0)}/-{changed.get('deletions', 0)}"
        )
    return "\n".join(lines) + "\n"


def capture_case(repo: str, number: int, case_id: str, output_root: Path):
    fields = (
        "number,url,title,body,author,baseRefOid,headRefOid,additions,deletions,"
        "changedFiles,files,statusCheckRollup,closingIssuesReferences"
    )
    pr = github_json(["pr", "view", str(number), "--repo", repo, "--json", fields])
    case_dir = output_root / case_id
    if case_dir.exists():
        raise FileExistsError(case_dir)
    patch = capture_patch(repo, number)
    issues = hydrate_issues(pr.get("closingIssuesReferences"), repo)
    checks = []
    for check in pr.get("statusCheckRollup") or []:
        checks.append(
            {
                key: check.get(key)
                for key in ("name", "conclusion", "state", "status", "workflowName")
                if check.get(key) is not None
            }
        )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "case_id": case_id,
        "repo": repo,
        "pr_number": number,
        "url": pr["url"],
        "title": pr["title"],
        "body": pr.get("body") or "",
        "author": (pr.get("author") or {}).get("login") or "unknown",
        "base_sha": pr["baseRefOid"],
        "comparison_base_sha": comparison_base(repo, pr["baseRefOid"], pr["headRefOid"]),
        "head_sha": pr["headRefOid"],
        "additions": pr["additions"],
        "deletions": pr["deletions"],
        "changed_files": pr["changedFiles"],
        "files": pr["files"],
        "checks": checks,
        "issues": issues,
        "captured_at": utc_now(),
    }
    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{case_id}.", dir=output_root) as temp:
        temporary_case = Path(temp)
        patch_path = temporary_case / "PATCH.diff"
        patch_path.write_text(patch)
        manifest["patch_sha256"] = digest(patch_path)
        write_json(temporary_case / "manifest.json", manifest)
        (temporary_case / "PR_SNAPSHOT.md").write_text(markdown_snapshot(manifest))
        verify_case(temporary_case)
        temporary_case.rename(case_dir)


def validate_manifest(manifest):
    required = {
        "schema_version",
        "case_id",
        "repo",
        "pr_number",
        "url",
        "title",
        "base_sha",
        "comparison_base_sha",
        "head_sha",
        "additions",
        "deletions",
        "changed_files",
        "files",
        "checks",
        "issues",
        "patch_sha256",
    }
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"missing manifest keys: {sorted(missing)}")
    leaked = FORBIDDEN_EXECUTOR_KEYS.intersection(key.lower() for key in manifest)
    if leaked:
        raise ValueError(f"executor manifest leaks outcome keys: {sorted(leaked)}")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported manifest schema")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["base_sha"]):
        raise ValueError("base_sha must be a full SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["comparison_base_sha"]):
        raise ValueError("comparison_base_sha must be a full SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["head_sha"]):
        raise ValueError("head_sha must be a full SHA")
    if len(manifest["files"]) != manifest["changed_files"]:
        raise ValueError("changed_files does not match files list")


def verify_case(case_dir: Path):
    manifest = read_json(case_dir / "manifest.json")
    validate_manifest(manifest)
    patch_path = case_dir / "PATCH.diff"
    if digest(patch_path) != manifest["patch_sha256"]:
        raise ValueError("patch digest mismatch")
    snapshot = (case_dir / "PR_SNAPSHOT.md").read_text()
    if manifest["head_sha"] not in snapshot or manifest["url"] not in snapshot:
        raise ValueError("snapshot omits exact head or PR URL")


def verify_all(cases_root: Path, selection_path: Path | None = None):
    case_dirs = sorted(path.parent for path in cases_root.glob("*/manifest.json"))
    if not case_dirs:
        raise ValueError("no real PR cases found")
    for case_dir in case_dirs:
        verify_case(case_dir)
    if selection_path:
        selection = read_json(selection_path)
        selected = {case["number"]: case for case in selection["cases"]}
        captured = {
            read_json(case_dir / "manifest.json")["pr_number"]: read_json(
                case_dir / "manifest.json"
            )
            for case_dir in case_dirs
        }
        if set(selected) != set(captured):
            raise ValueError("captured cases do not match the frozen selection")
        for number, expected in selected.items():
            actual = captured[number]
            for selected_key, captured_key in (
                ("title", "title"),
                ("url", "url"),
                ("changed_files", "changed_files"),
                ("additions", "additions"),
                ("deletions", "deletions"),
            ):
                if expected[selected_key] != actual[captured_key]:
                    raise ValueError(
                        f"captured case {number} differs from selection field {selected_key}"
                    )
    return len(case_dirs)


def apply_captured_patch(work: Path, patch_path: Path, base_sha: str):
    first_line = patch_path.read_text().splitlines()[0] if patch_path.stat().st_size else ""
    if re.fullmatch(r"From [0-9a-f]{40} Mon Sep 17 00:00:00 2001", first_line):
        run(
            [
                "git",
                "-c",
                "user.name=eval",
                "-c",
                "user.email=e@e.co",
                "am",
                "--committer-date-is-author-date",
                str(patch_path),
            ],
            cwd=work,
        )
        run(["git", "reset", "--soft", base_sha], cwd=work)
    else:
        run(["git", "apply", "--index", "--whitespace=nowarn", str(patch_path)], cwd=work)


def isolate_comparison_tree(work: Path, comparison_base_sha: str):
    """Replace the borrowed object database with one commit containing only the base tree."""
    shutil.rmtree(work / ".git")
    run(["git", "init", "-q"], cwd=work)
    run(["git", "add", "-A"], cwd=work)
    run(
        [
            "git",
            "-c",
            "user.name=eval",
            "-c",
            "user.email=e@e.co",
            "commit",
            "-qm",
            f"frozen comparison base {comparison_base_sha}",
        ],
        cwd=work,
    )
    return run(["git", "rev-parse", "HEAD"], cwd=work).strip()


def materialize(case_dir: Path, repo_cache: Path, output: Path):
    case_dir = case_dir.resolve()
    repo_cache = repo_cache.resolve()
    output = output.resolve()
    verify_case(case_dir)
    manifest = read_json(case_dir / "manifest.json")
    if output.exists():
        raise FileExistsError(output)
    run(["git", "clone", "-q", "--shared", "--no-checkout", str(repo_cache), str(output)])
    try:
        comparison = manifest["comparison_base_sha"]
        run(["git", "cat-file", "-e", comparison + "^{commit}"], cwd=output)
        run(["git", "checkout", "-q", "--detach", comparison], cwd=output)
        isolated_base = isolate_comparison_tree(output, comparison)
        apply_captured_patch(output, case_dir / "PATCH.diff", isolated_base)
        context = output / ".pr-review-eval"
        context.mkdir()
        shutil.copy2(case_dir / "PR_SNAPSHOT.md", context / "PR_SNAPSHOT.md")
        write_json(
            context / "CASE.json",
            {
                "case_id": manifest["case_id"],
                "source_head": manifest["head_sha"],
                "base_sha": manifest["base_sha"],
                "comparison_base_sha": comparison,
                "patch_sha256": manifest["patch_sha256"],
            },
        )
    except Exception:
        shutil.rmtree(output)
        raise
    return (
        "Review the historical pull request frozen in .pr-review-eval/PR_SNAPSHOT.md and the "
        "staged working-tree patch. Inspect the repository's real production paths. Give the "
        "code-review conclusion and concrete next step. Do not modify files, use network access, "
        "or contact anyone."
    )


def verify_materialization(cases_root: Path, repo_cache: Path):
    case_dirs = sorted(path.parent for path in cases_root.glob("*/manifest.json"))
    if not case_dirs:
        raise ValueError("no real PR cases found")
    with tempfile.TemporaryDirectory(prefix="pr-review-real-fixtures-") as temp:
        root = Path(temp)
        for case_dir in case_dirs:
            output = root / case_dir.name
            materialize(case_dir, repo_cache, output)
            staged = subprocess.run(
                ["git", "diff", "--cached", "--quiet"], cwd=output, check=False
            ).returncode
            if staged != 1:
                raise ValueError(f"{case_dir.name} did not materialize one staged PR patch")
    return len(case_dirs)


def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    pool = sub.add_parser("capture-pool")
    pool.add_argument("--repo", required=True)
    pool.add_argument("--created-from", required=True)
    pool.add_argument("--created-to", required=True)
    pool.add_argument("--limit", type=int, default=500)
    pool.add_argument("--output", type=Path, required=True)
    select = sub.add_parser("select")
    select.add_argument("--pool", type=Path, required=True)
    select.add_argument("--policy", type=Path, required=True)
    select.add_argument("--output", type=Path, required=True)
    diverse = sub.add_parser("select-diverse")
    diverse.add_argument("--pool", type=Path, action="append", required=True)
    diverse.add_argument("--policy", type=Path, required=True)
    diverse.add_argument("--output", type=Path, required=True)
    diverse_verify = sub.add_parser("verify-diverse-selection")
    diverse_verify.add_argument("--candidates", type=Path, required=True)
    diverse_verify.add_argument("--policy", type=Path, required=True)
    diverse_verify.add_argument("--selection", type=Path, required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--repo", required=True)
    capture.add_argument("--number", type=int, required=True)
    capture.add_argument("--case-id", required=True)
    capture.add_argument("--output-root", type=Path, required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--cases-root", type=Path, required=True)
    verify.add_argument("--selection", type=Path)
    material = sub.add_parser("materialize")
    material.add_argument("--case", type=Path, required=True)
    material.add_argument("--repo-cache", type=Path, required=True)
    material.add_argument("--output", type=Path, required=True)
    material_check = sub.add_parser("verify-materialization")
    material_check.add_argument("--cases-root", type=Path, required=True)
    material_check.add_argument("--repo-cache", type=Path, required=True)
    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "capture-pool":
        capture_pool(args.repo, args.created_from, args.created_to, args.output, args.limit)
    elif args.command == "select":
        capture_selected(args.pool, args.policy, args.output)
    elif args.command == "select-diverse":
        capture_diverse_selection(args.pool, args.policy, args.output)
    elif args.command == "verify-diverse-selection":
        print(
            f"verified {verify_diverse_selection(args.candidates, args.policy, args.selection)} "
            "diverse PR cases"
        )
    elif args.command == "capture":
        capture_case(args.repo, args.number, args.case_id, args.output_root)
    elif args.command == "verify":
        print(
            f"verified {verify_all(args.cases_root, args.selection)} real PR cases"
        )
    elif args.command == "materialize":
        print(materialize(args.case, args.repo_cache, args.output))
    elif args.command == "verify-materialization":
        print(
            f"materialized {verify_materialization(args.cases_root, args.repo_cache)} real PR cases"
        )


if __name__ == "__main__":
    main()
