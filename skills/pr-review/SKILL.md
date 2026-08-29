---
name: pr-review
description: "Review one pull request or a PR queue from problem value through code correctness. Use for a new review, rereview, batch review, or Approve/Comment recommendation. Do not use to implement or respond to feedback, report status only, draft or merge a PR, or monitor checks."
---

# PR Review

Judge whether the proposed solution deserves to exist before checking its code. Remain read-only unless authorized.

## Anchor one exact head

Read repository and review rules. Capture:

- clickable PR and Issue links, titles, author, base, and exact head SHA;
- additions, deletions, changed files and paths;
- exact-head CI, mergeability, reviews, comments, and unresolved threads.

Separate facts, conclusions, and gaps; never mix heads.

## Prove the problem first

Ask first:

> What problem does this PR solve? How does it solve it? Is the problem defined correctly? Do the problem definition and solution follow first principles and Occam's razor?

Seek evidence independent of the patch: a report, reproduction, log, or real failing check. A new test proves neither demand nor prior failure. Classify the problem as **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**.

Map the Issue's setup, inputs, observed and expected results to PR coverage. Another scenario is not a fix. Do not approve with value or scope unknown.

## Trace ownership and production composition

Explain the mechanism, natural owner, authoritative state, and real composition boundary. Follow production wiring, persistence, and lifecycle ownership beyond changed helpers or fixtures.

Check whether the change:

- restores one invariant at its owner or adds parallel authority, mirrored state, synchronization, or another loop;
- extends an existing seam or adds another wrapper, state machine, compatibility path, or implementation;
- stays atomic across supported interruption, retry, concurrency, restart, and recovery;
- is tested through owned production composition: fixtures do not prove launchers, helpers do not prove callers, and in-process tests do not prove process races.

## Minimize coherent entropy

Report total diff and production/test split. Account for every substantial region as necessary behavior, necessary evidence, or removable surface. A regression test must fail on old behavior through production composition, not a bypassed fixture or low-value matrix.

In the decision packet, use an **Entropy delta** subsection to state owners, authorities, durable states, synchronization rules, lifecycle paths, contracts, representations, wrappers, and tests added or removed. Before Approve, prove each addition is required, correctly owned, and part of the smallest coherent solution; avoidable additions are review gaps. Preserve live obligations until evidence proves they ended.

> Is this the smallest complete solution? What low-value tests, code, wrappers, states, or old paths can disappear? Can the result converge on one owner without losing required behavior?

Judge concepts, not lines: a necessary process regression can outweigh a tiny duplicate authority.

## Report only reachable findings

Classify the triggering path first:

1. normal user or supported operational path;
2. reasonable failure, reconnect, concurrency, or recovery path;
3. attacker-controlled trust boundary;
4. contrived path requiring several unsupported premises.

Crashes, disconnects, retries, races, partial writes, restarts, and recovery are category 2. Category 4 is normally **No finding** unless it risks irreversible data loss, privilege breach, core-authority destruction, or broad outage.

- **P0** — blocks release.
- **P1** — must be fixed before merge: reachable security, durable-state, data-loss, money, sustained-outage, or broadly unusable core-workflow failure.
- **P2** — bounded or recoverable wrong behavior, including user-visible state; normally non-blocking.
- **P3** — minor and deferrable, with no meaningful wrong outcome.

Avoidable complexity without a wrong outcome is P3 unless project policy makes it blocking.

Each finding states its category, condition, consequence, evidence, location, and smallest correction. Merge duplicates by cause; state when none remain.

## Deliver the decision packet

Use this order:

1. **Facts** — copy exact clickable PR/Issue URLs, head SHA, numeric `+A/-D`, file count, production/test split, CI, mergeability, and review state.
2. **Problem** — evidence, truth classification, and scenario match.
3. **Solution and entropy delta** — mechanism, owner, production composition, necessary additions, and removable surface.
4. **Findings** — P0–P3 or none.
5. **Recommendation** — begin with exactly one: **Approve**, **Comment**, **Wait**, or **Human confirmation required**; state any missing condition.

Facts come first; never reveal the recommendation earlier. For user-visible changes, use **Human confirmation required** until the manual acceptance path and current design primitives, including Astryx when authoritative, are verified.

For a queue, delegation, rereview, or public review, read [references/queue-and-publication.md](references/queue-and-publication.md) first.

Done means the packet proves value and scope at one exact head, traces production ownership, accounts for every diff region and avoidable concept, calibrates findings, and preserves human responsibility.
