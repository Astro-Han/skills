# Frozen pull request snapshot

- PR: https://github.com/neovim/neovim/pull/41342 — `ci: bundle wasm output with demo into a single zip`
- Author: Rawan10101
- Target base head: `0c091cedc291ee4dd13ccae192057d92878aee0e`
- Comparison base: `b78adb98bac2d589551a5b09bb0a7e39887321f4`
- Exact source head: `732da013c70124b6ef66c696091e736d0f07c33b`
- Diff: 29 additions, 6 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This PR bundles the wasm build output with the browser demo into a single zip and wires it into the release workflow. It will be easy to just unzip and run `python3 serve.py`.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- label: SKIPPED
- s390x: SKIPPED
- Backport Pull Request: SUCCESS
- old-cmake: SUCCESS
- Analyze: SUCCESS
- docs: SUCCESS
- lint-commits: SUCCESS
- check: SUCCESS
- Build nvim.wasm (Emscripten + Zig): SUCCESS
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
- request-reviewer: SKIPPED
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

- `.github/scripts/build_wasm.sh`: +21/-0
- `.github/workflows/release.yml`: +8/-6
