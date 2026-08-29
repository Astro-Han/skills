# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3230 — `feat(cli): set up managed remote Runtime Hosts`
- Author: M4n5ter
- Target base head: `57593a904c4062b55f80633d59071ba62acd7941`
- Comparison base: `57593a904c4062b55f80633d59071ba62acd7941`
- Exact source head: `05ddec011d4f6bcb57b4497328549977113778f5`
- Diff: 1472 additions, 78 deletions, 28 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<details open>
<summary>English</summary>

## Summary

Add one idempotent Host-side setup flow for managed remote Runtime Hosts. A released CLI can now:

- copy its exact self-contained package into a Maka-owned persistent deployment
- install or repair the existing Linux systemd user service
- replace the credential for one stable Client identity instead of accumulating credentials
- verify the authenticated loopback Runtime Host before returning framed connection facts
- remove the managed deployment during service uninstall while retaining the State Root

This is the CLI contract that the later Desktop **Add Computer** wizard will invoke through interactive system SSH. Desktop UI, version switching, automatic updates, and macOS service support remain outside this PR.

Fixes #3229

## Verification

- `npm run build:test`
- `npm run typecheck`
- `npm --workspace @maka/runtime-host test` — 979 passed
- `npm --workspace maka-agent test` — 285 passed
- Biome check and `git diff --check`
- Real Linux systemd user-service test with a packed release artifact:
  - setup completed twice and retained exactly one active credential for the stable principal
  - a new local Client authenticated through an SSH tunnel after the setup SSH session ended
  - uninstall stopped and removed the service and managed package while retaining the State Root and access authority

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: OpenAI Codex assisted with implementation, tests, documentation, and validation under the maintainer's direction

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No

</details>

<details>
<summary>简体中文</summary>

## 摘要

为托管的远程 Runtime Host 增加一个幂等的 Host 侧 setup 流程。发布版 CLI 现在可以：

- 将当前精确的自包含 package 复制到 Maka-owned 的持久 deployment
- 安装或修复现有 Linux systemd user service
- 替换稳定 Client identity 的 credential，而不是不断累积 credential
- 返回带 framing 的连接信息前，验证经过认证的 loopback Runtime Host
- 卸载 service 时删除托管 deployment，同时保留 State Root

这是后续 Desktop **添加电脑** 向导通过交互式 system SSH 调用的 CLI 契约。Desktop UI、版本切换、自动更新和 macOS service 支持不属于本 PR。

修复 #3229

## 验证

- `npm run build:test`
- `npm run typecheck`
- `npm --workspace @maka/runtime-host test` — 979 项通过
- `npm --workspace maka-agent test` — 285 项通过
- Biome check 与 `git diff --check`
- 使用打包 release artifact 完成真实 Linux systemd user service 验证：
  - 连续执行两次 setup 后，稳定 principal 只有一个 active credential
  - setup SSH session 结束后，新 Local Client 仍可通过 SSH tunnel 完成认证
  - uninstall 会停止并删除 service 和托管 package，同时保留 State Root 与 access authority

## AI 使用

OpenAI Codex 在维护者指导下协助实现、测试、文档与验证；权威选择见英文部分

## 检查清单

- 测试覆盖新增行为，并会在缺少实现时失败
- lint、format、typecheck 与受影响测试均在本地通过
- 本 PR 包含上文已说明的行为变化

</details>

## Linked issues

### https://github.com/apache/maka/issues/3229 — Add an idempotent managed Runtime Host setup contract

<details open>
<summary>English</summary>

## Problem

PR #3205 can install and operate a persistent Linux Runtime Host service once a compatible Maka CLI is already present. Preparing a new remote computer still requires an operator to install the correct package, invoke several service and access commands, transfer the resulting endpoint and Root identity, and recover partial setup manually.

Desktop onboarding should not reproduce that lifecycle as a sequence of shell snippets. CLI and TUI also need the same reliable setup boundary.

## Desired outcome

Provide one idempotent, machine-readable CLI setup contract that can be invoked through interactive system SSH. It should install an exact Maka version into a Maka-owned location, install or repair the managed service, pair one stable Client identity, verify an authenticated connection, and return the facts a Client needs to create a remote Profile.

This becomes the Host-side foundation for the Desktop **Add Computer** wizard tracked by #3228.

## Scope

- Add a versioned setup command with framed progress, completion, and stable failure output
- Install the exact invoking Maka version into an owned, persistent deployment instead of pointing the service at an npm execution cache
- Reuse the #3205 service lifecycle for Linux systemd user services
- Make repeated setup for the same Client pairing identity converge without accumulating services or credentials
- Deliver the credential secret only in the terminal success result; never persist it in service config, deployment state, arguments, or logs
- Verify service readiness, Root identity, and an authenticated Runtime Host connection before reporting success
- Preserve an existing healthy service and all State Root data when setup fails
- Validate first install, retry, interrupted setup, SSH disconnect, and clean uninstall on a real Linux systemd user service

## Success criteria

- A supported Linux machine with Node.js, npm, systemd user services, and user lingering can be prepared through one setup invocation
- Repeating or retrying setup does not create duplicate managed deployments, services, or active credentials for the same pairing identity
- The persistent service survives the setup SSH session and does not depend on shell startup files or npm cache paths
- Partial failure returns an actionable stable error and leaves setup safely retryable
- Successful output is sufficient for a Client to construct and verify a remote Profile without manually copying internal service details

