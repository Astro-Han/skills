#!/usr/bin/env python3
"""Run headless A/B evals for the skills in this repository.

One run is one fixture, one agent CLI, one arm. The provider is a parameter: everything
after the CLI returns — git diff, tests, outputs, timing — is provider-independent.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from review_feedback_cases import (
    CAUSAL_SYNTHESIS_DESIGN_CASES,
    CAUSAL_SYNTHESIS_HOLDOUT_CASES,
    REVIEW_FEEDBACK_CASES,
)
from pr_review_cases import (
    DESIGN_CASES as PR_REVIEW_DESIGN_CASES,
    HOLDOUT_CASES as PR_REVIEW_HOLDOUT_CASES,
    NO_STATUS_CASES as PR_REVIEW_NO_STATUS_CASES,
    PARTIAL_FACT_CASES as PR_REVIEW_PARTIAL_FACT_CASES,
    PR_REVIEW_CASES,
    REACHABILITY_CASES as PR_REVIEW_REACHABILITY_CASES,
)

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT.parent / "skills"
CONCURRENCY = 6
REAL_PR_CASES = ROOT / "pr-review" / "real" / "cases"
REAL_PR_FIXTURE = ROOT / "pr-review" / "real_fixture.py"
REAL_PR_SELECTION = ROOT / "pr-review" / "real" / "selection.json"
DIVERSE_PR_CASES = ROOT / "pr-review" / "diverse" / "cases"
DIVERSE_PR_SELECTION = ROOT / "pr-review" / "diverse" / "selection.json"
RECALL_PR_CASES = ROOT / "pr-review" / "recall" / "cases"
RECALL_PR_SELECTION = ROOT / "pr-review" / "recall" / "selection.json"
EVIDENCE_RECONCILIATION_SELECTION = (
    ROOT / "pr-review" / "evidence-reconciliation" / "selection.json"
)

# The arm under test is the shipped skill itself, read from skills/<name>/. A named arm is a
# frozen historical baseline under evals/baselines/ — those exist to be compared against, and
# are the only skill text this directory owns a copy of.
SHIPPED = "shipped"
PR_REVIEW_PRE_REACHABILITY_REF = "3e9300fb74ebbecdcd07aad92c5e97a98457f55a"
PR_REVIEW_COMPLETE_FACTS_REF = "72f6f3472fafaa798b5e651fb53f7547c7966749"
PR_REVIEW_THREE_STATES_REF = "d4ea3b6bc9dc198a43024ae500373b8d0f5567ae"
REVIEW_FEEDBACK_STRUCTURAL_BASELINE_REF = "36021bbfa0fed9b63b7a286bf48d83264aad4417"
REVIEW_FEEDBACK_CAUSAL_BASELINE_REF = "af79986"
PR_REVIEW_RECALL_BASELINE_REF = "e28f7da5a9503ec0a93c4db86108d6e8f222fd7d"

PROMPTS = {
    "shared-sections": (
        "Our export job builds several monthly reports in one process. Bug report from "
        "ops: the second report also contains all the sections that were added to the "
        "first report, and vice versa. You can see it with `python3 demo.py` — both "
        "January and February show each other's sections. Please figure out what's "
        "going on and fix it."
    ),
    "diagnose-only": (
        "Support says order totals come out different depending on the order the "
        "coupons were entered in, for the same set of coupons. Before we change "
        "anything I need to know exactly why this happens — please diagnose and report "
        "the root cause with evidence. Do NOT change the code yet; the intended "
        "semantics need a product decision first."
    ),
    "coupon-feature": (
        "Add coupon support to cartlib. `apply_coupon(code)` on Cart, with two known "
        "codes: SAVE10 = 10% off the subtotal, capped at a $20 discount; WELCOME5 = "
        "flat $5 off, but the total never goes below $0. Applying a second coupon "
        "replaces the first. `total()` should reflect the active coupon; unknown codes "
        "raise ValueError."
    ),
    "remove-crash": (
        "Bug: calling `cart.remove('something-not-in-the-cart')` crashes with a "
        "KeyError. It should be a safe no-op instead. Please fix."
    ),
}
PROMPTS.update({name: case["prompt"] for name, case in REVIEW_FEEDBACK_CASES.items()})
PROMPTS.update({name: case["prompt"] for name, case in PR_REVIEW_CASES.items()})


# --- providers -------------------------------------------------------------
#
# A provider differs in three places only: how the CLI is invoked, how a skill arm is
# injected, and how its transcript reports the final message and token usage.


def claude_command(model, prompt, skill_args):
    return ["claude", "-p", "--model", model, "--setting-sources", "project",
            "--dangerously-skip-permissions", "--output-format", "stream-json",
            "--verbose", *skill_args, prompt]


def claude_install(work, arm_dir, skill_name):
    shutil.copytree(arm_dir, work / ".claude" / "skills" / skill_name)
    return []


def claude_parse(events):
    final, tokens = "", 0
    for event in events:
        if event.get("type") == "result":
            final = event.get("result") or ""
            usage = event.get("usage") or {}
            tokens = sum(usage.get(key, 0) for key in ("input_tokens", "output_tokens"))
    return final, tokens


def pi_command(model, prompt, skill_args):
    return ["pi", "-p", "--mode", "json", "--no-session", "--no-extensions",
            "--no-prompt-templates", "--no-themes", "--no-context-files",
            "--no-skills", "--model", model, *skill_args, prompt]


def pi_install(work, arm_dir, skill_name):
    return ["--skill", str(arm_dir)]


def pi_parse(events):
    final, tokens = "", 0
    for event in events:
        message = event.get("message") or {}
        if event.get("type") == "message_end" and message.get("role") == "assistant":
            usage = message.get("usage") or {}
            tokens += sum(usage.get(key, 0) for key in ("input", "output"))
            texts = [part.get("text", "") for part in message.get("content", [])
                     if isinstance(part, dict) and part.get("type") == "text"]
            if texts:
                final = "\n".join(texts)
    return final, tokens


def codex_command(model, prompt, skill_args):
    command = [
        "codex", "exec", "-s", "workspace-write",
        "-c", 'model_reasoning_effort="high"', "--json", "--ephemeral",
        "--ignore-user-config", "--disable", "memories",
    ]
    if model:
        command.extend(["--model", model])
    return [*command, *skill_args, prompt]


def codex_install(work, arm_dir, skill_name):
    shutil.copytree(arm_dir, work / ".agents" / "skills" / skill_name)
    return []


def codex_disable_user_skill(skill_name):
    """Return a CLI override that removes the user's same-name skill from the catalog."""
    user_skill = Path.home() / ".agents" / "skills" / skill_name / "SKILL.md"
    value = "skills.config=[{{path={},enabled=false}}]".format(
        json.dumps(str(user_skill))
    )
    return ["-c", value]


