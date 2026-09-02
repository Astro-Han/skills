#!/usr/bin/env python3
"""Deterministic grader: parses stream-json transcripts and run outputs."""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from review_feedback_cases import REVIEW_FEEDBACK_CASES
from pr_review_cases import PR_REVIEW_CASES

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tdd"))
import metrics as tdd_metrics  # noqa: E402

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


def module_mutable_bindings(root, prefix):
    """Count module-level containers that can become a second mutable authority."""
    count = 0
    package = root / prefix.rstrip("/")
    if not package.exists():
        return count
    for path in package.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in tree.body:
            value = None
            names = []
            if isinstance(node, ast.Assign):
                value = node.value
                names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            elif isinstance(node, ast.AnnAssign):
                value = node.value
                names = [node.target.id] if isinstance(node.target, ast.Name) else []
            if not any(not name.startswith("__") for name in names):
                continue
            if isinstance(value, (ast.List, ast.Dict, ast.Set)):
                count += 1
            elif (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                  and value.func.id in {"list", "dict", "set"}):
                count += 1
    return count


def annotated_class_fields(root, prefix):
    """Count persisted-looking class fields without prescribing their names."""
    count = 0
    package = root / prefix.rstrip("/")
    if not package.exists():
        return count
    for path in package.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                count += sum(isinstance(child, ast.AnnAssign) for child in node.body)
    return count


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
    expected_severity = case.get("expected_severity", "P2")
    expect(exp, "Reclassified the defect as {} using P0-P3".format(expected_severity),
           comments_have_severity(ledger, case["comments"][:2], expected_severity),
           ledger[:300])
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


def first_position(text, terms):
    positions = [text.find(term.lower()) for term in terms if text.find(term.lower()) >= 0]
    return min(positions) if positions else None


def section_position(text, english, chinese):
    patterns = (
        r"(?im)^#{{1,4}}\s*{}\b".format(re.escape(english)),
        r"(?im)^#{{1,4}}\s*{}".format(re.escape(chinese)),
    )
    positions = [match.start() for pattern in patterns if (match := re.search(pattern, text))]
    return min(positions) if positions else None


def component_split_present(text, label, additions, deletions):
    text = text.lower()
    label_pattern = (r"(?:production|prod|生产(?:代码)?)" if label == "production"
                     else r"(?:tests?|测试)")
    window = r"[^\n]{0,80}"
    compact = re.search(
        label_pattern + window + r"\+\s*{}\s*/\s*-\s*{}".format(additions, deletions),
        text,
    )
    verbose = re.search(
        label_pattern + window + r"{}\s+additions?".format(additions)
        + window + r"{}\s+deletions?".format(deletions),
        text,
    )
    additions_only = re.search(
        label_pattern + window + r"\+?\s*{}(?:\D|$)".format(additions), text
    )
    return bool(compact or verbose or additions_only)


def split_reported(text, production_add, production_del, test_add, test_del):
    lower = text.lower()
    combined = re.search(
        r"(?:production|prod|生产)(?:\s*/\s*(?:tests?|测试))?\s+split"
        r"[^\n]{{0,30}}\+\s*{}\s*/\s*-\s*{}\s*/\s*\+\s*{}\s*/\s*-?\s*{}".format(
            production_add, production_del, test_add, test_del
        ),
        lower,
    )
    return bool(combined) or (
        component_split_present(lower, "production", production_add, production_del)
        and component_split_present(lower, "tests", test_add, test_del)
    )


def formal_review_state(text):
    """Return an invented Approve/Comment/Wait output state, if present."""
    choices = ("approve", "comment", "wait")
    headings = ("recommendation", "conclusion", "next step", "建议", "结论", "下一步")
    lines = text.lower().splitlines()
    for index, line in enumerate(lines):
        normalized = line.replace("**", "").strip(" #*_-—:`")
        heading = next((term for term in headings if normalized.startswith(term)), None)
        candidates = [(normalized, False)] if heading is None else [(
            normalized.removeprefix(heading).strip(" :：—-*"), True
        )]
        if heading is not None:
            for next_line in lines[index + 1:index + 13]:
                if next_line.lstrip().startswith("#"):
                    break
                candidates.append((next_line.replace("**", "").strip(" #*_-—:`"), True))
        for candidate, under_heading in candidates:
            if candidate in choices:
                return candidate
            if under_heading:
                for choice in choices:
                    if candidate.startswith(choice + " ") or candidate.startswith(choice + " —"):
                        return choice
    return None


