# Frozen pull request snapshot

- PR: https://github.com/microsoft/vscode/pull/332826 — `agentHost: move chat draft and title restore into chat contributions`
- Author: connor4312
- Target base head: `e340d31886e8a80a86624ad2c3f4a8c5fe1015ff`
- Comparison base: `e340d31886e8a80a86624ad2c3f4a8c5fe1015ff`
- Exact source head: `1444f8143d31faf45027129dc2eb5d1cd09f395b`
- Diff: 320 additions, 64 deletions, 9 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Merge remote-tracking branch 'origin/main' into connor4312/chat-draft-contribution



## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Compile & Hygiene: SUCCESS
- Analyze (actions): SUCCESS
- Screenshots & Tests: SUCCESS
- Monaco Editor checks: SUCCESS
- Check metadata: SUCCESS
- chat-lib tests (ubuntu-latest): SUCCESS
- Analyze (c-cpp): SUCCESS
- chat-lib tests (macos-latest): SUCCESS
- Analyze (csharp): SUCCESS
- chat-lib tests (windows-latest): SUCCESS
- Analyze (go): SUCCESS
- Analyze (java-kotlin): SUCCESS
- Analyze (javascript-typescript): SUCCESS
- Analyze (python): SUCCESS
- Analyze (ruby): SUCCESS
- Analyze (rust): SUCCESS
- Linux / CLI: SUCCESS
- Linux / Electron: SUCCESS
- Linux / Electron-Smoke: SUCCESS
- Linux / Browser: SUCCESS
- Linux / Remote: SUCCESS
- macOS / Electron: SUCCESS
- macOS / Electron-Smoke: SUCCESS
- macOS / Browser: SUCCESS
- macOS / Remote: SUCCESS
- Windows / Electron: SUCCESS
- Windows / Electron-Smoke: SUCCESS
- Windows / Browser: SUCCESS
- Windows / Remote: SUCCESS
- Copilot - Check Test Cache: SUCCESS
- Copilot - Check Telemetry: SUCCESS
- Copilot - Test (Linux): SUCCESS
- Copilot - Test (Windows): SUCCESS
- CodeQL: SUCCESS
- Dependencies Check: SUCCESS
- VS Code PR Check: SUCCESS
- license/cla: SUCCESS

## Changed files

- `src/vs/platform/agentHost/common/agentHostChatContributionsService.ts`: +22/-0
- `src/vs/platform/agentHost/node/agentHostChatContributionsService.ts`: +17/-1
- `src/vs/platform/agentHost/node/agentService.ts`: +12/-36
- `src/vs/platform/agentHost/node/agentSideEffects.ts`: +0/-23
- `src/vs/platform/agentHost/node/chatContributions/TODO.md`: +35/-0
- `src/vs/platform/agentHost/node/chatContributions/builtInChatContributions.ts`: +2/-0
- `src/vs/platform/agentHost/node/chatContributions/chatDraft/chatDraftContribution.ts`: +74/-0
- `src/vs/platform/agentHost/node/chatContributions/sessionTitle/sessionTitleContribution.ts`: +27/-1
- `src/vs/platform/agentHost/test/node/chatContributions.test.ts`: +131/-3
