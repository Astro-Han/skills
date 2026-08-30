# Frozen pull request snapshot

- PR: https://github.com/nushell/nushell/pull/18603 — `fix: stop `run` from trying to parse big non-text files`
- Author: fdncred
- Target base head: `e3dcf2d9bb5dd585e3bc96ca0fdab4f90ab6eff8`
- Comparison base: `35f2c1015383c154d5c2d3a930700fc4bce612b0`
- Exact source head: `18fa73d2b3b12c9b702e7bafad1505242d57c39c`
- Diff: 437 additions, 52 deletions, 5 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<!--
Thanks for contributing to Nushell!

Before submitting, please read the contributing guide:
https://github.com/nushell/nushell/blob/main/CONTRIBUTING.md

This template helps reviewers understand your changes and allows us to generate high-quality release notes.
-->

## Description
This PR stops the `run` command from trying to parse non-text files nor files that are big. There's a heuristic that determines non-text by looking at the first 8192 bytes of a file and big is currently set at 1_048_576 bytes.

<!--
Explain what this PR does and why.

This section is intentionally flexible:
- Describe the problem
- Explain your approach
- Include technical details if relevant

Good examples:
- "In this PR, I fixed..."
- "In this PR, I added support for..."
- "This change improves X by..."

Write as much or as little as needed for reviewers to understand your changes.
-->

## User-facing changes (Release notes)
Stop `run` from hanging by not parsing files over 1MB or non-text.

<!--
This section is used (mostly as-is) for https://www.nushell.sh/blog/

Describe how Nushell behavior changes from a user's perspective.
Do NOT describe internal Rust changes here.

Write in a release note style, for example:
- "Added support for..."
- "Fixed an issue where..."
- "Nushell now supports..."
- "Improved performance of..."

If your changes do NOT affect users (internal refactors, cleanup, etc.),
just write:
- "n/a"
- "nan"
- or similar

This tells us the change should not appear in the changelog.

Tips:
- Focus on observable behavior
- Include examples if helpful
- Keep it concise

You can:
- Write a short paragraph (will appear as a bullet point), OR
- Use headings (###) if your change needs more structure

Avoid writing things like:
- "In this PR, I refactored..."
- "This updates internal code..."

You may leave this blank until the PR is ready.
-->

## Additional notes
closes https://github.com/nushell/nushell/issues/18597
<!--
Optional.

Examples:
- fixes #123
- closes #456
- related #789

Anything else reviewers should know.
Remove this section if not needed.
-->

## Linked issues

### https://github.com/nushell/nushell/issues/18597 — The new `run` command (`0.114.0`) hangs depending on its argument

### Bug report form

- [x] I have done a basic search of the issue tracker to find any existing issues that are similar.
- [x] I have checked that my version is at least the latest stable release available via my installation method.

### Describe the bug

It seems that `run` arguments (files) are read then parsed before the command is even executed.
If a file is "big enough", `nu` will hang and use `>1Go` or RAM.

### How to reproduce

1. Go to an empty directory
1. Put a file with with at last 50Mo
1. Type `run <Tab>` (the word "run", the `space` key then the `tab` key)

Here is a minimal code:
**WARNING** your shell might hang

```nu
cd (mktemp -d)

# Add a file big enough to trigger the freezing ...but not too big
http get https://github.com/nushell/nushell/releases/download/0.114.1/nu-0.114.1-x86_64-unknown-linux-musl.tar.gz
| save --progress nu-0.114.1-x86_64-unknown-linux-musl.tar.gz

run <Tab>

```

### Expected behavior

1. No hang
1. No excessive RAM usage

### Configuration

| key                  | value                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| version              | 0.114.1                                                                                                                                          |
| major                | 0                                                                                                                                                |
| minor                | 114                                                                                                                                              |
| patch                | 1                                                                                                                                                |
| branch               |                                                                                                                                                  |
| commit_hash          | 0df4ca222cc713e79b6b1684ad8ccaec584ce4ac                                                                                                         |
| build_os             | linux-x86_64                                                                                                                                     |
| build_target         | x86_64-unknown-linux-musl                                                                                                                        |
| rust_version         | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                              |
| rust_channel         | 1.95.0-x86_64-unknown-linux-gnu                                                                                                                  |
| cargo_version        | cargo 1.95.0 (f2d3ce0bd 2026-03-21)                                                                                                              |
| build_time           | 2026-07-11 16:18:14 +00:00                                                                                                                       |
| build_rust_channel   | release                                                                                                                                          |
| allocator            | standard                                                                                                                                         |
| features             | default, lsp, mcp, network, plugin, rustls-tls, sqlite, static-link-openssl, trash-support                                                       |
| installed_plugins    |                                                                                                                                                  |
| experimental_options | example=false, dc-glob=false, reorder-cell-paths=true, pipefail=true, enforce-runtime-annotations=true, native-clip=false, cell-path-types=false |

## Exact-head checks

- triage: SUCCESS
- Milestone Update: SUCCESS
- Spell Check with Typos: SUCCESS
- `cargo` in root (Ubuntu): SUCCESS
- `cargo` in nu-parser/fuzz (Ubuntu): SUCCESS
- `cargo` in nu-path/fuzz (Ubuntu): SUCCESS
- `cargo` in root (Windows): SUCCESS
- `cargo` in nu-parser/fuzz (Windows): SUCCESS
- `cargo` in nu-path/fuzz (Windows): SUCCESS
- `cargo` in root (MacOS): SUCCESS
- `cargo` in nu-parser/fuzz (MacOS): SUCCESS
- `cargo` in nu-path/fuzz (MacOS): SUCCESS
- `cargo` in root (WASM): SUCCESS
- std-lib-and-python-virtualenv (ubuntu-22.04, py): SUCCESS
- std-lib-and-python-virtualenv (macos-latest, py): SUCCESS
- std-lib-and-python-virtualenv (windows-latest, py): SUCCESS

## Changed files

- `crates/nu-command/src/misc/run.rs`: +34/-2
- `crates/nu-command/tests/commands/run.rs`: +122/-1
- `crates/nu-parser/src/parse_source.rs`: +86/-49
- `crates/nu-protocol/src/errors/parse_error.rs`: +30/-0
- `crates/nu-protocol/src/parser_path.rs`: +165/-0
