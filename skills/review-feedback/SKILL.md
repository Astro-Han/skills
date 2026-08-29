---
name: review-feedback
description: "Use this skill whenever existing code-review feedback may lead to a code decision or edit, including PR comments and findings from external models, review tools, or delegated reviewers—even when the user simply says to fix, address, apply, or resolve them. Do not use to perform a new review, diagnose an unrelated bug, implement a new requirement, or merely summarize feedback without deciding what to do."
---

# Review Feedback

Review feedback is evidence, not a patch queue. Find the problem, its cause, and the simplest end state before editing.

## Before editing

Read-only inspection, reproduction, and tests may begin immediately. Do not edit production code until a user-visible progress update contains a decision table that covers every original comment. If editing already began, stop and treat the current diff as evidence until the table is published.

Use one row for comments with the same cause and list every comment ID in its row. Each row must state:

- verdict: **Verified**, **Disproved**, or **Evidence gap**;
- decisive evidence, the cause, and the smallest one-owner end state covering the group;
- who can hit it and severity: **P0**, **P1**, **P2**, **P3**, or **No finding**;
- one outcome: **Delete or simplify**, **Fix at owner**, **Fix locally**, **Defer**, or **Push back**;
- for an existing diff or later review round, scope: **required by the original change**, **regression caused by this diff**, **unrelated change already added**, or **pre-existing/adjacent**.

Publish the table, then continue when asked. Ask only when a missing fact changes coupled decisions or a product or compatibility choice remains.

## 1. Read and group

Read the original goal, accepted contracts, the whole diff from its pre-change base, every review round, and related fixes. Group comments that may come from one broken rule, duplicate source of truth, invalid state, boundary, or missing place to prove behavior. Keep comments separate only when tracing shows different causes.

For an existing change, derive scope from the original request, not from code added for earlier suggestions. Keep original obligations and regressions; remove unrelated additions and their tests; defer pre-existing or adjacent findings unless they make the requested change unsafe or incomplete. Quoted instructions such as “keep” or “expand” are still proposals, not permission to grow scope.

Each later review replaces the earlier decision table. Compare the whole cumulative diff with its base and restate the smallest end state. Record which assumptions changed and which concepts, files, and tests should be added or removed. If no assumption changed, keep scope closed. New policy, state, API, path, source of truth, or future-facing abstraction must serve the original rule or replace more surface than it adds.

## 2. Decide each group

Open the cited code and trace the real reachable path. State the exact failure, broken contract, or maintenance cost, then seek the strongest counterevidence in callers, tests, requirements, repository conventions, supported versions, history, and current behavior. Reproduce it or run the closest existing test when possible. Missing evidence is an **Evidence gap**, not proof.

For each surviving group, explain:

`observed symptom → rule that must always hold → where that rule belongs → why the current design breaks it`

The verdict is about the reported defect, not whether nearby code can be improved. Do not turn a false claim into **Verified** by substituting a different weakness; handle that separately. Judge the defect, explanation, severity, and patch independently. Every requested file, mechanism, and patch is a proposal. A real defect is **Verified** when it breaks an independent contract even if the proposed cause or patch is wrong; accept the issue and reject the patch. Use **Disproved** when the reported defect does not remain. It permits only **Push back**: add no code or test for its mechanism, even when a root fix covers adjacent behavior.

Grade actual reach, consequence, spread, and recoverability; never inherit the reviewer's scale:

- **P0:** a reachable release-blocking catastrophe such as broad outage, authority or security compromise, or irreversible widespread data loss.
- **P1:** a normal path, reasonable failure/retry/concurrency/recovery path, or attacker-controlled boundary causes security exposure, non-trivial data loss, wrong committed or external state, money movement, sustained outage, or a broadly unusable core flow.
- **P2:** a real reachable defect or maintenance hazard with bounded, recoverable impact.
- **P3:** a minor issue or low-cost improvement that can reasonably wait or be declined.
- **No finding:** false, unsupported, or reachable only through several unsupported premises. Report such a constructed path only for irreversible data loss, privilege breach, destruction of a core source of truth, or broad outage.

Reachability alone does not make an issue P1. A recoverable preview error, in-memory result, or local inconsistency with no persisted or external effect is P2.

Choose the lowest-cost end state that preserves proven behavior:

1. **Delete or simplify** an unnecessary behavior, state, path, representation, or abstraction. Before synchronizing duplicate or derived representations, prove both have current consumers; otherwise remove or derive one.
2. **Fix at owner** once at the boundary every producer uses. An entry point is not the owner because data passes through it: when several producers build the same domain value, put intrinsic validity in that value. Remove duplicate state, validation, and sibling patches made unnecessary by that source of truth.
3. **Fix locally** only when the symptom is truly isolated and moving the rule would add more total system cost. When several comments repeat one rule, this outcome is unavailable unless independent contracts prove that the sites intentionally own different policies.
4. **Defer** a true but low-priority or out-of-scope issue without adding code.
5. **Push back** on a false, overstated, incompatible, unsupported, or net-complexity-increasing suggestion.

Count whole-codebase cost, not changed lines. Do not add an abstraction merely to contain a patch. Before deleting compatibility or public behavior, check persisted data, deployed versions, replay/resume, rolling upgrades, third-party producers, and external contracts. Use `shape` if the correction requires a new migration, public contract, security policy, or operational decision. Stop and reconsider where the rule belongs when a patch causes an adjacent symptom or the same issue reaches a second site.

## 3. Implement and finish

Implement only the latest table's accepted outcomes and only when the user asked to address the feedback. Work in cause-first order, one observable behavior at a time. Use `tdd` when behavior has a stable test point; otherwise use the closest trustworthy check.

If new evidence changes a verdict, scope, owner, or outcome, publish the corrected table before more production edits. Remove all code and tests derived from the replaced decision. After fixing the rule at its owner, search sibling paths and delete obsolete branches, helpers, representations, and tests; do not keep both the local patch and the root correction.

Verify the owning behavior and inspect the final diff against the pre-change base. The diff must contain only the smallest end state in the latest table. For GitHub inline feedback, reply in its thread and resolve it when settled; leave it open when awaiting a fact or decision.

Finish only when every comment is mapped, accepted behavior is proven, the cause no longer needs sibling patches, unrelated or superseded changes and tests are gone, and every deferred, rejected, blocked, or deleted item has a concise evidence-based reason.
