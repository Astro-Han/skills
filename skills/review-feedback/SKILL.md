---
name: review-feedback
description: "Evaluate review feedback before changing code. Use whenever PR comments, review tools, external models such as invoke, or delegated reviewers have returned findings that may be fixed, applied, addressed, or rejected. Do not use to perform a fresh review, diagnose an ordinary bug, or handle a new requirement."
---

# Review Feedback

A review is evidence about one system, not a queue of independent patches. Do not edit until you have a system-level repair plan.

## 1. Model the whole change

Read the full review, diff or intended change, earlier rounds, and related fixes. Trace affected callers, state, and boundaries far enough to explain how the system should work.

Group findings by shared invariant, owner, boundary, duplicated rule, invalid state, or missing verification seam. Form one repair hypothesis per group. Treat a finding as isolated only when the traced system shows no shared cause.

If an unclear item changes how coupled items should be handled, ask one precise question and wait. Otherwise continue evaluating independent items.

Done: every finding belongs to a repair hypothesis or is demonstrably isolated.

## 2. Verify the model

Trace each claim through real code. Reproduce it or run the closest existing test when possible. Check requirements, conventions, target versions, history, and current behavior rather than generic best practice. Use the evidence to confirm, revise, merge, or reject its repair hypothesis.

Before expanding scope, search for actual callers, users, and specifications. No demand may make deletion better than a broader implementation.

Classify each finding without inheriting the reviewer's severity or implementation:

- **Fix at the owner** — make the invariant true at its narrowest responsible boundary.
- **Fix locally** — the symptom is isolated and deeper work adds more system cost than it removes.
- **Delete or simplify** — the path or abstraction lacks enough demand.
- **Defer** — true but low priority or outside scope; record why without adding code.
- **Push back** — false, overstated, speculative, incompatible, or disproportionate.

Done: every claim has decisive evidence or an explicit gap, and the surviving hypotheses explain all coupled findings without contradiction.

## 3. Choose one repair plan

For each verified hypothesis, compare:

- the smallest local change that removes the reported symptom;
- the smallest change that makes the underlying invariant true at its natural owner and removes the need for sibling fixes.

Prefer the root correction while controlled: it serves the current goal, is reversible and reliably verifiable, and adds no public-contract, migration, security, or operational-risk decision. Otherwise present the alternatives and use `shape` before expanding scope.

Judge size by total system cost, not changed lines: duplicated rules, branches, states, API surface, blast radius, testability, and future rework. A larger diff can be simpler; an abstraction is not cleaner merely because it is general.

Reject the local-patch plan and reassess the owner when:

- the same issue class reaches the same seam a second time;
- a review-response round leaves the prior issue unresolved or produces an adjacent symptom;
- several comments point to one duplicated rule, invalid state, misplaced responsibility, or missing verification seam.

Trace where the invariant should live. Consider deleting the unnecessary path, consolidating representations, moving enforcement to the owner, making invalid states unrepresentable, or fixing the test seam. Do not wait for a third patch.

Done: the plan names the owning layer, dependency order, verification seam, and outcome of every finding. If several local edits enforce the same rule, reassess.

## 4. Execute and close

Lead with the decision and decisive evidence. When local and root solutions differ materially, name the chosen layer and why. Ground pushback in a conflicting test, requirement, usage, version, or cost. Avoid praise, agreement theater, and defensive prose.

Implement only when the user asked to address, apply, or fix the feedback. Execute the plan in dependency order, one observable behavior at a time. Use `tdd` with a stable test seam; otherwise use the nearest trustworthy verification. Do not implement unverified, deferred, or out-of-scope suggestions.

After a root correction, search sibling paths for the superseded rule, verify the invariant at its owner, and remove obsolete branches or helpers. Do not leave the old patch path beside the new source of truth.

For GitHub inline feedback, reply inside the thread and resolve it once the issue is settled. If the reply asks for clarification or awaits a decision, leave it open.

Done: every item is classified; changes are verified at the chosen layer; repeated symptoms need no sibling patches; and every non-fix has a concise evidence-backed reason.
