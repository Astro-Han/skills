---
name: pr-review
description: "Perform a new evidence-backed review of one pull request or triage and review a PR queue, starting with whether each PR solves the stated problem. Use when asked to review, rereview, batch-review, or recommend Approve/Comment for proposed changes. Do not use to implement or respond to existing review feedback, report PR or CI status only, draft a PR, merge, or monitor checks."
---

# PR Review

A pull request is a proposed change to a real problem, not merely a diff. Decide whether the change deserves to exist before deciding whether its code is correct.

Review read-only unless the user separately authorizes an external action. Keep observed facts, supported conclusions, and evidence gaps distinct.

## Establish the review unit

Read the repository instructions and resolve the PR, its linked Issue or other problem statement, and the project's human-review rules. Capture one exact-head snapshot:

- PR and Issue links, titles, author, base, and exact head SHA;
- additions, deletions, changed-file count, and changed paths;
- CI checks for that SHA, mergeability, existing reviews and comments, and unresolved threads.

Use the host's PR API or CLI rather than search snippets. Treat absent or stale evidence as unknown. CI, reviews, and conclusions belong to one SHA; never combine them across heads. Initial fact gathering is complete when a reader can identify the proposal, stated problem, reviewed code, and known review state without opening another page.

## Prove the problem before reading the solution

Answer this compact checklist in the review:

> 这个 PR 解决了什么问题？这个 PR 如何解决这个问题？这个问题定义的对吗？解决方式和问题定义是否符合第一性原理，是否符合奥卡姆剃刀原理。

For the problem half, seek user reports, a reproducible scenario, logs, a real failing check, or another observation independent of the proposed patch. A test written in the PR proves neither demand nor prior failure. Classify the problem as **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**.

Map the Issue's setup, inputs, observed result, and expected result to what the PR actually covers. A clean patch for a different scenario is not a fix for the reported problem. State the mismatch before discussing code quality. Do not approve while material value or scope alignment remains unknown.

This step is complete when the report says what breaks, who or what observed it, and whether the PR covers that same reachable scenario.

## Trace the solution through production composition

Explain the mechanism in plain language, then identify the natural owner, authoritative state, and composition boundary that every real producer uses. Follow the production entry point through wiring, launchers, factories, dependency injection, persistence, and lifecycle ownership; do not stop at a helper or fixture named by the diff.

Check whether the change:

- restores one invariant at its owner or creates a second authority, mirrored state, synchronization rule, or loop;
- extends an existing seam or adds a parallel implementation, wrapper, state machine, or compatibility path;
- is atomic across interruption, retry, concurrency, restart, and recovery where those are supported paths;
- exercises the owned production composition. A detached fixture cannot prove an owned launcher, a helper test cannot prove its caller, and an in-process test cannot prove a process-lifecycle race.

Prefer the smallest coherent end state that covers all current producers. Existing complexity is evidence to investigate, not a reason to add more.

## Audit the whole diff for subtraction

Quantify production and test changes separately. Name the regression test that fails on the real old behavior and passes through the production seam. Distinguish it from low-value matrices that only enumerate defensive shapes, restate implementation, or exercise a fixture the product bypasses.

Use this second checklist without turning it into a questionnaire:

> 针对要解决的问题，本次的所有改动已经是最优解了吗？是否符合第一性原理，是否符合奥卡姆剃刀？是否有可以删除的低质量测试，有可以删除的代码？是否可以重构为最优解？

Account for removable code, tests, wrappers, states, representations, and superseded paths. Judge net codebase cost, not raw line count: a larger process-level regression may be necessary, while a small duplicate authority may be too expensive. The audit is complete when every substantial diff region either carries necessary behavior/evidence or has a concrete deletion or consolidation suggestion.

## Report only reachable findings

Classify the triggering path before assigning severity:

1. normal user path;
2. reasonable failure, reconnect, concurrency, or recovery path;
3. attacker-controlled trust boundary;
4. contrived path requiring several unsupported premises.

A deliberate everyday product action is category 1. A crash, killed process, disconnect, retry,
race, partial write, restart, or recovery is category 2 even when it occurs during an otherwise
normal workflow. Do not collapse those two labels.

Category 4 is normally **No finding**. Report it only for irreversible data loss, privilege or trust-boundary breach, destruction of a core authority, or broad outage. Severity follows actual reach, consequence, scope, and recoverability—not a theoretical worst case or a security-sounding label.

- **P0** — blocks release: the shipped version cannot responsibly go out.
- **P1** — must be fixed before merge: a reachable merge-blocking correctness, security, durable-state, data-loss, money-movement, sustained-outage, or broadly unusable core-workflow failure.
- **P2** — should be fixed but normally does not block: bounded or recoverable incorrect behavior without those consequences.
- **P3** — minor; may be deferred or left unchanged.

Each finding must name its path category, exact condition, consequence, evidence or reproduction, location, and smallest actionable correction. Merge duplicates by root cause. If no real gap remains, say explicitly that no findings were found.

## Deliver a decision packet

For each PR, report in this order:

1. **Facts** — clickable PR and Issue links, exact head, total `+additions/-deletions`, changed-file count, production/test split, CI, mergeability, and unresolved review state;
2. **Problem** — what is demonstrated, its evidence, and whether the Issue and PR scenarios match;
3. **Solution and simplification** — mechanism, owner, authority, production composition, and removable diff surface;
4. **Findings** — ordered P0–P3, or an explicit statement that none were found;
5. **Recommendation** — **Approve**, **Comment**, **Wait**, or **Human confirmation required**, with the missing condition stated.

The first substantive section must be Facts. Do not mention or imply the action recommendation
before the final section; labels such as “review conclusion” also violate this order. Never lead
with approval. UI, UX, visual, or user-visible interaction changes require an explicit manual acceptance path and a check against the project's current design primitives, including Astryx when it is that project's authority; recommend human confirmation before any public review or approval.

When reviewing a queue, delegating independent angles, rereviewing, or preparing a public review, read [references/queue-and-publication.md](references/queue-and-publication.md) before acting.

Done means the decision packet identifies the exact reviewed head, establishes whether the stated problem is real and matched, traces the solution through production ownership, accounts for the full diff, reports only calibrated reachable findings, and leaves every external action behind the host project's confirmation and human-responsibility boundary.
