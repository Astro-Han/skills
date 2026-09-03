# Review Feedback Evals

The experimental multi-flow synthesis gate and its predeclared decision rule live in
[`causal-synthesis.md`](causal-synthesis.md). It is isolated from the shipped 12-case
structural-compression gate below.

Evaluation record for [`review-feedback`](../../skills/review-feedback/). Case definitions live in
[`review_feedback_cases.py`](../review_feedback_cases.py). Fixtures cover owner-level causes,
mirrored or obsolete representations, lifecycle rules, false findings, committed-state boundaries,
and compatibility obligations.

## Fixtures

| Fixture | Original role | What it plants |
| --- | --- | --- |
| `quoteview` | regression | Two local-patch suggestions with one domain-owner cause, plus one false finding and a nonstandard severity scale. |
| `seatmap` | holdout | Two synchronization suggestions caused by mirrored state, plus a false zero-capacity finding. |
| `handlekit` | holdout | Two caller-level case-folding suggestions whose rule belongs in one canonicalizer. |
| `profilefmt` | holdout | Two synchronization suggestions caused by an obsolete legacy representation. |
| `jobflow` | holdout | Two caller-level history patches whose lifecycle rule belongs in one transition owner. |
| `batchplan` | second holdout | Two local clamp suggestions whose policy belongs in one normalizer, plus a false empty-sum finding. |
| `wireview` | second holdout | Two exporter patches whose representation belongs to the wire-contract owner. |
| `launchmode` | second holdout | Two synchronization patches caused by an obsolete toggle that should be deleted. |
| `cartsummary` | final holdout | A real stale-result symptom whose proposed fix would preserve an obsolete derived cache. |
| `transferlog` | compression holdout | A shared domain invariant whose violation reaches externally committed state and must remain P1. |
| `credrotate` | compression holdout | A compatibility representation with a live deployed reader that must be preserved at one lifecycle owner. |
| `mediathread` | cumulative-diff regression | A second review round that must retain owner-level fixes while removing adjacent scope expansion. |
| `digestflow` | causal-synthesis design | Shuffled findings whose owner-level fixes must also cover an unmentioned sibling path without adding parallel identity or fallback state. |
| `shipmentflow` | causal-synthesis holdout | A non-isomorphic identity case: two findings share an email owner, display names require a separate rule, and a live compatibility field must remain. |
| `subscriptionflow` | fresh causal holdout | Mixed lifecycle, latest-revision projection, false runtime, speculative alias, and live renewal compatibility pressures. |
| `policyflow` | fresh causal holdout | Similar string symptoms whose email, external-key, display, and deployed compatibility contracts require different owners. |

## Run

```bash
python3 evals/runner.py --provider codex --model gpt-5.6-luna --suite review-feedback-structural-compression --reps 2
python3 evals/grader.py
```

## Current decision

The baseline is the accepted five-stage behavior before workflow compression at
`36021bbfa0fed9b63b7a286bf48d83264aad4417` (1,882 words). Compare it with the shipped skill on
all twelve review-feedback fixtures, two paired repetitions each, using GPT-5.6 Luna
with high reasoning. One pair is one fixture and repetition. Its score is the fraction
of deterministic expectations passed, so fixtures have equal weight.

Adopt the candidate only when it is no more than 1,195 words (at least 35% shorter),
all local tests pass, and the one-sided 90% paired-bootstrap lower bound for
`candidate - baseline` is above the non-inferiority margin of -0.03. Track the edit
gate, owner-level end state, rejection of false suggestions, acceptance behavior, and
cumulative-diff cleanup separately, but do not treat one discordant pair as a regression.
A critical behavior blocks adoption only when the inspected artifact proves a
deterministic violation, or the same expectation loses to its paired baseline in at
least two independent runs and has more paired losses than gains. Otherwise the
predeclared non-inferiority result controls the decision; do not add repetitions to
chase a perfect count.

Earlier staged comparisons are retained in Git history rather than as parallel runner paths. This
12-case comparison is the sole current review-feedback gate.

## Compression round (iteration `compress-1`) — predeclared

The candidate rewrites `SKILL.md` at 1,194 words (baseline 1,882): the ledger keeps
four fields (verdict, severity, root cause and owner, outcome), the scope-relation
taxonomy folds into the multi-round section, duplicated admonitions collapse to one
each, the description is rewritten for triggering on plain "fix the review comments"
phrasings, and the multi-round bloat pattern (each round patching the prior round's
patches) is named directly with an explicit entropy requirement on repairs.

Decision, declared before any run: the standing 12-case gate above applies verbatim
(word cap met; adopt only on the -0.03 paired-bootstrap non-inferiority bound).
Additionally run `review-feedback-causal-holdout` (3 cases, 2 paired reps against the
`af79986` causal baseline): the candidate must not lose that comparison by more than
one expectation in total, since the rewrite compresses the causal-synthesis text the
holdout was built to protect. Trigger quality is observed via the grader's
`skill_triggered` field across all runs and must not drop below the baseline arm's
rate; a dedicated multi-skill trigger evaluation is out of scope here and recorded as
a limit.

