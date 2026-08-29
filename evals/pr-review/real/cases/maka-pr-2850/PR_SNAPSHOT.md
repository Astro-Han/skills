# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/2850 — `test(core): trim search normalizer matrices`
- Author: jackwener
- Target base head: `7fc533782964ab56e4e39122094876e74f7bb53b`
- Comparison base: `7fc533782964ab56e4e39122094876e74f7bb53b`
- Exact source head: `308d5c8f2cb89b7d9c6df8312d29fdefa8034051`
- Diff: 12 additions, 78 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary
- collapse equivalent Search and WebSearch normalization matrices to one owner per production predicate
- retain security, freshness-language, bound, and malformed-input boundaries
- remove stale PR-history comments while preserving current privacy and credential invariants

## Validation
- `npx biome check packages/core/src/__tests__/web-search.test.ts packages/core/src/web-search.ts packages/core/src/__tests__/search.test.ts packages/core/src/search.ts`
- `git diff --check`
- static reference and predicate-ownership audit

Test suites intentionally not run; CI owns execution.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- changes: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: FAILURE
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SKIPPED
- storybook: SKIPPED
- test: SUCCESS

## Changed files

- `packages/core/src/__tests__/search.test.ts`: +4/-8
- `packages/core/src/__tests__/web-search.test.ts`: +1/-3
- `packages/core/src/search.ts`: +3/-37
- `packages/core/src/web-search.ts`: +4/-30
