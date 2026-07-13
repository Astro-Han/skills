# Goal Writer Minimal-Contract A/B

## Decision

Adopt the candidate only if every holdout preserves the requested outcome, a decidable acceptance criterion, named false-completion exclusions, and necessary authorization boundaries, while reducing resident skill context or output redundancy.

Baseline: commit `5dce642`. Candidate: the change committed with this evaluation. Both variants used separate ephemeral Codex consult sessions with the same four-case batch and no tools. A third ephemeral Codex session reviewed anonymized outputs; candidate was A and baseline was B. Batching keeps cost bounded but means cases were not independent model runs.

## Holdouts

1. A complete inventory web-app v1 across desktop and mobile, with four named flows, explicit exclusions, and automated plus rendered evidence.
2. A production PostgreSQL unique-index approval package with six required artifacts and no authorization to execute production.
3. An intermittent high-concurrency duplicate-delivery investigation requiring falsifiable hypotheses, no attempt cap, and mechanism-level regression or stress evidence.
4. Independent accessibility PR production during a two-day window, with no invented count and explicit Git/PR authorization boundaries.

## Raw outputs

### Candidate (A)

1. `完成团队内部库存盘点 Web 应用的可用 v1：基于现有设计系统和本地 mock 数据，实现桌面与手机端的库存查看、搜索、编辑及错误恢复；以相关自动化检查全部通过，且实际渲染证据证明各目标流程在两类设备尺寸下可用、错误后可恢复为完成标准。不包含账号系统、云同步或部署。`
2. `Prepare the production PostgreSQL unique index on users.email by completing the duplicate-data report, migration, staging rehearsal, lock-time measurement, rollback steps, and approval package; completion requires evidence that the rehearsal succeeds, lock impact is measured, rollback is validated, and reviewers have the information needed to decide on execution. Do not execute the production migration without explicit approval.`
3. `调查高并发下的消息重复投递问题：基于日志、指标和最小实验持续形成并证伪假设，直至定位重复投递机制并实施修复；完成仅以回归或压力证据证明修复可阻止该机制且未破坏正常投递为准，未能复现或仅完成若干次尝试不算完成。`
4. `Within the two-day window, turn independent accessibility fixes from the queue into review-ready PRs, each based on the latest main branch and containing evidence that independently verifies its fix without relying on another PR. Do not merge, approve, release, force-push, or create stacked PRs unless a documented real dependency requires stacking.`

Lengths: 134, 432, 104, and 350 characters; 1020 total.

### Baseline (B)

1. `/goal 完成团队内部库存盘点 Web 应用的可用 v1，复用现有设计系统和本地 mock 数据，支持桌面与手机上的库存查看、搜索、编辑及错误恢复；完成以相关自动化检查全部通过，且实际渲染证据证明上述流程在桌面与手机视口均可用为准。不实现账号系统、云同步或部署。`
2. `Goal: Prepare a production PostgreSQL unique index on users.email, including the duplicate-data report, migration, staging rehearsal, measured lock time, rollback steps, and approval package. Complete when the package demonstrates that the migration succeeds in staging, its operational impact and rollback are documented, and it is ready for authorized production review. Do not execute the production migration.`
3. `/goal 调查并修复高并发下的消息重复投递问题：基于日志、指标和最小实验形成可证伪假设，定位导致重复投递的机制并实施修复；完成以回归测试或压力测试证据验证该机制已被阻断且未破坏正常投递为准。未能复现或仅增加观测手段不算完成，不预设尝试次数。`
4. `Goal: During the two-day window, turn the queue of independent accessibility fixes into review-ready PRs, each based on the latest main branch and independently verifiable with relevant automated checks and rendered or assistive-technology evidence. Do not merge, approve, release, force-push, or create stacked PRs unless a real dependency requires stacking and is documented.`

Lengths: 132, 413, 121, and 377 characters; 1043 total.

## Blind review and adjudication

The blind reviewer passed A in all four cases, passed B in cases 1, 3, and 4, and preferred B/A/A/A respectively. It failed B in case 2 because B documented rather than validated rollback.

That failure is rejected on source comparison: the holdout required rollback steps to be ready, not validated. B satisfies the stated requirement; A adds a stricter condition. The adjudicated result is therefore:

- both variants pass all four holdouts;
- baseline is preferred in cases 1 and 2;
- candidate is preferred in cases 3 and 4;
- candidate output is 2.2% shorter in aggregate;
- resident `SKILL.md` shrinks from 3173 to 2284 characters (28.0%) and from 470 to 334 words (28.9%).

This evidence supports semantic non-inferiority and better context efficiency for these holdouts. It is not a statistical claim; fresh cases or repeated runs could change the comparative output result.
