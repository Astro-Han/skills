# Pull request snapshot

- PR: https://example.test/pulls/433 — `fix(routes): canonicalize mixed-case method names`
- Issue: https://example.test/issues/430 — `mixed-case method misses registered route`
- Author: coral
- Base: main
- Exact head: `4337e570`
- Diff: 196 additions, 5 deletions, 2 files
- Split: production 12 additions, 5 deletions; tests 184 additions, 0 deletions
- Files: `route_registry.py`, `tests/test_route_registry.py`
- CI for `4337e570`: unit SUCCESS; lint SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

A user report, request trace, and minimal reproduction demonstrate that `pOsT` misses a route
registered as `POST`. `RouteRegistry.canonical_method()` is already the single normalization
owner. The production change applies that canonicalizer at lookup and removes a caller-specific
lowercase conversion.

The tests add a 36-row case matrix across six spellings, three unrelated paths, and two handler
names. Only three partitions exercise different behavior: canonical uppercase, mixed case, and an
unsupported method. Existing tests already cover path and handler variation. The three boundary
tests fail before the production change and pass after it; the other 33 rows add no distinct
contract, branch, failure mode, or production composition.
