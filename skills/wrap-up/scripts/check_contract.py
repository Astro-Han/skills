#!/usr/bin/env python3
"""Check wrap-up's bounded session-close contract."""

from __future__ import annotations

import re
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"
EXPECTED_DESCRIPTION = (
    "Close a session cleanly by resolving session-owned loose ends and reporting the final state. "
    "Use when the session is ending or the user asks to wrap up or audit its end."
)


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    description_match = re.search(r"^description:\s*(.+)$", text, flags=re.MULTILINE)
    description = description_match.group(1).strip('"\'') if description_match else ""

    errors: list[str] = []
    if description != EXPECTED_DESCRIPTION:
        errors.append("description does not match the approved What/When contract")

    required = {
        "touched-repository scope": r"repositor(?:y|ies)[^.]+(?:touched|used) (?:in|by) this session|touched repositor(?:y|ies)",
        "final git state": r"git status",
        "ownership separation": r"session-owned[^.]+(?:pre-existing|existing user)|(?:pre-existing|existing user)[^.]+session-owned",
        "runtime cleanup": r"(?:processes|servers)[^.]+browser sessions",
        "artifact cleanup": r"temporary artifacts[^.]+worktrees|worktrees[^.]+temporary artifacts",
        "direct drift repair": r"directly caused[^.]+(?:documentation|configuration)",
        "safe deletion": r"Trash",
        "authority boundary": r"does not grant|already authori[sz]ed",
        "final verification": r"re-run[^.]+verification|final verification",
    }
    forbidden = {
        "remote sync audit": r"check sync status with remote",
        "all-stash audit": r"uncommitted changes, stash",
        "merged-branch sweep": r"merged local branches",
        "memory audit": r"memory index or equivalent manifest",
        "mandatory retrospective": r"interaction retrospective",
    }
    for label, pattern in required.items():
        if not re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"missing {label}")
    for label, pattern in forbidden.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"retains {label}")

    if errors:
        for error in errors:
            print(f"{SKILL}: {error}")
        return 1

    print(f"{SKILL}: bounded session-close contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
