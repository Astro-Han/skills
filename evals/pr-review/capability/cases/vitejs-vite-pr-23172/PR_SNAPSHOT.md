# Frozen pull request snapshot

- PR: https://github.com/vitejs/vite/pull/23172 — `refactor: remove HmrUrl concept`
- Author: sapphi-red
- Target base head: `616296895bd135386d35069a479a5f188c7de298`
- Comparison base: `616296895bd135386d35069a479a5f188c7de298`
- Exact source head: `796cd47ba8c13e3ad08ce573f52f81e113ffc6af`
- Diff: 39 additions, 29 deletions, 7 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This PR removes the "HmrUrl" concept.

There were three "Url" concept in Vite:

- "ModuleUrl"
  - the URL used in the module graph.
  - does not replace `\0`
  - does not have base
  - Example: `\0virtual:foo`
- "BrowserUrl"
  - the URL used by the browser
  - replaces `\0`
  - has base
  - Example: `/base/@id/__x00__virtual:foo?t=123`
- "HmrUrl"
  - the URL used in the HMR client.
  - replaces `\0`
  - does not have base
  - Example: `/@id/__x00__virtual:foo`

It is confusing to have three kinds of representation. I think the HmrUrl is not needed as well.

---

<sub>Stack created with <a href="https://github.com/github/gh-stack">GitHub Stacks CLI</a> • <a href="https://gh.io/stacks-feedback">Give Feedback 💬</a></sub>

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- copilot-setup-steps: SUCCESS
- Get changed files: SUCCESS
- Analyze (actions): SUCCESS
- preview: SUCCESS
- Semantic Pull Request: SUCCESS
- Run zizmor: SUCCESS
- Lint: node-24, ubuntu-latest: SUCCESS
- Build&Test: node-20, ubuntu-latest: FAILURE
- Build&Test: node-22, ubuntu-latest: FAILURE
- Build&Test: node-24, ubuntu-latest: FAILURE
- Build&Test: node-26, ubuntu-latest: FAILURE
- Build&Test: node-24, macos-latest: FAILURE
- Build&Test: node-24.15.0, windows-latest: FAILURE
- Build & Test Passed or Skipped: SKIPPED
- Build & Test Failed: SUCCESS
- Header rules - vite-docs-main: NEUTRAL
- Pages changed - vite-docs-main: NEUTRAL
- Redirect rules - vite-docs-main: NEUTRAL
- CodeQL: SUCCESS
- zizmor: SUCCESS
- Continuous Releases: SUCCESS
- unnamed: SUCCESS

## Changed files

- `packages/vite/src/client/client.ts`: +7/-1
- `packages/vite/src/module-runner/hmrHandler.ts`: +1/-4
- `packages/vite/src/node/plugins/importAnalysis.ts`: +7/-8
- `packages/vite/src/node/server/hmr.ts`: +4/-12
- `packages/vite/src/node/server/transformRequest.ts`: +4/-4
- `packages/vite/types/customEvent.d.ts`: +8/-0
- `packages/vite/types/hmrPayload.d.ts`: +8/-0
