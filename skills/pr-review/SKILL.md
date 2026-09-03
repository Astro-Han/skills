---
name: pr-review
description: "Review a pull request or queue from problem value through code correctness. Use for new review, rereview, batch review, or deciding findings and next steps. Do not use to implement feedback, report status, draft, merge, or monitor checks."
---

# PR Review

Answer a fixed chain of questions in order, with evidence. Stay read-only unless authorized.

## Pin down what you are reviewing

Read repository rules. Identify what is under review — the exact head SHA, or a provided patch or snapshot — and state any mismatch with the live PR. Gather PR/Issue links, `+A/-D`, files, the production/test split, CI, mergeability, and review state. Never mix versions. Name missing facts; gaps do not block analysis.

## What problem does this PR solve, and is it real?

State, in the PR's own terms, what problem it solves and how. Then check the problem is real: seek a report, reproduction, log, or failing check — an Issue is optional, and a new test proves neither demand nor prior failure. Classify the problem **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**, and confirm the PR covers the reported scenario rather than a different one.

## Is the problem defined correctly, and is this the right solution?

Judge both from first principles: does the change fix the cause at the code that owns it, or patch around it with copied state, another loop, a second source of truth, or a compatibility path? Follow the real production path — the shortest supported route that could prove the fix wrong — and compare old and new behavior where producer meets consumer:

- fixtures do not prove launchers, helpers do not prove callers, and in-process tests do not prove process races;
- supported callers and later use of changed data must survive failure, retry, concurrency, restart, and recovery;
- prefer an existing extension point over a new implementation, wrapper, or state machine.

## Is this the smallest complete solution?

Sketch the smallest change that meets the issue's stated acceptance, then ablate the PR against it: for each mechanism the PR adds beyond that shape — module, state, authority, API, wrapper, test matrix — remove it mentally and check whether the acceptance still holds. What survives ablation is the solution; the rest is excess.

A merged PR should lower the codebase's entropy, or at least not raise it. Flag parallel implementations, duplicated authorities, mirrored state, and machinery with no demonstrated demand. A PR many times larger than the smallest shape meeting its own acceptance is a finding, not a style remark.

Ask what can be deleted: low-value tests, dead paths, unneeded wrappers. Regression tests must fail on old behavior through the production owner, not a bypassed fixture; prefer the fewest tests proving distinct obligations. Preserve live obligations — persisted data, deployed versions, rolling upgrades, external callers — until evidence proves they ended.

## Findings — P0–P3

Before grading, show a supported entry reaching an observable consequence. Classify the triggering path:

1. normal or supported operation;
2. reasonable failure, reconnect, concurrency, or recovery;
3. attacker-controlled input or trust boundary;
4. several unsupported premises together.

Category 4 is normally **No finding**, except for irreversible data loss, privilege breach, loss of a core source of truth, or broad outage. Grade reachable impact and recovery; low probability does not erase proof, and possibility is not proof.

- **P0** — blocks release.
- **P1** — fix before merge: reachable security exposure, data loss, money movement, sustained outage, wrong committed state, an unusable core workflow — or a solution far larger than the smallest shape meeting the same acceptance, when the excess adds standing authorities, paths, or state.
- **P2** — bounded or recoverable wrong behavior; usually non-blocking.
- **P3** — minor complexity without meaningful wrong behavior.

Give each finding's path category, trigger, consequence, evidence, location, and smallest fix. Merge duplicates; report none when none survive.

## Report

Use this order: **Facts** — content, links, head, numeric `+A/-D`, production/test split, gaps; **Problem** — evidence and classification; **Solution** — real path, smallest shape, what can be removed; **Findings** — P0–P3 or none; **Next step** — what should happen and why. Never label the conclusion Approve, Comment, or Wait; keep pending CI, stale heads, human approval, and manual acceptance under Next step. If the reviewed content is a snapshot, require a refresh before anyone acts; never call it approvable. For user-visible changes, name the manual checks a human must run.

For a queue, delegation, rereview, or public review, read [references/queue-and-publication.md](references/queue-and-publication.md) first.
