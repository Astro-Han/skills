#!/usr/bin/env python3
"""Run headless Pi (DeepSeek Flash) A/B evals for the tdd skill."""

import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import runner  # PROMPTS

ROOT = Path(__file__).resolve().parent
MODEL = "ark-coding-plan/deepseek-v4-flash"
TIMEOUT_S = 1200

RUNS = []
for rep in (1, 2, 3):
    for eval_name in ("coupon-feature", "remove-crash"):
        for arm, skill_arm in (("without_skill", None), ("with_skill", "tdd-current")):
            RUNS.append({"eval": eval_name, "rep": rep, "arm": arm,
                         "fixture": "cartlib", "skill_arm": skill_arm})


def run_one(spec):
    label = "pi/{}-r{}/{}".format(spec["eval"], spec["rep"], spec["arm"])
    rundir = (ROOT / "tdd-workspace" / "iteration-pi-1"
              / "{}-r{}".format(spec["eval"], spec["rep"]) / spec["arm"])
    work = rundir / "work"
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    shutil.copytree(ROOT / "fixtures" / spec["fixture"], work)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.email=e@e.co", "-c", "user.name=eval", "commit", "-qm", "fixture"]):
        subprocess.run(cmd, cwd=work, check=True, capture_output=True)

    cmd = ["pi", "-p", "--mode", "json", "--no-session", "--no-extensions",
           "--no-prompt-templates", "--no-themes", "--no-context-files",
           "--no-skills", "--model", MODEL]
    if spec["skill_arm"]:
        cmd += ["--skill", str(ROOT / "skill-arms" / spec["skill_arm"])]
    cmd.append(runner.PROMPTS[spec["eval"]])

    t0 = time.time()
    status = "ok"
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=TIMEOUT_S)
        if proc.returncode != 0:
            status = "exit-{}".format(proc.returncode)
        (rundir / "stderr.log").write_text(proc.stderr)
        with open(rundir / "transcript.jsonl", "w") as out:
            for line in proc.stdout.splitlines():
                if '"type":"message_update"' in line or '"type": "message_update"' in line:
                    continue
                out.write(line + "\n")
    except subprocess.TimeoutExpired:
        status = "timeout"
        (rundir / "transcript.jsonl").write_text("")
    duration = time.time() - t0

    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached"], cwd=work,
                          capture_output=True, text=True).stdout
    tests = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                           cwd=work, capture_output=True, text=True, timeout=120)

    final_text, tokens = "", 0
    for line in (rundir / "transcript.jsonl").read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "message_end" and e["message"].get("role") == "assistant":
            usage = e["message"].get("usage") or {}
            tokens += usage.get("output", 0)
            texts = [c.get("text", "") for c in e["message"].get("content", [])
                     if isinstance(c, dict) and c.get("type") == "text"]
            if texts:
                final_text = "\n".join(texts)

    outputs = rundir / "outputs"
    outputs.mkdir()
    (outputs / "final_message.md").write_text(final_text)
    (outputs / "diff.patch").write_text(diff)
    (outputs / "test_result.txt").write_text(
        "exit={}\n".format(tests.returncode) + tests.stdout + tests.stderr)
    (rundir / "timing.json").write_text(json.dumps({
        "total_tokens": tokens, "duration_ms": int(duration * 1000),
        "total_duration_seconds": round(duration, 1), "run_status": status,
    }, indent=2))
    (rundir.parent / "eval_metadata.json").write_text(json.dumps({
        "eval_name": rundir.parent.name, "prompt": runner.PROMPTS[spec["eval"]],
        "assertions": []}, indent=2))
    return label, status, round(duration)


def main():
    print("{} pi runs".format(len(RUNS)), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for label, status, secs in pool.map(run_one, RUNS):
            print("{} -> {} ({}s)".format(label, status, secs), flush=True)


if __name__ == "__main__":
    sys.exit(main())
