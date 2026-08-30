# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/60301 — `Fix hanging updates after system sleep`
- Author: Anthony-Eid
- Target base head: `4aa8ad9742b1ee948d64429a5814d9b9a861350a`
- Comparison base: `31fc9d5f4710e30a4908525f6f0b930fce71e6f6`
- Exact source head: `8ddbe4d034692d3f1eee3f0f952adfaef511a158`
- Diff: 60 additions, 17 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

When Zed was downloading an update and the machine went to sleep, the download would hang indefinitely on wake because the in-flight TCP connection had silently died and nothing ever timed it out or retried. This adds an inactivity `read_timeout` to the HTTP client so a stalled response body errors out instead of hanging forever (slow-but-progressing downloads are unaffected, since the timeout resets on each chunk). It also promotes `App::on_system_wake` to a multi-subscriber `Subscription` API and uses it in the auto-updater to cancel an interrupted check/download on wake and start a fresh attempt.

## Self-Review Checklist:

- [x] I've reviewed my own diff for quality, security, and reliability
- [x] Unsafe blocks (if any) have justifying comments
- [x] The content adheres to Zed's UI standards ([UX/UI](https://github.com/zed-industries/zed/blob/main/CONTRIBUTING.md#uiux-checklist) and [icon](https://github.com/zed-industries/zed/blob/main/crates/icons/README.md) guidelines)
- [ ] Tests cover the new/changed behavior
- [x] Performance impact has been considered and is acceptable

Release Notes:

- Fix hanging Zed update downloads after system sleep


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- route-pr: SKIPPED
- route-pr: SKIPPED
- route-pr: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- route-pr: SUCCESS
- batch-suggestions: SUCCESS
- notify-slack: SUCCESS
- check-authorship-and-label: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- orchestrate: SUCCESS
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

- `crates/auto_update/src/auto_update.rs`: +28/-0
- `crates/gpui/src/app.rs`: +30/-17
- `crates/reqwest_client/src/reqwest_client.rs`: +2/-0
