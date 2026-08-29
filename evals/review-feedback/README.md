# Review Feedback Evals

Evaluation record for [`review-feedback`](../../skills/review-feedback/). Case definitions live in
[`review_feedback_cases.py`](../review_feedback_cases.py). Fixtures cover owner-level causes,
mirrored or obsolete representations, lifecycle rules, false findings, committed-state boundaries,
and compatibility obligations.

## Fixtures

| Fixture | Original role | What it plants |
| --- | --- | --- |
| `quoteview` | regression | Two local-patch suggestions with one domain-owner cause, plus one false finding and a nonstandard severity scale. |
| `seatmap` | holdout | Two synchronization suggestions caused by mirrored state, plus a false zero-capacity finding. |
| `handlekit` | holdout | Two caller-level case-folding suggestions whose rule belongs in one canonicalizer. |
| `profilefmt` | holdout | Two synchronization suggestions caused by an obsolete legacy representation. |
| `jobflow` | holdout | Two caller-level history patches whose lifecycle rule belongs in one transition owner. |
| `batchplan` | second holdout | Two local clamp suggestions whose policy belongs in one normalizer, plus a false empty-sum finding. |
| `wireview` | second holdout | Two exporter patches whose representation belongs to the wire-contract owner. |
| `launchmode` | second holdout | Two synchronization patches caused by an obsolete toggle that should be deleted. |
| `cartsummary` | final holdout | A real stale-result symptom whose proposed fix would preserve an obsolete derived cache. |
| `transferlog` | compression holdout | A shared domain invariant whose violation reaches externally committed state and must remain P1. |
| `credrotate` | compression holdout | A compatibility representation with a live deployed reader that must be preserved at one lifecycle owner. |
| `mediathread` | cumulative-diff regression | A second review round that must retain owner-level fixes while removing adjacent scope expansion. |

## Run

```bash
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-structural-compression --reps 2
python3 evals/grader.py
```

## Current decision

The baseline is the complete scope-aware skill at
`fd4056164c7c7c618db5c4cc45f1d4cc3cb599df`. Compare it with the shipped skill on
all twelve review-feedback fixtures, two paired repetitions each, using GPT-5.6 Luna
with high reasoning. One pair is one fixture and repetition. Its score is the fraction
of deterministic expectations passed, so fixtures have equal weight.

Adopt the candidate only when it is no more than 1,195 words (at least 35% shorter),
all local tests pass, and the one-sided 90% paired-bootstrap lower bound for
`candidate - baseline` is above the non-inferiority margin of -0.03. Track the edit
gate, owner-level end state, rejection of false suggestions, acceptance behavior, and
cumulative-diff cleanup separately, but do not treat one discordant pair as a regression.
A critical behavior blocks adoption only when the inspected artifact proves a
deterministic violation, or the same expectation loses to its paired baseline in at
least two independent runs and has more paired losses than gains. Otherwise the
predeclared non-inferiority result controls the decision; do not add repetitions to
chase a perfect count.

Earlier staged comparisons are retained in Git history rather than as parallel runner paths. This
12-case comparison is the sole current review-feedback gate.
