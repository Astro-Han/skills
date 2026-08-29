# PR Review Evals

Evaluation record for [`pr-review`](../../skills/pr-review/). The fixtures and assertions cover
problem value, scope, real production paths, ownership, tests, simplification, UX, severity,
partial live facts, close non-triggers, and holdouts. Case definitions live in
[`pr_review_cases.py`](../pr_review_cases.py); fixtures use the `prreview-*` prefix under
[`fixtures/`](../fixtures/).

## Run

```bash
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-holdout --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-reachability --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-partial-facts --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-no-statuses --reps 4
python3 evals/grader.py
```

## Adoption decision

Compare the shipped skill with no installed skill in 48 paired A/B runs: four repetitions of eight
review requests, two close non-triggers, and two held-out simplification traps. The decision gates
are: correct invocation in every run; no approval when a material gap remains; PR/Issue/head/diff
facts and problem value before the recommendation; the real production path; a clear account of
what the PR adds and what can be removed; preservation of necessary process tests, live
compatibility, and durable recovery state; and at least 90% of predeclared report assertions in
both design and holdout suites.

The accepted `gpt-5.6-luna`/high run used 96 model executions. On the 10-case design suite the
candidate scored 406/412 assertions (98.5%) versus 123/412 (29.9%) without the skill. On the two-case
holdout it scored 111/112 (99.1%) versus 45/112 (40.2%). Invocation was correct in 48/48 candidate
runs; decision-critical facts and problem-first ordering were 40/40; unresolved material gaps were
not approved in 32/32 applicable runs; required explicit Approve or manual-check decisions were
8/8; and additions or possible removals were reported in 40/40 reviews. Runner failures were 0/96.

This supports adoption, not broad statistical generalization. The answer keys are fixed but
inspectable by the author, grading is phrase-based free-text evaluation, fixtures do not exercise a
live GitHub API, and only one model/reasoning configuration was tested. Keep those limits explicit
when changing the skill or extrapolating to another model.

## Reachability decision

Compare the frozen pre-revision skill at `3e9300fb74ebbecdcd07aad92c5e97a98457f55a`
with the shipped skill on four repetitions of the guarded-edit regression. Adopt the revision only
if every candidate run traces the visible Edit action through the downstream production guard,
rejects the unsupported P1 instead of grading theoretical loss, and waits for manual checks
for the actual UI change. This case reproduces the failure that motivated the revision, so it can
prove regression repair but not generalization; the pre-existing severity, production-path, and
contrived-path cases remain the supporting non-regression evidence.

Under the rubric used for that `gpt-5.6-luna`/high run, the four pairs scored 54/56 assertions
(96.4%) for the candidate versus 50/56 (89.3%) for the frozen skill, with 0/8 runner failures.
Both arms traced the production guard and rejected the unsupported P1 in 4/4 runs. The score
difference came from the required manual-check decision, so this run supports more consistent
output but does not prove a reachability improvement. The motivating case is not an independent
holdout.

## Compression decision

The full package is frozen at `538bf102514f54277ea6e829e6785f73d165af31`. Adopt a compressed
package only when `SKILL.md` is at most 750 words, the directly loaded package is at most 1,000
words, and it contains no Chinese text. The accepted package uses 750 + 223 words and meets the
behavioral decision above; do not trade away its hard decision gates merely to reduce word count.

The plain-language revision at that point removed longer invented labels but retained
Approve/Comment/Wait. The later no-status decision below supersedes that output contract. Historical
percentages must not be rescored as new model evidence after changing the rubric.

## No-status decision

Compare the frozen three-state skill at `d4ea3b6bc9dc198a43024ae500373b8d0f5567ae`
with the candidate on four repetitions of two cases: one PR with a real P1 plus a separate manual
UX check, and one clean exported snapshot whose current PR state is unavailable. This is eight A/B
pairs and sixteen model runs.

Adopt only if every candidate output avoids Approve/Comment/Wait as an invented review state,
keeps code findings separate from CI, current-head, human-approval, and manual-acceptance conditions,
still requires the real P1 to be fixed, does not recommend approval of the stale snapshot, and scores
no lower overall than the frozen skill. The stale-snapshot case was not used to design the original
three-state contract, but both cases are now used to validate this revision; they are regression
evidence rather than a broad holdout.

Two 16-run attempts were invalid. Codex could discover the user-level
`~/.agents/skills/pr-review` symlink as well as the isolated `pr-review-eval` copy; seven of eight
frozen-arm runs in the final attempt read the user-level candidate instead of the frozen skill.
The resulting scores and percentages have no comparative meaning and are not adoption evidence.

The attempted runs still exposed one useful candidate-only failure: conditional approval language
for an unverified snapshot. The skill now says to report only the snapshot findings and require a
live refresh, and deterministic English/Chinese tests cover the observed forms. The direct package
tests and validator pass, and the user confirmed the three-state output was confusing in real use.
This supports removing the states for that observed workflow, not broad generalization. Keep this
suite for a fresh paired run after the previously deferred eval-runner isolation fix.

## Partial-facts decision

Compare the frozen complete-facts wording at `72f6f3472fafaa798b5e651fb53f7547c7966749`
with the candidate on four repetitions of two cases: an offline PR patch and an exported snapshot
whose current approval state cannot be refreshed. Adopt only if every candidate run completes a
substantive review without inventing missing facts or approving unverified content, all four
current-approval runs use Wait, and the candidate scores no lower overall than the frozen skill.

These cases test the revised boundary directly. The exported-snapshot case was held out from the
exact wording edit, but both cases were authored for this decision, so they do not establish broad
generalization. The first execution was invalid because its patch counts and answer key
contradicted the fixture; it is excluded rather than rescored. An intermediate run exposed a
conditional Approve for an unverified current PR and led to the explicit current-head gate.

On the historical `gpt-5.6-luna`/high run, the candidate scored 84/112 assertions (75.0%) versus
71/112 (63.4%) for the frozen skill, with 0/16 runner failures. All eight candidate runs completed
substantive review without approving unverified current content; all four offline runs avoided
invented URLs, and all four current-approval runs explicitly used Wait under the now-superseded
three-state contract. Some reports still omitted numeric diff or production/test split, so this
supports the partial-facts boundary only, not overall review quality or broad generalization.

The `with_skill` arm reads `skills/<name>/` directly, so an eval always measures the shipped skill.
`evals/baselines/` holds frozen older variants to compare against; it is the only place this
directory keeps historical skill text.
