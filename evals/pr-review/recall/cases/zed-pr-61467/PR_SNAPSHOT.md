# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/61467 — `terminal: Actually close process groups when the terminal is closed`
- Author: feitreim
- Target base head: `ec3d887507f272119d9fe146c685f0a941d0e798`
- Comparison base: `2c4e44704c37ee87e59ac84e3e17388178b28545`
- Exact source head: `b587ef686d0ddc7c222ffa8ff2672a0a6333c535`
- Diff: 227 additions, 20 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

# Objective

Closes #47412

Currently, processes that ignore SIGHUP/SIGTERM will not be killed when the terminal is closed or Zed is closed.

## Solution

We need to follow up on the processes to ensure that they have been properly killed BEFORE zed closes fully. We send SIGTERM then 100ms later send SIGKILL, this gives programs some time to exit gracefully before being SIGKILL'd.

## Testing

I tested it by both closing the terminal pane and closing zed completely, both worked. There is a new test added as well. The best way to test it is with the reproduction in this comment:
https://github.com/zed-industries/zed/issues/47412#issuecomment-4596563655

I only tested this on MacOS 27. It might be worth testing on linux, but also mac/linux behavior here should be quite similar. Windows behavior as well should be unchanged but could be worth testing.

## Self-Review Checklist:

- [x] I've reviewed my own diff for quality, security, and reliability
- [x] Unsafe blocks (if any) have justifying comments

Okay there is an unsafe block in this PR, but its just being moved from one location to another, and it didn't originally have a comment, I assume because its just a libc call so its pretty clear.

- [x] The content adheres to Zed's UI standards ([UX/UI](https://github.com/zed-industries/zed/blob/main/CONTRIBUTING.md#uiux-checklist) and [icon](https://github.com/zed-industries/zed/blob/main/crates/icons/README.md) guidelines)
- [x] Tests cover the new/changed behavior
- [x] Performance impact has been considered and is acceptable

## Showcase

Video showcasing the new behavior:

https://github.com/user-attachments/assets/b2b8cb0c-0648-41b4-b940-91c466aeaab3



---

Release Notes:

- Terminal: Prevents processes from being left alive when the terminal is closed.


## Linked issues

### https://github.com/zed-industries/zed/issues/47412 — Child processes not terminated when integrated terminal closes

## Description

When running long-lived CLI processes (e.g., `claude` CLI) in Zed's integrated terminal, closing Zed or the terminal tab does not properly terminate the child processes. They become orphaned and continue running in the background.

## Reproduction

1. Open Zed
2. Open integrated terminal
3. Run a long-lived CLI process (e.g., `claude`, `node`, or any REPL)
4. Close Zed (or close the terminal tab)
5. Check for orphaned processes: `ps aux | grep <process> | awk '$7 == "??"'`

## Observed behavior

Child processes remain running with no controlling terminal (TTY shows `??`):

```
$ ps -p <pid> -o pid,tty,state,command
  PID TTY      STAT COMMAND
 4754 ??       S    claude --dangerously-skip-permissions
```

Multiple orphaned processes accumulate over time, consuming memory.

## Expected behavior

Child processes should receive SIGHUP (or SIGTERM) when:
- The terminal tab is closed
- Zed is quit

This is standard terminal behavior - iTerm and Terminal.app both handle this correctly.

## Environment

- macOS (Darwin 25.2.0)
- Zed (latest stable)

## Workaround

Manually kill orphaned processes:
```bash
ps aux | grep <process> | awk '$7 == "??" {print $2}' | xargs kill
```

## Exact-head checks

- batch-suggestions: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- route-pr: SUCCESS
- route-pr: SUCCESS
- route-pr: SUCCESS
- route-pr: SUCCESS
- route-pr: SUCCESS
- route-pr: SUCCESS
- react: SUCCESS
- check-authorship-and-label: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- orchestrate: SUCCESS
- cherry-pick-suggestions: SKIPPED
- build_nix_mac_aarch64: SKIPPED
- build_nix_mac_aarch64: SKIPPED
- build_nix_mac_aarch64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- bundle_linux_x86_64: SKIPPED
- check_style: SUCCESS
- build_static_bwrap_linux_aarch64: SKIPPED
- build_static_bwrap_linux_aarch64: SKIPPED
- build_static_bwrap_linux_aarch64: SKIPPED
- clippy_windows: SUCCESS
- build_static_bwrap_linux_x86_64: SKIPPED
- build_static_bwrap_linux_x86_64: SKIPPED
- build_static_bwrap_linux_x86_64: SKIPPED
- clippy_linux: SUCCESS
- bundle_mac_aarch64: SKIPPED
- bundle_mac_aarch64: SKIPPED
- bundle_mac_aarch64: SKIPPED
- clippy_mac: SUCCESS
- bundle_mac_x86_64: SKIPPED
- bundle_mac_x86_64: SKIPPED
- bundle_mac_x86_64: SKIPPED
- clippy_mac_x86_64: SUCCESS
- bundle_windows_aarch64: SKIPPED
- bundle_windows_aarch64: SKIPPED
- bundle_windows_aarch64: SKIPPED
- run_tests_windows: SUCCESS
- bundle_windows_x86_64: SKIPPED
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

- `crates/terminal/src/pty_info.rs`: +72/-11
- `crates/terminal/src/terminal.rs`: +155/-9
