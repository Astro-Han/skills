---
name: review-feedback
description: "Use this skill whenever code-review feedback already exists and may affect a code decision or change. This includes PR comments, findings returned by invoke or any external model or review tool, and delegated-review results—even when the user simply says to fix, address, apply, or resolve them. Do not use to perform a new review, diagnose an unrelated bug, implement a new requirement, or merely summarize or explain feedback without deciding about code."
---

# Review Feedback

Review feedback is evidence about one system, not a queue of patches. Adjudicate the reported problem and the proposed remedy separately before editing.

## 1. Model the whole review

Read all feedback, the intended change, earlier review rounds, and related fixes before changing code. Group comments that may be symptoms of the same invariant, owner, boundary, duplicated rule, invalid state, or missing verification seam. Treat a comment as isolated only when tracing shows no shared cause.

If an unclear item changes how coupled items should be handled, ask one precise question and wait. Otherwise continue evaluating independent items.

Done: every comment belongs to a shared issue hypothesis or is demonstrably isolated.

## 2. Try to disprove the claim

Open the cited code and trace the real path. State the concrete failure, contract violation, or maintenance consequence the claim predicts, then check the strongest available counterevidence: callers, tests, requirements, project conventions, target versions, history, and current behavior. Reproduce the issue or run the closest existing test when possible. Missing evidence is a gap, not confirmation.

Before expanding scope, search for actual callers, users, and specifications. No demand may mean the right change is deletion, not a more elaborate implementation.

Judge the proposed cause, severity, and implementation independently. A real symptom does not make the reviewer's explanation or patch correct.

Done: every issue hypothesis is verified, disproved, or has an explicit evidence gap; surviving hypotheses explain their grouped comments without contradiction.

## 3. Choose the right layer

For every verified issue, compare:

- leaving behavior unchanged and pushing back or deferring;
- the smallest local change that removes the reported symptom;
- the smallest change that makes the underlying invariant true at its natural owner and removes the need for sibling fixes.

Prefer the root correction while it remains controlled. Judge size by total codebase cost, not changed lines: duplicated rules, branches, states, API surface, migration, blast radius, testability, and future rework. A larger diff can be the simpler solution; an abstraction is not cleaner merely because it is more general.

A root correction is controlled when it serves the current change's goal, is reversible, has reliable verification, and does not introduce a public-contract, data-migration, security, or operational-risk decision. If those boundaries would be crossed, present the alternatives and use `shape` before expanding scope.

Stop making local patches and reassess the system when:

- the same issue class reaches the same seam a second time;
- a review-response round leaves the prior issue unresolved or produces an adjacent symptom;
- several comments point to one duplicated rule, invalid state, misplaced responsibility, or missing verification seam.

Trace where the invariant should live. Consider deleting the unnecessary path, consolidating representations, moving enforcement to the owner, making invalid states unrepresentable, or fixing the test seam. Do not wait for a third patch.

## 4. Adjudicate before editing

Do not inherit the reviewer's severity, priority, or proposed implementation. Re-evaluate truth, reach, impact, reversibility, and proportion. A rare case can still be critical when it risks security, money, or data.

Before any edit, produce a concise decision ledger for the grouped issues: decisive evidence, underlying invariant and natural owner, and one outcome. Map every original comment to a group so none becomes an implicit patch instruction.

Choose one outcome per group:

- **Fix at the owner** — correct the invariant at the narrowest responsible boundary.
- **Fix locally** — the symptom is isolated and a deeper change would add more system cost than it removes.
- **Defer** — true but currently low priority or outside the requested scope; record the reason without adding code.
- **Push back** — false, overstated, unsupported, incompatible with project constraints, or more complex to fix than its impact warrants.
- **Delete or simplify** — the path or abstraction lacks enough demand to justify its maintenance cost.

When the issue is valid but the proposed patch is not, accept the issue and explicitly reject that implementation in favor of the chosen owner or local fix. Do not edit until every item is accounted for.

## 5. Respond with evidence

Lead with the decision and decisive evidence. When local and root solutions materially differ, state which layer you chose and why. For pushback, name the conflicting test, requirement, usage evidence, version, or complexity trade-off. For an ambiguous item, ask only what changes the decision.

Do not praise the reviewer, perform agreement, or write defensive prose. If later evidence overturns your pushback, state the correction in one sentence and proceed.

## 6. Implement and close the loop

Implement when the user asked to address, apply, or fix the feedback. Work in dependency order and one observable behavior at a time. Use `tdd` when the change has a stable test seam; otherwise use the nearest trustworthy verification. Implement only the ledger's accepted actions; do not implement unverified, deferred, pushed-back, or out-of-scope suggestions.

After a root correction, search sibling paths for the superseded rule and verify the invariant at its owner. Remove obsolete branches or helpers made unnecessary by the fix; do not leave both the old patch path and the new source of truth.

For GitHub inline feedback, reply inside the thread and resolve it once the issue is settled. If the reply asks for clarification or awaits a decision, leave it open.

Done means every item is classified, implemented changes are verified at the chosen layer, repeated symptoms no longer require sibling patches, and deferred, rejected, blocked, or deleted items have a concise evidence-backed reason.
