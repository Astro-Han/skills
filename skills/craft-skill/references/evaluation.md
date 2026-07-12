# Evaluate a skill

Evaluation earns its cost only when it can change a named decision. Before running anything, record:

- the decision;
- the primary success criterion and evaluation unit;
- the candidate and fair baseline;
- how a supporting, refuting, insufficient, or invalid result changes the next action.

If these are not actionable, do not evaluate.

## Protect the comparison

Change only the skill version. Keep the task, inputs, model, tools, permissions, and relevant environment equal. Snapshot an old skill before editing it; use separate fresh contexts and isolated output directories. Give executors raw task-local inputs, not the author's diagnosis, expected answer, or intended fix. Remove artifacts that a later run could discover.

Set criteria, evaluation units, and aggregation before viewing outputs. Keep the blind-review answer key outside the reviewer's accessible package, and use a reviewer that did not observe the executions. Blinding labels cannot repair a reviewer whose context already reveals the variants.

Cases used to produce a revision cannot alone validate it. Use untouched holdout cases or new cases before claiming a general improvement.

## Choose discriminating evidence

Use the least expensive evidence that can overturn the decision.

| Decision | Evidence |
| --- | --- |
| Will an automatically invoked skill be called correctly? | Realistic should-call and close should-not-call prompts; skip for explicit-only platforms |
| Does a skill improve an objective artifact or behavior? | Paired baseline/candidate runs with predeclared assertions from an independent source of truth |
| Could stochastic variance reverse the choice? | Repeat paired runs, retain raw results, and summarize only the predeclared metric |
| Is quality comparative but not objective? | Identity-blind review against criteria fixed before the outputs are seen |
| Does a discipline skill survive incentives to bypass it? | A realistic failure-eliciting scenario using only pressures the real task contains; record observed rationalizations, then vary the scenario |
| Is the output equal but the process wasteful? | Inspect transcripts for instructions that cause wasted work or operations repeatedly reimplemented across cases |
| Is stronger comparison unavailable? | Run the skill on a real task and ask the user to judge the artifact; state the evidence limit |

Do not force a winner. Classify the result as supporting, refuting, insufficient, or invalid. Stop according to the predeclared decision rule, not because a report looks complete.

## Deterministic helper

`scripts/eval.py` automates only operations an agent should not recreate ad hoc.

An evaluation manifest names one decision, one numeric metric, the baseline and candidate, and paired values:

```json
{
  "decision": "Adopt the candidate only if it improves task score.",
  "comparison": {"baseline": "baseline", "candidate": "candidate"},
  "metric": {"name": "task score", "direction": "higher"},
  "runs": [
    {"case_id": "case-1", "variant": "baseline", "value": 0},
    {"case_id": "case-1", "variant": "candidate", "value": 1}
  ]
}
```

Run from the skill directory:

```bash
python scripts/eval.py validate eval.json

python scripts/eval.py blind baseline-output candidate-output \
  --review-dir review-pack \
  --key private/answer-key.json

python scripts/eval.py summarize eval.json
```

`summarize` reports the variants' means, sample standard deviations when repeated values exist, and direction-adjusted paired improvement. It does not choose metrics, combine unlike cases, claim significance, or select a winner.