### Round 1 (`compress-1`) — rejected

Structural, 24 pairs: mean paired diff **-0.144**, one-sided 90% bootstrap lower
bound **-0.190** — far outside the -0.03 gate. Triggering held at 24/24 in both arms.
The losses were behavioral, verified in the workspaces, and concentrated where the
compression turned imperative rules into narrative: `rebase-cumulative-diff`
(0.85 → 0.35; the candidate kept the drift files and superseded edits instead of
reverting them — the scope-relation taxonomy and the "revert unrelated drift and its
tests" imperative had been folded away) and `remove-mirrored-state` (1.0 → 0.61; a
local patch kept the mirrored cache — the "Fix locally is not an available outcome"
rule had been softened). Lesson, consistent with the tdd rounds: principle prose gets
skipped by the weak model; itemized imperatives and required fields are the executors.

### Round 2 (`compress-2`) — predeclared

The rewrite keeps the compressed architecture but makes the load-bearing rules
structural instead of narrative: **scope** becomes a required ledger field (required /
regression / unrelated drift / pre-existing) with a per-value action table ("revert it
and its tests now" for drift), and the mirrored-rule prohibition returns as a bolded
imperative. 1,166 words. Decision: identical gates to round 1 — the standing 12-case
non-inferiority gate, the causal holdout within one expectation, and triggering not
below baseline.

The causal-synthesis experiment may reuse this suite as a behavior-only non-inferiority
check. Passing that check does not satisfy or replace this compression gate; see
[`causal-synthesis.md`](causal-synthesis.md) for its separate decision.

## Five-stage workflow compression result

The 1,065-word candidate at `3ca212a` reorganized the skill into five explicit stages while
retaining the ledger, P0-P3, shared/independent/mixed synthesis, owner selection, and cumulative
diff rules in shorter form. It was frozen before evaluation and compared with `36021bb` in two
fresh paired repetitions of all twelve fixtures: 24 pairs and 48 GPT-5.6 Luna/high executions,
with no runner failures.

- baseline mean: `88.9%`;
- candidate mean: `77.5%`;
- paired mean delta: `-11.3` percentage points;
- paired outcomes: `4` wins, `4` ties, and `16` losses;
- one-sided 90% paired-bootstrap lower bound: `-15.9` percentage points.

The candidate followed the visible five-stage shape but repeatedly patched API/importer callers
instead of the shared owner, accepted disproved empty-value suggestions, and lost cumulative-diff
adjudication in both repetitions. These are artifact-level critical regressions, so the candidate
was rejected without running holdouts or adding repetitions and was reverted by `a60a15e`.

## Structure-only experiment

The next candidate isolates information architecture from compression. It may move complete
paragraphs, change heading levels, and add navigation headings, but it must preserve every
non-heading line from `36021bb` exactly. Word count is descriptive, not an adoption criterion.

Compare the frozen candidate with `36021bb` on the same twelve fixtures and two paired
GPT-5.6 Luna/high repetitions. Adopt only if the one-sided 90% paired-bootstrap lower bound is
above `-3%` and no critical behavior has a deterministic artifact failure or repeated paired loss:
owner-level repair, Push back for disproved findings, and cumulative-diff rebase. If this gate
passes, use new holdouts before claiming general improvement; do not tune wording against the
regression fixtures.

The structure-only candidate at `1ed9404` preserved every non-heading baseline line exactly and
added only fourteen heading words. Across 24 fresh pairs and 48 executions with no runner failures:

- baseline mean: `93.7%`;
- candidate mean: `94.0%`;
- paired mean delta: `+0.4` percentage points;
- paired outcomes: `5` wins, `16` ties, and `3` losses;
- one-sided 90% paired-bootstrap lower bound: `-2.0` percentage points.

The aggregate gate passed and cumulative-diff scores improved in both repetitions. The owner
submetric moved from `19/22` to `18/22`: two baseline-only passes and one candidate-only pass. One
normalization run used an incomplete owner contract; one compatibility run patched callers; the
candidate instead won one obsolete-toggle owner result. An initial strict reading of the
cross-fixture tripwire rejected the candidate and produced revert `02c3604`.

On review, that interpretation was too strong for the evidence. The overall comparison supports
non-inferiority, the owner difference is one result across 22 checks, the paired losses did not
repeat on the same fixture, and the baseline also failed the other compatibility repetition. Treat
the owner outcomes as residual stochastic risk rather than an established structural regression.
The structure-only candidate was accepted and restored by `da8bad0`; this result supports the
reordering on the evaluated suite but does not claim a general behavior improvement.
