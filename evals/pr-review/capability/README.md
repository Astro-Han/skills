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

## Result

The `capability-luna-high-v1` comparison produced 28 reliable paired reviews after excluding two
fixture materialization failures and two Skill-path contamination cases. On the remaining 15
positive cases, the baseline found a required problem in 8 cases (53.3 percent) and the candidate in
12 (80.0 percent). The candidate had five unique wins and one loss, spanning five change types and
four repositories. Its one-sided paired sign test gives `p = 0.109375`, enough for the user's chosen
80-percent directional threshold but not a 95-percent claim.

The result is not a perfect-reviewer claim. Unsupported P1/P2 findings and severity overgrades each
increased by one, while decision-ready reviews rose from 21 to 24, valid simplification advice rose
from 4 to 6, harmful simplification advice stayed at 2, median commands rose 2.0 percent, and token
cost fell. The frozen all-gates rule therefore did not pass. After seeing the complete blinded
comparison, the user chose internal adoption because the decision is which version is more likely
to find core problems, with complex reviews using independent angles and one final adjudicator to
manage reviewer variance.

[`results/capability-luna-high-v1.json`](results/capability-luna-high-v1.json) preserves the paired
cases, calibration and cost metrics, failed frozen gates, exclusions, evidence hashes, decision
threshold, and limits. Do not present its 50-percent relative gain as a universal or
95-percent-confidence effect.
