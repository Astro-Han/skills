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

## Results

Recorded after grading; see the corresponding commit messages.
