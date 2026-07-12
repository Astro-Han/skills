# Agent Goal Patterns

Read only the section that matches the user's task.

## PR Batch Production

Use when the user wants Codex to keep producing PRs or repeat a narrow mechanical change.

Include:

- target branch and worktree/branch policy;
- user-provided PR count when the user gives one;
- production-loop stop conditions when the user wants throughput but does not give a count;
- flat-first topology rule;
- review-sized, independently verifiable candidate queue;
- touched-file or route/source boundaries;
- per-PR verification;
- final topology table;
- no review/approve/merge/release;
- stop conditions for conflicts, overlapping active workstreams, unclear ownership, failing verification, or review overhead.

Do not use "low-risk" as the main candidate filter unless the user asks for conservative work. Prefer "review-sized", "independently verifiable", and "reversible". If a candidate is too costly for the current window, skip it with evidence and continue the loop instead of pausing the whole goal.

Compact shape when the user gives a PR count:

```text
/goal Run a controlled PR production window for [narrow queue].
Context: first read [issue/plan/status/docs] and current target branch state.
Scope: create up to [soft] flat PRs, hard stop at [cap], all from latest [branch], touching only [paths].
Constraints: no stacked PRs unless there is a real compile/test/review dependency; no merge, release, approve, force-push, or unrelated cleanup.
Verification: for each PR run [focused checks] and verify the diff contains only its slice.
Iteration: finish one PR before starting the next; update a compact handoff/topology table after each PR.
Stop when: [cap] ready PRs exist or no safe non-overlapping slice remains.
Pause if: conflicts, active workstream ownership, CI failures, product decisions, or topology ambiguity become the bottleneck.
Final report: PR table with number/title/base/head/touched files/dependency reason/verification/review order.
```

Compact shape when the user asks for an open production window without a PR count:

```text
/goal Keep producing review-ready PRs for [narrow queue/time window] while useful independent candidates remain.
Context: first read [issue/plan/status/docs], active PRs/worktrees, current target branch, and available verification commands.
Scope: repeatedly choose the next non-overlapping, review-sized, independently verifiable candidate from [queue/area], create one flat PR from latest [branch], report it, then continue to the next candidate.
Constraints: no stacked PRs unless there is a real compile/test/review dependency; no merge, release, approve, force-push, or unrelated cleanup.
Verification: for each PR run [focused checks] and verify the diff contains only its slice.
Iteration: finish one PR before starting the next; update a compact handoff/topology table after each PR.
Stop when: the time window ends, no clear independent candidate remains, review overhead becomes the bottleneck, ownership is unclear, or repeated verification failures stop narrowing.
Pause if: product decisions, destructive/public actions, credentials, production data, active workstream ownership, or topology ambiguity require human input.
Final report: PR table with number/title/base/head/touched files/dependency reason/verification/review order plus skipped candidates and blockers.
```

## Product, UI, Or Frontend Build

Use when the user asks for an app, website, game, dashboard, visual prototype, or complete product slice.

Include:

- the user's requested product completeness, such as prototype, complete v1, production-ready slice, or launch preparation;
- existing design system or restrained defaults;
- accounts, backend, cloud sync, deployment, paid APIs, or copyrighted assets only when requested or clearly required by the stated outcome;
- gates before public launch, paid services, credentials, irreversible data changes, or ownership-sensitive actions;
- desktop and mobile rendered checks;
- screenshot or browser evidence;
- bounded visual iteration.

Avoid shrinking a complete-product request into a toy demo. If the user asks for "完整可用 v1", keep the complete v1 in scope and make launch or production steps conditional on explicit approval.

## Bug Fix

Use when the user reports a failure, crash, regression, flaky test, or broken behavior.

Include:

- reproduce or inspect the failing evidence first;
- identify the failing layer before changing setup or source;
- narrow fix at the lowest correct layer;
- regression test when cheap and meaningful;
- no test weakening or broad refactor;
- stop after repeated same-symptom failure and revisit the root-cause hypothesis.

## High-Risk Or Regulated Work

Use when the task touches secrets, auth, payment, production data, destructive operations, legal/medical/financial claims, privacy-sensitive data, app-store submission, or live deployment.

Default to discovery-first without deleting the user's final objective:

```text
Goal: Prepare and validate [risky final objective] so a human can approve the risky step with evidence.
Context to read first: read [docs/config/logs/sample data] and identify required permissions.
Scope: discovery, implementation in a safe environment, dry-run/rehearsal, rollback planning, and approval package.
Non-goals: do not execute the irreversible production/public/destructive step without explicit approval.
Constraints: no unsupervised production data use, secrets exposure, destructive writes, paid services, public claims, or live deployment.
Verification: report exact sources inspected, risks found, dry-run or rehearsal evidence if available, and the smallest safe next step.
Iteration: reduce uncertainty with evidence; do not guess domain rules.
Stop when: the approval package, verification evidence, and blockers are documented.
Pause if: credentials, production access, legal/medical/financial judgment, destructive action, public launch, or account ownership is required.
```

## Skill Creation

Use when the user wants a new or improved agent skill.

Include:

- for Codex, use `$skill-creator`; otherwise use the target product's local skill/plugin creation process or write the skill files directly;
- decide the smallest useful skill shape;
- initialize in the chosen skill location;
- write concise `SKILL.md` with strong trigger description;
- add scripts/references only when they improve reliability;
- run `quick_validate.py`;
- create realistic eval prompts and a deterministic lint/eval if possible;
- forward-test when the skill is complex.
