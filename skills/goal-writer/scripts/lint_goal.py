#!/usr/bin/env python3
"""Lint goal contracts for reliable mechanical defects."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TODO_PLACEHOLDERS = [r"\bTBD\b", r"\bTODO\b", r"待定", r"待补充"]

DEFAULT_MAX_CHARS = 4000
DEFAULT_WARN_CHARS = 2000


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
    for pattern in TODO_PLACEHOLDERS:
        matches.extend(match.group(0) for match in re.finditer(pattern, text, flags=re.IGNORECASE))
    return matches


def lint_text(text: str, source: str, max_chars: int = DEFAULT_MAX_CHARS) -> tuple[list[str], list[str]]:
    text = strip_fences(text)
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        errors.append("Goal contract is empty.")

    for matched in placeholder_matches(text):
        errors.append(f"Unresolved placeholder matched `{matched}`.")

    length = len(text)
    if length > max_chars:
        errors.append(
            f"Goal block is {length} chars, over the {max_chars}-char hard limit (same raw count for any language). The target field may reject or truncate it; trim the contract to fit."
        )
    elif length > DEFAULT_WARN_CHARS:
        warnings.append(
            f"Goal block is {length} chars; review anything over {DEFAULT_WARN_CHARS} chars for plans, repetition, or facts that do not change completion."
        )

    errors = [f"{source}: {error}" for error in errors]
    warnings = [f"{source}: {warning}" for warning in warnings]
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint agent goal contract files.")
    parser.add_argument("files", nargs="+", help="Agent goal markdown/text files to lint; use - for stdin")
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
