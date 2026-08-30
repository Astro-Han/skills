# Frozen pull request snapshot

- PR: https://github.com/sveltejs/svelte/pull/18580 — `chore: deduplicate client/server context helpers`
- Author: Nic-Polumeyv
- Target base head: `3dde011d3a9e7b9145169da0b75dcd607a378c0e`
- Comparison base: `3dde011d3a9e7b9145169da0b75dcd607a378c0e`
- Exact source head: `1464c2af88c59a5c4395db1cef9cac9b31010890`
- Diff: 73 additions, 91 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

The server copy of `createContext` shipped without the `missing_context` throw and #17580 had to hand-mirror the client body back in, so this duplication has already cost a bug. This moves the realm-independent parts, the `createContext` tuple, `get_parent_context`, and `get_or_init_context_map`, into `internal/shared/context.js`, and each realm keeps its public context functions as thin wrappers over its own state. No behavior change, generated types are byte-identical.

### Before submitting the PR, please make sure you do the following

- [ ] It's really useful if your PR references an issue where it is discussed ahead of time. In many cases, features are absent for a reason. For large changes, please create an RFC: https://github.com/sveltejs/rfcs
- [x] Prefix your PR title with `feat:`, `fix:`, `chore:`, or `docs:`.
- [x] This message body should clearly illustrate what problems it solves.
- [ ] Ideally, include a test that fails without this PR but passes with it.
- [x] If this PR changes code within `packages/svelte/src`, add a changeset (`npx changeset`).

### Tests and linting

- [x] Run the tests with `pnpm test` and lint the project with `pnpm lint`


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Tests (20, windows-latest): SUCCESS
- Tests (20, macOS-latest): SUCCESS
- Tests (20, ubuntu-latest): SUCCESS
- Tests (22, ubuntu-latest): SUCCESS
- Tests (24, ubuntu-latest): SUCCESS
- TestNoAsync: SUCCESS
- TSGo: SUCCESS
- Lint: SUCCESS
- Benchmarks: SUCCESS
- unnamed: PENDING
- vite-ecosystem-ci: SKIPPED
- Vercel Agent Review: SUCCESS

## Changed files

- `.changeset/shared-context-helpers.md`: +5/-0
- `packages/svelte/src/internal/client/context.js`: +8/-44
- `packages/svelte/src/internal/server/context.js`: +8/-47
- `packages/svelte/src/internal/shared/context.js`: +52/-0
