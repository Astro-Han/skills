# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/2991 — `feat(agent-graph): browse historical graph runs`
- Author: me2seeks
- Target base head: `b03b85e8596abfa448b119112197fadbfab6e1b8`
- Comparison base: `b03b85e8596abfa448b119112197fadbfab6e1b8`
- Exact source head: `d42bf37ee6986ae4375d35651df08e5c05e1cbf1`
- Diff: 561 additions, 60 deletions, 20 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

- add bounded Runtime Host reads for a root Session's current and historical Agent Graph epochs
- let Desktop browse prior Graph runs while keeping historical controls read-only
- add `/graph history` to the TUI without starting an agent Turn

The Runtime Host remains the only historical graph reader: clients request an epoch directory and an exact graph snapshot, while the Host validates that the requested graph belongs to the same root Session. Desktop follows the current epoch by default and fences stale refreshes when the user switches runs.

This is the historical-read slice of #2588 and builds on #2969.

Refs #2588

Ready for review.

## Verification

- `npm run build:test`
- `npm run typecheck`
- Agent Graph, Desktop bridge/panel, and TUI tests on the latest-main stack — 146 passed
- Biome check on all changed files
- `git diff --check`

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — Desktop and TUI can inspect earlier Agent Graph runs in a root Session
- [ ] No

<details>
<summary>中文说明</summary>

## 摘要

- 增加由 Runtime Host 提供的有界 Graph epoch 历史读取
- Desktop 可以切换查看之前的 Graph 运行，历史运行只读且不会出现停止或关闭控制
- TUI 增加 `/graph history`，查看历史不会启动 Agent Turn

客户端不会直接读取 SQLite。Runtime Host 会验证指定 graph 确实属于同一个 root Session，再返回 epoch 目录和精确历史快照。Desktop 默认跟随当前 epoch，并通过 generation fence 防止较慢的旧请求覆盖用户刚选择的新页面。

这是 #2588 的历史读取部分，建立在 #2969 的 epoch 生命周期边界之上。

已转为 Ready，请求 review。

</details>

## AI disclosure / AI 披露

This PR was implemented by Codex under me2seeks’s direction and review. / 本 PR 由 Codex 在 me2seeks 的指导与审核下完成。

## Visual evidence

Representative Desktop capture using the PR copy and graph states. The historical selection is explicitly read-only and does not expose the current-run Stop action.

| Before — current graph only | After — historical run selected |
| --- | --- |
| ![Agent Graph before historical browsing](https://raw.githubusercontent.com/me2seeks/maka-agent/437384a659e2b6f8c77eb2477bc9d14f0e5bb6b8/pr-2991-before.png) | ![Agent Graph historical run selected](https://raw.githubusercontent.com/me2seeks/maka-agent/437384a659e2b6f8c77eb2477bc9d14f0e5bb6b8/pr-2991-after.png) |\n\n## AI use\n- [ ] No generative tool was used for implementation.\n- [x] Generative tooling was used and the result was reviewed and verified by the author.\n\nTool(s) and scope: OpenAI Codex (Maka) assisted with implementation, review remediation, tests, and PR documentation.\n\nFinal squash trailer: `Generated-by: Maka`

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- changes: SUCCESS
- Build immutable tarball: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- windows_sandbox_w0_protocol: SUCCESS
- astryx_surface: SUCCESS
- Validate installed CLI Linux x64 / Node 22.19: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- Validate installed CLI Linux x64 / Node 24: SUCCESS
- Validate installed CLI macOS arm64 / Node 24: SUCCESS
- Validate installed CLI Windows x64 / Node 24: SUCCESS
- typecheck: SUCCESS
- Validate installed CLI Eval: SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS
- unnamed: SUCCESS

## Changed files

- `apps/desktop/src/main/__tests__/agent-graph-panel.test.ts`: +260/-17
- `apps/desktop/src/main/__tests__/runtime-host-session-domains-ipc-main.test.ts`: +14/-0
- `apps/desktop/src/main/runtime-host-client.ts`: +4/-0
- `apps/desktop/src/main/runtime-host-session-domains-ipc-main.ts`: +17/-2
- `apps/desktop/src/preload/bridge-contract.d.ts`: +2/-1
- `apps/desktop/src/preload/preload.ts`: +8/-2
- `apps/desktop/src/renderer/agent-graph-panel.tsx`: +66/-12
- `packages/cli/src/__tests__/pi-tui-runner.test.ts`: +49/-0
- `packages/cli/src/pi-tui-runner.ts`: +1/-0
- `packages/runtime-host/src/__tests__/agent-graph-coordinator.test.ts`: +6/-3
- `packages/runtime-host/src/__tests__/agent-graph-protocol.test.ts`: +7/-3
- `packages/runtime-host/src/__tests__/agent-graph-two-client-uds.test.ts`: +8/-3
- `packages/runtime-host/src/__tests__/execution-composition.test.ts`: +4/-1
- `packages/runtime-host/src/__tests__/root-turn-coordinator.test.ts`: +51/-0
- `packages/runtime-host/src/protocol/agent-graph.ts`: +19/-3
- `packages/runtime-host/src/server/agent-graph-coordinator.ts`: +5/-4
- `packages/runtime-host/src/server/execution-composition.ts`: +3/-1
- `packages/runtime-host/src/server/root-turn-coordinator.ts`: +13/-7
- `packages/runtime/src/__tests__/stream-graph-coordinator.test.ts`: +16/-0
- `packages/runtime/src/stream-graph-coordinator.ts`: +8/-1
