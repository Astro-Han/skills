# Review Feedback Evals

Evaluation record for [`review-feedback`](../../skills/review-feedback/). Case definitions live in
[`review_feedback_cases.py`](../review_feedback_cases.py). Fixtures cover owner-level causes,
mirrored or obsolete representations, lifecycle rules, false findings, committed-state boundaries,
and compatibility obligations.

## Fixtures

| Fixture | Role | What it plants |
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

## Run

```bash
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-holdout --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-second-holdout --reps 6
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-final-holdout --reps 8
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-matrix --reps 5
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-compression --reps 3
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-compression-holdout --reps 5
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-structural-compression --reps 2
python3 evals/grader.py
```

## Compression decision

The full arm is frozen at `0685def7c43dc8a3f16944bc3804c1871583f504`; only the
shipped skill changes. Adopt the compressed arm only when it is at most 820 words, its total
score is not below the full arm in either the nine-case regression suite or the unseen holdout,
and edit-gate, owner-level end state, false-suggestion-not-implemented, and acceptance counts
are each no lower in either suite. Otherwise restore the frozen full skill.

## Structural compression decision

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
