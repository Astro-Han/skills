# Pull request snapshot

- PR: https://example.test/pulls/203 — `fix(preview): refresh badge after retry`
- Issue: https://example.test/issues/198 — `badge can show the previous preview briefly`
- Author: north
- Base: main
- Exact head: `203decaf`
- Diff: 18 additions, 4 deletions, 2 files
- Files: `preview-cache.ts`, `preview-cache.test.ts`
- CI for `203decaf`: unit SUCCESS; lint SUCCESS
- Mergeability: clean
- Existing review: "P1 security: stale preview data may be exposed after a retry"
- Unresolved threads: 1 (the severity claim above)

Issue evidence: on a normal Refresh click, a failed first request can leave the previous badge for
up to the existing one-second retry. The retry then replaces it. The badge is local, contains no
secret or cross-user data, is not persisted, and has no external side effect. The behavior is
reproduced in a screen recording and a deterministic fake-clock test.

The PR clears the local badge before scheduling the existing retry and adds the fake-clock test.
