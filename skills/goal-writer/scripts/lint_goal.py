#!/usr/bin/env python3
"""Lint goal contracts for reliable mechanical defects."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


OBJECTIVE_PATTERNS = [r"(?m)^\s*/goal\b", r"(?im)^\s*(Goal|目标)[:：]"]

PLACEHOLDER_HINTS = re.compile(
    r"\b(one|files?|issues?|logs?|docs?|commands?|current|state|scope|context|constraints?|verification|iteration|stop|pause|final|goal|outcome|target|surface|what|why|how|which|path|url|branch|tests?|artifact|evidence)\b|待定|待补充|填写|占位|补充",
    flags=re.IGNORECASE,
)
TODO_PLACEHOLDERS = [r"\bTBD\b", r"\bTODO\b", r"待定", r"待补充"]

VAGUE_OR_DANGEROUS = [
    r"make sure it works",
    r"edit anything",
    r"change whatever",
    r"keep trying",
    r"until it (looks|seems|feels) good",
    r"fix everything",
    r"improve everything",
    r"随便改",
    r"随意修改",
    r"一直尝试",
    r"直到满意",
    r"看起来不错就行",
    r"感觉可以",
]

DEFAULT_MAX_CHARS = 4000


def strip_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)


def placeholder_matches(text: str) -> list[str]:
    matches: list[str] = []
    for match in re.finditer(r"\[([^\]\n]{1,80})\]", text):
        content = match.group(1).strip()
        if not content:
            continue
        if match.end() < len(text) and text[match.end()] == "(":
            continue
        if re.fullmatch(r"#?\d+|[0-9]{4}-[0-9]{2}-[0-9]{2}", content):
            continue
        if PLACEHOLDER_HINTS.search(content) and (
            content.islower() or " " in content or "," in content or "/" in content or re.search(r"待|补|填|占位", content)
        ):
            matches.append(match.group(0))

    for match in re.finditer(r"<([^>\n]{1,80})>", text):
        content = match.group(1).strip()
        if re.fullmatch(r"/?[a-z][a-z0-9-]*", content):
            continue
        if PLACEHOLDER_HINTS.search(content) or re.search(r"\s|\.md|\b(TODO|TBD)\b|待定|待补充", content, flags=re.IGNORECASE):
            matches.append(match.group(0))

    for pattern in TODO_PLACEHOLDERS:
        matches.extend(match.group(0) for match in re.finditer(pattern, text, flags=re.IGNORECASE))
    return matches


NEGATION_BEFORE_DANGER = re.compile(r"(do not|don't|never|no|without|unless|avoid|forbid|禁止|不要|不得|不能|不允许|不应|避免|停止)", flags=re.IGNORECASE)


def dangerous_matches(text: str) -> list[str]:
    matched: list[str] = []
    for pattern in VAGUE_OR_DANGEROUS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            line_start = text.rfind("\n", 0, match.start()) + 1
            prefix = text[line_start : match.start()]
            if NEGATION_BEFORE_DANGER.search(prefix[-80:]):
                continue
            matched.append(pattern)
            break
    return matched


def lint_text(text: str, source: str, max_chars: int = DEFAULT_MAX_CHARS) -> tuple[list[str], list[str]]:
    text = strip_fences(text)
    errors: list[str] = []
    warnings: list[str] = []

    if re.search(r"(?m)^\s*/目标\b", text):
        errors.append("Use `/goal`, not `/目标`, when the target product is Codex; for other products use `Goal:` or the product's native command.")

    for matched in placeholder_matches(text):
        errors.append(f"Unresolved placeholder matched `{matched}`.")

    for pattern in dangerous_matches(text):
        errors.append(f"Dangerous vague instruction matched `{pattern}`.")

    goal_line = next(
        (
            line.strip()
            for line in text.splitlines()
            if line.strip().startswith("/goal") or re.match(r"(?i)^\s*(Goal|目标)[:：]", line.strip())
        ),
        "",
    )
    objective = re.sub(r"(?i)^\s*(/goal|Goal[:：]|目标[:：])\s*", "", goal_line).strip()
    if not any(re.search(pattern, text) for pattern in OBJECTIVE_PATTERNS):
        errors.append("Missing goal entry: use `/goal` for Codex or `Goal:` / `目标：` for a plain-text contract.")
    elif not objective:
        errors.append("Goal outcome is empty.")

    length = len(text)
    if length > max_chars:
        errors.append(
            f"Goal block is {length} chars, over the {max_chars}-char hard limit (same raw count for any language). The target field may reject or truncate it; trim the contract to fit."
        )

    errors = [f"{source}: {error}" for error in errors]
    warnings = [f"{source}: {warning}" for warning in warnings]
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint agent goal contract files.")
    parser.add_argument("files", nargs="+", help="Agent goal markdown/text files to lint; use - for stdin")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS, help="Hard character limit for the goal block")
    args = parser.parse_args(argv)

    results = []
    for raw_path in args.files:
        if raw_path == "-":
            source = "<stdin>"
            text = sys.stdin.read()
            errors, warnings = lint_text(text, source, args.max_chars)
        else:
            path = Path(raw_path)
            source = str(path)
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                errors = [f"{path}: cannot read file: {exc}"]
                warnings = []
            else:
                errors, warnings = lint_text(text, source, args.max_chars)
        results.append({"file": source, "passed": not errors, "errors": errors, "warnings": warnings})

    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for result in results:
            if result["passed"]:
                print(f"{result['file']}: goal lint passed")
            else:
                for error in result["errors"]:
                    print(error, file=sys.stderr)
            for warning in result["warnings"]:
                print(f"warning: {warning}", file=sys.stderr)

    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
