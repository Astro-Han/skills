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

ROOT = Path(__file__).resolve().parent
CONCURRENCY = 6

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
    "zero-drift": (
        "Our nightly inventory sync has been reporting zero drift for every item "
        "since a refactor last sprint, even though the deltas are definitely being "
        "applied — the final quantities in the store come out correct. A teammate "
        "suspects the drift report formatting but we're not sure. `python3 demo.py` "
        "reproduces it. We haven't been able to figure this one out; please find "
        "what's going on and fix it."
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
    "claude": Provider("claude", "claude-haiku-4-5-20251001", 900,
                       claude_command, claude_install, keep_all, claude_parse, True),
    "pi": Provider("pi", "ollama-cloud/deepseek-v4-flash", 1200,
                   pi_command, pi_install, drop_message_updates, pi_parse, False),
}


# --- suites ----------------------------------------------------------------


def suite_runs(provider_name, reps=3):
    runs = []
    for rep in range(1, reps + 1):
        if provider_name == "claude":
            for eval_name, fixture in (("shared-sections", "reportlib"),
                                       ("diagnose-only", "pricer")):
                for arm, skill_arm in (("without_skill", None),
                                       ("with_skill", "debug-current")):
                    runs.append({"workspace": "debug-workspace", "eval": eval_name,
                                 "rep": rep, "arm": arm, "fixture": fixture,
                                 "skill_arm": skill_arm, "skill_name": "debug"})
            arms = (("without_skill", None), ("old_skill", "tdd-old"),
                    ("with_skill", "tdd-current"))
        else:
            arms = (("without_skill", None), ("with_skill", "tdd-current"))
        for eval_name in ("coupon-feature", "remove-crash"):
            for arm, skill_arm in arms:
                runs.append({"workspace": "tdd-workspace", "eval": eval_name,
                             "rep": rep, "arm": arm, "fixture": "cartlib",
                             "skill_arm": skill_arm, "skill_name": "tdd"})
    return runs


# --- one run ---------------------------------------------------------------


def prepare(provider, spec, iteration):
    rundir = (ROOT / spec["workspace"] / iteration
              / "{}-r{}".format(spec["eval"], spec["rep"]) / spec["arm"])
    work = rundir / "work"
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    shutil.copytree(ROOT / "fixtures" / spec["fixture"], work)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.email=e@e.co", "-c", "user.name=eval",
                 "commit", "-qm", "fixture"]):
        subprocess.run(cmd, cwd=work, check=True, capture_output=True)
    skill_args = []
    if spec["skill_arm"]:
        skill_args = provider.install_skill(
            work, ROOT / "skill-arms" / spec["skill_arm"], spec["skill_name"])
    return rundir, work, skill_args


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


def finalize(provider, rundir, work, status, duration):
    """Provider-independent: collect the diff, the tests, and the run's numbers."""
    if provider.strip_dotclaude:
        shutil.rmtree(work / ".claude", ignore_errors=True)
    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached"], cwd=work,
                          capture_output=True, text=True).stdout
    tests = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                           cwd=work, capture_output=True, text=True, timeout=120)

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
    (outputs / "test_result.txt").write_text(
        "exit={}\n".format(tests.returncode) + tests.stdout + tests.stderr)
    (rundir / "timing.json").write_text(json.dumps({
        "total_tokens": tokens, "duration_ms": int(duration * 1000),
        "total_duration_seconds": round(duration, 1), "run_status": status,
    }, indent=2))


def run_one(provider, spec, iteration):
    label = "{}/{}/{}-r{}/{}".format(provider.name, spec["workspace"], spec["eval"],
                                     spec["rep"], spec["arm"])
    rundir, work, skill_args = prepare(provider, spec, iteration)
    cmd = provider.command(provider.model, PROMPTS[spec["eval"]], skill_args)
    status, duration = invoke(provider, cmd, work, rundir)
    finalize(provider, rundir, work, status, duration)
    return label, status, round(duration)


# --- entry point -----------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=sorted(PROVIDERS), default="claude")
    parser.add_argument("--model", help="override the provider's default model")
    parser.add_argument("--iteration", default="iteration-1",
                        help="name of the output directory under each workspace")
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the planned runs and the exact CLI command")
    args = parser.parse_args()

    provider = PROVIDERS[args.provider]
    if args.model:
        provider = Provider(provider.name, args.model, provider.timeout_s,
                            provider.command, provider.install_skill,
                            provider.keep_line, provider.parse, provider.strip_dotclaude)
    runs = suite_runs(provider.name, args.reps)

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
        futures = {pool.submit(run_one, provider, spec, args.iteration): spec
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
