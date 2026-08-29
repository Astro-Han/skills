# Queue, rereview, and publication

Load this reference only when the task covers a PR queue, independent reviewer delegation, a changed head, or a public review action.

## Triage a queue

Scan the whole requested queue before opening every diff. Record exclusions such as drafts, bots, out-of-scope repositories, blocked dependencies, and PRs already carrying unresolved feedback from us. Prioritize by recent meaningful activity, reviewability, size, and whether a decision is currently useful.

A changed head is not by itself a reason to repeat a review. Rereview when new changes touch the prior reasoning or when prior comments are resolved. If an old review comment is still unresolved and the relevant code is unchanged, report that state instead of mechanically reviewing again.

Batch small, independent PRs. Keep large or architecture-sensitive work separate so its evidence does not get compressed into a queue summary.

## Use independent reviewers proportionally

When delegation is available, allowed, and useful, split a complex PR by decision angle—problem value, architecture/authority, concurrency/recovery, tests/production composition, simplification, or UI/UX—not by arbitrary file ranges. Give each reviewer the raw PR/Issue facts and a bounded question; do not leak an expected verdict.

One main reviewer owns the final report: cross-check critical claims, deduplicate findings, calibrate reach and severity, and resolve conflicts. Do not delegate a small PR merely to create parallel activity.

## Refresh before publication

Immediately before a public Comment, Approve, Request changes, or merge recommendation, refresh the exact head SHA, CI for that SHA, mergeability, and unresolved threads. If the head changed, identify whether the change invalidates the analysis; do not silently attach an old conclusion to new code.

Follow the host project's confirmation, identity, and human-accountability rules. Approval, publication, and merge are external actions, not implied by a review request. For UI or UX changes, wait for the named manual acceptance path and human decision.

Write public reviews for the author:

- open with a brief thanks;
- put precise line-local defects inline and the overall decision in the top-level review;
- state the reviewed head and decisive evidence;
- keep the tone collaborative and the correction actionable;
- when the user prefers it, place a Chinese counterpart in a collapsed details block;
- disclose the AI-assisted role and what the accountable human actually verified.

Publication is complete only when the submitted review still matches the refreshed head and its public state, destination, identity, body, and human responsibility are explicit.
