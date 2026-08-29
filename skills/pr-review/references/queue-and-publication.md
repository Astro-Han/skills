# Queue, rereview, and publication

Load only for a PR queue, reviewer delegation, changed head, or public action.

## Triage

Scan before opening every diff. Record drafts, bots, blocked dependencies, exclusions, and PRs carrying our unresolved feedback. Prioritize activity, reviewability, size, and decision value.

A changed head alone does not justify rereview. Rereview when changes affect prior reasoning or resolve feedback. If our comment remains unresolved and relevant code is unchanged, report that state. Batch small PRs; separate architecture-sensitive work.

## Delegate proportionally

When delegation is allowed and useful, split a complex PR by decision angle: value, ownership, concurrency, production path, tests and removable code, or UI/UX. Give raw facts and bounded questions without an expected verdict.

The main reviewer cross-checks claims, deduplicates findings, calibrates severity, and resolves conflicts. Do not delegate small PRs merely to create activity.

## Publish

Before Comment, Approve, Request changes, or merge recommendation, refresh exact head, its CI, mergeability, and unresolved threads. If head changed, decide whether analysis remains valid.

Follow project confirmation, identity, and human-accountability rules. Review requests do not imply external action. For UI/UX changes, use **Wait** and name the manual checks that remain.

Open with thanks. Put line-local defects inline and the decision at top level. State head and evidence, keep corrections collaborative, optionally collapse a requested translation, and disclose AI assistance plus human verification.
