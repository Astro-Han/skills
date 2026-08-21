---
name: tdd
description: "Test-driven development for production behavior. Use whenever implementing a feature, fixing a bug, or changing observable production behavior that can be exercised by a fast, reliable automated test through a stable public seam. Also use before refactoring to establish or verify a green safety net. Do not use for docs-only changes, test-only maintenance, generated artifacts, or exploratory prototypes unless the user asks for TDD."
---

# TDD

Work in vertical slices: one test → one minimal implementation → refactor while green → repeat.

## Before RED

Inspect existing tests, public interfaces, project conventions, and relevant ADRs or `CONTEXT.md`. Choose the narrowest trustworthy seam yourself; do not ask the user to approve the test layer. A seam is the public boundary where behavior can be driven and observed, such as a function, API, CLI, UI interaction, or service interface.

If no fast, reliable test can exercise the behavior through a stable seam, use the nearest trustworthy validation instead and say that the work was not TDD.

## The loop

1. **RED** — Write one test for the next observable behavior. Run it and confirm it fails for the predicted reason, not a typo, missing import, or unrelated path.
2. **GREEN** — Write only enough production code to pass that test. Run it, then run the nearest related tests.
3. **REFACTOR** — Improve names, structure, and duplication without changing behavior. Keep tests green throughout.

Then choose the next behavior and repeat. Do not write a batch of tests followed by a batch of implementation.

Bug fixes require a failing regression test that reproduces the original symptom before the fix.

## Pure refactors

Start from a green safety net. If existing tests do not protect the behavior being preserved, add a characterization test and watch it pass before refactoring. Do not invent a failing behavior test for a behavior-preserving change.

## Test quality

Tests specify observable behavior through public interfaces and survive internal refactors. Expected values come from an independent source of truth, not a reimplementation of the production logic.

TDD may use unit, integration, contract, or UI tests. Choose the fastest level that exercises the real contract with acceptable fidelity. Mock only at system boundaries you do not control.

Read [tests.md](tests.md) when designing assertions or diagnosing brittle tests. Read [mocking.md](mocking.md) when a test needs doubles, dependency injection, a database, time, randomness, filesystem access, or an external service.

## Done

- Saw RED fail for the predicted reason.
- Watched the minimum implementation turn it GREEN.
- Ran the nearest related tests.
- Kept the suite green through refactoring.
