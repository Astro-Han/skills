# Causal synthesis experiment

## Decision

Replace the comment-queue workflow in `review-feedback` only if a system-first candidate
keeps adjudication quality while resolving accepted findings through their governing
authorities and produces a smaller coherent end state.

## Protected comparison

- Model: GPT-5.6 Luna, high reasoning.
- Baseline: current v3 at `af79986`.
- Candidate: the shipped skill on the experiment branch.
- Design case: `synthesize-digest-flows`.
- Unseen non-isomorphic holdout: `synthesize-shipment-flows`; do not execute it until a
  candidate is frozen.
- Unit: one fresh agent execution in an isolated fixture checkout.

The prompts contain raw shuffled review comments. They do not ask for a flowchart,
root-cause synthesis, batching, or repair slices.

## Predeclared behavior

Before the first production edit, a successful execution must:

1. publish the complete verdict ledger for this all-Verified design case;
2. reconstruct the relevant authorities from code and repository contracts rather than
   accepting proposed mechanisms as the starting design;

False and out-of-scope adjudication remain separate metrics in the structural suite. The
non-isomorphic holdout combines them with shared and independent repair pressures only
after the candidate is frozen.

The final artifact must pass hidden behavioral checks, including an unmentioned sibling
path, keep the existing tests green, and add no parallel mutable authority. File names,
group labels, and exact architectures are not scored.

## Diagnostic rule

Run two paired repetitions of the design case. Treat transcript structure as diagnostic;
the decision metric is adjudication, hidden sibling behavior, authority growth, and the
final end-to-end contract. Repetition cannot repair an invalid fixture.

## Candidate gate

After a candidate is frozen, compare it with the same v3 baseline on the design case,
then execute the untouched holdout. Adopt only if it improves the design case, handles
the holdout's opposite grouping and compatibility pressures, and causes no critical loss
on the existing 12-case structural suite. Do not tune the skill against holdout output.

## Initial result

The first narrow causal-synthesis comparison supported the system-first architecture
with limited confidence:

- two paired design runs improved from `6/10, 6/10` to `7/10, 10/10`; a later minimal
  confirmation pair tied `6/10`;
- three holdout pairs tied at `10/10`, showing no regression on the opposite grouping and
  live-compatibility case;
- one full structural pass averaged `86.2%` for v3 and `83.5%` for the candidate, a
  `-2.7` percentage-point delta inside the existing `-3%` non-inferiority margin;
- after tightening the shared-owner decision, the critical adjudication repeat produced
  `9/9, 5/9` for the candidate versus `9/9, 7/9` for v3. The loss did not repeat across
  both candidate runs, but the behavior remains stochastic.

This was directional evidence, not a statistical claim of solved behavior.

## Expanded cross-fixture result

The narrow result did not survive a broader paired comparison. On 2026-08-30, the frozen
candidate and the structural baseline were run twice on each of the twelve independent
review-feedback fixtures using GPT-5.6 Luna with high reasoning: 24 paired samples and
48 model executions, with no runner failures.

- baseline mean: `91.8%`;
- candidate mean: `80.9%`;
- paired mean delta: `-10.9` percentage points;
- paired outcomes: `5` wins, `4` ties, and `15` losses;
- one-sided 90% paired-bootstrap lower bound: `-16.2` percentage points, below the
  predeclared `-3%` non-inferiority margin.

The losses include artifact-level failures, not only transcript-format misses. Candidate
runs repeatedly patched API and importer callers instead of the shared domain owner,
failed hidden owner-level acceptance, and in one cumulative-diff run retained and expanded
the out-of-scope policy, registry, and transport changes. Therefore the candidate is
refuted by the current gate and must not be adopted as the shipped skill.

These twelve fixtures are now design evidence for the next revision. Freeze any revised
candidate before evaluating fresh multi-comment holdouts; rerunning only these observed
fixtures cannot establish generalization.

## Stable-base revision

Two compressed rewrites were rejected before the final revision:

- the 1,191-word rewrite averaged `79.1%` against `91.4%` for the structural baseline;
  its paired delta was `-12.3` percentage points and its one-sided 90% lower bound was
  `-16.7` points;
- a 1,251-word v3-based revision averaged `86.3%` against `87.2%`; its paired delta was
  `-0.9` points, but the 90% lower bound was `-5.6` points and normalization failed at
  the caller layer in both repetitions.

The final candidate at `36021bb` instead keeps the complete structural baseline and changes
only the synthesis decision: possible groups remain hypotheses while each comment is
adjudicated, then the surviving claims are compared once and assigned a shared,
independent, or mixed repair shape.

On the same twelve fixtures and two repetitions, reusing the immediately preceding frozen
baseline executions and running 24 fresh candidate executions:

- baseline mean: `87.2%`;
- candidate mean: `90.3%`;
- paired mean delta: `+3.1` percentage points;
- paired outcomes: `7` wins, `13` ties, and `4` losses;
- one-sided 90% paired-bootstrap lower bound: `-0.1` percentage points, above the `-3%`
  non-inferiority margin;
- normalization and committed-boundary behavior passed both repetitions, while cumulative
  diff cleanup scored `10/10` and `9/10`.

After freezing the skill, two new multi-comment holdouts were revealed. `subscriptionflow`
mixes lifecycle, latest-revision projection, false runtime, speculative alias, and live
compatibility pressures. `policyflow` requires similar string symptoms to remain split
across email identity, case-sensitive external keys, display labels, and deployed
compatibility.

- fresh-holdout baseline: `35/40` expectations;
- final candidate: `39/40` expectations;
- the candidate passed both `subscriptionflow` runs at `10/10` and `policyflow` at
  `10/10, 9/10`;
- the single loss lowercased a case-sensitive bucket in one policy run; it passed the
  other independent run and therefore is stochastic residual risk, not a repeated
  deterministic regression under the predeclared rule.

The final candidate passes the behavioral causal-synthesis gate. It is 1,882 words and
therefore is not a successful compression candidate; adopt it only for the behavior
improvement, without claiming that the separate 35% compression objective was met.
