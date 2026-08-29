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

## Skill suites

Each skill owns its suite-specific fixtures, commands, baselines, decisions, results, and limits.
This file documents only the shared harness.

| Skill | Evaluation record | Case definitions |
| --- | --- | --- |
| `pr-review` | [PR Review evals](pr-review/README.md) | [`pr_review_cases.py`](pr_review_cases.py) |
| `review-feedback` | [Review Feedback evals](review-feedback/README.md) | [`review_feedback_cases.py`](review_feedback_cases.py) |

The remaining fixtures currently exercise `tdd` (`cartlib`), `debug` (`pricer`, `reportlib`),
and `simplify-audit` (`feedhub`). A fixture is an exam paper, not a library: its value is the
specific mistakes an agent can make in it. Findable items alone measure eagerness; traps and open
questions are what separate judgment from enthusiasm.

## Run

Run commands from the repository root:

```bash
python3 evals/runner.py --dry-run
python3 evals/runner.py --provider pi --reps 1
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite <suite> --reps <n>
python3 evals/grader.py
```

The runner writes model-specific workspaces under `evals/<skill>-workspace/`. Those outputs are
ignored by Git and can be regenerated. Keep durable conclusions in the corresponding skill eval
record and in the commit message, not in raw transcripts.

## Read a result

Report the metric, repetitions per arm, and model. A difference that a handful of repetitions
cannot resolve is not a result. Free-text reports are especially sensitive to the scoring method,
so state whether the score came from deterministic assertions, regexes, or model review.
