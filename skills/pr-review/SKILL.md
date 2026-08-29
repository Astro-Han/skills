---
name: pr-review
description: "Perform a new evidence-backed review of one pull request or triage and review a PR queue, starting with whether each PR solves the stated problem. Use when asked to review, rereview, batch-review, or recommend Approve/Comment for proposed changes. Do not use to implement or respond to existing review feedback, report PR or CI status only, draft a PR, merge, or monitor checks."
---

# PR Review

A pull request proposes a solution to a problem. Decide whether it deserves to exist before deciding whether its code is correct. Remain read-only unless separately authorized.

## Anchor one exact head

Read repository and review rules. Use the host's PR API or CLI to capture:

- clickable PR and Issue links, titles, author, base, and exact head SHA;
- additions, deletions, changed files and paths;
- exact-head CI, mergeability, reviews, comments, and unresolved threads.

Separate facts, conclusions, and gaps; never mix heads.

## Prove the problem first

Ask first:

> What problem does this PR solve? How does it solve it? Is the problem defined correctly? Do the problem definition and solution follow first principles and Occam's razor?

Seek a report, reproduction, log, real failing check, or other observation independent of the patch. A new test proves neither demand nor prior failure. Classify the problem as **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**.

Map the Issue's setup, inputs, observed and expected results to PR coverage. A patch for another scenario is not a fix. Do not approve with value or scope unknown.

## Trace ownership and production composition

Explain the mechanism, natural owner, authoritative state, and composition boundary used by real producers. Follow production wiring, persistence, and lifecycle ownership rather than stopping at a changed helper or fixture.

Check whether the change:

- restores one invariant at its owner or adds parallel authority, mirrored state, synchronization, or another loop;
- extends an existing seam or adds another wrapper, state machine, compatibility path, or implementation;
- stays atomic across supported interruption, retry, concurrency, restart, and recovery;
- is tested through owned production composition. A detached fixture cannot prove an owned launcher, a helper cannot prove its caller, and an in-process test cannot prove a process-lifecycle race.

## Audit the whole diff for subtraction

Report total diff and production/test split. Identify a regression test that fails on old behavior through production composition, not matrices or bypassed fixtures.

> Is this the smallest complete solution? What low-value tests, code, wrappers, states, or old paths can disappear? Can the result converge on one owner without losing required behavior?

Judge net codebase cost, not line count: a process-level regression may be necessary, while a tiny duplicate authority may be too expensive.

## Report only reachable findings

Classify the triggering path first:

1. normal user or supported operational path;
2. reasonable failure, reconnect, concurrency, or recovery path;
3. attacker-controlled trust boundary;
4. contrived path requiring several unsupported premises.

A crash, killed process, disconnect, retry, race, partial write, restart, or recovery is category 2, never category 1. Category 4 is normally **No finding** unless it risks irreversible data loss, privilege breach, destruction of a core authority, or broad outage.

- **P0** — blocks release.
- **P1** — must be fixed before merge: reachable security, durable-state, data-loss, money, sustained-outage, or broadly unusable core-workflow failure.
- **P2** — bounded or recoverable wrong behavior, including user-visible state; normally non-blocking.
- **P3** — minor and deferrable, with no meaningful wrong outcome.

Each finding states its category, condition, consequence, evidence, location, and smallest correction. Merge duplicates by cause; say explicitly when none remain.

## Deliver the decision packet

Use this order:

1. **Facts** — copy exact clickable PR/Issue URLs, head SHA, numeric `+A/-D`, file count, production/test split, CI, mergeability, and review state.
2. **Problem** — evidence, truth classification, and scenario match.
3. **Solution and simplification** — mechanism, owner, authority, production composition, and removable surface.
4. **Findings** — P0–P3 or none.
5. **Recommendation** — begin with exactly one: **Approve**, **Comment**, **Wait**, or **Human confirmation required**; state any missing condition.

Facts must be the first substantive section; do not reveal the recommendation earlier. For UI or user-visible changes, use **Human confirmation required** until the manual acceptance path and current design primitives, including Astryx when authoritative, are verified.

When reviewing a queue, delegating independent angles, rereviewing, or preparing a public review, read [references/queue-and-publication.md](references/queue-and-publication.md) before acting.

Done means the packet proves value and scope at one exact head, traces production ownership, accounts for the diff, calibrates findings, and preserves project confirmation and human responsibility.
