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
