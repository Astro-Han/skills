# Frozen pull request snapshot

- PR: https://github.com/sveltejs/svelte/pull/18720 — `fix: render `selected` options for `<select multiple>` with an array `value` on the server`
- Author: Nic-Polumeyv
- Target base head: `aadc97ce1be06e3dad4b98469ac385a07f34fd06`
- Comparison base: `aadc97ce1be06e3dad4b98469ac385a07f34fd06`
- Exact source head: `e828d441c3d3a340ac57e72f4ea87469fa79ab5d`
- Diff: 43 additions, 19 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

`<select multiple value={['a', 'c']}>` and `bind:value` with an array now render `selected` on the matching options, so server output matches what the client selects after hydration instead of showing nothing selected until then.

`Renderer.option` in `internal/server/renderer.js` compared each option value with `===` against `local.select_value`, which for a multiple select is the array itself, so nothing matched. #18591 added a `select_default_multiple` flag that switches to `includes`, but only when the value came from `defaultValue`.

The flag is gone, `option` checks `is_array(select_value) ? select_value.includes(value) : value === select_value`. `binding-select-multiple` gets an `ssrHtml` since the server output changed.

Follow-up to #18591.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Tests (20, windows-latest): SUCCESS
- Tests (20, macOS-latest): SUCCESS
- Tests (20, ubuntu-latest): SUCCESS
- Tests (22, ubuntu-latest): SUCCESS
- Tests (24, ubuntu-latest): SUCCESS
- TestNoAsync: SUCCESS
- TSGo: SUCCESS
- Lint: SUCCESS
- Benchmarks: SUCCESS
- unnamed: PENDING
- vite-ecosystem-ci: SKIPPED
- Vercel Agent Review: SUCCESS

## Changed files

- `packages/svelte/src/internal/server/renderer.js`: +10/-9
- `packages/svelte/tests/runtime-legacy/samples/binding-select-multiple/_config.js`: +23/-10
- `packages/svelte/tests/server-side-rendering/samples/select-multiple-value/_expected.html`: +5/-0
- `packages/svelte/tests/server-side-rendering/samples/select-multiple-value/main.svelte`: +5/-0
