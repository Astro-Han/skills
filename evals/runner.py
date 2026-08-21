#!/usr/bin/env python3
"""Run headless Haiku A/B evals for the debug and tdd skills."""

import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = "claude-haiku-4-5-20251001"
TIMEOUT_S = 900
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

RUNS = []
for rep in (1, 2, 3):
    for eval_name, fixture in (("shared-sections", "reportlib"), ("diagnose-only", "pricer")):
        for arm, skill_arm in (("without_skill", None), ("with_skill", "debug-current")):
            RUNS.append({
                "workspace": "debug-workspace", "eval": eval_name, "rep": rep,
                "arm": arm, "fixture": fixture, "skill_arm": skill_arm, "skill_name": "debug",
            })
    for eval_name in ("coupon-feature", "remove-crash"):
        for arm, skill_arm in (
            ("without_skill", None), ("old_skill", "tdd-old"), ("with_skill", "tdd-current"),
        ):
            RUNS.append({
                "workspace": "tdd-workspace", "eval": eval_name, "rep": rep,
                "arm": arm, "fixture": "cartlib", "skill_arm": skill_arm, "skill_name": "tdd",
            })


def run_one(spec):
    label = "{}/{}-r{}/{}".format(spec["workspace"], spec["eval"], spec["rep"], spec["arm"])
    rundir = ROOT / spec["workspace"] / "iteration-1" / "{}-r{}".format(spec["eval"], spec["rep"]) / spec["arm"]
    work = rundir / "work"
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    shutil.copytree(ROOT / "fixtures" / spec["fixture"], work)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.email=e@e.co", "-c", "user.name=eval", "commit", "-qm", "fixture"]):
        subprocess.run(cmd, cwd=work, check=True, capture_output=True)
    if spec["skill_arm"]:
        shutil.copytree(ROOT / "skill-arms" / spec["skill_arm"],
                        work / ".claude" / "skills" / spec["skill_name"])

    t0 = time.time()
    status = "ok"
    with open(rundir / "transcript.jsonl", "w") as out, open(rundir / "stderr.log", "w") as err:
        try:
            proc = subprocess.run(
                ["claude", "-p", "--model", MODEL, "--setting-sources", "project",
                 "--dangerously-skip-permissions", "--output-format", "stream-json",
                 "--verbose", PROMPTS[spec["eval"]]],
                cwd=work, stdout=out, stderr=err, stdin=subprocess.DEVNULL, timeout=TIMEOUT_S)
            if proc.returncode != 0:
                status = "exit-{}".format(proc.returncode)
        except subprocess.TimeoutExpired:
            status = "timeout"
    duration = time.time() - t0

    shutil.rmtree(work / ".claude", ignore_errors=True)
    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached"], cwd=work, capture_output=True, text=True).stdout
    tests = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                           cwd=work, capture_output=True, text=True, timeout=120)

    final_text, total_tokens = "", 0
    for line in (rundir / "transcript.jsonl").read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            final_text = event.get("result") or ""
            usage = event.get("usage") or {}
            total_tokens = sum(usage.get(k, 0) for k in ("input_tokens", "output_tokens"))

    outputs = rundir / "outputs"
    outputs.mkdir()
    (outputs / "final_message.md").write_text(final_text)
    (outputs / "diff.patch").write_text(diff)
    (outputs / "test_result.txt").write_text(
        "exit={}\n".format(tests.returncode) + tests.stdout + tests.stderr)
    (rundir / "timing.json").write_text(json.dumps({
        "total_tokens": total_tokens, "duration_ms": int(duration * 1000),
        "total_duration_seconds": round(duration, 1), "run_status": status,
    }, indent=2))
    return label, status, round(duration)


def main():
    print("{} runs, concurrency {}".format(len(RUNS), CONCURRENCY), flush=True)
    failures = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(run_one, spec): spec for spec in RUNS}
        done = 0
        for future in as_completed(futures):
            done += 1
            try:
                label, status, secs = future.result()
                print("[{}/{}] {} -> {} ({}s)".format(done, len(RUNS), label, status, secs), flush=True)
                if status != "ok":
                    failures += 1
            except Exception as exc:
                failures += 1
                print("[{}/{}] ERROR {}".format(done, len(RUNS), exc), flush=True)
    print("done, {} failures".format(failures), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
