# Core-Finding Recall Comparison

This evaluation decides whether one small wording change improves core correctness discovery without
weakening the shipped Skill's false-positive and severity calibration. It is a diagnostic enriched
sample, not an estimate of defect prevalence or a public percentage claim.

## Frozen decision

Compare the Skill at commit `e28f7da5a9503ec0a93c4db86108d6e8f222fd7d` with the candidate that
only replaces the existing interruption/retry/concurrency bullet. Keep the model, high reasoning,
prompt, tools, permissions, exact patch, and repository snapshot equal. Use GPT-5.6 Luna and one
fresh paired execution per case.

Adopt the candidate only if all of these hold on the frozen holdout:

- it matches at least two more required findings than the baseline and loses none that the baseline
  matches;
- responses containing unsupported P1/P2 findings do not increase;
- decision-ready reviews do not decrease;
- median commands and output length do not increase by more than 20 percent.

One net finding, mixed recall wins and losses, or too few reliable positive cases is insufficient.
Equal or lower recall, worse calibration, or materially more review work rejects the candidate.

## Sample boundary

Freeze sixteen real PRs from 2026-05-30 through 2026-08-29: eight with independently demonstrated,
decision-critical findings and eight nearby clean controls, spanning at least six repositories.
Prefer different languages, product shapes, and failure mechanisms. The positive set may be enriched
using later reverts, follow-up fixes, reproductions, or independently proven production failures;
therefore its finding rate must never be presented as representative.

Exclude every PR used to design, revise, or previously evaluate the Skill, including the 24-case
diverse holdout and the three opened trajectory cases. Freeze the candidate wording and this decision
before inspecting new PR code. Build gold before opening any model output. Each required finding needs
a supported production entry, observable consequence, exact code evidence, and calibrated severity.
Clean controls require an independent full review, not merely green CI or absence of later fixes.

Cases opened during selection or gold construction become development evidence and cannot validate a
later wording revision. If fewer than eight reliable positives can be obtained without relaxing the
gold standard, stop and report insufficient evidence rather than filling the set with speculative
findings.

## Scoring

Randomize arm labels independently per case. Score blind against private gold that executors cannot
access. Keep these metrics separate:

- required-finding recall and paired case wins/losses;
- responses and claims containing unsupported P1/P2 findings;
- decision-ready reviews;
- commands, tokens, duration, and final-output length as cost diagnostics.

The three already opened trajectory cases may be rerun only to confirm that the new instruction
changes the intended review behavior. They never count toward adoption.

## Result

The frozen `recall-luna-high-v1` comparison rejected the candidate. All 32 GPT-5.6 Luna/high runs
completed and read only their isolated Skill arm. Two blind scorers independently agreed on every
required-finding match and unsupported P1/P2 count before the arm labels were opened.

The baseline matched 3 of 8 required findings; the candidate matched 2. The candidate lost the
mutable-hash/cache finding in `pydantic-pr-13503` and added no required finding. Unsupported P1/P2
responses increased from 8 to 9, decision-ready reviews decreased from 6 to 5, and median command
count grew 23.5 percent. Median final-output length grew only 1.6 percent, so the extra work was in
exploration rather than reporting.

Trajectory inspection found the decisive failure: the candidate run for `pydantic-pr-13503`
constructed a production-shaped cache probe whose lookup changed from success to failure after
mutating the new hash input, but its final review still reported no code finding. The added question
therefore increased exploration without making contradictory evidence authoritative in the final
decision. Four possible gold gaps remain noted as limitations; even accepting all of them would
produce only one net candidate discovery with a baseline-only loss, which is still insufficient
under the frozen rule.

[`results/recall-luna-high-v1.json`](results/recall-luna-high-v1.json) contains the aggregate scores,
costs, gate decisions, trajectory evidence, and limitations. The candidate wording has been removed;
the Skill remains at the frozen baseline behavior.