def recommends_approval(text):
    lower = text.lower()
    if formal_review_state(text) == "approve":
        return True
    approval = re.compile(
        r"\b(?:ready|safe|okay|ok|can|should)\s+(?:to\s+)?approve\b"
        r"|\b(?:snapshot|code|pr)\s+can\s+be\s+approved\b"
        r"|\bapprove\s+(?:now|this\s+pr)\b"
        r"|(?:可以|可|应该|应当|能够|能)\s*(?:直接)?批准"
    )
    for match in approval.finditer(lower):
        clause = lower[max(
            lower.rfind("\n", 0, match.start()),
            lower.rfind("。", 0, match.start()),
            lower.rfind("；", 0, match.start()),
            lower.rfind(";", 0, match.start()),
        ) + 1:match.start()]
        if re.search(r"(?:\bnot\b|cannot|can't|do not|不|不能|不可|不得|无法)[^。；;\n]{0,60}$", clause):
            continue
        return True
    return False


def grade_pr_review_case(exp, final, triggered, case):
    lower = final.lower()
    should_trigger = case["should_trigger"]
    expect(exp, "Trigger decision matches the declared boundary",
           triggered == should_trigger,
           "triggered={}, expected={}".format(triggered, should_trigger))

    if not should_trigger:
        if case.get("require_head", True):
            expect(exp, "Reported the exact reviewed head",
                   case["head"].lower() in lower, final[:300])
        expect(exp, "Reported the requested CI facts without a review decision",
               all(all(term in lower for term in pair) for pair in case["status_pairs"])
               and section_position(lower, "next step", "下一步") is None
               and not re.search(r"(?i)\bP[0-3]\b", final),
               final[:300])
        return

    if head := case.get("head"):
        expect(exp, "Reported the exact reviewed head",
               head.lower() in lower, final[:300])

    additions, deletions = case["diff_counts"]
    link_facts = tuple(
        case[key].lower() for key in ("pr_url", "issue_url") if case.get(key)
    )
    verbose_terms = (
        "{} addition{}".format(additions, "" if additions == 1 else "s"),
        "{} deletion{}".format(deletions, "" if deletions == 1 else "s"),
    )
    verbose_diff = all(term in lower for term in verbose_terms)
    compact_diff = re.search(
        r"\+{}\s*/\s*-{}".format(additions, deletions), lower
    )
    facts_ok = all(term in lower for term in link_facts) and (verbose_diff or bool(compact_diff))
    expect(exp, "Reported the available PR facts and diff",
           facts_ok, final[:500])

    production_add, production_del, test_add, test_del = case["split_counts"]
    expect(exp, "Reported the production/test split",
           split_reported(lower, production_add, production_del, test_add, test_del),
           final[:500])

    expect(exp, "Reported what the change adds and what can be removed",
           any(term in lower for term in (
               "add", "remove", "delete", "keep", "preserve", "necessary", "required",
               "unnecessary", "nothing to remove", "增加", "新增", "移除", "删除", "保留",
               "必要", "无需"
           )) and any(term in lower for term in (
               "source of truth", "owner", "state", "lifecycle", "contract", "wrapper",
               "test", "path", "loop", "数据源", "状态", "路径", "测试", "循环"
           )), final[-700:])

    for index, terms in enumerate(case.get("required_term_groups", ())):
        expect(exp, "Covered case-specific review obligation {}".format(index + 1),
               any(term.lower() in lower for term in terms),
               "expected one of {}; {}".format(terms, final[-700:]))

    if forbidden_terms := case.get("forbidden_terms"):
        expect(exp, "Did not invent unavailable live facts",
               not any(term.lower() in lower for term in forbidden_terms),
               "forbidden terms={}; {}".format(forbidden_terms, final[:500]))

    problem_pos = section_position(lower, "problem", "问题")
    solution_pos = section_position(lower, "solution", "解法")
    if solution_pos is None:
        solution_pos = section_position(lower, "solution", "方案")
    if problem_pos is None:
        problem_pos = first_position(lower, tuple(term.lower() for term in case["problem_terms"]))
    if solution_pos is None:
        solution_pos = first_position(lower, tuple(term.lower() for term in case["solution_terms"]))
    next_step_pos = section_position(lower, "next step", "下一步")
    if next_step_pos is None:
        next_step_pos = first_position(lower, tuple(
            term.lower() for term in case["next_step_terms"]
        ))
    expect(exp, "Established the problem before solution and next step",
           problem_pos is not None and solution_pos is not None and next_step_pos is not None
           and problem_pos < solution_pos < next_step_pos,
           "positions problem={}, solution={}, next_step={}".format(
               problem_pos, solution_pos, next_step_pos))

    fact_positions = [lower.find(term) for term in link_facts]
    diff_position = first_position(lower, (verbose_terms[0],))
    if diff_position is None and compact_diff:
        diff_position = compact_diff.start()
    fact_positions.append(diff_position if diff_position is not None else -1)
    expect(exp, "Placed decision-critical PR, Issue, and diff facts before the next step",
           next_step_pos is not None and all(position >= 0 and position < next_step_pos
                                            for position in fact_positions),
           "fact positions={}, next_step={}".format(fact_positions, next_step_pos))

    expect(exp, "Named the predeclared next step",
           next_step_pos is not None
           and any(term.lower() in lower[next_step_pos:] for term in case["next_step_terms"]),
           final[-400:])
    expect(exp, "Did not invent an Approve/Comment/Wait workflow state",
           formal_review_state(final) is None, final[-400:])
    if case.get("forbid_approve"):
        expect(exp, "Did not recommend approval for an unresolved material gap",
               not recommends_approval(final),
               final[-400:])
    if severity := case.get("severity"):
        expect(exp, "Calibrated the finding as {}".format(severity),
               severity.lower() in lower, final[-500:])
    if case.get("forbid_p1"):
        expect(exp, "Did not preserve the overstated P1 severity",
               "p1" not in lower or any(term in lower for term in (
                   "not p1", "不是 p1", "p1 不成立", "p1不成立", "p1 is overstated",
                   "reject the p1", "withdraw", "撤回", "降为 p2", "降级", "p1 → p2",
                   "不成立", "不应定为 p1", "disproved", "invalid", "should be closed",
                   "should be dismissed", "false/unproven p1"
               )),
               final[-500:])
    if reach_terms := case.get("reach_terms"):
        expect(exp, "Named the triggering reachability category",
               any(term.lower() in lower for term in reach_terms), final[-500:])