def codex_parse(events):
    final, tokens = "", 0
    for event in events:
        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message" and item.get("text"):
                final = item["text"]
        elif event.get("type") == "turn.completed":
            usage = event.get("usage") or {}
            tokens = sum(usage.get(key, 0) for key in ("input_tokens", "output_tokens"))
    return final, tokens


def keep_all(line):
    return True


def drop_message_updates(line):
    return '"type":"message_update"' not in line and '"type": "message_update"' not in line


@dataclass(frozen=True)
class Provider:
    name: str
    model: str
    timeout_s: int
    command: Callable
    install_skill: Callable
    keep_line: Callable
    parse: Callable
    strip_dotclaude: bool


PROVIDERS = {
    "codex": Provider("codex", "gpt-5.6-luna", 1200,
                      codex_command, codex_install, keep_all, codex_parse, False),
    "claude": Provider("claude", "claude-haiku-4-5-20251001", 900,
                       claude_command, claude_install, keep_all, claude_parse, True),
    "pi": Provider("pi", "ollama-cloud/deepseek-v4-flash", 1200,
                   pi_command, pi_install, drop_message_updates, pi_parse, False),
}


# --- suites ----------------------------------------------------------------


def suite_runs(provider_name, reps=3, suite=None):
    runs = []
    real_suites = {
        "pr-review-real",
        "pr-review-diverse",
        "pr-review-recall",
        "pr-review-evidence-reconciliation",
    }
    single_run_real_suites = {"pr-review-real", "pr-review-diverse", "pr-review-recall"}
    if suite in single_run_real_suites and reps != 1:
        raise ValueError("the real PR holdout requires exactly one paired run per case")
    pr_review_suites = {
        "pr-review": PR_REVIEW_DESIGN_CASES,
        "pr-review-holdout": PR_REVIEW_HOLDOUT_CASES,
        "pr-review-reachability": PR_REVIEW_REACHABILITY_CASES,
        "pr-review-partial-facts": PR_REVIEW_PARTIAL_FACT_CASES,
        "pr-review-no-statuses": PR_REVIEW_NO_STATUS_CASES,
    }
    supported_suites = set(pr_review_suites) | {
        "pr-review-real",
        "pr-review-diverse",
        "pr-review-recall",
        "pr-review-evidence-reconciliation",
        "review-feedback-causal-design",
        "review-feedback-causal-holdout",
        "review-feedback-structural-compression",
        "debug",
        "tdd",
    }
    if suite not in supported_suites:
        raise ValueError("unsupported suite: {!r}".format(suite))
    if suite == "debug" and provider_name != "claude":
        raise ValueError("the debug suite currently supports only the claude provider")
    if suite in real_suites and provider_name != "codex":
        raise ValueError("the real PR holdout currently supports only the codex provider")

    for rep in range(1, reps + 1):
        if suite == "pr-review-real":
            selection = json.loads(REAL_PR_SELECTION.read_text())
            for case in selection["cases"]:
                case_id = "maka-pr-{}".format(case["number"])
                for arm, skill_arm in (("without_skill", None), ("with_skill", SHIPPED)):
                    runs.append({"workspace": "pr-review-real-workspace",
                                 "eval": case_id, "rep": rep,
                                 "arm": arm, "real_case": REAL_PR_CASES / case_id,
                                 "review_only": True,
                                 "skill_arm": skill_arm,
                                 "skill_name": "pr-review",
                                 "installed_skill_name": "pr-review-eval"})
            continue

        if suite == "pr-review-diverse":
            selected_ids = json.loads(DIVERSE_PR_SELECTION.read_text())["cases"]
            indexed = {}
            for manifest_path in DIVERSE_PR_CASES.glob("*/manifest.json"):
                manifest = json.loads(manifest_path.read_text())
                indexed[f"{manifest['repo']}#{manifest['pr_number']}"] = (
                    manifest_path.parent,
                    manifest,
                )
            for selected_id in selected_ids:
                case_dir, manifest = indexed[selected_id]
                for arm, skill_arm in (("without_skill", None), ("with_skill", SHIPPED)):
                    runs.append({"workspace": "pr-review-diverse-workspace",
                                 "eval": manifest["case_id"], "rep": rep,
                                 "arm": arm, "real_case": case_dir,
                                 "repo": manifest["repo"],
                                 "review_only": True,
                                 "skill_arm": skill_arm,
                                 "skill_name": "pr-review",
                                 "installed_skill_name": "pr-review-eval"})
            continue

        if suite == "pr-review-recall":
            selected_ids = json.loads(RECALL_PR_SELECTION.read_text())["cases"]
            indexed = {}
            for manifest_path in RECALL_PR_CASES.glob("*/manifest.json"):
                manifest = json.loads(manifest_path.read_text())
                indexed[f"{manifest['repo']}#{manifest['pr_number']}"] = (
                    manifest_path.parent,
                    manifest,
                )
            for selected_id in selected_ids:
                case_dir, manifest = indexed[selected_id]
                arms = (
                    ("baseline_skill", "git:" + PR_REVIEW_RECALL_BASELINE_REF),
                    ("candidate_skill", SHIPPED),
                )
                for arm, skill_arm in arms:
                    runs.append({"workspace": "pr-review-recall-workspace",
                                 "eval": manifest["case_id"], "rep": rep,
                                 "arm": arm, "real_case": case_dir,
                                 "repo": manifest["repo"],
                                 "review_only": True,
                                 "skill_arm": skill_arm,
                                 "skill_name": "pr-review",
                                 "installed_skill_name": "pr-review-eval"})
            continue

        if suite == "pr-review-evidence-reconciliation":
            selected_ids = json.loads(
                EVIDENCE_RECONCILIATION_SELECTION.read_text()
            )["cases"]
            indexed = {}
            for manifest_path in RECALL_PR_CASES.glob("*/manifest.json"):
                manifest = json.loads(manifest_path.read_text())
                indexed[f"{manifest['repo']}#{manifest['pr_number']}"] = (
                    manifest_path.parent,
                    manifest,
                )
            for selected_id in selected_ids:
                case_dir, manifest = indexed[selected_id]
                arms = (
                    ("baseline_skill", "git:" + PR_REVIEW_RECALL_BASELINE_REF),
                    ("candidate_skill", SHIPPED),
                )
                for arm, skill_arm in arms:
                    runs.append({
                        "workspace": "pr-review-evidence-reconciliation-workspace",
                        "eval": manifest["case_id"],
                        "rep": rep,
                        "arm": arm,
                        "real_case": case_dir,
                        "repo": manifest["repo"],
                        "review_only": True,
                        "skill_arm": skill_arm,
                        "skill_name": "pr-review",
                        "installed_skill_name": "pr-review-eval",
                    })
            continue

        if suite in pr_review_suites:
            cases = pr_review_suites[suite]
            for eval_name in cases:
                fixture = PR_REVIEW_CASES[eval_name]["fixture"]
                if suite == "pr-review-reachability":
                    arms = (("pre_reachability", "git:" + PR_REVIEW_PRE_REACHABILITY_REF),
                            ("with_skill", SHIPPED))
                elif suite == "pr-review-partial-facts":
                    arms = (("complete_facts", "git:" + PR_REVIEW_COMPLETE_FACTS_REF),
                            ("with_skill", SHIPPED))
                elif suite == "pr-review-no-statuses":
                    arms = (("three_states", "git:" + PR_REVIEW_THREE_STATES_REF),
                            ("with_skill", SHIPPED))
                else:
                    arms = (("without_skill", None), ("with_skill", SHIPPED))
                for arm, skill_arm in arms:
                    runs.append({"workspace": "pr-review-workspace",
                                 "eval": eval_name, "rep": rep,
                                 "arm": arm, "fixture": fixture,
                                 "skill_arm": skill_arm,
                                 "skill_name": "pr-review",
                                 "installed_skill_name": "pr-review-eval"})
            continue

        if suite == "review-feedback-structural-compression":
            arms = (("baseline_skill", "git:" + REVIEW_FEEDBACK_STRUCTURAL_BASELINE_REF),
                    ("candidate_skill", SHIPPED))
            for eval_name, case in REVIEW_FEEDBACK_CASES.items():
                if case.get("kind") == "causal_synthesis":
                    continue
                for arm, skill_arm in arms:
                    runs.append({"workspace": "review-feedback-workspace",
                                 "eval": eval_name, "rep": rep,
                                 "arm": arm, "fixture": case["fixture"],
                                 "skill_arm": skill_arm,
                                 "skill_name": "review-feedback",
                                 "installed_skill_name": "review-feedback-eval"})
            continue

        if suite in ("review-feedback-causal-design", "review-feedback-causal-holdout"):
            cases = (CAUSAL_SYNTHESIS_DESIGN_CASES
                     if suite == "review-feedback-causal-design"
                     else CAUSAL_SYNTHESIS_HOLDOUT_CASES)
            arms = (("baseline_skill", "git:" + REVIEW_FEEDBACK_CAUSAL_BASELINE_REF),
                    ("candidate_skill", SHIPPED))
            for eval_name in cases:
                case = REVIEW_FEEDBACK_CASES[eval_name]
                for arm, skill_arm in arms:
                    runs.append({"workspace": "review-feedback-workspace",
                                 "eval": eval_name, "rep": rep,
                                 "arm": arm, "fixture": case["fixture"],
                                 "skill_arm": skill_arm,
                                 "skill_name": "review-feedback",
                                 "installed_skill_name": "review-feedback-eval"})
            continue

        if suite == "debug":
            for eval_name, fixture in (("shared-sections", "reportlib"),
                                       ("diagnose-only", "pricer")):
                for arm, skill_arm in (("without_skill", None),
                                       ("with_skill", SHIPPED)):
                    runs.append({"workspace": "debug-workspace", "eval": eval_name,
                                 "rep": rep, "arm": arm, "fixture": fixture,
                                 "skill_arm": skill_arm, "skill_name": "debug"})

            continue

        if provider_name == "claude":
            arms = (("without_skill", None), ("old_skill", "tdd-old"),
                    ("with_skill", SHIPPED))
        else:
            arms = (("without_skill", None), ("with_skill", SHIPPED))
        for eval_name in ("coupon-feature", "remove-crash"):
            for arm, skill_arm in arms:
                runs.append({"workspace": "tdd-workspace", "eval": eval_name,
                             "rep": rep, "arm": arm, "fixture": "cartlib",
                             "skill_arm": skill_arm, "skill_name": "tdd"})
    return runs


