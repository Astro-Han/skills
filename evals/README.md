# Evals

Paired A/B evidence for the skills in this repository. A skill change is not done because
it reads better; it is done when a paired run says the agent got better at the job.

## The three pieces

| Piece | What it does |
| --- | --- |
| `runner.py` | Run a headless agent against a fixture, once per arm, and collect the transcript, diff, and test result. The agent CLI is a `--provider` argument; only the invocation, the skill-arm injection, and the transcript schema differ between them. |
| `grader.py` + `acceptance/` | Turn each run into a number: parse the transcript, run the case's acceptance script against the resulting workspace. |
| `skills/craft-skill/scripts/eval.py` | Validate the paired manifest, summarize it, and build a blind review pack. |

They compose in that order: run → grade → summarize. Nothing here judges a skill by reading it.

## Fixtures

Small, self-contained projects that stand in for real work. Each one is an exam paper, not a
library: its value is the specific mistakes an agent can make in it.

| Fixture | Used for | What it plants |
| --- | --- | --- |
| `cartlib` | `tdd` | A feature to add and a crash to fix, both with a clear acceptance test. |
| `pricer` | `debug` | Order-dependent coupon totals — diagnosis only, the fix needs a product decision. |
| `reportlib` | `debug` | Shared mutable section state leaking between reports. |
| `feedhub` | `simplify-audit` | Seven removable concepts, four traps that must survive, and one open product question that must be escalated rather than deleted. Answer key: [`feedhub.md`](fixtures/feedhub.md). |
| `quoteview` | `review-feedback` | Two local-patch suggestions with one domain-owner cause, plus one false finding and a nonstandard severity scale. |
| `seatmap` | `review-feedback` holdout | Two synchronization suggestions caused by mirrored state, plus one false zero-capacity finding. |
| `handlekit` | `review-feedback` holdout | Two caller-level case-folding suggestions whose rule belongs in one canonicalizer. |
| `profilefmt` | `review-feedback` holdout | Two synchronization suggestions caused by an obsolete legacy representation. |
| `jobflow` | `review-feedback` holdout | Two caller-level history patches whose lifecycle rule belongs in one transition owner. |
| `batchplan` | `review-feedback` second holdout | Two local clamp suggestions whose policy belongs in one normalizer, plus a false empty-sum finding. |
| `wireview` | `review-feedback` second holdout | Two exporter patches whose representation belongs to the wire-contract owner. |
| `launchmode` | `review-feedback` second holdout | Two synchronization patches caused by an obsolete toggle that should be deleted. |
| `cartsummary` | `review-feedback` final holdout | A real stale-result symptom whose proposed fix would preserve an obsolete derived cache. |
| `transferlog` | `review-feedback` compression holdout | A shared domain invariant whose violation reaches externally committed state and must remain P1. |
| `credrotate` | `review-feedback` compression holdout | A compatibility representation with a live deployed reader that must be preserved at one lifecycle owner. |
| `prreview-*` | `pr-review` | Review cases for value, scope, real production paths, ownership, tests, simplification, UX, severity, partial live facts, close non-triggers, and holdouts. |

A simplification fixture needs all three kinds. Findable items alone measure eagerness; the
traps and the open question are what separate judgment from enthusiasm.

## Running one

```bash
python3 evals/runner.py --dry-run                  # list the planned runs, no model calls
python3 evals/runner.py --provider pi --reps 1     # writes evals/<skill>-workspace/iteration-1/...
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-holdout --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-second-holdout --reps 6
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-final-holdout --reps 8
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-matrix --reps 5
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-compression --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-compression-holdout --reps 5
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-holdout --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-reachability --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-partial-facts --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite pr-review-no-statuses --reps 4
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-structural-compression --reps 2
python3 evals/grader.py                            # scores those runs
```

### PR-review adoption decision

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
8/8; and additions or possible removals were reported in 40/40 reviews. Runner
failures were 0/96.

This supports adoption, not broad statistical generalization. The answer keys are fixed but
inspectable by the author, grading is phrase-based free-text evaluation, fixtures do not exercise a
live GitHub API, and only one model/reasoning configuration was tested. Keep those limits explicit
when changing the skill or extrapolating to another model.

### PR-review reachability decision

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

### PR-review compression decision

The full package is frozen at `538bf102514f54277ea6e829e6785f73d165af31`. Adopt a compressed
package only when `SKILL.md` is at most 750 words, the directly loaded package is at most 1,000
words, and it contains no Chinese text. The accepted package uses 750 + 223 words and meets the
behavioral decision above; do not trade away its hard decision gates merely to reduce word count.

The plain-language revision at that point removed longer invented labels but retained
Approve/Comment/Wait. The later no-status decision below supersedes that output contract. Historical
percentages must not be rescored as new model evidence after changing the rubric.

### PR-review no-status decision

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

### PR-review partial-facts decision

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
three-state contract. Some reports still omitted
numeric diff or production/test split, so this supports the partial-facts boundary only, not overall
review quality or broad generalization.

The `with_skill` arm reads `skills/<name>/` directly, so an eval always measures the shipped
skill. `evals/baselines/` holds frozen older variants to compare against — the only skill text
this directory keeps a copy of.

Run outputs are ignored by git: they are large, model-specific, and regenerable by re-running.
Keep the conclusion in the skill and in the commit message, not the transcripts.

### Review-feedback compression decision

The full arm is frozen at `0685def7c43dc8a3f16944bc3804c1871583f504`; only the
shipped skill changes. Adopt the compressed arm only when it is at most 820 words, its total
score is not below the full arm in either the nine-case regression suite or the unseen holdout,
and edit-gate, owner-level end state, false-suggestion-not-implemented, and acceptance counts
are each no lower in either suite. Otherwise restore the frozen full skill.

### Review-feedback structural compression decision

The baseline is the complete scope-aware skill at
`fd4056164c7c7c618db5c4cc45f1d4cc3cb599df`. Compare it with the shipped skill on
all twelve review-feedback fixtures, two paired repetitions each, using GPT-5.6 Luna
with high reasoning. One pair is one fixture and repetition. Its score is the fraction
of deterministic expectations passed, so fixtures have equal weight.

Adopt the candidate only when it is no more than 1,195 words (at least 35% shorter),
all local tests pass, and the one-sided 90% paired-bootstrap lower bound for
`candidate - baseline` is above the non-inferiority margin of -0.03. In addition, the
candidate must not reduce the aggregate counts for the edit gate, owner-level end
state, rejection of false suggestions, acceptance behavior, or cumulative-diff scope
cleanup. Otherwise keep the baseline.

If a candidate clears the score bound but misses exactly one hard gate, a wording-only
correction may use one additional all-fixture repetition. Adopt it only when that run's
total score and every hard-gate count are no lower than its paired baseline; do not add
more repetitions.

## Reading a result

Report the metric, the number of reps per arm, and the model. A difference that a handful of
reps cannot resolve is not a result — say so instead of picking the flattering direction.
Free-text reports are the hard case: regex scoring and model scoring disagree on the same
report often enough that a scoring method has to be stated alongside the number.