def grade_scope_rebase_case(exp, events, work, files, tests_green, triggered, case):
    src_edit = first_production_edit(events, case["production_paths"])
    ledger_index, ledger = adjudication_before(
        events, src_edit if src_edit is not None else len(events), comments=case["comments"]
    )
    ledger_lower = ledger.lower()

    def line_has(comment, *terms):
        lines = " ".join(comment_lines(ledger, comment)).lower()
        return all(any(option in lines for option in term) for term in terms)

    expect(exp, "Loaded the isolated review-feedback eval arm",
           triggered, "local eval skill loaded: {}".format(triggered))
    expect(exp, "Rebased the complete second-round ledger before editing",
           ledger_index is not None and src_edit is not None and ledger_index < src_edit,
           "ledger idx {}, first source edit idx {}".format(ledger_index, src_edit))
    expect(exp, "Classified A1 and A2 as current-diff obligations",
           line_has("A1", ("introduced", "current diff", "current pr", "required", "本 pr", "当前 diff"),
                    ("fix at owner", "fix locally", "修复"))
           and line_has("A2", ("introduced", "current diff", "current pr", "required", "本 pr", "当前 diff"),
                        ("fix at owner", "fix locally", "delete or simplify", "修复", "删除")),
           ledger[:500])
    expect(exp, "Rejected the transport scope drift",
           line_has("A3", ("drift", "out of scope", "outside", "original goal",
                           "范围外", "越界", "原始目标"),
                    ("delete", "revert", "push back", "defer", "删除", "撤回", "恢复",
                     "拒绝", "延后")),
           " ".join(comment_lines(ledger, "A3"))[:500])
    expect(exp, "Rejected speculative remote-image infrastructure",
           line_has("A4", ("future", "speculative", "no demand", "未来", "假想", "无需求"),
                    ("push back", "delete or simplify", "defer", "拒绝", "删除", "延后")),
           " ".join(comment_lines(ledger, "A4"))[:500])
    expect(exp, "Rejected the false empty-render finding",
           line_has("A5", ("disproved", "no finding", "false", "不成立"),
                    ("push back", "拒绝")),
           " ".join(comment_lines(ledger, "A5"))[:500])

    changed_production = {
        path for path in files if path.startswith("mediathread/")
    }
    expect(exp, "Final cumulative production diff contains only the feature owners",
           changed_production == {
               "mediathread/copying.py",
               "mediathread/loader.py",
               "mediathread/preview.py",
           },
           "changed production: {}".format(sorted(changed_production)))
    expect(exp, "Removed superseded policy, registry, and transport edits",
           not (work / "mediathread" / "policy.py").exists()
           and not (work / "mediathread" / "registry.py").exists()
           and "allow_preview_payload" not in (work / "mediathread" / "transport.py").read_text()
           and "test_export_reuses_preview_policy" not in (
               work / "tests" / "test_mediathread.py"
           ).read_text(),
           "policy={}, registry={}, transport_changed={}".format(
               (work / "mediathread" / "policy.py").exists(),
               (work / "mediathread" / "registry.py").exists(),
               "mediathread/transport.py" in files,
           ))
    ok, evidence = acceptance(work, case["acceptance"])
    expect(exp, "Acceptance: feature closes both authorities without adjacent scope", ok, evidence)
    expect(exp, "Existing suite green at the end", tests_green, "")