def select_cases(runs, case_names):
    if not case_names:
        return runs
    requested = set(case_names)
    selected = [run for run in runs if run["eval"] in requested]
    missing = requested - {run["eval"] for run in selected}
    if missing:
        raise ValueError("cases not in suite: {}".format(", ".join(sorted(missing))))
    return selected


def select_arms(runs, arm_names):
    if not arm_names:
        return runs
    requested = set(arm_names)
    selected = [run for run in runs if run["arm"] in requested]
    missing = requested - {run["arm"] for run in selected}
    if missing:
        raise ValueError("arms not in suite: {}".format(", ".join(sorted(missing))))
    return selected


# --- one run ---------------------------------------------------------------


def materialize_real_case(case_dir, repo_cache, work):
    result = subprocess.run(
        [sys.executable, str(REAL_PR_FIXTURE), "materialize",
         "--case", str(case_dir), "--repo-cache", str(repo_cache),
         "--output", str(work)],
        check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def repository_cache_for(spec, repo_cache=None, repo_cache_root=None):
    if repo := spec.get("repo"):
        if repo_cache_root is None:
            raise ValueError("diverse PR runs require a repository cache root")
        return repo_cache_root / repo.replace("/", "--")
    if repo_cache is None:
        raise ValueError("real PR runs require a repository cache")
    return repo_cache


def prepare(provider, spec, iteration, repo_cache=None, repo_cache_root=None):
    rundir = (ROOT / spec["workspace"] / iteration
              / "{}-r{}".format(spec["eval"], spec["rep"]) / spec["arm"])
    work = rundir / "work"
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    if real_case := spec.get("real_case"):
        cache = repository_cache_for(spec, repo_cache, repo_cache_root)
        prompt = materialize_real_case(real_case, cache, work)
    else:
        prompt = PROMPTS[spec["eval"]]
        shutil.copytree(ROOT / "fixtures" / spec["fixture"], work,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                    ["git", "-c", "user.email=e@e.co", "-c", "user.name=eval",
                     "commit", "-qm", "fixture"]):
            subprocess.run(cmd, cwd=work, check=True, capture_output=True)
    case = REVIEW_FEEDBACK_CASES.get(spec["eval"], {})
    if seed_patch := case.get("seed_patch"):
        subprocess.run(
            ["git", "apply", "--recount", str(ROOT / "seeds" / seed_patch)],
            cwd=work, check=True, capture_output=True,
        )
        subprocess.run(["git", "add", "-A"], cwd=work, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.email=e@e.co", "-c", "user.name=eval",
             "commit", "-qm", "seed current PR"],
            cwd=work, check=True, capture_output=True,
        )
    skill_args = codex_disable_user_skill(spec["skill_name"]) if provider.name == "codex" else []
    if spec["skill_arm"]:
        if spec["skill_arm"].startswith("git:"):
            ref = spec["skill_arm"].removeprefix("git:")
            arm_dir = rundir / "frozen-skill"
            arm_dir.mkdir()
            skill_text = subprocess.run(
                ["git", "show", "{}:skills/{}/SKILL.md".format(ref, spec["skill_name"])],
                cwd=ROOT.parent, check=True, capture_output=True, text=True,
            ).stdout
            (arm_dir / "SKILL.md").write_text(skill_text)
        else:
            arm_dir = (SKILLS / spec["skill_name"] if spec["skill_arm"] == SHIPPED
                       else ROOT / "baselines" / spec["skill_arm"])
        installed_name = spec.get("installed_skill_name", spec["skill_name"])
        skill_args.extend(provider.install_skill(work, arm_dir, installed_name))
    return rundir, work, skill_args, prompt


