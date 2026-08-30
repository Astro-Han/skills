# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/60321 — `Revert "Fix hanging updates after system sleep (#60301)"`
- Author: maxdeviant
- Target base head: `bb48a42983f2a4bb9ac9d31c63abe02497088f67`
- Comparison base: `bb48a42983f2a4bb9ac9d31c63abe02497088f67`
- Exact source head: `75d6896b581f5763208c5fea6e5df4ab01743286`
- Diff: 17 additions, 60 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This reverts commit 2882636c06923e58d83865ecc370bd0d8199d738.

This was causing Zed to crash immediately on startup with the following error:

```
thread 'main' (74835290) panicked at /Users/maxdeviant/.cargo/git/checkouts/reqwest-dc13ba947e7b959e/c156624/src/async_impl/body.rs:365:33:
there is no reactor running, must be called from the context of a Tokio 1.x runtime
```

Closes FR-118.

Release Notes:

- Reverted https://github.com/zed-industries/zed/pull/60301


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

- `crates/auto_update/src/auto_update.rs`: +0/-28
- `crates/gpui/src/app.rs`: +17/-30
- `crates/reqwest_client/src/reqwest_client.rs`: +0/-2
