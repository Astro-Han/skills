# TDD evals

## Problem

The observed failure mode of the shipped skill is over-testing: redundant and
low-value tests accumulate because the quality gate judges each test in isolation and
the REFACTOR step names only production code. Ten overlapping tests each pass the
single-test gate while nine are waste.

## Candidate revision

Two changes to `skills/tdd/SKILL.md`:

1. REFACTOR explicitly covers the test suite: delete or merge subsumed tests,
   including stepping-stone tests written to force generalization.
2. A suite-level bar in Test quality: keep the fewest tests that prove distinct
   obligations; delete a test whose deletion leaves every behavior still detected.

## Predeclared decisions

Declared before any run output was viewed.

- **Decision 1 (adopt the revision).** Compare `baseline_skill`
  (git 4220041, pre-revision) against `with_skill` (candidate) on the `tdd` suite,
  codex provider (`gpt-5.6-luna`, reasoning high), 3 reps. Adopt only if the
  candidate lowers mean `excess_tests` across the three cases without losing
  acceptance or the process expectations, with `kill_rate` not lower. The
  `without_skill` arm bounds what either skill buys at all.
- **Decision 2 (per-concept ablation).** For each variant in
  `evals/tdd/make_ablations.py`, compare against `with_skill` on the
  `tdd-ablation` suite, 2 reps. Delete a concept only when its removal does not
  degrade any predeclared metric on a case that can discriminate it; where no case
  exercises the concept, record insufficient evidence and keep the text unjudged.

## Metrics

`evals/tdd/metrics.py` generates single-site mutants of `cartlib/cart.py` and runs
each passing test against each mutant:

- `excess_tests` — passing tests beyond a greedy minimal cover of every mutant the
  suite can kill; the over-testing signal.
- `kill_rate` — killed/generated mutants; the guard against under-testing.
- `tests_added` — passing tests beyond the fixture's seeded count.

Deterministic per-run expectations stay in `grader.py`: the TDD process checks, the
acceptance scripts, and for `coupon-cluttered` the seeded-test cleanup checks
(garbage shapes deleted, duplicate families collapsed, final excess <= 1,
kill rate >= 0.75).

## Cases

- `coupon-feature` (cartlib): five distinct obligations; measures how many tests a
  fresh feature accretes.
- `remove-crash` (cartlib): minimal bug fix; measures restraint on a one-obligation
  change.
- `coupon-cluttered` (cartlib-cluttered): same feature request on a fixture whose
  suite already carries three duplicate tests and four garbage-shape tests around
  the code being touched; measures whether the agent cleans up what it touches.

## Known limits

- Mutants are generated from each arm's own final `cart.py`, so `kill_rate` is a
  normalized fraction over slightly different mutant sets across arms.
- The greedy cover picks one representative among equivalent tests arbitrarily;
  `excess_tests` counts are stable, membership of `redundant_tests` is not.
- Name-based cluttered checks assume the seeded test names are kept or deleted, not
  renamed; a legitimate merge under a new name can be misread. Judged acceptable
  because the metric expectation (`excess_tests <= 1`) does not depend on names.

## Results — round 1 (iteration `dedup-1`)

Revision 1 (suite-level bar sentence + REFACTOR-covers-tests sentence) was **refuted**:

- `excess_tests`, baseline → candidate: cluttered 9.33 → 8.67, coupon 2.0 → 2.33,
  remove 2.0 → 2.0. No adoption-rule improvement; acceptance and kill rate equal.
- `without_skill` added the fewest tests (coupon 5.0 vs 6.0+, excess 1.33 vs 2.0+):
  the skill text itself pushes toward extra tests relative to no skill.
- Cleanup of the seeded cluttered suite was bimodal, not concept-driven: 0/5 full-skill
  reps cleaned up, while single reps in `no-keep-gate`, `no-pure-refactors`, and
  `no-before-red` arms independently deleted all seeds (excess 2–3). The model can do
  the cleanup; principle-style text does not reliably trigger it.
- Ablations: `no-suite-bar` and `no-test-refactor` matched the full skill on every
  metric — both round-1 additions measured inert and were removed. `no-refuse-shapes`
  and `no-closing` degraded cluttered excess (10.0 vs 9.0) — both earn their place.
  `no-before-red`, `no-keep-gate`, `no-pure-refactors`, `no-single-behavior`:
  insufficient evidence at 2 reps (differences inside the bimodal noise); kept.

## Round 2 — predeclared (iteration `dedup-2`)

Revision 2 replaces the two inert sentences with a procedural `## Finish` gate:
enumerate obligations, map tests one-to-one, delete the excess, report the mapping.

Declared before viewing any `dedup-2` output:

- **Adopt revision 2** only if, versus `baseline_skill` at 3 reps: mean cluttered
  `excess_tests` drops by more than 3 (reliable cleanup, not one lucky rep), coupon
  `excess_tests` and `tests_added` do not exceed baseline, and acceptance, process
  expectations, and kill rate hold.
- **Ablation** (2 reps, all variants regenerated from revision 2): same rule as
  round 1; `no-finish-gate` is the new discriminating variant.
- Caveat: the cluttered case informed revision 2, so `dedup-2` is design-set
  evidence; a claim of general improvement needs a fresh holdout case.