def invoke(provider, cmd, work, rundir):
    """Run the agent CLI and write its transcript. Returns (status, seconds)."""
    started = time.time()
    status, stdout, stderr = "ok", "", ""
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=provider.timeout_s)
        stdout, stderr = proc.stdout, proc.stderr
        if proc.returncode != 0:
            status = "exit-{}".format(proc.returncode)
    except subprocess.TimeoutExpired as expired:
        status = "timeout"
        stdout = expired.stdout or ""
        stderr = expired.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
    (rundir / "stderr.log").write_text(stderr)
    kept = [line for line in stdout.splitlines() if provider.keep_line(line)]
    (rundir / "transcript.jsonl").write_text("\n".join(kept) + ("\n" if kept else ""))
    return status, time.time() - started


def finalize(provider, rundir, work, status, duration, run_tests=True):
    """Provider-independent: collect the diff, the tests, and the run's numbers."""
    if provider.strip_dotclaude:
        shutil.rmtree(work / ".claude", ignore_errors=True)
    shutil.rmtree(work / ".agents", ignore_errors=True)
    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached"], cwd=work,
                          capture_output=True, text=True).stdout
    tests = None
    if run_tests:
        tests = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
            cwd=work, capture_output=True, text=True, timeout=120,
        )

    events = []
    for line in (rundir / "transcript.jsonl").read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    final_text, tokens = provider.parse(events)

    outputs = rundir / "outputs"
    outputs.mkdir(exist_ok=True)
    (outputs / "final_message.md").write_text(final_text)
    (outputs / "diff.patch").write_text(diff)
    test_result = (
        "not run: review-only evaluation\n"
        if tests is None
        else "exit={}\n".format(tests.returncode) + tests.stdout + tests.stderr
    )
    (outputs / "test_result.txt").write_text(test_result)
    (rundir / "timing.json").write_text(json.dumps({
        "total_tokens": tokens, "duration_ms": int(duration * 1000),
        "total_duration_seconds": round(duration, 1), "run_status": status,
    }, indent=2))