def grade_causal_synthesis_case(exp, events, work, files, tests_green, triggered, case):
    src_edit = first_production_edit(events, case["production_paths"])
    ledger_index, before_edit = adjudication_before(
        events, src_edit if src_edit is not None else len(events), comments=case["comments"]
    )

    expect(exp, "Loaded the isolated review-feedback eval arm",
           triggered, "local eval skill loaded: {}".format(triggered))
    expect(exp, "Published a complete ledger before editing production code",
           ledger_index is not None and src_edit is not None and ledger_index < src_edit,
           "ledger idx {}, first source edit idx {}".format(ledger_index, src_edit))

    authority_hits = [
        term for term in case["authority_terms"] if term.lower() in before_edit.lower()
    ]
    expect(exp, "Reconstructed relevant system authorities before editing",
           len(authority_hits) >= 2, "authority terms: {}".format(authority_hits))

    if case.get("false_comment"):
        false_lines = " ".join(comment_lines(before_edit, case["false_comment"])).lower()
        expect(exp, "Rejected the false finding",
               any(term in false_lines for term in ("disproved", "no finding", "不成立"))
               and any(term in false_lines for term in (
                   "push back", "拒绝", "不加", "不改", "不进入", "不实现"
               )),
               false_lines[:300])
    if case.get("deferred_comment"):
        deferred_lines = " ".join(comment_lines(before_edit, case["deferred_comment"])).lower()
        expect(exp, "Kept the adjacent policy out of scope",
               any(term in deferred_lines for term in (
                   "defer", "push back", "out of scope", "延后", "拒绝", "范围外",
                   "暂不进入", "不进入实现", "不实现", "不扩展", "暂不修"
               )), deferred_lines[:300])

    entropy_ok, entropy_evidence = source_terms_match(work, {}, case["entropy_forbidden"])
    fixture_root = ROOT / "fixtures" / case["fixture"]
    baseline_mutable = module_mutable_bindings(fixture_root, case["production_prefix"])
    final_mutable = module_mutable_bindings(work, case["production_prefix"])
    baseline_fields = annotated_class_fields(fixture_root, case["production_prefix"])
    final_fields = annotated_class_fields(work, case["production_prefix"])
    expect(exp, "Did not accept the reviewer's parallel authority or semantic fallback",
           entropy_ok, entropy_evidence)
    expect(exp, "Did not add mutable module authority",
           final_mutable <= baseline_mutable,
           "module mutable bindings: {} -> {}".format(baseline_mutable, final_mutable))
    expect(exp, "Did not grow the persisted model to carry a patch",
           final_fields <= baseline_fields,
           "annotated class fields: {} -> {}".format(baseline_fields, final_fields))
    for label, script in case["acceptance_checks"]:
        ok, evidence = acceptance(work, script)
        expect(exp, "Acceptance: {}".format(label), ok, evidence)
    expect(exp, "Existing suite green at the end", tests_green, "")


