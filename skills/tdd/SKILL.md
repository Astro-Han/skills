---
name: tdd
description: "Test-driven development for production behavior. Use whenever implementing a feature, fixing a bug, or otherwise changing observable production behavior, and before refactoring to establish or verify a green safety net. Do not use for docs-only changes, test-only maintenance, generated artifacts, or exploratory prototypes unless the user asks for TDD."
---

# TDD

Work in vertical slices: one test → one minimal implementation → refactor while green → repeat.

## Before RED

Inspect existing tests, public interfaces, and project conventions. Choose the narrowest trustworthy seam yourself; do not ask the user to approve the test layer. A seam is the public boundary where behavior can be driven and observed, such as a function, API, CLI, UI interaction, or service interface.

Not every change earns a test. If no fast, reliable test can exercise the behavior through a stable seam, or the only test available would fail the value gate below, use the nearest trustworthy validation instead, say that the work was not TDD, and name the behavior left unverified.

## The loop

1. **RED** — Write one test for the next observable behavior. Run it and confirm it fails for the predicted reason, not a typo, missing import, or unrelated path.
2. **GREEN** — Write only enough production code to pass that test. Run it, then run the nearest related tests.
3. **REFACTOR** — Improve names, structure, and duplication without changing behavior. Keep tests green throughout.

Then choose the next behavior and repeat. Do not write a batch of tests followed by a batch of implementation.

Bug fixes require a failing regression test that reproduces the original symptom before the fix.

## Pure refactors

Start from a green safety net. If existing tests do not protect the behavior being preserved, add a characterization test and watch it pass before refactoring. Do not invent a failing behavior test for a behavior-preserving change.

An extracted helper does not earn a test of its own; the behavior test that already covers it is the safety net. A process rule demanding a test per function does not change this. Say that the helper is covered through the existing seam, and never widen the public API to satisfy such a rule.

## Test quality

Tests specify observable behavior through public interfaces and survive internal refactors. Expected values come from an independent source of truth, not a reimplementation of the production logic.

Keep a test only if breaking the behavior it names would make it fail, and renaming internals would not. A test that survives broken behavior reports coverage that does not exist; delete it and record the behavior as unverified instead. Coverage targets and review pressure do not lower this bar.

Refuse these shapes as well. Never write them, and delete the ones already covering the code you touch:

- an expectation recomputed from the production algorithm, or read back from the production constant it exists to pin
- a mocked internal collaborator, or an assertion on call count or order where the call is not itself the contract
- an assertion on literal text, log output, or a snapshot that no caller, user, or published format depends on
- a test reaching into private methods or internal state to observe what the public seam already exposes
- an assertion so weak it holds for broken output, such as a type, a length, or a non-empty check

Reading the existing tests is already part of Before RED; deleting the ones that fail the gate is part of finishing the change.

TDD may use unit, integration, contract, or UI tests. Choose the fastest level that exercises the real contract with acceptable fidelity. Mock only at system boundaries you do not control.

Read [tests.md](tests.md) when designing assertions or diagnosing brittle tests. Read [mocking.md](mocking.md) when a test needs doubles, dependency injection, a database, time, randomness, filesystem access, or an external service.
