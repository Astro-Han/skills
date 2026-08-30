# Frozen pull request snapshot

- PR: https://github.com/sveltejs/svelte/pull/18719 — `fix: keep the current selection of a `<select>` when its `defaultValue` is applied`
- Author: Nic-Polumeyv
- Target base head: `aadc97ce1be06e3dad4b98469ac385a07f34fd06`
- Comparison base: `aadc97ce1be06e3dad4b98469ac385a07f34fd06`
- Exact source head: `cd3f5474d28e199f5080dc91ee30718c24bdbddd`
- Diff: 204 additions, 42 deletions, 8 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

A `<select>` with nothing selected stays that way when `defaultValue` is applied, a default whose option arrives later gets selected, and applying a default no longer touches every option on unrelated updates.

`set_default_select_value` in `internal/client/dom/elements/bindings/select.js` marks the default options with the `selected` attribute, then writes `option.selected = selected.has(option)` to every option to restore the current selection. Each of those writes asks the select for a reset, so when no option was selected (`value={null}`, or a `bind:value` that matches nothing) the browser picks the first enabled option. The same restore treats the browser's implicit first-option pick as a choice, so `<select defaultValue="b">` whose options come from an `#each` that fills later never selects `b`. The call is also unconditional, so a spread `attribute_effect` or the element's template effect rerunning for an unrelated attribute repeats it; on a 500 option select a class change costs 501 property writes and 499 attribute writes. `<select value={x} defaultValue>` compiles to two `$.init_select` calls, one from `build_element_special_value_attribute` and one from the `defaultValue` block, so two `MutationObserver`s run both passes per mutation.

`set_default_select_value` returns early when `__defaultValue` is unchanged. After mount a default change never moves the current selection, the same contract as `set_default_value` for inputs, and the restore only writes where something moved, through `selectedIndex` for a single select and per option for `multiple`. When the options change the attributes are applied without restoring, so an option that arrives later carrying the default gets selected the way an inserted `<option selected>` does natively, and `__value` re-asserts the value afterwards. `init_select` is emitted once per `<select>` by the compiler, with `attribute_effect` covering spreads.

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

- `packages/svelte/src/compiler/phases/3-transform/client/visitors/RegularElement.js`: +20/-16
- `packages/svelte/src/internal/client/dom/elements/attributes.js`: +2/-2
- `packages/svelte/src/internal/client/dom/elements/bindings/select.js`: +41/-23
- `packages/svelte/tests/runtime-runes/samples/form-default-value-select/_config.js`: +1/-1
- `packages/svelte/tests/runtime-runes/samples/select-default-value-preserve-selection/_config.js`: +52/-0
- `packages/svelte/tests/runtime-runes/samples/select-default-value-preserve-selection/main.svelte`: +37/-0
- `packages/svelte/tests/runtime-runes/samples/select-default-value-single-observer/_config.js`: +30/-0
- `packages/svelte/tests/runtime-runes/samples/select-default-value-single-observer/main.svelte`: +21/-0
