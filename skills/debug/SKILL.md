---
name: debug
description: "Diagnose and fix bugs, failures, and performance regressions. Read this skill BEFORE touching any code whenever the user reports a bug, broken behavior, a crash, wrong output, or a regression — even when the cause looks obvious and the user only asked for a fix. Do not use for a simple explanation of a known error when no diagnosis is requested."
---

# Debug

A bug is solved only when the original symptom is captured, the cause is supported by discriminating evidence, and the original scenario verifies the result.

## Establish the signal

Read the relevant code, tests, project guidance, and available artifacts. Build the smallest practical feedback loop that distinguishes failure from success: a test, command, request, replay, trace, benchmark, or bounded manual check.

The signal should exercise the real path, be repeatable enough to guide decisions, and run cheaply enough to use after each meaningful change. For intermittent failures, measure a bounded reproduction rate. For performance regressions, record a baseline before changing code.

When the exact environment is unavailable, use the strongest available evidence at the nearest controllable boundary. State what remains unverified; do not turn static plausibility into proven root cause.

## Isolate the cause

Reproduce or observe the symptom, then remove irrelevant inputs and steps. Form falsifiable explanations and run the cheapest probe that distinguishes them. Change one variable at a time.

Claim a root cause only when evidence connects the suspected condition to the observed failure. Prefer toggling the suspected condition or comparing known-good and failing states. Error suppression, retries, disabled features, and changed expectations are not causal proof by themselves.

State the cause plainly: what breaks, under which condition, and why that condition produces the symptom.

## Report or fix

For diagnosis-only requests, report the cause, decisive evidence, location, and remaining uncertainty, then stop.

For a requested fix:

1. Preserve the failing signal as a regression test when a trustworthy seam exists; otherwise say so rather than adding a misleading test.
2. Apply the smallest change that removes the supported cause without changing unrelated behavior.
3. Run the regression test or nearest trustworthy check, related tests, and the original scenario.

If the original symptom survives, reassess the diagnosis instead of stacking another speculative patch.

## Finish

Remove temporary instrumentation and artifacts created for the diagnosis. Report what broke, the evidence that isolated it, what changed if anything, and how the original symptom was checked.
