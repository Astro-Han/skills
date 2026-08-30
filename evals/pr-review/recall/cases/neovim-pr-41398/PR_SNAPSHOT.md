# Frozen pull request snapshot

- PR: https://github.com/neovim/neovim/pull/41398 — `fix(lsp): do not expand $VAR in tagfunc filenames`
- Author: shubhxho
- Target base head: `31de0d69fc745b342352f04a03cbcb90211c4edc`
- Comparison base: `31de0d69fc745b342352f04a03cbcb90211c4edc`
- Exact source head: `6d9c6083906d7e2d75159952b4c0e90ccf606d7d`
- Diff: 20 additions, 1 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Problem:
`CTRL-]` via `vim.lsp.tagfunc` passes URI paths through `:tag`, which expands `$VAR`. Files such as `people_.$personId.tsx` then fail with E429.

Solution:
`fnameescape()` the filename in tag items so `$` is treated as literal.

Fixes #41313

## Linked issues

### https://github.com/neovim/neovim/issues/41313 — LSP: dollar signs in URIs treated as variables to expand

### Problem

I have a filename that contains a dollar sign (because I'm using [TanStack Router's file-based routing](https://tanstack.com/router/latest/docs/routing/file-based-routing), where dollar signs have special meaning). When I try to jump to the definition of the symbol under my cursor (using `CTRL-]`), Neovim treats the whole segment that includes the dollar sign as blank, and complains that there is no file with a matching name:

```
E429: File ".../people_..tsx" does not exist
```

After some investigation, it seems that Neovim is trying to expand the variable $personId, and replaces it with an empty string as it's not set. I can tell this is happening because if I `export $personId=1` before starting Neovim, then I get the error "E429: File ".../people_.1.tsx" does not exist".

As a workaround, I can `export $personId='$personId'` before starting Neovim, and code navigation in this file works.


### Steps to reproduce using "nvim --clean -u minimal_init.lua"

Create four files:

minimal_init.lua:

```lua
local pattern = "typescriptreact"
-- Taken from https://github.com/neovim/nvim-lspconfig/blob/51dbf5359da86721662c87ca10eb73add973737b/lsp/tsc.lua#L66
local cmd = function(dispatchers, config)
	local cmd = "tsc"
	local bins = { "tsc", "tsgo" }
	for _, bin in ipairs(bins) do
		if (config or {}).root_dir then
			local local_cmd = vim.fs.joinpath(config.root_dir, "node_modules/.bin", bin)
			if vim.fn.executable(local_cmd) == 1 then
				cmd = local_cmd
				break
			end
		end
		if vim.fn.executable(bin) == 1 then
			cmd = bin
			break
		end
	end
	return vim.lsp.rpc.start({ cmd, "--lsp", "--stdio" }, dispatchers)
end
local root_markers =
	{ "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock", ".git", ".editorconfig" }
local settings = vim.empty_dict()

vim.api.nvim_create_autocmd("FileType", {
	pattern = pattern,
	callback = function(args)
		local match = vim.fs.find(root_markers, { path = args.file, upward = true })[1]
		local root_dir = match and vim.fn.fnamemodify(match, ":p:h") or nil
		vim.lsp.start({
			name = "bugged-ls",
			cmd = cmd,
			root_dir = root_dir,
			settings = settings,
		})
	end,
})
```

.editorconfig (empty)

a.tsx:

```tsx
function f(x: string) { return x }
```

a.$b.tsx:


```tsx
function g(x: string) { return x }
```

- Install tsc, e.g. `npm init -y`, `npm install typescript`.
- Run `nvim --clean -u minimal_init.lua a.tsx`, and hit `CTRL-]` on the final `x`. Your cursor will be taken to the `x` parameter.
- Make sure the the env var `b` is unset. Run `nvim --clean -u minimal_init.lua a.\$b.tsx`, and hit `CTRL-]` on the final `x`. You will see an error similar to the above.


### Expected behavior

`CTRL-]` on the final `x` works without error in a.$b.tsx too, taking the cursor to the `x` parameter.

### Nvim version (nvim -v)

NVIM v0.13.0-dev-1315+g69e61d52e2

### Language server name/version

tsc 7.0.2

### Operating system/version

ubuntu 26.04

### Log file

https://gist.github.com/mattgallagher92/1a4a45a9a4e7d0d159204100a7a52d26

## Exact-head checks

- label: SKIPPED
- s390x: SKIPPED
- Backport Pull Request: SUCCESS
- old-cmake: SUCCESS
- Analyze: SUCCESS
- docs: SUCCESS
- lint-commits: SUCCESS
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
- macos arm clang functionaltest: FAILURE
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

- `runtime/lua/vim/lsp/_tagfunc.lua`: +2/-1
- `test/functional/plugin/lsp_spec.lua`: +18/-0
