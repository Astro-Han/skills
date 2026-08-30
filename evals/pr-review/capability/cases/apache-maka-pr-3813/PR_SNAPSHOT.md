# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3813 — `refactor(runtime-host): unify local deployment handoffs`
- Author: me2seeks
- Target base head: `10d2454147ea00a20ac36e4d840edde822bef50d`
- Comparison base: `10d2454147ea00a20ac36e4d840edde822bef50d`
- Exact source head: `3939cbffee3d7153c3ff38082176e6a0634e49b5`
- Diff: 226 additions, 169 deletions, 5 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

- generalize the durable local authority from owner-only transfer to one deployment handoff that supports both owner-preserving replacement and cross-owner transfer
- remove the direct `select` transition so an owned deployment cannot change without the handoff transaction
- rename the local-process coordinator and its recovery states around the shared handoff contract
- cover same-owner replacement, cross-owner transfer, retry, rollback, stale revision, and serialized cutover

## Why

#3769 delivered the serialized local-process transaction, but intentionally required different installation owners. Installed npm CLI upgrades in #3243 also need to replace a deployment while retaining the same persistent owner.

A separate same-owner replacement transaction would duplicate the durable state, authority lock, cutover phases, and crash-recovery rules. This change keeps one physical sequence for both cases:

1. stage and verify the exact target;
2. persist handoff intent under the account-local authority lock;
3. retire or re-observe the selected Host;
4. observe sole-writer release;
5. activate and verify exact Ready evidence;
6. commit the target deployment and resulting owner.

The owner may stay the same or change. No source-specific CLI, Desktop, `npx`, managed-service, remote-operator, or presentation policy is added here.

## Simplification and first-principles audit

**GO.** The final diff adds no authority, lock, journal, or state kind. It removes the uncoordinated `select` path and makes the existing transaction deep enough for both owner-preserving and cross-owner handoffs. A selected deployment can now change only at initial claim, verified handoff commit, or explicit rollback.

## Verification

- `npm --workspace @maka/runtime-host run build`
- `npm --workspace @maka/runtime-host run typecheck`
- focused owner + handoff tests: 30/30 passed
- scoped Biome check
- `git diff --check`

The repository-wide Runtime Host test command cannot provide an additional local signal in this checkout because the existing dependency closure lacks `minisearch` and has an incompatible `https-proxy-agent` export; the missing `minisearch` import reproduces from the unchanged main worktree.

Refs #3243
Refs #3231
Refs #3709

<details>
<summary>简体中文摘要</summary>

本 PR 把 #3769 的“仅跨 owner 转移”深化为一条统一的本地 deployment handoff：`from` 与 `to` 可以相同，也可以不同。这样，同一 persistent CLI installation 更新 deployment 与 Desktop/CLI 等跨 owner 转移复用同一份 durable state、同一把 authority lock、同一套退场/单写者释放/Ready 验证/崩溃恢复规则。

同时删除可绕过 Host 退场与 Ready 证明直接修改 selected deployment 的 `select` transition。最终 selected deployment 只能在初始 claim、验证完成后的 handoff commit，或明确 rollback 时变化。

本 PR 不加入 CLI、Desktop、临时 `npx`、managed service、remote operator 或 TUI 展示策略。双重审查结论为 GO：没有新增 authority、lock、journal 或 state kind，反而消除了一条并行状态变更路径。

验证：Runtime Host build 与 typecheck 通过；owner + handoff 聚焦测试 30/30；scoped Biome 与 diff-check 通过。全包 Runtime Host 测试在本地受既有依赖闭包缺失影响，纯 main 可复现，与本 diff 无关。

</details>

Generated-by: Codex


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- test: SUCCESS
- owner (windows-latest): SUCCESS
- owner (macos-latest): SUCCESS

## Changed files

- `packages/runtime-host/src/__tests__/local-deployment-owner.test.ts`: +67/-24
- `packages/runtime-host/src/__tests__/local-process-deployment-handoff.test.ts`: +71/-27
- `packages/runtime-host/src/operator/index.ts`: +7/-7
- `packages/runtime-host/src/operator/local-deployment-owner.ts`: +33/-63
- `packages/runtime-host/src/operator/local-process-deployment-handoff.ts`: +48/-48
