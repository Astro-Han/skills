# Frozen pull request snapshot

- PR: https://github.com/rust-lang/rust/pull/161796 — `Remove dead parse error recovery (underscores in expressions)`
- Author: fmease
- Target base head: `0f33d0912709e847199218ebab88e2311872f364`
- Comparison base: `be0ea33bba5000ac134e58acde780af83d908e44`
- Exact source head: `8de399ac7b7cce3314f4f7e2cd2e1285b1608e14`
- Diff: 2 additions, 23 deletions, 1 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Back in https://github.com/rust-lang/rust/pull/63337/changes/b7f7756566c9e10983ee51bc97afe9852838299a (2019) the parser was extended to recover from `_`s as elements of tuple expressions (this was later extended to also cover call expressions). At the time, `_` obviously wasn't an expression yet.

Nowadays `parse_expr_res` will *always* successfully parse `_` as an `ExprKind::Underscore` (irrespective of the passed `Restrictions`). Consequently, we will never reach the special case in `parse_expr_catch_underscore`. Drop this entire wrapper function.

<sub>(No LLM was or will be used by me during the entire creation process of this PR)</sub>

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Calculate job matrix: SUCCESS
- PR - pr-check-1: SUCCESS
- PR - pr-check-2: SUCCESS
- PR - tidy: SUCCESS
- PR - x86_64-gnu-llvm-21: SUCCESS
- PR - aarch64-gnu-llvm-21-1: SUCCESS
- PR - aarch64-gnu-llvm-21-2: SUCCESS
- PR - x86_64-gnu-tools: SUCCESS
- PR - x86_64-gnu-miri: SUCCESS
- PR - x86_64-gnu-gcc: SUCCESS
- PR - x86_64-gnu-gcc-core-tests: SUCCESS
- PR - x86_64-gnu-next-trait-solver-polonius: SUCCESS
- publish toolstate: SKIPPED

## Changed files

- `compiler/rustc_parse/src/parser/expr.rs`: +2/-23
