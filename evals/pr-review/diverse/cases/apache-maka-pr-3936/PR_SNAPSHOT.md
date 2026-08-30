# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3936 — `refactor(runtime-host): remove the uncalled execution.inspect.resolve operation`
- Author: liuxiaocs7
- Target base head: `1c6b68ece63bca6ca6b8af26142b4627af1d68b9`
- Comparison base: `01369b08248d8b66b6c5a1a6204f9683397a10a1`
- Exact source head: `01c3e5d8aa771afb8f73ecb0d73fd6f6caf5b081`
- Diff: 93 additions, 373 deletions, 14 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

`execution.inspect` exposed two operations, but Desktop calls only `execution.inspect.query` (with `kind: 'turn_trace'` and the Session/Turn trace kinds). `execution.inspect.resolve` was registered in the protocol, the operation table, and the coordinator, yet had **no non-test caller anywhere in the repository** — a second inspection contract that no shipped surface reads.

This removes `resolve` end to end across every layer that maintained it:

- **Protocol** (`execution-inspect.ts`): the operation spec, its input/output decoders and assertions, the `ExecutionInspectCandidate` / `ExecutionInspectEntityKind` types, the candidate decoder, and the `EXECUTION_INSPECT_CANDIDATE_MAX_ITEMS` limit.
- **Operation table** (`operations.ts`): the `execution.inspect.resolve` entry. `ExecutionInspectOperationKey` collapses to just `query` automatically.
- **Coordinator** (`execution-inspect-coordinator.ts`): the handler entry, `#resolve`, its `#findSession` / `#findRunInSession` / `compareCandidates` helpers, and the now single-value `failure()` helper (assertion dropped).
- **Storage**: `ExecutionAgentRunReader.findRunsById` — the only reader reachable exclusively from `resolve` — plus the resolve-only `core_agent_runs_identity` SQLite index. `AgentRunIdentitySearchResult` / `assertIdentitySearchLimit` stay; `listSessionRunsBounded` shares them.
- **Compatibility epoch**: bumped `RUNTIME_HOST_COMPATIBILITY_EPOCH` to 64 (rebased onto main, which advanced it to 63) so a peer that still knows `resolve` fails the handshake rather than sending a removed operation mid-connection (same treatment `oauth.account.usage.fetch` received).
- **Retired credential grant**: registered `execution.inspect.resolve` as a retired operation grant so an access file issued before the removal releases the grant on decode instead of throwing `RuntimeHostAccessInputError` and blocking Host startup.
- **Storage schema**: bumped the core-execution schema version 5 → 6 and drop the stale index on upgrade so existing databases reconcile to the new target schema.

`execution.inspect.query` and all four of its result kinds (`session`, `agent_run`, `turn_trace`, `session_trace_page`) — including the Turn/Session trace paths Desktop renders — are untouched.

Fixes #3932

## Verification

- **Typecheck**: `@maka/core`, `@maka/storage`, and `@maka/runtime` build clean; `@maka/storage` and `@maka/runtime-host` both pass `tsc --noEmit` with zero errors. (An earlier run reported a `workhub-coordination-action-gate.test.ts` type error; that was a stale-dependency-dist artifact from building out of order and does **not** reproduce on a clean full build — noted here for transparency since the first revision's description mentioned it.)
- **Affected suites pass locally** (`node --test` on built output):
  - runtime-host: `execution-inspect-protocol`, `execution-inspect-coordinator`, `execution-inspect-uds`, `protocol` (incl. the new epoch-64 test), `access-credential-metadata` (incl. the new retired-grant regression test), `handshake-compatibility`.
  - storage: `sqlite-core-execution-store` (incl. the new "drops the obsolete AgentRun identity index on upgrade" migration test).
- **Lint/format**: `biome check` clean on all changed files.

## Migration / Rollout

Removing `resolve` is a wire-contract change, so the compatibility epoch is bumped (mixed-version peers fail the handshake by design) and the core-execution schema version is bumped so an upgraded Host drops the obsolete index on first open. Both paths have regression tests. Access files that recorded the `resolve` grant now decode cleanly with the grant released.

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: Claude Opus (via Claude Code) — traced the reachable set, performed the end-to-end deletion, added the epoch/credential/schema retirements and their tests. Both commits carry a `Generated-by: Claude Opus` trailer.

## Checklist

- [x] Tests cover the change and fail without it — the epoch bump, retired grant, and index drop each have a regression test that fails on the pre-change behavior; the deleted `resolve` tests are removed and the retained `query` suites still pass.
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary / Migration above (handshake boundary + storage migration; no change to any shipped feature)
- [ ] No


## Linked issues

### https://github.com/apache/maka/issues/3932 — refactor(runtime-host): remove the uncalled execution.inspect.resolve operation

## Problem

`execution.inspect` exposes two operations. Desktop calls only `execution.inspect.query`, and only with `kind: 'turn_trace'` (`apps/desktop/src/main/runtime-host-boot.ts:1479`). `execution.inspect.resolve` is registered in the protocol (`packages/runtime-host/src/protocol/execution-inspect.ts:111`), in the operation table (`packages/runtime-host/src/protocol/operations.ts:255`), and handled by the coordinator (`packages/runtime-host/src/server/execution-inspect-coordinator.ts:73`), but it has no non-test caller anywhere in the repository.

## Desired outcome

Delete `execution.inspect.resolve` end to end: the operation spec, its input/output decoders and assertions, the operation-table entry, the coordinator branch, and any storage reader reachable only from it.

Keep: `execution.inspect.query`, both of its result kinds, and the Turn trace path Desktop renders.

## Scope note

The working draft estimated 2.2k–2.4k lines for this candidate. That number does not hold — `execution-inspect.ts` and `execution-inspect-coordinator.ts` are 380 and 555 lines together, and `query` stays. Expect a much smaller deletion, and confirm the real reachable set before sizing the PR.

## Alternatives or workarounds

Keeping `resolve` maintains a second inspection contract that no shipped surface reads.

Proposed in [#3618](https://github.com/apache/maka/discussions/3618). The rule for this issue is one end-to-end deletion, one PR, and strictly fewer maintained concepts; moving the same idea behind a new facade or compatibility bridge does not count.

Claude verified the consumer claims below against current `main`. A human contributor must confirm them and own the resulting change.



## Exact-head checks

- test: SUCCESS
- windows_recovery: SUCCESS

## Changed files

- `packages/runtime-host/src/__tests__/access-credential-metadata.test.ts`: +34/-1
- `packages/runtime-host/src/__tests__/execution-inspect-coordinator.test.ts`: +1/-36
- `packages/runtime-host/src/__tests__/execution-inspect-protocol.test.ts`: +2/-58
- `packages/runtime-host/src/__tests__/execution-inspect-uds.test.ts`: +0/-8
- `packages/runtime-host/src/__tests__/protocol.test.ts`: +9/-0
- `packages/runtime-host/src/protocol/execution-inspect.ts`: +0/-143
- `packages/runtime-host/src/protocol/index.ts`: +4/-1
- `packages/runtime-host/src/protocol/operations.ts`: +0/-1
- `packages/runtime-host/src/server/access-credential-store.ts`: +3/-0
- `packages/runtime-host/src/server/execution-inspect-coordinator.ts`: +8/-95
- `packages/storage/src/__tests__/sqlite-core-execution-store.test.ts`: +29/-0
- `packages/storage/src/agent-run-store.ts`: +0/-23
- `packages/storage/src/execution-stores.ts`: +0/-3
- `packages/storage/src/sqlite-core-execution-schema.ts`: +3/-4
