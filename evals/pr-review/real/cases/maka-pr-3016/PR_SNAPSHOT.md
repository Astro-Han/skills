# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3016 — `fix(runtime): fence node-pty writes at PTY exit`
- Author: M4n5ter
- Target base head: `e3885576be0970421289ed3538d53b7e56415d1b`
- Comparison base: `e3885576be0970421289ed3538d53b7e56415d1b`
- Exact source head: `388910c5d251d92a748ff4d6041f5c7c0eba55d5`
- Diff: 258 additions, 0 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

Patch the node-pty Unix writer so queued PTY input cannot outlive its raw file descriptor and corrupt a subsequently opened file after fd reuse. Writes now use the already nonblocking descriptor synchronously, verify descriptor identity before retries, and stop at every exit or close fence.

Add an isolated deterministic regression that blocks the sole libuv worker, reopens a sentinel at the exact retired PTY fd, and proves that the unpatched queued write reaches that sentinel.

Fixes #2978

## Verification

- `npm ci` — patch-package reapplies `node-pty@1.2.0-beta.14`
- `npm run build:test`
- `npm run typecheck`
- `npm --workspace @maka/runtime test` — 2,836 tests, 0 failures
- Targeted regression on Node 22.19, Node 24.5, and Node 26.3
- `npm run lint`
- `npm run format:check`
- Regression confirmed to fail with the patch reversed and pass after restoration

## Review focus

This is a temporary dependency patch for an upstream Unix lifecycle defect. Remove it when node-pty publishes an equivalent fix. This PR intentionally does not upgrade to beta.15 because that release does not modify the Unix write path.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck, and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — queued Unix PTY writes stop at descriptor retirement instead of reaching a reused file
- [ ] No

AI disclosure: Codex prepared this draft with direction from M4n5ter; M4n5ter is the contributor of record and will review the result.



## Linked issues

### https://github.com/apache/maka/issues/2978 — flaky test: shell-run-manager secret redaction across a soft wrap

`redacts a secret across a soft wrap and the scrollback/screen boundary` in `packages/runtime/src/__tests__/shell-run-manager.test.ts` fails intermittently on CI.

**Observed:** [run 31716295489](https://github.com/maka-agent/maka-agent/actions/runs/31716295489/job/94501836643), `test_workspaces`. The case failed at 27.6ms; the enclosing `ShellRunProcessManager` suite took 8.1s. It surfaced on #2962, which touches only `packages/runtime-host/src/client` and `packages/eval` and does not change `packages/runtime` at all. `main` was green at the time. Running the case alone locally passes in 549ms.

**Suspected cause:** the assertion depends on when the PTY flushes across the soft-wrap and scrollback/screen boundary, which shifts under CI load. The fix is to wait for a settled terminal state rather than a particular flush ordering.

This is not a redaction defect — the production behaviour under test looks correct; only the test's timing assumption is unsound.


## Exact-head checks

- changes: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS

## Changed files

- `packages/runtime/src/__tests__/node-pty-write-lifecycle.test.ts`: +116/-0
- `patches/README.md`: +10/-0
- `patches/node-pty+1.2.0-beta.14.patch`: +132/-0
