#!/usr/bin/env python3
"""Generate one-concept-removed variants of the current TDD skill.

Historical variants and results remain documented in README.md. Generated
variants are scratch inputs, not additional instruction authorities.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT.parent / "skills" / "tdd" / "SKILL.md"
OUT = ROOT / "baselines" / "tdd-ablations"

PREFIXES = {
    "no-existing-red": "For a defect already captured",
    "no-cost": "Count parameter rows,",
    "no-fallback": "If no trustworthy automated signal",
    "no-pure-refactors": "If explicitly using this skill",
    "no-honest-signal": "Expected results come from",
    "no-refuse-shapes": "Reject implementation-detail checks,",
}


def main():
    source = SKILL.read_text()
    spans = {}
    for name, prefix in PREFIXES.items():
        matches = [line for line in source.splitlines(keepends=True)
                   if line.startswith(prefix)]
        if len(matches) != 1:
            raise SystemExit(f"{name}: expected exactly one matching sentence")
        spans[name] = matches[0]
    if source.count("## Finish\n") != 1:
        raise SystemExit("no-finish-gate: expected one Finish section")
    spans["no-finish-gate"] = "## Finish\n" + source.split("## Finish\n", 1)[1]

    if OUT.exists():
        shutil.rmtree(OUT)
    for name, span in spans.items():
        text = source.replace(span, "", 1)
        target = OUT / name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(text)
        print(f"{name}: {len(source)} -> {len(text)} chars")


if __name__ == "__main__":
    main()
