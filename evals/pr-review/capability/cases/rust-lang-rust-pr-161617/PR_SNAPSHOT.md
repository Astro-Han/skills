# Frozen pull request snapshot

- PR: https://github.com/rust-lang/rust/pull/161617 — `Add custom allocators to `(try_)map` on `Box`, `Rc`, `Arc``
- Author: maxdexh
- Target base head: `9a4ad59ae3073b013cd62f53f8349ddc61a012e8`
- Comparison base: `9a4ad59ae3073b013cd62f53f8349ddc61a012e8`
- Exact source head: `c158e179965998fdc994c82f19f6398550750271`
- Diff: 265 additions, 252 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Adds custom allocators to `(try_)map` on `Box`, `Rc`, `Arc`. 

Not on `UniqueArc`/`UniqueRc` because too much allocator-related API is missing atm and I didn't want to end up writing unsound garbage. The `else` branch in those needs to drop a weakref, I'll get to that later.

cc rust-lang/rust#160534

r? nia-e

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

- `library/alloc/src/boxed.rs`: +71/-76
- `library/alloc/src/rc.rs`: +96/-87
- `library/alloc/src/sync.rs`: +96/-87
- `tests/ui/privacy/suggest-box-new.stderr`: +2/-2
