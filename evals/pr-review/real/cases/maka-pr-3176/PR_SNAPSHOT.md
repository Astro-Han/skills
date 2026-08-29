# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3176 — `fix(eval): isolate the external metering checkpoint from the subject`
- Author: 1625567290
- Target base head: `5d9ce0d2020b641b37eccbc89e25416358db2d55`
- Comparison base: `a81719d836d1df9095b7342e252cb52ea89c4276`
- Exact source head: `d0916963ed3be7d3356f99b32680cb04e38615cc`
- Diff: 267 additions, 59 deletions, 8 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

The host recovers external-subject usage from `agent/<profile>.provider-usage.json`. That path is in the subject's writable log directory, so a symlink or an oversized write can become settlement evidence. The wrapper also chmodded the published file after rename, so a host that raced the publish could see a `0600` snapshot left by umask `077`.

- The temporary snapshot is chmodded to `0644` before rename, so the published inode is already readable.
- Recovery opens the path with `O_NOFOLLOW` and accepts only a regular file of at most 64 KiB.
- Shared write/read helpers live in `metering-checkpoint.ts` so the wrapper and the host use one contract.

Fixes #3149

## Verification

- `node --test packages/eval/dist/__tests__/metering-checkpoint.test.js packages/eval/dist/__tests__/external-subject.test.js` — 15/15
- `@maka/eval` typecheck

## Checklist

- [x] Tests cover the change and fail without it
- [x] Focused lint/typecheck and the affected suites pass locally
- [ ] Full workspace lint/format/typecheck

Does this PR entail a change in behavior?

- [x] Yes — a subject-controlled symlink or oversized file at the checkpoint path is no longer treated as usage evidence; a host racing rename sees `0644`


## Linked issues

### https://github.com/apache/maka/issues/3149 — eval: harden the external-subject metering checkpoint boundary

Follow-up from #2971 review. The subject container can write `/logs/agent/<profile>.provider-usage.json`; the host trusts it for usage/cost settlement. Authenticate or isolate the checkpoint from the subject, bound reads, and chmod the temp file before rename. (Raised by @M4n5ter in the approving review.)

## Exact-head checks

- changes: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- astryx_surface: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- typecheck: SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS

## Changed files

- `packages/eval/README.md`: +5/-2
- `packages/eval/src/__tests__/external-subject.test.ts`: +50/-32
- `packages/eval/src/__tests__/metering-checkpoint.test.ts`: +112/-0
- `packages/eval/src/__tests__/provider-admission-integration.test.ts`: +2/-0
- `packages/eval/src/external-subject.ts`: +6/-3
- `packages/eval/src/harbor-external-subject.ts`: +10/-20
- `packages/eval/src/harness-executor.ts`: +7/-2
- `packages/eval/src/metering-checkpoint.ts`: +75/-0
