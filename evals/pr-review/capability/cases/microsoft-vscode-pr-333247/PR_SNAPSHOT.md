# Frozen pull request snapshot

- PR: https://github.com/microsoft/vscode/pull/333247 — `Fix chat customization migration dependency cycle`
- Author: dmitrivMS
- Target base head: `cefc83193036e53a85e980c5d0b22e9d66cd267e`
- Comparison base: `cefc83193036e53a85e980c5d0b22e9d66cd267e`
- Exact source head: `80399c0f74209c773704de8b04a1ee94b4771470`
- Diff: 54 additions, 10 deletions, 5 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

- break the `ChatService` → customization migration → agent host tools dependency cycle that prevented Browser and Remote test workbenches from starting
- register the customization migration hint provider after `ChatService` has been constructed
- preserve migration hint behavior and update its focused tests

This fixes the startup failure observed in #331439 after #333216 merged.

## Validation

- `npm run typecheck-client`
- 4 focused `ChatService` migration hint tests
- `scripts\test-remote-integration.bat` reached the extension host test suite without the dependency-cycle failure and ran 330 tests; the run ended on an unrelated active-editor timing failure (`#49125`)
- repository pre-commit hygiene hook

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
- CodeQL: NEUTRAL
- Dependencies Check: SUCCESS
- VS Code PR Check: SUCCESS
- license/cla: SUCCESS

## Changed files

- `src/vs/workbench/contrib/chat/browser/chat.shared.contribution.ts`: +16/-0
- `src/vs/workbench/contrib/chat/common/chatService/chatService.ts`: +3/-1
- `src/vs/workbench/contrib/chat/common/chatService/chatServiceImpl.ts`: +18/-5
- `src/vs/workbench/contrib/chat/test/common/chatService/chatService.test.ts`: +12/-4
- `src/vs/workbench/contrib/chat/test/common/chatService/mockChatService.ts`: +5/-0