def run_one(provider, spec, iteration, repo_cache=None, repo_cache_root=None):
    label = "{}/{}/{}-r{}/{}".format(provider.name, spec["workspace"], spec["eval"],
                                     spec["rep"], spec["arm"])
    rundir, work, skill_args, prompt = prepare(
        provider, spec, iteration, repo_cache, repo_cache_root
    )
    cmd = provider.command(provider.model, prompt, skill_args)
    status, duration = invoke(provider, cmd, work, rundir)
    finalize(provider, rundir, work, status, duration,
             run_tests=not spec.get("review_only", False))
    return label, status, round(duration)


# --- entry point -----------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=sorted(PROVIDERS), default="claude")
    parser.add_argument("--model", help="override the provider's default model")
    parser.add_argument("--iteration", default="iteration-1",
                        help="name of the output directory under each workspace")
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--case", action="append", dest="cases",
                        help="run only this exact case from the selected suite; repeatable")
    parser.add_argument("--arm", action="append", dest="arms",
                        help="run only this exact arm from the selected suite; repeatable")
    parser.add_argument("--repo-cache", type=Path,
                        help="full local repository used to materialize real PR fixtures")
    parser.add_argument("--repo-cache-root", type=Path,
                        help="directory of OWNER--REPO caches for the diverse real-PR suite")
    parser.add_argument("--suite", choices=("pr-review", "pr-review-holdout",
                                            "pr-review-reachability", "pr-review-partial-facts",
                                            "pr-review-no-statuses", "pr-review-real",
                                            "pr-review-diverse", "pr-review-recall",
                                            "pr-review-evidence-reconciliation",
                                            "review-feedback-causal-design",
                                            "review-feedback-causal-holdout",
                                            "review-feedback-structural-compression",
                                            "debug", "tdd"),
                        required=True)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the planned runs and the exact CLI command")
    args = parser.parse_args()

    provider = PROVIDERS[args.provider]
    if args.model:
        provider = Provider(provider.name, args.model, provider.timeout_s,
                            provider.command, provider.install_skill,
                            provider.keep_line, provider.parse, provider.strip_dotclaude)
    runs = select_cases(suite_runs(provider.name, args.reps, args.suite), args.cases)
    runs = select_arms(runs, args.arms)

    if args.suite == "pr-review-real" and not args.dry_run and args.repo_cache is None:
        parser.error("--repo-cache is required for pr-review-real")
    if args.suite in {"pr-review-diverse", "pr-review-recall"} and not args.dry_run \
            and args.repo_cache_root is None:
        parser.error("--repo-cache-root is required for diverse real-PR suites")

    if args.dry_run:
        for spec in runs:
            print("{}/{}-r{}/{}".format(spec["workspace"], spec["eval"],
                                        spec["rep"], spec["arm"]))
        print("\n{} runs; example command:".format(len(runs)))
        print(" ".join(provider.command(provider.model, "<prompt>", [])[:-1]))
        return 0

    print("{} runs on {}, concurrency {}".format(len(runs), provider.name, CONCURRENCY),
          flush=True)
    failures = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(run_one, provider, spec, args.iteration,
                               args.repo_cache, args.repo_cache_root): spec
                   for spec in runs}
        for done, future in enumerate(as_completed(futures), start=1):
            try:
                label, status, secs = future.result()
                print("[{}/{}] {} -> {} ({}s)".format(done, len(runs), label, status, secs),
                      flush=True)
                if status != "ok":
                    failures += 1
            except Exception as exc:
                failures += 1
                print("[{}/{}] ERROR {}".format(done, len(runs), exc), flush=True)
    print("done, {} failures".format(failures), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