def grade_run(rundir, eval_name):
    events, final = load_events(rundir / "transcript.jsonl")
    diff = real_diff(rundir / "work")
    tests_green = (rundir / "outputs" / "test_result.txt").read_text().startswith("exit=0")
    work = rundir / "work"
    files = diff_files(diff)
    exp = []
    metrics_payload = None
    triggered = any(
        ev["name"] == "Skill"
        or (ev["name"] == "Bash"
            and any(path in str(ev["input"].get("command", "")) for path in (
                "review-feedback-eval/SKILL.md", "pr-review-eval/SKILL.md")))
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

    elif eval_name in ("coupon-feature", "remove-crash", "coupon-cluttered"):
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
        script = "accept_remove.py" if eval_name == "remove-crash" else "accept_coupon.py"
        ok, ev = acceptance(work, script)
        expect(exp, "Acceptance: delivered behavior matches the request", ok, ev)
        if eval_name == "remove-crash":
            expect(exp, "Fix stayed minimal (few added implementation lines)",
                   len(added_lines(diff, "cartlib/cart.py")) <= 6,
                   "{} added lines in cart.py".format(len(added_lines(diff, "cartlib/cart.py"))))

        fixture = "cartlib-cluttered" if eval_name == "coupon-cluttered" else "cartlib"
        suite_stats = tdd_metrics.suite_metrics(work)
        seeded_tests = len(re.findall(
            r"^\s*def (test_\w+)",
            (ROOT / "fixtures" / fixture / "tests" / "test_cart.py").read_text(),
            flags=re.M))
        suite_stats["tests_added"] = suite_stats["tests_passing"] - seeded_tests
        metrics_payload = suite_stats

        if eval_name == "coupon-cluttered":
            tests_text = "".join(
                path.read_text() for path in sorted((work / "tests").glob("*.py")))
            garbage = ("test_items_stored_internally", "test_subtotal_matches_computed_sum",
                       "test_subtotal_is_float", "test_add_many_items_nonempty")
            remaining_garbage = [name for name in garbage if name in tests_text]
            expect(exp, "Deleted the seeded garbage-shape tests it touched",
                   not remaining_garbage, "remaining: {}".format(remaining_garbage))
            subtotal_family = ("test_subtotal_sums_items", "test_subtotal_two_items",
                               "test_subtotal_three_items")
            kept_subtotal = [name for name in subtotal_family if name in tests_text]
            expect(exp, "Collapsed the duplicate subtotal tests to one",
                   len(kept_subtotal) == 1, "kept: {}".format(kept_subtotal))
            total_family = ("test_total_matches_subtotal", "test_total_matches_subtotal_again")
            kept_total = [name for name in total_family if name in tests_text]
            expect(exp, "Collapsed the duplicate total tests",
                   len(kept_total) <= 1, "kept: {}".format(kept_total))
            expect(exp, "Ended with a minimal covering suite (excess tests <= 1)",
                   suite_stats["excess_tests"] <= 1,
                   "excess={}, redundant={}".format(suite_stats["excess_tests"],
                                                    suite_stats["redundant_tests"][:5]))
            expect(exp, "Kept detection strength (kill rate >= 0.75)",
                   suite_stats["kill_rate"] >= 0.75,
                   "kill_rate={}".format(suite_stats["kill_rate"]))

    elif eval_name in REVIEW_FEEDBACK_CASES:
        case = REVIEW_FEEDBACK_CASES[eval_name]
        if case.get("kind") == "scope_rebase":
            grade_scope_rebase_case(
                exp, events, work, files, tests_green, triggered, case,
            )
        elif case.get("kind") == "causal_synthesis":
            grade_causal_synthesis_case(
                exp, events, work, files, tests_green, triggered, case,
            )
        else:
            grade_review_feedback_case(
                exp, events, work, files, tests_green, triggered, case,
            )

    elif eval_name in PR_REVIEW_CASES:
        grade_pr_review_case(exp, final, triggered, PR_REVIEW_CASES[eval_name])

    grading = {"expectations": exp, "skill_triggered": triggered}
    if metrics_payload is not None:
        grading["metrics"] = metrics_payload
    return grading


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
