---
name: pr-review
description: "Review a pull request or PR queue from problem value through code correctness. Use for new review, rereview, batch review, or an Approve/Comment/Wait decision. Do not use to implement or respond to feedback, report status, draft or merge, or monitor checks."
---

# PR Review

First decide if the problem is real and the PR is needed. Stay read-only unless authorized.

## Identify the reviewed change

Read repository rules. Require a reviewable change and its scope. Prefer the exact head SHA; otherwise identify the patch, snapshot, or checkout and say it may not match the current PR.

Gather available PR/Issue links, `+A/-D`, files, production/test split, CI, mergeability, and review state. Never invent them. Name gaps; missing facts do not block analysis. Never mix versions.

## Check the problem first

Ask first:

> What problem does this PR solve? How does it solve it? Is the problem defined correctly? Do the problem definition and solution follow first principles and Occam's razor?

Seek a report, reproduction, log, or failing check. An Issue helps but is optional; use the PR description or other evidence. A new test proves neither demand nor prior failure. Call the problem **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**. Compare the reported scenario and expected result with PR coverage. Do not approve a different scenario or unknown value.

## Follow the real code path

Explain how it works, where the rule and source of truth belong, and how production calls them. Trace beyond helpers and fixtures. Check whether it:

- fixes the rule at one owner or adds copied state, synchronization, another loop, or a second source of truth;
- uses an existing extension point or adds another implementation, wrapper, state machine, or compatibility path;
- stays correct through supported interruption, retry, concurrency, restart, and recovery;
- tests the real path: fixtures do not prove launchers, helpers do not prove callers, and in-process tests do not prove process races.

## Simplify the change

For each substantial change, say why it is needed or remove it. Cover code, tests, owners, stored state, synchronization, paths, contracts, and wrappers. Regression tests must fail on old behavior through the real path, not a bypassed fixture or low-value matrix. Before Approve, every addition must be necessary, correctly owned, and part of the smallest complete solution. Preserve live obligations until evidence proves they ended.

> Is this the smallest complete solution? What low-value tests, code, wrappers, states, or old paths can disappear? Can the result converge on one owner without losing required behavior?

Judge concepts, not lines; process tests can matter more than large fixture matrices.

## Report only real findings

Before P0–P3, show a supported entry reaching an observable consequence through production checks. If a link is unproven or blocked, record an evidence gap or **No finding**.

Classify the path:

1. normal user or supported operation;
2. reasonable failure, reconnect, concurrency, or recovery;
3. attacker-controlled input or trust boundary;
4. several unsupported premises combined.

Category 4 is normally **No finding**, except for irreversible data loss, privilege breach, loss of a core source of truth, or broad outage. Grade reachable impact and recovery, not the worst imaginable result. Low probability does not erase proof; possibility is not proof.

- **P0** — blocks release.
- **P1** — must be fixed before merge: reachable security exposure, data loss, money movement, sustained outage, wrong committed state, or unusable core workflow.
- **P2** — bounded or recoverable wrong behavior; normally non-blocking.
- **P3** — minor or avoidable complexity with no meaningful wrong outcome.

Give each finding's category, trigger, consequence, evidence, location, and smallest fix. Merge duplicates; report none.

## Give the decision

Use this order:

1. **Facts** — reviewed content, PR/Issue links and head, numeric `+A/-D`, production/test split, live facts, and gaps.
2. **Problem** — evidence, truth classification, and scenario match.
3. **Solution** — how it works, who owns it, the production path, what is needed, and what can be removed.
4. **Findings** — P0–P3 or none.
5. **Recommendation** — end with exactly one: **Approve**, **Comment**, or **Wait**; state the missing condition.

Start with Facts. **Approve** requires proof that the reviewed content is current. Without it, finish the review but use **Wait** for a current-PR decision. Other gaps limit only dependent conclusions. For user-visible changes, name remaining manual checks, including Astryx primitives when standard.

For a queue, delegation, rereview, or public review, read [references/queue-and-publication.md](references/queue-and-publication.md) first.

Done means the review states its evidence boundary, judges value, follows code, accounts for changes and removals, and calibrates findings.
