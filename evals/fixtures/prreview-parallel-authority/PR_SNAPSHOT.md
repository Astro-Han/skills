# Pull request snapshot

- PR: https://example.test/pulls/420 — `fix(chat): recover stalled sends automatically`
- Issue: https://example.test/issues/418 — `send can remain stalled after runtime disconnect`
- Author: birch
- Base: main
- Exact head: `420f00d1`
- Diff: 96 additions, 11 deletions, 4 files
- Split: production 70 additions, 8 deletions; tests 26 additions, 3 deletions
- Files: `runtime/retry-loop.ts`, `ui/use-send-recovery.ts`, `ui/composer.tsx`, `ui/send-recovery.test.ts`
- CI for `420f00d1`: unit SUCCESS; integration SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Telemetry and a captured disconnect reproduce a stalled send. The host queue is the durable owner
of queued content and already owns retry and reconnect. The PR adds a timeout heuristic to the
runtime retry loop and a second UI loop that watches the same send state. When the UI timer fires,
it calls `stop()`, clears the composer queue, and then calls `send()` with a reconstructed message.
Stop and send are separate operations: a reconnect between them lets the host deliver the original
item while the UI sends a duplicate, and a failed reconstruction loses the queued content.

The new tests mount the UI hook with a fake runtime and assert its timer sequence; they do not use
the host queue or reconnect path. Product has not decided whether a timeout should silently resend,
show recovery controls, or preserve the stalled state for inspection. This is a user-visible UX
change and the repository's Astryx primitive for recoverable sends is `RecoveryBanner`.
