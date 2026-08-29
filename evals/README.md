# Evals

Paired A/B evidence for selected skills in this repository. A skill change is not done because
it reads better; it is done when a predeclared comparison says the agent got better at the job.

## The three pieces

| Piece | What it does |
| --- | --- |
| `runner.py` | Run one named suite against isolated fixture copies and retain each arm's transcript, workspace diff, and test result. Providers own CLI invocation, skill injection, transcript parsing, and any provider-specific suite support. |
| `grader.py` + `acceptance/` | Parse a run and persist its expectation ledger. Acceptance scripts verify resulting workspaces where a case has executable behavior. |
| `skills/craft-skill/scripts/eval.py` | Independently validate and summarize a numeric paired manifest, or build a blind review pack. The runner and grader do not generate that manifest. |

The runner and grader compose directly. The manifest tool is a separate boundary for comparisons
that have already assigned one declared value to each arm. Nothing here judges a skill by reading it.

## Skill suites

Each skill owns its suite-specific fixtures, commands, baselines, decisions, results, and limits.
This file documents only the shared harness.

| Skill | Evaluation record | Case definitions |
| --- | --- | --- |
| `pr-review` | [PR Review evals](pr-review/README.md) | [`pr_review_cases.py`](pr_review_cases.py) |
| `review-feedback` | [Review Feedback evals](review-feedback/README.md) | [`review_feedback_cases.py`](review_feedback_cases.py) |

The remaining executable suites exercise `tdd` (`cartlib`) and `debug` (`pricer`, `reportlib`).
The `debug` suite currently supports Claude only. A fixture is an exam paper, not a library: its value is the
specific mistakes an agent can make in it. Findable items alone measure eagerness; traps and open
questions are what separate judgment from enthusiasm.

## Run

Run commands from the repository root:

```bash
python3 evals/runner.py --provider claude --suite debug --reps 1 --dry-run
python3 evals/runner.py --provider pi --suite tdd --reps 1
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite <suite> --reps <n>
python3 evals/grader.py
```

The runner writes each arm under
`evals/<workspace>/<iteration>/<case>-r<rep>/<arm>/`. Reuse an iteration name only when replacing
that run intentionally. Outputs are ignored by Git and can be regenerated. Keep durable conclusions
in the corresponding skill eval record and in the commit message, not in raw transcripts.

## Read a result

Report the metric, repetitions per arm, and model. A difference that a handful of repetitions
cannot resolve is not a result. Free-text reports are especially sensitive to the scoring method,
so state whether the score came from deterministic assertions, regexes, or model review.
