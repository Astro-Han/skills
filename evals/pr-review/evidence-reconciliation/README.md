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