## Non-goals

- Desktop UI
- Automatic Node.js installation, silent `sudo`, or changes to the user's SSH config
- Version switching, update channels, automatic updates, or rollback across storage migrations
- macOS LaunchAgent or Windows service support
- Deleting the State Root during setup or service uninstall

Depends on #3205. Part of #3228.

</details>

<details>
<summary>简体中文</summary>

## 问题

PR #3205 已经可以在兼容的 Maka CLI 存在时安装和管理持久的 Linux Runtime Host service。但准备一台新的远程电脑仍需要操作者自行安装正确版本、调用多条 service 与 access 命令、传递 endpoint 和 Root identity，并手工处理不完整的 setup。

Desktop onboarding 不应把这套 lifecycle 重新实现成一串 shell 片段；CLI 与 TUI 也需要复用同一个可靠的 setup 边界。

## 期望结果

提供一条幂等、机器可读，并且可以通过交互式 system SSH 调用的 CLI setup 契约。它负责把精确 Maka 版本安装到 Maka-owned 的持久目录，安装或修复 managed service，为一个稳定 Client identity 完成配对，验证经过认证的连接，并返回 Client 创建 remote Profile 所需的事实。

该能力将成为 #3228 中 Desktop **添加电脑** 向导的 Host 侧基础。

## 范围

- 增加带版本的 setup 命令，输出带 framing 的进度、完成与稳定失败结果
- 将当前精确 Maka 版本安装到 owned、持久的 deployment，不能让 service 指向 npm execution cache
- 复用 #3205 的 Linux systemd user service lifecycle
- 同一 Client pairing identity 重复 setup 时能够收敛，不累积 service 或 credential
- Credential secret 只在最终成功结果中交付一次，不进入 service config、deployment state、命令参数或日志
- 报告成功前验证 service readiness、Root identity 和经过认证的 Runtime Host 连接
- Setup 失败时保留已有健康 service 和全部 State Root 数据
- 在真实 Linux systemd user service 上验证首次安装、重试、中断恢复、SSH 断开和干净卸载

## 完成标准

- 具备 Node.js、npm、systemd user service 和 user lingering 的受支持 Linux 机器可以通过一次 setup 调用完成准备
- 重复或重试 setup 不会为同一 pairing identity 创建重复的 managed deployment、service 或 active credential
- 持久 service 在 setup SSH session 结束后继续运行，且不依赖 shell startup file 或 npm cache path
- 部分失败返回可操作的稳定错误，并保持 setup 可以安全重试
- 成功输出足以让 Client 构造并验证 remote Profile，无需用户手工复制 service 内部细节

## 非目标

- Desktop UI
- 自动安装 Node.js、静默执行 `sudo`，或修改用户 SSH config
- 版本切换、更新频道、自动更新，或跨 storage migration 回退
- macOS LaunchAgent 或 Windows service 支持
- 在 setup 或 service uninstall 中删除 State Root

依赖 #3205，属于 #3228。

</details>


## Exact-head checks

- changes: SUCCESS
- Build immutable tarball: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
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

- `apps/desktop/src/renderer/settings/runtime-host-profiles-section.tsx`: +2/-1
- `docs/runtime-host-remote-access.md`: +23/-2
- `docs/runtime-host-remote-access.zh-CN.md`: +18/-2
- `packages/cli/README.md`: +21/-5
- `packages/cli/README.zh-CN.md`: +16/-2
- `packages/cli/src/__tests__/runtime-host-operator-command.test.ts`: +2/-0
- `packages/cli/src/__tests__/runtime-host-service-manager.test.ts`: +107/-3
- `packages/cli/src/__tests__/runtime-host-setup.test.ts`: +246/-0
- `packages/cli/src/cli-core.ts`: +29/-0
- `packages/cli/src/runtime-host-access-command.ts`: +36/-0
- `packages/cli/src/runtime-host-cli.ts`: +92/-30
- `packages/cli/src/runtime-host-managed-deployment.ts`: +234/-0
- `packages/cli/src/runtime-host-service-management-command.ts`: +4/-2
- `packages/cli/src/runtime-host-service-manager.ts`: +68/-11
- `packages/cli/src/runtime-host-setup-command.ts`: +318/-0
- `packages/runtime-host/src/__tests__/authenticated-websocket.test.ts`: +27/-3
- `packages/runtime-host/src/__tests__/websocket-listener.test.ts`: +1/-0
- `packages/runtime-host/src/client/host-profile.ts`: +3/-2
- `packages/runtime-host/src/client/index.ts`: +9/-0
- `packages/runtime-host/src/client/setup-frame.ts`: +99/-0
- `packages/runtime-host/src/client/ssh-tunnel.ts`: +3/-2
- `packages/runtime-host/src/protocol/access-authority.ts`: +14/-0
- `packages/runtime-host/src/protocol/index.ts`: +1/-0
- `packages/runtime-host/src/protocol/websocket-path.ts`: +18/-0
- `packages/runtime-host/src/server/access-authority.ts`: +65/-10
- `packages/runtime-host/src/server/host-kernel.ts`: +3/-0
- `packages/runtime-host/src/server/operation-dispatcher.ts`: +7/-0
- `packages/runtime-host/src/server/websocket-listener.ts`: +6/-3
