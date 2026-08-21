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
| `feedhub` | `simplify-audit` | Seven removable concepts, four traps that must survive, and one open product question that must be escalated rather than deleted. |

A simplification fixture needs all three kinds. Findable items alone measure eagerness; the
traps and the open question are what separate judgment from enthusiasm.

## Running one

```bash
python3 evals/runner.py --dry-run                  # list the planned runs, no model calls
python3 evals/runner.py --provider pi --reps 1     # writes evals/<skill>-workspace/iteration-1/...
python3 evals/grader.py                            # scores those runs
```

Run outputs are ignored by git: they are large, model-specific, and regenerable by re-running.
Keep the conclusion in the skill and in the commit message, not the transcripts.

## Reading a result

Report the metric, the number of reps per arm, and the model. A difference that a handful of
reps cannot resolve is not a result — say so instead of picking the flattering direction.
Free-text reports are the hard case: regex scoring and model scoring disagree on the same
report often enough that a scoring method has to be stated alongside the number.
