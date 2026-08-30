# Frozen pull request snapshot

- PR: https://github.com/neovim/neovim/pull/41489 — `revert: "fix(lsp): do not expand $VAR in tagfunc filenames"`
- Author: justinmk
- Target base head: `8adf6e769f6573ba98168bb4c81039cc8e0d5831`
- Comparison base: `8adf6e769f6573ba98168bb4c81039cc8e0d5831`
- Exact source head: `c11ecd38292768bef92e886f97bf21de47df4427`
- Diff: 1 additions, 20 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Reverts neovim/neovim#41398

https://github.com/neovim/neovim/pull/41398#issuecomment-5414331869

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- lint-commits: FAILURE
- s390x: SKIPPED
- Backport Pull Request: SUCCESS
- old-cmake: SUCCESS
- Analyze: SUCCESS
- docs: SUCCESS
- label: SUCCESS
- check: SUCCESS
- remove-reviewers: SUCCESS
- Run zizmor: SUCCESS
- lintc: SUCCESS
- FreeBSD: SUCCESS
- wasmtime: SUCCESS
- windows-asan: SKIPPED
- use-existing-src: SUCCESS
- ai-assisted: SUCCESS
- lint: SUCCESS
- OpenBSD: SUCCESS
- request-reviewer / request-reviewer: SUCCESS
- clang-analyzer: SUCCESS
- ubuntu asan clang unittest: SUCCESS
- ubuntu asan clang functionaltest: SUCCESS
- ubuntu asan clang oldtest: SUCCESS
- ubuntu tsan clang functionaltest: SUCCESS
- ubuntu release gcc unittest: SUCCESS
- ubuntu release gcc functionaltest: SUCCESS
- ubuntu release gcc oldtest: SUCCESS
- ubuntu arm clang unittest: SUCCESS
- ubuntu arm clang functionaltest: SUCCESS
- macos intel clang unittest: SUCCESS
- macos intel clang functionaltest: SUCCESS
- macos intel clang oldtest: SUCCESS
- macos arm clang unittest: SUCCESS
- macos arm clang functionaltest: SUCCESS
- macos arm clang oldtest: SUCCESS
- ubuntu puc-lua gcc functionaltest: SUCCESS
- ubuntu puc-lua gcc oldtest: SUCCESS
- build using zig build (linux): SUCCESS
- build using zig build (macos 15): SUCCESS
- build using zig build (windows): SUCCESS
- windows / windows (functional): SUCCESS
- windows / windows (old): SUCCESS
- with-external-deps: SUCCESS
- CodeQL: SUCCESS
- zizmor: SUCCESS

## Changed files

- `runtime/lua/vim/lsp/_tagfunc.lua`: +1/-2
- `test/functional/plugin/lsp_spec.lua`: +0/-18
