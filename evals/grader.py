#!/usr/bin/env python3
"""Deterministic grader: parses stream-json transcripts and run outputs."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from review_feedback_cases import REVIEW_FEEDBACK_CASES

ROOT = Path(__file__).resolve().parent

PI_NAME_MAP = {"bash": "Bash", "write": "Write", "edit": "Edit", "read": "Read"}


def load_events_pi(transcript):
    events, results, final = [], {}, ""
    for line in transcript.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = e.get("type")
        if t == "message_end" and e["message"].get("role") == "assistant":
            texts = []
            for c in e["message"].get("content", []):
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "toolCall":
                    args = c.get("arguments") or {}
                    events.append({"id": c.get("id"),
                                   "name": PI_NAME_MAP.get(c.get("name"), c.get("name")),
                                   "input": {"file_path": args.get("path", ""),
                                             "command": args.get("command", "")},
                                   "result": ""})
                elif c.get("type") == "text":
                    texts.append(c.get("text", ""))
            if texts:
                events.append({"id": None, "name": "AssistantText",
                               "input": {"text": "\n".join(texts)}, "result": ""})
                final = "\n".join(texts)
        elif t == "tool_execution_end":
            content = e.get("result", {}).get("content", [])
            text = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            results[e.get("toolCallId")] = text
    for ev in events:
        ev["result"] = results.get(ev["id"], "")
    return events, final


def load_events_codex(transcript):
    events, final = [], ""
    for line in transcript.read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "item.completed":
            continue
        item = event.get("item") or {}
        kind = item.get("type")
        if kind == "agent_message" and item.get("text"):
            final = item["text"]
            events.append({"id": item.get("id"), "name": "AssistantText",
                           "input": {"text": item["text"]}, "result": ""})
        elif kind == "command_execution":
            events.append({"id": item.get("id"), "name": "Bash",
                           "input": {"command": item.get("command", "")},
                           "result": item.get("aggregated_output", "")})
        elif kind == "file_change":
            for change in item.get("changes") or []:
                events.append({"id": item.get("id"), "name": "Edit",
                               "input": {"file_path": change.get("path", "")},
                               "result": change.get("kind", "")})
    return events, final


def load_events(transcript):
    """Return ordered [(name, input, result_text)] for tool calls, plus final text."""
    first = transcript.read_text().split("\n", 1)[0]
    if '"type":"thread.started"' in first or '"type": "thread.started"' in first:
        return load_events_codex(transcript)
    if '"type":"session"' in first or '"type": "session"' in first:
        return load_events_pi(transcript)
    events, results, final = [], {}, ""
    for line in transcript.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "assistant":
            texts = []
            for c in e["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    events.append({"id": c.get("id"), "name": c["name"],
                                   "input": c.get("input") or {}, "result": ""})
                elif isinstance(c, dict) and c.get("type") == "text" and c.get("text"):
                    texts.append(c["text"])
            if texts:
                events.append({"id": None, "name": "AssistantText",
                               "input": {"text": "\n".join(texts)}, "result": ""})
        elif e.get("type") == "user":
            for c in e["message"].get("content", []) if isinstance(e["message"].get("content"), list) else []:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    results[c.get("tool_use_id")] = str(c.get("content"))
        elif e.get("type") == "result":
            final = e.get("result") or ""
    for ev in events:
        ev["result"] = results.get(ev["id"], "")
    return events, final


def first_edit(events, path_sub):
    for i, ev in enumerate(events):
        if ev["name"] in ("Write", "Edit", "NotebookEdit"):
            if path_sub in str(ev["input"].get("file_path", "")):
                return i
        if ev["name"] == "Bash":
            cmd = str(ev["input"].get("command", ""))
            if re.search(r"(>>?|tee)\s*\S*" + re.escape(path_sub.split("/")[-1]), cmd):
                return i
    return None


def first_production_edit(events, paths):
    edits = [index for path in paths if (index := first_edit(events, path)) is not None]
    return min(edits) if edits else None


def adjudication_before(events, edit_index, comments=("C1", "C2", "C3")):
    messages = [
        (i, str(event["input"].get("text", "")))
        for i, event in enumerate(events[:edit_index])
        if event["name"] == "AssistantText"
    ]
    text = "\n".join(message for _, message in messages)
    if not messages or not all(comment in text for comment in comments):
        return None, text
    return messages[-1][0], text


def has_all_comments(text, comments):
    return all(comment in text for comment in comments)


def says_no_finding(text):
    lower = text.lower()
    return any(term in lower for term in ("no finding", "无 finding", "disproved", "不成立"))


def comment_lines(text, comment):
    return [line for line in text.splitlines() if comment.lower() in line.lower()]


def comments_have_severity(text, comments, severity):
    lower_severity = severity.lower()
    return all(any(lower_severity in line.lower() for line in comment_lines(text, comment))
               for comment in comments)


def bash_runs(events, pred):
    return [(i, ev) for i, ev in enumerate(events)
            if ev["name"] == "Bash" and pred(str(ev["input"].get("command", "")))]


def is_test_cmd(cmd):
    return "unittest" in cmd or "pytest" in cmd or bool(re.search(r"python3?\s+\S*tests?/", cmd))


def looks_failed(text):
    return any(s in text for s in ("FAILED", "FAIL:", "Error", "Traceback", "error"))


def diff_files(diff):
    return set(re.findall(r"^diff --git a/(\S+)", diff, flags=re.M))


def added_lines(diff, path_sub):
    lines, in_file = [], False
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            in_file = path_sub in line
        elif in_file and line.startswith("+") and not line.startswith("+++"):
            lines.append(line[1:])
    return lines


def expect(items, text, passed, evidence):
    items.append({"text": text, "passed": bool(passed), "evidence": evidence[:300]})


def acceptance(work, script):
    proc = subprocess.run(["python3", str(ROOT / "acceptance" / script)], cwd=work,
                          capture_output=True, text=True, timeout=60,
                          env={**os.environ, "PYTHONPATH": "."})
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def real_diff(work):
    root = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"],
                          cwd=work, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
    return subprocess.run(
        ["git", "diff", root, "--", ".", ":(exclude).claude",
         ":(exclude)**/__pycache__/**", ":(exclude)**/*.pyc"],
        cwd=work, capture_output=True, text=True).stdout


def source_terms_match(work, required, forbidden):
    evidence = []
    passed = True
    for path, terms in required.items():
        text = (work / path).read_text().lower()
        missing = [term for term in terms if term.lower() not in text]
        passed = passed and not missing
        if missing:
            evidence.append("{} missing {}".format(path, missing))
    for path, terms in forbidden.items():
        text = (work / path).read_text().lower()
        present = [term for term in terms if term.lower() in text]
        passed = passed and not present
        if present:
            evidence.append("{} retained {}".format(path, present))
    return passed, "; ".join(evidence)


def grade_review_feedback_case(exp, events, work, files, tests_green, triggered, case):
    src_edit = first_production_edit(events, case["production_paths"])
    ledger_index, ledger = adjudication_before(
        events, src_edit if src_edit is not None else len(events), comments=case["comments"]
    )
    ledger_lower = ledger.lower()
    root_ok = (all(term.lower() in ledger_lower for term in case["root_all"])
               and any(term.lower() in ledger_lower for term in case["root_any"]))
    false_lines = comment_lines(ledger, case["comments"][-1])
    false_ok = (any(says_no_finding(line) and "push back" in line.lower()
                    for line in false_lines)
                and any(term.lower() in ledger_lower for term in case["false_terms"]))
    changed_production = files.intersection(case["production_paths"])
    owner_files = set(case["owner_files"])
    sources_ok, source_evidence = source_terms_match(
        work, case["owner_required"], case["owner_forbidden"]
    )
    false_source_ok, false_source_evidence = source_terms_match(
        work, {}, case["false_forbidden"]
    )

    expect(exp, "Loaded the isolated review-feedback eval arm",
           triggered, "local eval skill loaded: {}".format(triggered))
    expect(exp, "Published a complete ledger before editing production code",
           ledger_index is not None and src_edit is not None and ledger_index < src_edit,
           "ledger idx {}, first source edit idx {}".format(ledger_index, src_edit))
    expect(exp, "Grouped comments at the natural owner: {}".format(case["root_label"]),
           root_ok, ledger[:300])
    expect(exp, "Reclassified the bounded defect as P2 using P0-P3",
           comments_have_severity(ledger, case["comments"][:2], "P2"), ledger[:300])
    expect(exp, "Rejected the false finding: {}".format(case["false_label"]),
           false_ok, ledger[:300])
    expect(exp, "Implemented the owner-level end state without sibling patches",
           changed_production == owner_files and not files.intersection(case["forbidden_files"])
           and sources_ok,
           "changed production: {}; {}".format(sorted(changed_production), source_evidence))
    expect(exp, "Did not implement the false suggestion",
           false_source_ok, false_source_evidence)
    ok, evidence = acceptance(work, case["acceptance"])
    expect(exp, "Acceptance: owner-level behavior covers independent producers", ok, evidence)
    expect(exp, "Existing suite green at the end", tests_green, "")


def grade_run(rundir, eval_name):
    events, final = load_events(rundir / "transcript.jsonl")
    diff = real_diff(rundir / "work")
    tests_green = (rundir / "outputs" / "test_result.txt").read_text().startswith("exit=0")
    work = rundir / "work"
    files = diff_files(diff)
    exp = []
    triggered = any(
        ev["name"] == "Skill"
        or (ev["name"] == "Bash"
            and "review-feedback-eval/SKILL.md" in str(ev["input"].get("command", "")))
        for ev in events
    )
    finallower = final.lower()

    if eval_name == "shared-sections":
        src_edit = first_edit(events, "reportlib/")
        repro = bash_runs(events, lambda c: "demo.py" in c or "ReportBuilder" in c)
        expect(exp, "Reproduced the symptom before editing source",
               repro and (src_edit is None or repro[0][0] < src_edit),
               "first repro idx {} vs first src edit idx {}".format(repro[0][0] if repro else None, src_edit))
        expect(exp, "Named the root cause (shared mutable default argument)",
               any(k in finallower for k in ("mutable default", "default argument", "sections=[]",
                                             "shared list", "same list", "default parameter")),
               finallower[:200])
        expect(exp, "Fixed builder.py only; did not patch the innocent render cache or demo",
               "reportlib/builder.py" in files and "reportlib/render.py" not in files
               and "demo.py" not in files,
               "changed: {}".format(sorted(files)))
        expect(exp, "Added a regression test isolating two builders",
               any("ReportBuilder" in l for l in added_lines(diff, "tests/"))
               and any("def test" in l for l in added_lines(diff, "tests/")),
               "added test lines: {}".format(len(added_lines(diff, "tests/"))))
        expect(exp, "No leftover debug prints in library code",
               not any("print(" in l for l in added_lines(diff, "reportlib/")),
               "")
        expect(exp, "Verified after the fix (reran repro or tests after last source edit)",
               (lambda edits, checks: bool(edits) and bool(checks) and checks[-1][0] > edits[-1])(
                   [i for i, ev in enumerate(events) if ev["name"] in ("Write", "Edit")
                    and "reportlib/" in str(ev["input"].get("file_path", ""))],
                   bash_runs(events, lambda c: "demo.py" in c or is_test_cmd(c))),
               "")
        ok, ev = acceptance(work, "accept_sections.py")
        expect(exp, "Acceptance: two builders stay isolated", ok, ev)
        expect(exp, "Existing suite green at the end", tests_green, "")

    elif eval_name == "diagnose-only":
        expect(exp, "Did not modify pricer source or tests",
               not any(f.startswith(("pricer/", "tests/")) for f in files),
               "changed: {}".format(sorted(files)))
        expect(exp, "Left no scratch artifacts behind (working tree clean)",
               diff.strip() == "", "diff bytes: {}".format(len(diff)))
        expect(exp, "Named the root cause (percent applied to running total, not subtotal)",
               any(k in finallower for k in ("running total", "compound", "already discounted",
                                             "already-discounted", "intermediate total",
                                             "total instead of subtotal", "rather than the subtotal",
                                             "not the original subtotal", "discounted total")),
               finallower[:200])
        expect(exp, "Demonstrated the cause with an executed probe",
               bool(bash_runs(events, lambda c: re.search(r"python3?\s", c)
                              and "unittest" not in c)),
               "python runs: {}".format(len(bash_runs(events, lambda c: re.search(r"python3?\s", c) and "unittest" not in c))))

    elif eval_name in ("coupon-feature", "remove-crash"):
        test_edit = first_edit(events, "tests/")
        impl_edit = first_edit(events, "cartlib/cart.py")
        expect(exp, "Wrote a test before touching the implementation",
               test_edit is not None and (impl_edit is None or test_edit < impl_edit),
               "test edit idx {}, impl edit idx {}".format(test_edit, impl_edit))
        red = [i for i, ev in bash_runs(events, is_test_cmd)
               if looks_failed(ev["result"])]
        expect(exp, "Ran the new test and watched it fail before implementing",
               test_edit is not None and impl_edit is not None
               and any(test_edit < i < impl_edit for i in red),
               "failing runs at {}, window ({}, {})".format(red, test_edit, impl_edit))
        expect(exp, "Iterated in slices (three or more test runs)",
               len(bash_runs(events, is_test_cmd)) >= 3,
               "{} test runs".format(len(bash_runs(events, is_test_cmd))))
        expect(exp, "Suite green at the end", tests_green, "")
        script = "accept_coupon.py" if eval_name == "coupon-feature" else "accept_remove.py"
        ok, ev = acceptance(work, script)
        expect(exp, "Acceptance: delivered behavior matches the request", ok, ev)
        if eval_name == "remove-crash":
            expect(exp, "Fix stayed minimal (few added implementation lines)",
                   len(added_lines(diff, "cartlib/cart.py")) <= 6,
                   "{} added lines in cart.py".format(len(added_lines(diff, "cartlib/cart.py"))))

    elif eval_name in REVIEW_FEEDBACK_CASES:
        grade_review_feedback_case(
            exp, events, work, files, tests_green, triggered,
            REVIEW_FEEDBACK_CASES[eval_name],
        )

    return {"expectations": exp, "skill_triggered": triggered}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", default="iteration-1",
                        help="the output directory runner.py wrote, under each workspace")
    args = parser.parse_args()
    for workspace in sorted(ROOT.glob("*-workspace")):
        iteration = workspace / args.iteration
        if not iteration.is_dir():
            continue
        for evaldir in sorted(iteration.iterdir()):
            if not evaldir.is_dir():
                continue
            eval_name = re.sub(r"-r\d+$", "", evaldir.name)
            for arm in sorted(d for d in evaldir.iterdir() if d.is_dir()):
                grading = grade_run(arm, eval_name)
                (arm / "grading.json").write_text(json.dumps(grading, indent=2))
                passed = sum(1 for e in grading["expectations"] if e["passed"])
                print("{}/{}/{}: {}/{} passed, triggered={}".format(
                    workspace.name, evaldir.name, arm.name, passed,
                    len(grading["expectations"]), grading["skill_triggered"]))


if __name__ == "__main__":
    sys.exit(main())
