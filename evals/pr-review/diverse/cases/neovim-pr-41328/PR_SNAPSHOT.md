# Frozen pull request snapshot

- PR: https://github.com/neovim/neovim/pull/41328 — `fix(cwd): nvim_win_set_buf changes global CWD`
- Author: justinmk
- Target base head: `9cca923ab4f9ddca4b817e989eba546ddba675e1`
- Comparison base: `9cca923ab4f9ddca4b817e989eba546ddba675e1`
- Exact source head: `aeae2ff9577dc8784a13f6132284264ec40eec37`
- Diff: 43 additions, 10 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Problem:
nvim_win_set_buf() on a non-current win, while the current win has
a win-local dir, changes the global CWD:

    :vsplit | lcd ..
    :call nvim_win_set_buf(other_win, buf)
    :wincmd l
    :verbose pwd
    [global] /parent        " expected: the initial cwd

Analysis:
`globaldir` is where to return when no local dir applies; NULL means the
process CWD is already there. Switching to a window with no local dir
makes update_cwd() chdir back to `globaldir` and clear it. kCtxKeepCwd
restores the process CWD but not that bookkeeping, so the restored
window-local dir is mistaken for the global one.

Solution:
Save/restore `globaldir` with the CWD.

fix https://github.com/neovim/neovim/issues/41238


## Linked issues

### https://github.com/neovim/neovim/issues/41238 — `nvim_win_set_buf` might change global working directory

### Problem

Using `nvim_win_set_buf` on not current window while current window has window-local cwd leads to the change of global cwd.

### Steps to reproduce

1. Create the following `init.lua`:

    ```lua
    local init_win_id = vim.api.nvim_get_current_win()
    vim.cmd('vsplit')
    vim.cmd('lcd ..')
    vim.api.nvim_win_set_buf(init_win_id, vim.api.nvim_create_buf(false, true))
    ```

2. `nvim --clean -u init.lua`.
3. `:verbose pwd` correctly shows `[window] <path to ..>`.
4. `:wincmd l`
5. `:verbose pwd` not correctly shows `[global] <path to ..>` (parent path as the global working directory). The expected output is `[global] <initial cwd>`.

This particular behavior has started to get observed after 59597316a60b (#41218), but even before it the behavior is not correct (step 3 shows `[window] <initial cwd>`) up until going before ea3868bcf99b (#33320).

cc @erdivartanovich, @justinmk

### Expected behavior

Executing `nvim_win_set_buf(win_id, buf_id)` can change local working directory only if `buf_id` has set buffer-local working directory.

### Nvim version (nvim -v)

NVIM v0.13.0-dev-1275+ga08607b8d6

### Vim (not Nvim) behaves the same?

No, doesn't have this functionality

### Operating system/version

EndeavourOS Linux x86_64, 7.1.5-arch1-2

### Terminal name/version

Ghostty 1.3.1-arch2

### $TERM environment variable

xterm-ghostty

### Installation

Appimage and from source

## Exact-head checks

- Backport Pull Request: SKIPPED
- check: SKIPPED
- s390x: SKIPPED
- s390x: SKIPPED
- Backport Pull Request: SUCCESS
- old-cmake: SUCCESS
- Analyze: SUCCESS
- docs: SUCCESS
- label: SUCCESS
- lint-commits: SUCCESS
- check: SUCCESS
- request-reviewer: SUCCESS
- remove-reviewers: SUCCESS
- Run zizmor: SUCCESS
- lintc: SUCCESS
- FreeBSD: SUCCESS
- wasmtime: SUCCESS
- windows-asan: SKIPPED
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

- `src/nvim/context.c`: +19/-6
- `src/nvim/context_defs.h`: +3/-2
- `test/functional/ex_cmds/cd_spec.lua`: +21/-2
