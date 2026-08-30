# Cross-Type PR Review Capability

This evaluation tests whether a method-level rewrite improves core review capability across different
pull-request types without increasing the Skill's words, sections, resources, scripts, states, review
authorities, false positives, severity inflation, or review cost materially.

## Frozen comparison

The baseline is the PR Review Skill at `1095a1c3a7ce59c7b5a5b489d934b629a4b5f4a2`.
The candidate rewrites existing problem, production-path, and simplification guidance around a
falsifiable production contract, its responsible owner, and the shortest supported path that could
prove the solution wrong. Both versions contain 743 words, six body sections, one conditional
reference, no scripts, no new stored state, and one final review authority.

The candidate must be committed before any selected PR implementation is opened. Thirty-two unique
real PRs each run once per arm with GPT-5.6 Luna/high: sixteen independently proven positive cases
and sixteen clean or intentional-tradeoff controls, spread evenly across eight change types. Repeated
runs of the same arm and PR are excluded in favor of more repositories, stacks, and change shapes.

[`decision.json`](decision.json) freezes the sample, gold requirements, capability metrics, safety
gates, cost limits, and interpretation before case selection.

## Evidence boundary

Later reverts, follow-up fixes, reports, or production failures may identify candidate PRs, but a
required finding counts only when the frozen fixture itself contains a supported entry, responsible
owner, observable consequence, and reachable evidence. Hindsight alone is not gold. Case selection
and independent gold begin only after the candidate commit is frozen.

The repository stores only [`gold-attestation.json`](gold-attestation.json). The answer key remains
outside the executor workspace. Repository pool snapshots are supplemented only with exact metadata
for older in-window candidates found through later failure signals; the later evidence is excluded
from fixtures and gold review.
