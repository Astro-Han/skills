# Frozen pull request snapshot

- PR: https://github.com/nushell/nushell/pull/18620 — `feat(date): add new commands `date floor` and `date ceil``
- Author: pyz4
- Target base head: `b70fc60a8ea2bb329b4f818f392643c1f72abf1b`
- Comparison base: `7278ef34dd79016721be72f30c64a70dc3fd999c`
- Exact source head: `8c90a5dd762d62649b2572055d5fb5ce999db094`
- Diff: 289 additions, 0 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<!--
Thanks for contributing to Nushell!

Before submitting, please read the contributing guide:
https://github.com/nushell/nushell/blob/main/CONTRIBUTING.md

This template helps reviewers understand your changes and allows us to generate high-quality release notes.
-->

## Description
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
This PR adds two new commands `date floor` and `date ceil` that rounds a date value down and up, respectively, to a specified duration boundary. See examples

## User-facing changes (Release notes)
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
### Added `date floor` and `date ceil` commands

Users will have access to two new commands `date floor` and `date ceil` that rounds a date value down and up, respectively, to a specified duration boundary.
```nushell
#  Round down to the nearest hour
  > 2026-07-15T12:11:10-04:00 | date floor 1hr
  Wed, 15 Jul 2026 12:00:00 -0400

# Round list of dates down to the nearest 2day boundary
  > [2026-07-10T00:00:00-04:00 2026-07-15T00:00:00-04:00] | date floor 2day
  ╭───┬───────────────────────╮
  │ 0 │ 07/10/2026 12:00:00AM │
  │ 1 │ 07/14/2026 12:00:00AM │
  ╰───┴───────────────────────╯

#  Round date up to nearest hour
  > 2026-07-15T12:11:10-04:00 | date ceil 1hr
  Wed, 15 Jul 2026 12:59:59 -0400

#  Round list of dates up to nearest 2day boundary
  > [2026-07-10T00:00:00-04:00 2026-07-15T00:00:00-04:00] | date ceil 2day
  ╭───┬───────────────────────╮
  │ 0 │ 07/11/2026 11:59:59PM │
  │ 1 │ 07/15/2026 11:59:59PM │
  ╰───┴───────────────────────╯
```

## Additional notes
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

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

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

- `crates/nu-command/src/date/ceil.rs`: +143/-0
- `crates/nu-command/src/date/floor.rs`: +140/-0
- `crates/nu-command/src/date/mod.rs`: +4/-0
- `crates/nu-command/src/default_context.rs`: +2/-0
