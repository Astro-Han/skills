---
name: tdd
description: "Use test-driven development when requested, or when a clear behavior change has a trustworthy automated seam and test-first feedback is worth its cost. Do not trigger merely for code edits, pure refactors, visual tweaks, configuration, or exploratory work."
---

# TDD

## Choose the signal

Inspect the existing tests and public contract; use the cheapest trustworthy boundary that exercises the real behavior.
For a defect already captured by an existing test, add no tests or parameter rows; fix production code and only delete invalid or redundant tests. Otherwise extend an existing case before adding one for a worthwhile gap.
Count parameter rows, fixtures, environment startup, and CI work as test cost, not just test functions.
If no trustworthy automated signal exists, use the nearest reliable check and state the gap; do not manufacture a test seam.

## RED → GREEN → REFACTOR

1. **RED:** Express one valuable behavior and observe failure for the predicted reason before changing production code; an existing failing test already supplies RED.
2. **GREEN:** Make the smallest production change that passes, then run affected checks.
3. **REFACTOR:** Simplify implementation and tests while preserving behavior, then choose the next needed behavior.

Do not write a batch of tests followed by a batch of implementation.

If a behavior already passes, verify it without undoing working code to manufacture RED.

If explicitly using this skill for a pure refactor, start from passing checks; add a characterization test only for a worthwhile unprotected behavior, never an invented RED.

## Keep the signal honest

Expected results come from the contract, not a copy of the implementation; assertions must reject broken behavior and survive harmless internal changes.
Reject implementation-detail checks, internal mocks, unconsumed snapshots, and weak type/nonempty assertions that do not prove the contract; a new helper does not earn its own test.

## Finish

Map tests to valuable obligations and leave one representative per obligation; delete duplicate cases, parameter rows, and subsumed stepping-stone tests, then rerun affected checks.
Report retained obligations and any protection deliberately dropped.
