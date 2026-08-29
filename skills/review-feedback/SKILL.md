---
name: review-feedback
description: "Use this skill whenever existing code-review feedback may lead to a code decision or edit, including PR comments and findings from external models, review tools, or delegated reviewers—even when the user simply says to fix, address, apply, or resolve them. Do not use to perform a new review, diagnose an unrelated bug, implement a new requirement, or merely summarize feedback without deciding what to do."
---

# Review Feedback

Review feedback is evidence about one system, not a patch queue. Determine whether the reported problem is real, find why the system permits it, and choose the lowest-cost system state before editing.

## Hold the edit gate

Read-only inspection, reproduction, and tests may begin immediately. Do not edit production code until the next user-visible progress update contains a decision ledger covering every review comment. If you have already started editing, stop, inspect the diff as evidence only, and complete the ledger before continuing.

The ledger may group comments with one cause, but it must map every original comment to a group. For each group state:

- verdict: **Verified**, **Disproved**, or **Evidence gap**;
- reach: **normal user path**, **reasonable failure/retry/concurrency/recovery path**, **attacker-controlled trust boundary**, or **contrived unsupported path**;
- severity: **P0**, **P1**, **P2**, **P3**, or **No finding**;
- decisive evidence;
- root cause, violated invariant, and natural owner;
- outcome: **Delete or simplify**, **Fix at owner**, **Fix locally**, **Defer**, or **Push back**.

Use only P0–P3 for findings; do not invent parallel scales such as F1/F2. Publishing the ledger is the gate, not a request for approval: when the user already asked for fixes, continue with accepted actions unless a material choice requires `shape`.

## Model the whole review

Read all feedback, the intended change, earlier review rounds, and related fixes. Group comments that may be symptoms of the same invariant, authority, boundary, duplicated rule, invalid state, or missing verification seam. Treat a comment as isolated only when tracing shows no shared cause.

If an unclear item changes how coupled items should be handled, ask one precise question and wait. Otherwise continue evaluating independent items.

Done: every comment belongs to a causal group or is demonstrably isolated.

## Verify and find the cause

Open the cited code and trace the real reachable path. State the concrete failure, contract violation, or maintenance consequence predicted by the comment, then seek the strongest counterevidence in callers, tests, requirements, repository conventions, target versions, history, and current behavior. Reproduce the issue or run the closest existing test when possible. Missing evidence is a gap, not confirmation.

For each surviving group, trace the full causal chain:

`observed symptom → violated invariant → natural owner → why the current design permits the violation`

A restatement of the symptom, the failing line, or the absence of a guard is not yet a root cause. Judge the reviewer's claim, proposed cause, severity, and proposed implementation independently. A real symptom does not make the explanation or patch correct.

Done: every group is verified, disproved, or has an explicit evidence gap, and each verified group has one causal account that explains all of its comments without contradiction.

## Re-evaluate severity

Do not inherit the reviewer's priority. Grade realistic reach, consequence, scope, and recoverability:

- **P0 — blocks release:** a reachable catastrophic failure, such as broad outage, authority or security compromise, or irreversible widespread data loss.
- **P1 — must fix before merge:** a normal path, reasonable recovery/concurrency path, or attacker-controlled boundary can cause serious incorrect behavior, security exposure, or non-trivial data loss.
- **P2 — should fix, not merge-blocking:** a real and reachable defect or maintenance hazard with bounded, recoverable impact.
- **P3 — optional:** minor impact, narrow cleanup, or a low-cost improvement that can reasonably wait or be declined.
- **No finding:** false, unsupported, or reachable only through multiple unsupported premises.

A contrived unsupported path is normally **No finding**. Report it only when its consequence is irreversible data loss, privilege or trust-boundary breach, destruction of a core authority, or broad outage; severity follows actual reach and recoverability, not the worst imaginable consequence.

## Derive the simplest correction

Within the implicated boundary, derive the minimum concepts, authorities, states, paths, and contracts required by evidenced behavior. Treat extra representations, mirrored state, parallel paths, repeated validation, pass-through layers, speculative abstractions, and compatibility machinery without a proven producer as suspect—not as precedent.

For every verified group, compare these end states in order:

1. remove the unnecessary behavior, path, state, or abstraction;
2. consolidate the rule or representation at its natural owner so sibling fixes disappear;
3. make the invalid state unrepresentable or fix the verification seam;
4. apply a local patch only when the symptom is genuinely isolated and a deeper change would add more total system cost than it removes;
5. leave behavior unchanged and defer or push back.

Prefer the option that removes the most ongoing synchronization, branching, API surface, and future rework while preserving current obligations. Count total codebase cost, not changed lines. Do not add an abstraction merely to contain a patch.

Before deleting a compatibility or public path, verify persisted data, deployed versions, replay/resume, rolling upgrades, third-party producers, and external contracts. A root correction is controlled only when it serves the current change, is reversible, has reliable verification, and does not introduce a new public-contract, migration, security, or operational-policy decision. Use `shape` when such a decision is unavoidable.

Stop local patching and reassess the owner when the same issue reaches a seam twice, a prior response produces an adjacent symptom, or several comments expose one duplicated authority or invalid state. Do not wait for a third patch.

## Decide and communicate

Choose exactly one outcome per ledger group:

- **Delete or simplify** — remove an unjustified concept or combine duplicate authorities or paths.
- **Fix at owner** — restore the invariant at the narrowest responsible boundary.
- **Fix locally** — repair a demonstrably isolated symptom.
- **Defer** — record a true but low-priority or out-of-scope issue without adding code.
- **Push back** — reject a false, overstated, unsupported, incompatible, or net-complexity-increasing suggestion.

When the issue is valid but the proposed patch is not, accept the issue and reject that implementation explicitly. Lead with the decision and decisive evidence; avoid praise, defensiveness, and agreement theater.

## Implement and close the loop

Implement only when the user asked to address, apply, or fix the feedback, and only the ledger's accepted actions. Work in causal dependency order and one observable behavior at a time. Use `tdd` when the change has a stable test seam; otherwise use the nearest trustworthy verification.

After an owner-level correction, search sibling paths for the superseded rule. Remove obsolete branches, helpers, representations, and tests made unnecessary by the new source of truth; do not retain both the patch path and the root correction.

For GitHub inline feedback, reply inside the thread and resolve it once settled. Leave it open when awaiting clarification or a decision.

Done means the user saw a P0–P3 decision ledger before production edits, every comment is accounted for, accepted changes are verified at the owning layer, the causal issue no longer needs sibling patches, and every deferred, rejected, blocked, or deleted item has a concise evidence-backed reason.
