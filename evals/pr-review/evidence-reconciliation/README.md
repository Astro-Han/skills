# Evidence-Reconciliation Diagnostic

This development-only A/B test asks whether one sentence can stop a reviewer from dropping concrete
production evidence during the final verdict. It does not validate a general improvement and cannot
support a public percentage claim because every case was opened before the candidate was written.

## Frozen comparison

The baseline is the PR Review Skill at `e28f7da5a9503ec0a93c4db86108d6e8f222fd7d`.
The candidate replaces the existing evidence-gate sentence in `Report only real findings` and changes
nothing else.
Both arms use GPT-5.6 Luna with high reasoning, the same frozen PR material, tools, permissions, and
prompt. Eight cases run twice per arm: four known core-finding failures and four clean or intentional
rollback controls.

The primary unit is a run where the transcript itself contains concrete production-path evidence
that contradicts the intended behavior. The final verdict must either report the smallest justified
finding or explain why that evidence is inapplicable, pre-existing, intentionally restored, or
unreachable. Search breadth alone does not count as improvement.

[`decision.json`](decision.json) freezes the gates and definitions. [`selection.json`](selection.json)
freezes the cases and their diagnostic roles.

## Interpretation

Passing every gate only permits a new evaluation on untouched real PRs. It does not permit changing
the shipped Skill. A mechanism failure rejects this wording and stops further prompt accumulation;
only then should a separately justified tool-level evidence ledger be considered.

## Result

The `evidence-reconciliation-luna-high-v1` diagnostic rejected the candidate. All 32 runs completed
and read their isolated Skill arm. Two blind scorers independently agreed on every required-finding
match: the baseline matched three of eight positive runs and the candidate matched one. Both matched
`grafana-pr-127578-r2`; the baseline alone matched `grafana-pr-127578-r1` and
`pydantic-pr-13503-r1`; the candidate had no unique match.

The candidate also failed the intended mechanism. Under the broader transcript reading, it resolved
6 of 12 observed contradictions versus 9 of 13 for the baseline; under the stricter gold-only
reading, it resolved 8 of 9 versus 11 of 11. Both scorers found fewer decision-ready candidate
reviews. Median commands grew 8.6 percent and final output shrank 7.2 percent, while median token use
grew 27.1 percent.

The development cases cannot validate general improvement, but they can reject this wording: it did
not recover a core finding, lost two baseline findings, and did not improve evidence reconciliation.
The candidate sentence has therefore been removed and no fresh holdout was run. The next experiment,
if pursued, must test a tool-level mechanism without creating a second review authority.

[`results/evidence-reconciliation-luna-high-v1.json`](results/evidence-reconciliation-luna-high-v1.json)
contains the scores, cost diagnostics, gates, disagreements, and adoption decision.
