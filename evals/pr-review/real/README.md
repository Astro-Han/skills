# Real PR Holdout

This fixture freezes real public pull requests without handing the executor the review answer. It
is for a future public A/B claim; it is not another synthetic regression suite.

## Decision and success criterion

Claim an improvement only if the shipped Skill increases independently validated,
decision-critical finding recall or end-to-end decision-ready reviews without increasing unsupported
P1/P2 findings. Report raw counts and percentage points. Keep finding-level recall, unsupported
finding rate, and PR-level decisions separate.

## Sample before inspecting code

The population is `apache/maka` PRs created from 2026-08-01 through 2026-08-20. The checked-in
policy excludes every PR used to design the Skill or already inspected as field evidence, removes
bots and drafts, and selects twelve cases by a fixed hash seed across five metadata-only strata:
closed-unmerged, test/docs/CI, small, medium, and large. Selection uses no review outcome or code
inspection. This deliberately stratified set measures these twelve cases; it is not a prevalence
estimate for every pull request.

Capture the immutable pool and selection:

```bash
python3 evals/pr-review/real_fixture.py capture-pool \
  --repo apache/maka --created-from 2026-08-01 --created-to 2026-08-20 \
  --output evals/pr-review/real/pool.json
python3 evals/pr-review/real_fixture.py select \
  --pool evals/pr-review/real/pool.json \
  --policy evals/pr-review/real/selection-policy.json \
  --output evals/pr-review/real/selection.json
```

For each selected number, capture its final author-supplied head, PR/Issue text, exact-head checks,
changed-file list, and patch. The capture intentionally omits reviews, comments, mergeability,
merge outcome, and later fixes:

```bash
python3 evals/pr-review/real_fixture.py capture \
  --repo apache/maka --number <N> --case-id maka-pr-<N> \
  --output-root evals/pr-review/real/cases
python3 evals/pr-review/real_fixture.py verify \
  --cases-root evals/pr-review/real/cases \
  --selection evals/pr-review/real/selection.json
```

## Executor boundary

Materialize each case from a full local `apache/maka` clone. The executor receives only the
historical repository at the frozen comparison base, the staged source patch, and
`.pr-review-eval/` context:

```bash
python3 evals/pr-review/real_fixture.py materialize \
  --case evals/pr-review/real/cases/maka-pr-<N> \
  --repo-cache /path/to/maka \
  --output /isolated/run/work
```

Keep the predeclared answer key outside the materialized workspace. The no-Skill and with-Skill
arms must use the same model, reasoning, tools, prompt, repository, and exact patch. Codex runs must
disable the user-level same-name Skill in both arms; the shared runner now does that by exact path.
Before spending model calls, inspect the rendered prompt catalog and reject the run if the baseline
can see a functional `pr-review` package or the candidate can see more than its isolated copy.

The full run is twelve paired cases (24 executions). If paired arms materially disagree, repeat
only the four numbers already frozen in `selection-policy.json`, for at most 32 executions. Blind
adjudicators score the outputs after execution against private copies of
[`answer-key-template.json`](answer-key-template.json). Cases that informed the Skill may remain
regression tests but never enter the public holdout percentage.

Run the first paired execution with the weak model chosen for this decision. The runner rejects
additional repetitions for this suite:

```bash
python3 evals/runner.py \
  --provider codex --model gpt-5.6-luna \
  --suite pr-review-real --reps 1 \
  --iteration real-luna-high-v1 \
  --repo-cache /path/to/maka
```

Do not open `final_message.md` or transcripts before the independent answer keys are complete.

Two reviewers who did not design the Skill must independently complete each answer key before any
model output is opened, then reconcile evidence against the historical repository. A required
finding needs a reachable trigger, consequence, reproduction, code evidence, and calibrated
severity. A plausible but invalid P1/P2 belongs under `invalid_findings_to_watch`; it is not silently
discarded. Keep completed keys and reviewer identities outside the executor workspace.

## First paired execution

The `real-luna-high-v1` execution completed all 24 model calls without runner failures. The
candidate loaded only the isolated Skill in 12/12 runs, the baseline loaded it in 0/12, and neither
arm could see the user-level Skill. Two independent reviewers completed and reconciled the gold
before any model output was opened, then independently scored randomized A/B outputs. The verified
gold contained three required findings: two P1 and one P2.

| Metric | With Skill | Without Skill | Paired result |
| --- | ---: | ---: | --- |
| Required finding recall | 2/3 | 2/3 | no difference |
| Responses with unsupported P1/P2 | 6/12 | 8/12 | 2 wins, 0 losses, 10 ties |
| Unsupported P1/P2 claims | 8 | 14 | 4 wins, 0 losses, 8 ties |
| Decision-ready reviews | 5/12 | 2/12 | 3 wins, 0 losses, 9 ties |

This run supports a narrower claim: the Skill reduced unsupported high-severity claims and produced
more reviews that were ready to drive a decision. It did not improve recall; both arms found the
same two findings and missed the same authentic-checkpoint replay defect. Twelve deliberately
stratified PRs, one execution per arm, and one model configuration are not enough to advertise a
stable percentage improvement. Preserve these raw counts and run a new independent sample before
making a public effect-size claim. The machine-readable record is
[`results/real-luna-high-v1.json`](results/real-luna-high-v1.json).
