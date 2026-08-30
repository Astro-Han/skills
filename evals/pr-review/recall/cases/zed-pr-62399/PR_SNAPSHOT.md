# Frozen pull request snapshot

- PR: https://github.com/zed-industries/zed/pull/62399 — `Revert "terminal: Actually close process groups when the terminal is closed (#61467)"`
- Author: ChristopherBiscardi
- Target base head: `1271f8b0e8f3278eed5dd3fc12ad4bd30dce2c5d`
- Comparison base: `1271f8b0e8f3278eed5dd3fc12ad4bd30dce2c5d`
- Exact source head: `8371f25da4f9a84602b0bfbe61f28cc876a21682`
- Diff: 20 additions, 227 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This reverts commit 6297c88f428a99741a7bfb33f31dfe98123bb8e4.

---

fixes #62286
fixes #62095

https://github.com/zed-industries/zed/pull/61467 fixed its intended bug, but at the same time introduced an issue where running tasks that would cause new tasks to be terminated immediately. https://github.com/zed-industries/zed/pull/62322 tried to fix that forward, but was unsuccessful. In the mean-time I am going to revert the original PR.

We can try to re-land the original bugfix in a future PR.

Release Notes:

- N/A


## Linked issues

### https://github.com/zed-industries/zed/issues/62095 — Tasks terminate with SIGKILL when re-run in an existing terminal

### Reproduction steps

1. Create .zed/tasks.json:
`[
  {
    "label": "Repro",
    "command": "echo PID $$; sleep 5; echo done",
    "use_new_terminal": false
  }
]`
2. Run Tasks: Spawn and select "Repro"
3. Wait for the task to finish successfully
4. Leave the terminal tab open
5. Run Tasks: Spawn again and select "Repro"

Expected:
The task runs successfully a second time in the existing terminal.

Actual:
The task is immediately terminated:

PID 12345
⏵ Task `Repro` terminated by signal: 9
⏵ Command: /bin/bash -i -c 'echo PID $; sleep 5; echo done'

### Current vs. Expected behavior

Expected:
The task runs successfully a second time in the existing terminal.

Actual:
The task is immediately terminated:

PID 12345
⏵ Task `Repro` terminated by signal: 9
⏵ Command: /bin/bash -i -c 'echo PID $; sleep 5; echo done'

### Zed version and system specs

Zed: v1.14.2+preview.334.c56b44b30cc03f42b74e9335e471ee2570d807d9 (Zed Preview) 
OS: Linux Wayland ubuntu 26.04
Memory: 6.1 GiB
Architecture: x86_64
GPU: AMD Radeon Graphics (RADV RENOIR) || radv || Mesa 26.0.3-1ubuntu1

### Attach Zed log file

<details><summary>Zed.log</summary>

<!-- Paste your log inside the code block. -->
```log

```

</details>


### Relevant Zed settings

<details><summary>settings.json</summary>

<!-- Paste your settings inside the code block. -->
```json

```

</details>


### Relevant Keymap

<details><summary>keymap.json</summary>

<!-- Paste your keymap file inside the code block. -->
```json

```

</details>


### (for AI issues) Model provider details

_No response_

### If you are using WSL on Windows, what flavor of Linux are you using?

_No response_

### https://github.com/zed-industries/zed/issues/62286 — Task won't re-run

### Reproduction steps

Try to start this task with a key.
{
    "label": "Run App",
    "command": "odin run game -show-timings",
    "use_new_terminal": false,
    "allow_concurrent_runs": false,
  },

It will run once. It won't run again until you close the console.
It gives the follwing message in the console.

⏵ Task `Run App` terminated by signal: 15
⏵ Command: /bin/fish -i -c 'odin run game -show-timings'


### Current vs. Expected behavior

It does not run the task again
It should.

### Zed version and system specs

Zed: v1.14.2+stable (Zed) 
OS: Linux Wayland cachyos
Memory: 15.5 GiB
Architecture: x86_64
GPU: NVIDIA GeForce GTX 1660 SUPER || NVIDIA || 610.57.04

### Attach Zed log file

<details><summary>Zed.log</summary>

<!-- Paste your log inside the code block. -->
```log

```

</details>


### Relevant Zed settings

<details><summary>settings.json</summary>

<!-- Paste your settings inside the code block. -->
```json

```

</details>


### Relevant Keymap

<details><summary>keymap.json</summary>

<!-- Paste your keymap file inside the code block. -->
```json

```

</details>


### (for AI issues) Model provider details

_No response_

### If you are using WSL on Windows, what flavor of Linux are you using?

_No response_

## Exact-head checks

- route-pr: SKIPPED
- route-pr: SKIPPED
- route-pr: SKIPPED
- route-pr: SKIPPED
- route-pr: SKIPPED
- route-pr: SKIPPED
- batch-suggestions: SKIPPED
- batch-suggestions: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- build_nix_linux_x86_64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- bundle_linux_aarch64: SKIPPED
- route-pr: SUCCESS
- react: SUCCESS
- check-authorship-and-label: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
- danger: SUCCESS
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

- `crates/terminal/src/pty_info.rs`: +11/-72
- `crates/terminal/src/terminal.rs`: +9/-155
