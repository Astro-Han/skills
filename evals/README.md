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
python3 evals/grader.py                            # scores those runs
```

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

## Reading a result

Report the metric, the number of reps per arm, and the model. A difference that a handful of
reps cannot resolve is not a result — say so instead of picking the flattering direction.
Free-text reports are the hard case: regex scoring and model scoring disagree on the same
report often enough that a scoring method has to be stated alongside the number.
