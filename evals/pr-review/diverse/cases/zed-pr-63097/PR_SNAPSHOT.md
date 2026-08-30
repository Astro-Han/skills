# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/63097 — `terminal_view: Don't steal focus from an open modal when terminals appear`
- Author: butvinm
- Target base head: `d9ad6aff67e47de43abb270d22de75dd950f1b48`
- Comparison base: `fd82517a115d97a07835b52f0512b22b38e38ccf`
- Exact source head: `17f3aa269daeb704fac84f2a6b185f7d455541ba`
- Diff: 254 additions, 13 deletions, 1 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

# Objective

Pressing the recent projects shortcut right after launching Zed opens the picker, which then dismisses itself a moment later. The terminal panel takes focus after the keystroke, and the picker cancels on blur.

## Solution

Two paths focused the panel unconditionally at the end of async startup work: the tail of `TerminalPanel::restore_serialized_state`, and `RevealStrategy::Always` in `add_terminal_shell` (which `finish_restoration` uses to spawn the default shell). Both now check `has_active_modal`, as `add_center_terminal` already did. For the shell path the check is at reveal time, because the spawn is itself async.

## Testing

Three tests in `terminal_panel.rs`. Two of them fail with the source change reverted. Manually tested on Linux.

## Before:


https://github.com/user-attachments/assets/66ab9860-b381-46da-8f85-f7a58c5157e6


## After:


https://github.com/user-attachments/assets/57583fe2-3c8a-40e0-9130-bbb612c1e158


Release Notes:

- Fixed the terminal panel dismissing an open modal when terminals finish restoring during startup


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- build_nix_linux_x86_64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- danger: SUCCESS
- orchestrate: SUCCESS
- build_nix_mac_aarch64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- check_style: SUCCESS
- build_static_bwrap_linux_aarch64: SKIPPED
- clippy_windows: SUCCESS
- build_static_bwrap_linux_x86_64: SKIPPED
- clippy_linux: SUCCESS
- bundle_mac_aarch64: SKIPPED
- clippy_mac: SUCCESS
- bundle_mac_x86_64: SKIPPED
- clippy_mac_x86_64: SUCCESS
- bundle_windows_aarch64: SKIPPED
- run_tests_windows: SUCCESS
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

- `crates/terminal_view/src/terminal_panel.rs`: +254/-13
