#!/usr/bin/env python3
"""Mutation-based over-testing metrics for the tdd suite.

Judges a produced workspace's test suite by evidence, not by reading it: generate
single-site mutants of the production file, record which passing test kills which
mutant, and report how many tests exceed a greedy minimal cover of everything the
suite can detect. `excess_tests` is the over-testing signal; `kill_rate` guards
against trading coverage away for a smaller count.
"""

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HARNESS = """
import json, unittest

loader = unittest.defaultTestLoader
suite = loader.discover("tests", top_level_dir=".")
tests = []


def flatten(item):
    for entry in item:
        if isinstance(entry, unittest.TestSuite):
            flatten(entry)
        else:
            tests.append(entry)


flatten(suite)
out = {}
for test in tests:
    result = unittest.TestResult()
    test.run(result)
    out[test.id()] = result.wasSuccessful()
print(json.dumps(out))
"""

ARITH_SWAPS = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add, ast.Div: ast.Mult}
COMPARE_SWAPS = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
                 ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}


def _mutation_sites(tree):
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and type(node.op) in ARITH_SWAPS:
            sites.append(("binop", node))
        elif isinstance(node, ast.Compare) and len(node.ops) == 1 \
                and type(node.ops[0]) in COMPARE_SWAPS:
            sites.append(("compare", node))
        elif isinstance(node, ast.Constant) and type(node.value) in (int, float) \
                and not isinstance(node.value, bool):
            sites.append(("constant", node))
        elif isinstance(node, ast.FunctionDef):
            for index, statement in enumerate(node.body):
                sites.append(("drop-statement", (node, index)))
    return sites


def generate_mutants(source):
    """Return deterministic single-site mutants of `source`, each compilable."""
    mutants = []
    total = len(_mutation_sites(ast.parse(source)))
    for target in range(total):
        tree = ast.parse(source)
        kind, payload = _mutation_sites(tree)[target]
        if kind == "binop":
            payload.op = ARITH_SWAPS[type(payload.op)]()
        elif kind == "compare":
            payload.ops = [COMPARE_SWAPS[type(payload.ops[0])]()]
        elif kind == "constant":
            payload.value = payload.value + 1
        else:
            function, index = payload
            if len(function.body) == 1:
                function.body = [ast.Pass()]
            else:
                del function.body[index]
        mutated = ast.unparse(ast.fix_missing_locations(tree))
        if mutated != source and mutated not in mutants:
            mutants.append(mutated)
    return mutants


def _run_harness(workdir, timeout_s=60):
    """Return {test_id: passed}; None when the whole suite fails to run."""
    # -B: mutants are same-length single-character edits written within the same
    # second, which defeats the pyc header's mtime+size invalidation check.
    try:
        proc = subprocess.run([sys.executable, "-B", "-c", HARNESS], cwd=workdir,
                              capture_output=True, text=True, timeout=timeout_s,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None


def _greedy_cover(kills_by_test, killable):
    cover = []
    uncovered = set(killable)
    while uncovered:
        best = max(sorted(kills_by_test),
                   key=lambda test: len(kills_by_test[test] & uncovered))
        gained = kills_by_test[best] & uncovered
        if not gained:
            break
        cover.append(best)
        uncovered -= gained
    return cover


def suite_metrics(work, production_file="cartlib/cart.py"):
    work = Path(work)
    source = (work / production_file).read_text()
    mutants = generate_mutants(source)

    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / "work"
        shutil.copytree(work, copy,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc",
                                                      ".claude", ".agents"))
        clean = _run_harness(copy) or {}
        passing = sorted(test for test, ok in clean.items() if ok)
        kills_by_test = {test: set() for test in passing}
        for index, mutant in enumerate(mutants):
            (copy / production_file).write_text(mutant)
            outcome = _run_harness(copy, timeout_s=30)
            for test in passing:
                if outcome is None or not outcome.get(test, False):
                    kills_by_test[test].add(index)
        (copy / production_file).write_text(source)

    killable = set().union(*kills_by_test.values()) if kills_by_test else set()
    cover = _greedy_cover(kills_by_test, killable)
    return {
        "tests_total": len(clean),
        "tests_passing": len(passing),
        "mutants": len(mutants),
        "killed": len(killable),
        "kill_rate": round(len(killable) / len(mutants), 3) if mutants else 0.0,
        "excess_tests": len(passing) - len(cover),
        "minimal_cover": sorted(cover),
        "redundant_tests": sorted(set(passing) - set(cover)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path, help="workspace containing the produced code")
    parser.add_argument("--production-file", default="cartlib/cart.py")
    args = parser.parse_args()
    print(json.dumps(suite_metrics(args.work, args.production_file), indent=2))


if __name__ == "__main__":
    main()
