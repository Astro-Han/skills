---
name: review-feedback
description: "Adjudicate and act on existing code-review feedback: PR comments, inline threads, or findings from reviewers, review tools, external models, or delegated agents. Use whenever the user asks to fix, address, apply, resolve, respond to, or push back on review comments or findings — even a casual 'fix the review comments' — and before any code edit that review feedback may cause. Do not use to perform a fresh review, diagnose an unrelated bug, implement a new requirement, or merely summarize feedback."
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
- root cause, violated invariant, natural owner, and the smallest single-owner end state that covers the group;
- outcome: **Delete or simplify**, **Fix at owner**, **Fix locally**, **Defer**, or **Push back**.

When feedback targets an existing diff or follows an earlier review round, also state its scope relation: **required by the original change**, **regression caused by this diff**, **unrelated drift already in the diff**, or **pre-existing/adjacent**.

Use only P0–P3 for findings; do not invent parallel scales such as F1/F2. Publishing the ledger is the gate, not a request for approval: when the user already asked for fixes, continue with accepted actions unless a material choice requires `shape`.

Run the decisive checks before publishing the ledger. If later evidence changes a verdict, publish the correction before editing.

Verdict and outcome must agree. **Disproved** permits only **Push back**; **No finding** is not an independent reason to change behavior. Never implement code or tests derived solely from a disproved comment under labels such as defensive hardening, cleanup, consistency, or an implied requested behavior. Such a change needs independent evidence that existed before the feedback. A contradictory ledger does not open the edit gate.

Treat every requested file, location, mechanism, and patch—even when written as an imperative—as the reviewer's proposal, not a requirement. It becomes a constraint only when independent product, architecture, or compatibility evidence says so. For grouped comments, the ledger must explain why per-comment edits are not duplicate authorities before choosing them over the single-owner end state.

## Adjudicate every comment

### Verify and find the cause

Open the cited code and trace the real reachable path. State the concrete failure, contract violation, or maintenance consequence predicted by the comment, then seek the strongest counterevidence in callers, tests, requirements, repository conventions, target versions, history, and current behavior. Reproduce the issue or run the closest existing test when possible. Missing evidence is a gap, not confirmation.

For each surviving group, trace the full causal chain:

`observed symptom → violated invariant → natural owner → why the current design permits the violation`

A restatement of the symptom, the failing line, or the absence of a guard is not yet a root cause. Judge the reviewer's claim, proposed cause, severity, and proposed implementation independently. A real symptom does not make the explanation or patch correct.

The ledger verdict answers whether the reported product or system defect exists, not whether the suggested patch is correct. When the observed behavior is real and violates an independent contract, mark it **Verified** even if the reviewer's proposed invariant, owner, or implementation is wrong; then state that the proposal is rejected and fix the real owner. Use **Disproved** only when no reported defect remains after tracing the actual contract and consequence.

Done: every group is verified, disproved, or has an explicit evidence gap, and each verified group has one causal account that explains all of its comments without contradiction.

### Re-evaluate severity

Do not inherit the reviewer's priority. Grade realistic reach, consequence, scope, and recoverability:

- **P0 — blocks release:** a reachable catastrophic failure, such as broad outage, authority or security compromise, or irreversible widespread data loss.
- **P1 — must fix before merge:** a normal path, reasonable recovery/concurrency path, or attacker-controlled boundary can cause serious incorrect behavior, security exposure, or non-trivial data loss.
- **P2 — should fix, not merge-blocking:** a real and reachable defect or maintenance hazard with bounded, recoverable impact.
- **P3 — optional:** minor impact, narrow cleanup, or a low-cost improvement that can reasonably wait or be declined.
- **No finding:** false, unsupported, or reachable only through multiple unsupported premises.

A contrived unsupported path is normally **No finding**. Report it only when its consequence is irreversible data loss, privilege or trust-boundary breach, destruction of a core authority, or broad outage; severity follows actual reach and recoverability, not the worst imaginable consequence.

Reachability alone does not make a finding P1. Use P1 only when the reachable consequence itself is merge-blocking: security or trust-boundary exposure, non-trivial data loss, incorrect committed or externally visible state, money movement, sustained outage, or a broadly unusable core workflow. A bounded in-memory result, preview error, or recoverable local inconsistency with no persisted or external side effect is P2 even on a normal path.

## Rebase the cumulative diff before choosing repairs

When review targets an existing change, derive scope from its original request and accepted contracts, not from code that earlier rounds added. Fix original obligations and regressions; revert unrelated drift and its tests; defer pre-existing or adjacent findings unless leaving them makes the change unsafe or incomplete. Quoted “keep” or “expand” wording is still a proposal, not explicit user expansion. If no prior change scope exists, adjudicate the verified defect as the requested goal without inventing adjacent work.

