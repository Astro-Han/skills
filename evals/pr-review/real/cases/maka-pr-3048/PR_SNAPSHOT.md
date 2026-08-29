# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3048 — `fix(desktop): settle catch-up text before remounting a live conversation`
- Author: 1625567290
- Target base head: `e3885576be0970421289ed3538d53b7e56415d1b`
- Comparison base: `e3885576be0970421289ed3538d53b7e56415d1b`
- Exact source head: `2cead14b6034b95f4c47bdf62063e23ff5ef2ddd`
- Diff: 462 additions, 38 deletions, 14 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

Returning to a live conversation remounted the streaming bubble with the leftover prefix as `settledText`, then painted the Runtime Host seed catch-up through the per-frame display batch. `useStreamingText` treated that catch-up as a new stream, so already-produced text replayed (`…Acknowle` → `…Acknowledged steer` → …).

- While a session is waiting to be seeded, `text_delta` / `thinking_delta` apply immediately instead of waiting for rAF.
- Display readiness is keyed to the current observation generation, including A → B → A and Host recovery/restore, not only `sessionId + revision`.
- `ChatMessageSurface` withholds the live bubble until that generation finishes seeding, and snapshots the full buffer in the same activation.

Fixes #3044

## Verification\n\n- `npm --workspace @maka/desktop run typecheck`\n- Desktop main suite — 845/845 passed\n- Focused candidate and observer suites — 48/48 passed\n- `streaming-remount.spec.ts --repeat-each=10` — 20/20 passed\n- `npm run format:check` and `git diff --check`\n\n## Checklist

- [x] Tests cover the change and fail without it
- [x] Focused lint/typecheck and the affected suites pass locally
- [ ] Full workspace lint/format/typecheck

Does this PR entail a change in behavior?

- [x] Yes — switching back to a live conversation no longer replays already-accumulated assistant text
\n\n## AI use\n\n- [ ] No generative tool made a substantive contribution\n- [x] Generative tooling made a substantive contribution\n\nTool(s) and scope: Grok assisted the original implementation, as disclosed by the original contributor. Codex diagnosed the remaining review findings and implemented and tested the observation-restore failure follow-up under M4n5ter&apos;s direction.\n\n

## Linked issues

### https://github.com/apache/maka/issues/3044 — fix(ui): returning to a live conversation intermittently re-streams accumulated output — regression from #2975, flaking CI

## Symptom

`streaming-remount.spec.ts:65` ("returning to a live conversation settles output accumulated while away") fails intermittently on `main`: after switching back to a backgrounded live conversation, the output that accumulated while away is replayed progressively (partial-text paints) instead of appearing settled. This is a user-visible product regression, not only a flaky assertion: the transcript visibly re-streams content the model already produced.

Observed failures on `main` CI: [run 31791670100](https://github.com/maka-agent/maka-agent/actions/runs/31791670100) (2026-08-14). It has also hit unrelated PRs twice (#3032).

## Bisect

Locally reproducible at high rate on macOS (Darwin 25.6.0, Node 24.18):

| commit | result (`--repeat-each 4`) |
| --- | --- |
| `0f943f57e` (parent of #2975) | 4/4 pass |
| `6b8e3db26` (**perf(ui): virtualize long chat transcripts, #2975**) | 1/4 fail |
| current `main` (2632b8506) | 3/4 fail |

## Evidence

Instrumenting the spec's MutationObserver shows the streaming bubble's text after switching back growing in small per-paint steps until it reaches the full accumulated text (fail run):

```
"…stop the Turn."
"…stop the Turn.Acknowle"
"…stop the Turn.Acknowledged steer"
"…stop the Turn.Acknowledged steering: backg"
"…stop the Turn.Acknowledged steering: background outp"
… (ends at the full string)
```

The fake backend emits the steering echo as a **single** `text_delta`, and the projector's `seedActive` emits accumulated text as one cumulative delta — so these partials are not source chunks; the catch-up is being applied/painted incrementally after the remount.

Two mechanisms interact, both new or newly-exposed in #2975:

1. `app-shell-session-events.ts` now defers active-session `text_delta`/`thinking_delta` application to a per-frame flush (`scheduleDisplayEvent`, rAF + 100ms fallback). A catch-up burst that spans multiple tasks/frames is committed in several partial paints.
2. The virtualizer mounts the streaming turn (and paints) earlier on session switch than the previous progressive-mount path did, so the first paint now lands before the catch-up burst has finished arriving — pre-#2975 the burst had effectively completed before the streaming bubble mounted, which is why the same spec passed.

Additional diagnostic: holding a second persistent `window.maka.sessions.subscribeEvents(sessionId, …)` subscription open across the switch makes the failure deterministic and total — the returning view then never receives the accumulated echo at all (bubble stuck at the pre-steer text past a 10s timeout). That experiment perturbs observer registration, but it points at the catch-up/seed path racing observer lifecycle rather than at paint timing alone.

## Expected

Switching back to a live conversation renders everything that accumulated while away settled in the first paint (the spec's contract); only genuinely new output streams.

## Notes

- Reproduce: `cd apps/desktop && npm run build:with-deps && npm run build:test && npx playwright test e2e/streaming-remount.spec.ts:65 --config e2e/playwright.config.ts --repeat-each 4`.
- A fix probably wants the session-activation path to drain/apply the pending catch-up for the newly active session atomically before the streaming bubble's first paint, rather than letting it trickle through the per-frame display batch — but that touches #2975's frame-batching design, so deferring the approach to its author.

Bisect and analysis by Claude Code.

## Exact-head checks

- changes: SUCCESS
- request-review: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SKIPPED
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS
- unnamed: SUCCESS

## Changed files

- `apps/desktop/src/main/__tests__/live-content-seed.test.ts`: +57/-0
- `apps/desktop/src/main/__tests__/runtime-host-desktop-candidate.test.ts`: +131/-5
- `apps/desktop/src/main/__tests__/runtime-host-session-observer.test.ts`: +17/-0
- `apps/desktop/src/main/__tests__/streaming-handoff.test.ts`: +62/-0
- `apps/desktop/src/main/runtime-host-desktop-candidate.ts`: +17/-1
- `apps/desktop/src/main/runtime-host-session-observation-registry.ts`: +4/-0
- `apps/desktop/src/main/runtime-host-session-observer.ts`: +8/-0
- `apps/desktop/src/preload/bridge-contract.d.ts`: +1/-0
- `apps/desktop/src/preload/preload.ts`: +11/-0
- `apps/desktop/src/renderer/app-shell-effects.ts`: +16/-4
- `apps/desktop/src/renderer/app-shell-session-events.ts`: +32/-2
- `apps/desktop/src/renderer/app-shell.tsx`: +38/-14
- `apps/desktop/src/renderer/chat-message-surface.tsx`: +16/-12
- `apps/desktop/src/renderer/live-content-seed.ts`: +52/-0
