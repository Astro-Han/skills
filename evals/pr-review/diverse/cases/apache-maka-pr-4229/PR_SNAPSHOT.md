# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/4229 — `fix(desktop): enable relay discovery for Peer Mesh`
- Author: M4n5ter
- Target base head: `827b3fdf940f0bb5d309548a1f099104ec25da87`
- Comparison base: `827b3fdf940f0bb5d309548a1f099104ec25da87`
- Exact source head: `cac9e4ab6c81a834639d757492307618a1b8b688`
- Diff: 29 additions, 4 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<details open>
<summary>English</summary>

## Summary

Enable automatic coordination relay discovery for the Desktop-owned Peer Mesh endpoint and its direct-peer fallback. Existing Meshes keep their identity and state; their normal reconciliation picks up accepted reservations, and newly created invitations include them.

When discovery has not produced a reservation yet, the invitation view now states that the code contains direct routes only and may not work across NATs.

The verified invitation below contains two accepted `coordinationRelays` (the code view is scrolled past its one-time secret):

![](https://github.com/apache/maka/blob/ee7a6de68d5e79147dd0c7cf1dc8381ddaf3b207/desktop-peer-mesh-relays.png?raw=true)

## Verification

- `node --test --test-name-pattern='development uses the native peer addon only for the peer-enabled launch' apps/desktop/dist/main/__tests__/runtime-host-peer-client.test.js`
- `npm run lint`
- `npm run format:check`
- `npm run build`
- `npm run typecheck`
- `npx knip --workspace apps/desktop`
- Real Desktop run with the release peer native addon: an existing Mesh acquired two accepted coordination relays, and a newly generated invitation contained both addresses

## AI use

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: OpenAI Codex implemented the change and ran the checks under the contributor's direction. The contributor will review and decide whether to merge it.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No

</details>

<details>
<summary>中文</summary>

## 摘要

为 Desktop 自己持有的 Peer Mesh endpoint 及其 direct-peer 降级路径启用自动协调节点发现。已有 Mesh 保持原有 identity 和状态，由现有 reconciliation 接收成功的 reservation；之后生成的邀请码会包含这些地址。

如果 discovery 尚未取得 reservation，邀请界面会明确说明该代码只包含直接地址，跨 NAT 时可能无法连接。

下图中已验证的邀请码包含两个成功的 `coordinationRelays`（代码视图已滚过一次性 secret）：

![](https://github.com/apache/maka/blob/ee7a6de68d5e79147dd0c7cf1dc8381ddaf3b207/desktop-peer-mesh-relays.png?raw=true)

## 验证

- `node --test --test-name-pattern='development uses the native peer addon only for the peer-enabled launch' apps/desktop/dist/main/__tests__/runtime-host-peer-client.test.js`
- `npm run lint`
- `npm run format:check`
- `npm run build`
- `npm run typecheck`
- `npx knip --workspace apps/desktop`
- 使用 release peer native addon 真实运行 Desktop：已有 Mesh 成功取得两个协调节点 reservation，新生成的邀请码包含这两个地址

## AI 使用

- [ ] 没有生成式工具作出实质性贡献
- [x] 生成式工具作出了实质性贡献

工具与范围：OpenAI Codex 在贡献者指导下实现改动并执行检查；贡献者将审核并决定是否合并。

## 检查清单

- [x] 测试覆盖本次改动，且在缺少改动时会失败
- [x] lint、格式、类型检查及相关测试已在本地通过

本 PR 是否改变行为？

- [x] 是——已在上方摘要说明
- [ ] 否

</details>


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- test: SUCCESS
- label: SUCCESS
- label: SUCCESS
- package: SUCCESS

## Changed files

- `apps/desktop/src/main/__tests__/runtime-host-peer-client.test.ts`: +1/-0
- `apps/desktop/src/main/runtime-host-boot.ts`: +3/-1
- `apps/desktop/src/main/runtime-host-peer-client.ts`: +11/-3
- `apps/desktop/src/renderer/settings/runtime-host-peer-mesh-dialog.tsx`: +14/-0