Each later review round replaces the prior ledger; it does not append to it. Before further edits, compare the cumulative diff with its base, restate the smallest end state, and name which assumptions changed and which production concepts, files, and tests are added or removed. If no assumption changed, keep scope closed. A new authority, policy, state, API, path, or speculative abstraction closes the edit gate until tied to the original invariant or replacing more surface than it adds.

## Synthesize and choose the end state

### Model the whole review

Read all feedback, the intended change, earlier review rounds, and related fixes. Trace each comment to a verdict without choosing its repair; possible groupings are hypotheses until the evidence is complete. Then compare the surviving claims once: use one root when they share an invariant and natural owner, keep them independent when contracts or owners differ, and allow a mixed plan. Do not force a common root, and do not split one rule into caller patches merely because the comments arrived separately.

If an unclear item changes how coupled items should be handled, ask one precise question and wait. Otherwise continue evaluating independent items.

Done: every comment has a verdict and belongs to a proven causal group or is demonstrably isolated.

### Derive the simplest correction

Within the implicated boundary, derive the minimum concepts, authorities, states, paths, and contracts required by evidenced behavior. Treat extra representations, mirrored state, parallel paths, repeated validation, pass-through layers, speculative abstractions, and compatibility machinery without a proven producer as suspect—not as precedent.

Find the owner by asking which single boundary can keep the invariant true for every current and future producer. An entry point is not the owner merely because data passes through it; when several producers construct the same domain value, intrinsic validity belongs to that value unless its contract deliberately permits an invalid or transitional state.

For every verified group, compare these end states in order:

1. remove the unnecessary behavior, path, state, or abstraction;
2. consolidate the rule or representation at its natural owner so sibling fixes disappear;
3. make the invalid state unrepresentable or fix the verification seam;
4. apply a local patch only when the symptom is genuinely isolated and a deeper change would add more total system cost than it removes;
5. leave behavior unchanged and defer or push back.

Prefer the option that removes the most ongoing synchronization, branching, API surface, and future rework while preserving current obligations. Count total codebase cost, not changed lines. Do not add an abstraction merely to contain a patch.

When grouped comments repeat one invariant or synchronization rule at several sites, **Fix locally** is not an available outcome unless independent contract evidence proves those sites intentionally own different policies. Separate entry points, current caller count, and imperative patch wording are not such evidence. Remove mirrored state or enforce the rule once at its owner.

Before deleting a compatibility or public path, verify persisted data, deployed versions, replay/resume, rolling upgrades, third-party producers, and external contracts. A root correction is controlled only when it serves the current change, is reversible, has reliable verification, and does not introduce a new public-contract, migration, security, or operational-policy decision. Use `shape` when such a decision is unavoidable.

Stop local patching and reassess the owner when the same issue reaches a seam twice, a prior response produces an adjacent symptom, or several comments expose one duplicated authority or invalid state. Do not wait for a third patch.

### Decide and communicate

Choose exactly one outcome per ledger group:

- **Delete or simplify** — remove an unjustified concept or combine duplicate authorities or paths.
- **Fix at owner** — restore the invariant at the narrowest responsible boundary.
- **Fix locally** — repair a demonstrably isolated symptom.
- **Defer** — record a true but low-priority or out-of-scope issue without adding code.
- **Push back** — reject a false, overstated, unsupported, incompatible, or net-complexity-increasing suggestion.

When the issue is valid but the proposed patch is not, accept the issue and reject that implementation explicitly. Lead with the decision and decisive evidence; avoid praise, defensiveness, and agreement theater.

## Implement and close the loop

Implement only when the user asked to address, apply, or fix the feedback, and only the ledger's accepted actions. Work in causal dependency order and one observable behavior at a time. Follow `tdd`'s applicability criteria; otherwise use the nearest trustworthy verification.

The latest ledger is the sole authority for the final diff. If evidence changes a verdict, owner, or outcome after editing began, remove every edit and test derived from the superseded decision before continuing; verification must fail if an abandoned local patch remains.

After an owner-level correction, search sibling paths for the superseded rule. Remove obsolete branches, helpers, representations, and tests made unnecessary by the new source of truth; do not retain both the patch path and the root correction.

For GitHub inline feedback, reply inside the thread and resolve it once settled. Leave it open when awaiting clarification or a decision.

Done means the user saw a P0–P3 decision ledger before production edits, every comment is accounted for, the cumulative diff contains only the latest ledger's smallest end state, accepted changes are verified at the owning layer, the causal issue no longer needs sibling patches, and every deferred, rejected, blocked, or deleted item has a concise evidence-backed reason.
