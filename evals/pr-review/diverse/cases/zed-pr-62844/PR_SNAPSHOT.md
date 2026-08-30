# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/62844 — `workspace: Activate the right tab when restoring a workspace`
- Author: ArneshBanerjee
- Target base head: `aad75630f90fff7de9d29e7aad4f8384586297f7`
- Comparison base: `aad75630f90fff7de9d29e7aad4f8384586297f7`
- Exact source head: `de4209eba944cb9a12a6bf2689c72e160f524d73`
- Diff: 78 additions, 10 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

@SomeoneToIgnore this is the follow up you asked for in #62692, done as discussed.

`deserialize_to` keeps a `None` in `items` for every item that failed to deserialize, and those are never added to the pane. Any later tab therefore sits at a lower index in the pane than the one it was serialized with, so activating and previewing by serialized index lands on the tab that shifted into that slot. When the failing item is the last one, the index points past the end of the pane and nothing is activated or previewed.

The serialized index is now mapped to the pane's index by counting the items before it that actually restored, and an index whose own item failed to restore is skipped.

Closes #62843

Release Notes:

- Fixed the wrong tab being activated when restoring a workspace containing items that fail to open


## Linked issues

### https://github.com/zed-industries/zed/issues/62843 — Wrong tab is activated when restoring a workspace with items that fail to open

### Summary

When a workspace is restored, `SerializedPane::deserialize_to` (`crates/workspace/src/persistence/model.rs`) picks the active tab and the preview tab by their *serialized* index. Items that fail to deserialize are never added to the pane, so every tab after such an item ends up at a lower index than it was serialized with. The active and preview tabs then land on the wrong tab, or on no tab at all.

This is the same index desync that #62003 hit on the pinned count, which was fixed in #62692. The count was fixed there, the active and preview fields were left for a follow up.

### Steps to reproduce

1. Open a pane with three tabs.
2. Make the second tab one that cannot be restored (for example a file that is deleted or renamed while Zed is closed), and leave the third tab active.
3. Restart Zed.

### Expected

The tab that was active before the restart comes back active.

### Actual

The pane restores two tabs and activates the wrong one. The same happens to the preview tab. If the failing item was the last one serialized, the index points past the end of the pane and nothing is activated or previewed at all.

### Zed version

Reproduces on `main` (`crates/workspace/src/persistence/model.rs`, `SerializedPane::deserialize_to`).


## Exact-head checks

- batch-suggestions: SKIPPED
- batch-suggestions: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- route-pr: SUCCESS
- danger: SUCCESS
- orchestrate: SUCCESS
- cherry-pick-suggestions: SKIPPED
- cherry-pick-suggestions: SKIPPED
- build_nix_mac_aarch64: SKIPPED
- build_nix_mac_aarch64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- check_style: SUCCESS
- build_static_bwrap_linux_aarch64: SKIPPED
- build_static_bwrap_linux_aarch64: SKIPPED
- clippy_windows: SUCCESS
- build_static_bwrap_linux_x86_64: SKIPPED
- build_static_bwrap_linux_x86_64: SKIPPED
- clippy_linux: SUCCESS
- bundle_mac_aarch64: SKIPPED
- bundle_mac_aarch64: SKIPPED
- clippy_mac: SUCCESS
- bundle_mac_x86_64: SKIPPED
- bundle_mac_x86_64: SKIPPED
- clippy_mac_x86_64: SUCCESS
- bundle_windows_aarch64: SKIPPED
- bundle_windows_aarch64: SKIPPED
- run_tests_windows: SUCCESS
- bundle_windows_x86_64: SKIPPED
- bundle_windows_x86_64: SKIPPED
- run_tests_linux: SUCCESS
- run_tests_mac: SUCCESS
- miri_scheduler: SUCCESS
- doctests: SUCCESS
- check_workspace_binaries: SUCCESS
- build_visual_tests_binary: SUCCESS
- check_wasm: SUCCESS
- check_dependencies: SUCCESS
- check_docs: SUCCESS
- check_licenses: SKIPPED
- check_scripts: SKIPPED
- check_postgres_and_protobuf_migrations: SUCCESS
- extension_tests: SKIPPED
- tests_pass: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `crates/workspace/src/persistence/model.rs`: +6/-6
- `crates/workspace/src/workspace.rs`: +72/-4
