---
name: pr-review
description: "Review a pull request or PR queue from problem value through code correctness. Use for new review, rereview, batch review, or an Approve/Comment/Wait decision. Do not use to implement or respond to feedback, report status, draft or merge, or monitor checks."
---

# PR Review

First decide whether the problem is real and the PR is needed. Remain read-only unless authorized.

## Review one exact head

Read repository rules. Record clickable PR and Issue links, titles, author, base, exact head SHA, `+A/-D`, changed files, production/test split, exact-head CI, mergeability, reviews, comments, and unresolved threads. Keep facts, conclusions, and gaps separate; never mix heads.

## Check the problem first

Ask first:

> What problem does this PR solve? How does it solve it? Is the problem defined correctly? Do the problem definition and solution follow first principles and Occam's razor?

Look outside the patch for a report, reproduction, log, or failing check. A new test proves neither demand nor prior failure. Call the problem **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**. Compare the Issue's setup, inputs, observed and expected results with PR coverage. A different scenario is not a fix. Do not approve unknown value or scope.

## Follow the real code path

Explain how the change works, where the rule and source of truth belong, and how production calls them. Trace past changed helpers and fixtures. Check whether the PR:

- fixes the rule at one owner or adds copied state, synchronization, another loop, or a second source of truth;
- uses an existing extension point or adds another implementation, wrapper, state machine, or compatibility path;
- stays correct through supported interruption, retry, concurrency, restart, and recovery;
- tests the real path: fixtures do not prove launchers, helpers do not prove callers, and in-process tests do not prove process races.

## Simplify the change

For each substantial change, say why it is needed or what can be removed. Cover code, tests, owners, sources of truth, stored state, synchronization, paths, contracts, representations, and wrappers. A regression test must fail on old behavior through the real path, not a bypassed fixture or low-value matrix. Before Approve, every addition must be necessary, correctly owned, and part of the smallest complete solution. Preserve live obligations until evidence proves they ended.

> Is this the smallest complete solution? What low-value tests, code, wrappers, states, or old paths can disappear? Can the result converge on one owner without losing required behavior?

Judge concepts, not lines. A process test can be necessary; a large fixture matrix may not be.

## Report only real findings

Before P0–P3, show the concrete path from a supported entry through production checks to an observable consequence. If a link is unproven or a guard blocks it, record an evidence gap or **No finding**.

Classify the path:

1. normal user or supported operation;
2. reasonable failure, reconnect, concurrency, or recovery;
3. attacker-controlled input or trust boundary;
4. several unsupported premises combined.

Category 4 is normally **No finding**, except for irreversible data loss, privilege breach, loss of a core source of truth, or broad outage. Grade the reachable consequence and its recoverability, never the worst imaginable result. Low probability does not erase proof; possibility is not proof.

- **P0** — blocks release.
- **P1** — must be fixed before merge: reachable security exposure, data loss, money movement, sustained outage, wrong committed state, or a broadly unusable core workflow.
- **P2** — bounded or recoverable wrong behavior; normally non-blocking.
- **P3** — minor or avoidable complexity with no meaningful wrong outcome.

For each finding, give its category, trigger, consequence, evidence, location, and smallest correction. Merge duplicates; say when none remain.

## Give the decision

Use this order:

1. **Facts** — PR/Issue links, head, diff, CI, mergeability, and review state.
2. **Problem** — evidence, truth classification, and scenario match.
3. **Solution** — how it works, who owns it, the production path, what is needed, and what can be removed.
4. **Findings** — P0–P3 or none.
5. **Recommendation** — begin with exactly one: **Approve**, **Comment**, or **Wait**; state the missing condition.

Facts come first. For user-visible changes, use **Wait** and name the remaining manual checks, including Astryx primitives when they are the project standard.

For a queue, delegation, rereview, or public review, read [references/queue-and-publication.md](references/queue-and-publication.md) first.

Done means the review proves value and scope at one head, follows real code, accounts for substantial changes and removals, calibrates findings, and preserves human responsibility.
