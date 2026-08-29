# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/2969 — `feat(runtime): support sequential agent graph epochs`
- Author: me2seeks
- Target base head: `ce6534d6549241bcb0fa4cf20bd2e7fe3f602228`
- Comparison base: `ce6534d6549241bcb0fa4cf20bd2e7fe3f602228`
- Exact source head: `95059176ed205307b0ba8ad8ab007bccd368f2c9`
- Diff: 1274 additions, 117 deletions, 25 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

- persist monotonic root-to-graph epoch bindings while preserving the existing deterministic graph as epoch 1
- advance a finished, quiescent graph before the next graph/swarm root Turn is durably admitted
- fence supervisor wakes and resolve stop, permission, revision, and retirement paths through durable graph ownership

A finished graph remains immutable. The next graph-capable Turn receives a new deterministic graph ID, and concurrent Hosts converge through a storage CAS instead of reopening or skipping the previous graph. Ordinary default Turns leave the finished graph untouched. Legacy epoch 1 stays virtual until the first real cutover, so Sessions do not acquire graph state just by being read.

This establishes the lifecycle boundary needed by #2588. Historical graph selection and cross-epoch result inputs remain follow-up work.

Refs #2588

## Verification

- `npm --workspace @maka/core run test` — 539 passed
- `npm --workspace @maka/storage run test` — 777 passed, 16 skipped
- `npm --workspace @maka/runtime run test` — 2,788 passed, 6 skipped
- `npm --workspace @maka/runtime-host run test` — 910 passed
- builds for Core, Storage, Runtime, and Runtime Host
- Biome on all changed files
- `git diff --check`

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — a graph/swarm Turn can advance from a finished Agent Graph to a fresh graph epoch
- [ ] No

<details>
<summary>中文说明</summary>

## 摘要

- 持久化 root Session 到 Agent Graph 的单调 epoch 绑定，同时保持原有确定性 graph ID 作为 epoch 1
- 只有当前图已经结束且静默，才会在下一条 graph/swarm root Turn 持久化之前切换到新 epoch
- supervisor wake、停止、权限回答、会话修订与删除清理都通过 Runtime Host 的持久化 graph ownership 解析

已经 `finish` 的图仍然不可修改。下一条启用 Graph 的 Turn 使用新的确定性 graph ID；多个 Host 并发切换时由 Storage CAS 收敛，不会重开旧图或跳过 epoch。普通 default Turn 不会切换 graph epoch。第一次真正切换前，legacy epoch 1 只是只读兼容值，因此会话不会仅因查询而写入图状态。

本 PR 建立 #2588 所需的生命周期基础。历史图选择和跨 epoch 结果输入将在后续实现。

</details>


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- changes: SUCCESS
- audit: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: FAILURE
- test_runtime_host: SUCCESS
- e2e: SKIPPED
- storybook: SKIPPED
- test: FAILURE

## Changed files

- `packages/core/package.json`: +1/-0
- `packages/core/src/agent-graph-epoch.ts`: +110/-0
- `packages/core/src/agent-graph-supervisor-wake.ts`: +2/-0
- `packages/runtime-host/src/__tests__/agent-graph-coordinator.test.ts`: +3/-1
- `packages/runtime-host/src/__tests__/agent-graph-two-client-uds.test.ts`: +5/-1
- `packages/runtime-host/src/__tests__/root-turn-coordinator.test.ts`: +74/-0
- `packages/runtime-host/src/__tests__/sandbox-boundary-graph-wake.test.ts`: +46/-28
- `packages/runtime-host/src/__tests__/session-retirement-coordinator.test.ts`: +1/-0
- `packages/runtime-host/src/__tests__/session-revision-graph-references.test.ts`: +6/-0
- `packages/runtime-host/src/server/agent-graph-coordinator.ts`: +3/-3
- `packages/runtime-host/src/server/agent-graph-execution-coordinator.ts`: +12/-3
- `packages/runtime-host/src/server/execution-composition.ts`: +35/-9
- `packages/runtime-host/src/server/root-turn-coordinator.ts`: +33/-4
- `packages/runtime-host/src/server/sandbox-boundary-graph-wake.ts`: +6/-5
- `packages/runtime-host/src/server/session-retirement-coordinator.ts`: +7/-3
- `packages/runtime-host/src/server/session-revision-coordinator.ts`: +1/-1
- `packages/runtime-host/src/server/session-revision-graph-references.ts`: +33/-26
- `packages/runtime/src/__tests__/agent-graph-supervisor-wake.test.ts`: +104/-0
- `packages/runtime/src/__tests__/stream-graph-coordinator.test.ts`: +205/-0
- `packages/runtime/src/agent-graph-supervisor-wake.ts`: +11/-7
- `packages/runtime/src/stream-graph-coordinator.ts`: +151/-21
- `packages/storage/src/__tests__/agent-graph-epochs.test.ts`: +160/-0
- `packages/storage/src/__tests__/session-store.test.ts`: +1/-0
- `packages/storage/src/sqlite-session-metadata-schema.ts`: +18/-1
- `packages/storage/src/sqlite-session-metadata-store.ts`: +246/-4
