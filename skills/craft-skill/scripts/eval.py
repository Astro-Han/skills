#!/usr/bin/env python3
import argparse
import json
import secrets
import shutil
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def validate_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest.get("decision"), str) or not manifest["decision"].strip():
        raise ValueError("decision must be a non-empty string")
    metric = manifest.get("metric")
    if not isinstance(metric, dict) or metric.get("direction") not in {"higher", "lower"}:
        raise ValueError("metric.direction must be 'higher' or 'lower'")
    if not isinstance(metric.get("name"), str) or not metric["name"].strip():
        raise ValueError("metric.name must be a non-empty string")
    comparison = manifest.get("comparison")
    if not isinstance(comparison, dict):
        raise ValueError("comparison must name baseline and candidate variants")
    baseline = comparison.get("baseline")
    candidate = comparison.get("candidate")
    if not all(isinstance(item, str) and item.strip() for item in (baseline, candidate)):
        raise ValueError("comparison baseline and candidate must be non-empty strings")
    if baseline == candidate:
        raise ValueError("comparison baseline and candidate must differ")
    runs = manifest.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("runs must be a non-empty list")

    variants_by_case: dict[str, set[str]] = defaultdict(set)
    for run in runs:
        if not isinstance(run, dict):
            raise ValueError("each run must be an object")
        case_id = run.get("case_id")
        variant = run.get("variant")
        value = run.get("value")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("each run needs a non-empty case_id")
        if not isinstance(variant, str) or not variant.strip():
            raise ValueError("each run needs a non-empty variant")
        if variant in variants_by_case[case_id]:
            raise ValueError(f"duplicate run for {case_id!r} and {variant!r}")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("each run value must be numeric")
        variants_by_case[case_id].add(variant)

    variant_sets = list(variants_by_case.values())
    if len(variant_sets[0]) != 2 or any(item != variant_sets[0] for item in variant_sets[1:]):
        raise ValueError("every case must contain the same variants")
    if variant_sets[0] != {baseline, candidate}:
        raise ValueError("comparison variants must match every case")
    return manifest


def summarize(path: Path) -> dict[str, Any]:
    manifest = validate_manifest(path)
    baseline = manifest["comparison"]["baseline"]
    candidate = manifest["comparison"]["candidate"]
    values: dict[str, dict[str, float]] = defaultdict(dict)
    for run in manifest["runs"]:
        values[run["case_id"]][run["variant"]] = run["value"]

    baseline_values = [case[baseline] for case in values.values()]
    candidate_values = [case[candidate] for case in values.values()]
    sign = 1 if manifest["metric"]["direction"] == "higher" else -1
    improvements = [
        sign * (candidate_value - baseline_value)
        for baseline_value, candidate_value in zip(
            baseline_values, candidate_values, strict=True
        )
    ]

    def stats(items: list[float]) -> dict[str, float | None]:
        return {
            "mean": statistics.mean(items),
            "sample_stdev": statistics.stdev(items) if len(items) > 1 else None,
        }

    return {
        "decision": manifest["decision"],
        "metric": manifest["metric"],
        "baseline": stats(baseline_values),
        "candidate": stats(candidate_values),
        "paired_improvement": stats(improvements),
    }


def create_blind_pack(left: Path, right: Path, review_dir: Path, key_path: Path) -> None:
    if not left.exists() or not right.exists():
        raise ValueError("both blind inputs must exist")
    if left.is_dir() != right.is_dir():
        raise ValueError("blind inputs must both be files or both be directories")
    if key_path.resolve().is_relative_to(review_dir.resolve()):
        raise ValueError("answer key must be outside the review directory")
    if review_dir.exists() or key_path.exists():
        raise ValueError("review directory and answer key must not already exist")

    sources = [("left", left), ("right", right)]
    secrets.SystemRandom().shuffle(sources)
    review_dir.mkdir(parents=True)
    key: dict[str, dict[str, str]] = {}
    for label, (input_name, source) in zip(("A", "B"), sources, strict=True):
        target = review_dir / (label if source.is_dir() else f"{label}{source.suffix}")
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        key[label] = {"input": input_name, "path": str(source.resolve())}
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    blind = subparsers.add_parser("blind")
    blind.add_argument("left")
    blind.add_argument("right")
    blind.add_argument("--review-dir", required=True)
    blind.add_argument("--key", required=True)
    summarize_parser = subparsers.add_parser("summarize")
    summarize_parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        if args.command == "blind":
            create_blind_pack(
                Path(args.left),
                Path(args.right),
                Path(args.review_dir),
                Path(args.key),
            )
        else:
            print(json.dumps(summarize(Path(args.manifest)), indent=2))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
