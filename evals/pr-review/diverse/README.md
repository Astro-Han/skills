# Diverse Real-PR Holdout

This evaluation asks whether `pr-review` improves review quality across repositories, languages,
product shapes, and maintainer styles. It does not revise the Skill from any selected case.

## Frozen decision

Do not claim a general improvement unless an untouched 24-PR holdout improves decision-critical
finding recall or decision-ready conclusions without increasing unsupported P1/P2 findings. Keep
recall, unsupported findings, and decision readiness as separate metrics. A result that improves
only calibration supports only that narrower claim.

The executor comparison keeps the model, reasoning, prompt, repository snapshot, tools, and
permissions equal. The only arm difference is the isolated Skill. Use GPT-5.6 Luna at high
reasoning for the first comparison. Do not change the Skill after opening holdout code, gold, model
outputs, or transcripts.

## Candidate population

[`selection-policy.json`](selection-policy.json) freezes nine repositories, the 2026-05-30 through
2026-08-29 window, deterministic seed, metadata exclusions, 60 candidate slots, and 24 final slots.
The repositories cover agent software, package management, web applications, mature frameworks,
networking, editor state, product UI, native UI, and data validation.

Machine selection includes only merged, non-draft, non-bot PRs with 20-500 changed lines and at
most 20 changed files. It excludes dependency bumps, releases, backports, translations, mechanical
upstream Vim patches, documentation-only titles, and every case already used to design or assess
the Skill. These rules select reviewable candidates;
they do not assert that a candidate has a valid answer key.

Capture each repository's latest 200 PR metadata records in the frozen date window, then make the
deterministic 60-case candidate list:

```bash
python3 evals/pr-review/real_fixture.py capture-pool \
  --repo OWNER/REPO --created-from 2026-05-30 --created-to 2026-08-29 \
  --limit 200 \
  --output evals/pr-review/diverse/pools/OWNER--REPO.json

python3 evals/pr-review/real_fixture.py select-diverse \
  --pool evals/pr-review/diverse/pools/OWNER--REPO.json \
  --policy evals/pr-review/diverse/selection-policy.json \
  --output evals/pr-review/diverse/candidates.json
```

Pass all nine `--pool` arguments to `select-diverse`. The checked-in output records every pool
digest. This is a deliberately bounded candidate population, not a prevalence estimate for all PRs
merged by these projects in the period.

## Independent curation and gold

Two reviewers who did not design the Skill independently inspect all 60 candidates without seeing
A/B outputs. For each candidate they record:

- whether the problem and production path are recoverable from frozen public evidence;
- whether a required finding or clean conclusion can be justified independently;
- whether the case adds a distinct repository, problem type, or review style;
- whether domain knowledge, generated code, or missing history prevents reliable grading.

Reconcile only eligibility and evidence quality first. Freeze 24 cases using the repository quotas
in the policy, while retaining roughly one quarter clean cases and avoiding repeated versions of
the same defect. Required findings need a reachable trigger, observable consequence, reproduction,
code evidence, and calibrated severity. Store private answer keys outside executor workspaces.

Cases opened to change the Skill become development cases and must be replaced by untouched
holdouts. Repeated executions measure model variance; they never replace independent PRs.

## Frozen selection

Two independent reviewers assessed all 60 candidates before any new A/B execution. They agreed on
35 eligible and 17 ineligible cases and disagreed on eight. Reconciliation retained 24 cases at the
predeclared repository quotas; both reviewers then reported no hard obstacle to building reliable
gold for the final list. [`selection.json`](selection.json) records the selected IDs, input digests,
review-report digests, and agreement counts without exposing findings.

Verify its input identities, membership, uniqueness, and repository quotas before capture:

```bash
python3 evals/pr-review/real_fixture.py verify-diverse-selection \
  --candidates evals/pr-review/diverse/candidates.json \
  --policy evals/pr-review/diverse/selection-policy.json \
  --selection evals/pr-review/diverse/selection.json
```

The selection is not yet runnable evaluation evidence. The next gate is two independent private
answer keys for all 24 cases, followed by reconciliation and immutable case capture. Do not inspect
model outputs or change the Skill while preparing those keys.

Each selected case is captured with `real_fixture.py capture` under [`cases/`](cases/). Verify every
manifest and patch digest and require the captured `(repository, PR number)` set to equal the frozen
selection:

```bash
python3 evals/pr-review/real_fixture.py verify-diverse-cases \
  --cases-root evals/pr-review/diverse/cases \
  --selection evals/pr-review/diverse/selection.json
```

After reconciled private gold is frozen, place one local Git cache per repository under a cache
root using the `OWNER--REPO` directory name. Preview the exact 48-run plan before execution:

```bash
python3 evals/runner.py --provider codex --model gpt-5.6-luna \
  --suite pr-review-diverse --reps 1 --iteration diverse-luna-high-v1 \
  --repo-cache-root /path/to/cache-root --dry-run
```

Remove `--dry-run` only after the gold gate is complete. The runner materializes each case from its
own repository cache and keeps the same isolated Skill/no-Skill boundary as the first real-PR suite.

Before any model call, verify that every frozen patch applies to its repository's historical
production tree:

```bash
python3 evals/pr-review/real_fixture.py verify-diverse-materialization \
  --cases-root evals/pr-review/diverse/cases \
  --repo-cache-root /path/to/cache-root
```

The private gold gate is complete. Two independent reviewers reconciled 24 answer keys before any
A/B output existed: 21 clean cases and three required findings (two P1, one P2). A second reviewer
validated every key and the final reconciliation. [`gold-manifest.json`](gold-manifest.json)
records counts, attestations, Skill hashes, and the canonical private-gold digest without exposing
the answer keys.

## First paired execution

The `diverse-luna-high-v1` execution completed all 48 model calls without runner failures. The
candidate loaded only the isolated Skill in 24/24 runs, the baseline loaded it in 0/24, and neither
arm could see the user-level Skill. Two reviewers built and reconciled gold before outputs were
opened, then independently scored randomized A/B outputs. They agreed on the decision-critical
metrics after reconciling one decision-readiness judgment.

| Metric | With Skill | Without Skill | Paired result |
| --- | ---: | ---: | --- |
| Required finding recall | 1/3 | 2/3 | one fewer finding |
| Responses with unsupported P1/P2 | 8/24 | 11/24 | 3 wins, 0 losses, 21 ties |
| Unsupported P1/P2 claims | 8 | 12 | 4 wins, 0 losses, 20 ties |
| Decision-ready reviews | 14/24 | 11/24 | 3 wins, 0 losses, 21 ties |

The Skill again improved review discipline: it reduced unsupported high-severity findings and made
more conclusions usable for a merge decision. It did not improve core issue discovery. The Skill
arm missed a production text-result corruption in Maka #3958 that the baseline found; both arms
found the supported Tailscale #20673 race; and both missed the normal `:bcd` target-buffer regression
in Neovim #41328 after tracing the relevant production path.

This run therefore supports only a calibration and decision-quality claim. Three required findings
are too few to estimate a stable recall effect, but the lower observed recall blocks a claim that
the current Skill has proved better at discovering core bugs. Do not change the Skill from these
cases: they are now opened evaluation evidence. Diagnose the repeated production-transition miss,
then test any general method on new holdouts. The machine-readable record is
[`results/diverse-luna-high-v1.json`](results/diverse-luna-high-v1.json).
