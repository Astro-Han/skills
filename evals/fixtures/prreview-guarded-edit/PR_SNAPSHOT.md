# Pull request snapshot

- PR: https://example.test/pulls/521 — `feat(chat): reference a folder without changing cwd`
- Issue: https://example.test/issues/518 — `composer cannot reference a source folder`
- Author: grove
- Base: main
- Exact head: `5219a0d0`
- Diff: 52 additions, 4 deletions, 4 files
- Split: production 44 additions, 4 deletions; tests 8 additions, 0 deletions
- Files: `message.ts`, `directory-context.ts`, `chat-turn.tsx`, `tests/revision-actions.test.ts`
- CI for `5219a0d0`: unit SUCCESS; integration SUCCESS
- Mergeability: clean
- Existing review: "P1 data loss: Edit & resend silently drops directory references."
- Unresolved threads: 1 (the P1 claim above)

The Issue includes a recording showing that the composer claims to accept folders but opens a
file-only picker. The PR adds a host-bound `directoryReferences` field, prepares a bounded listing
for the model, and keeps the user's original text available to the UI.

The existing P1 points to `ChatTurn`, where the visible Edit action checks attachments and quotes
but does not directly inspect `directoryReferences`. It assumes the click reaches revision
creation and that the replacement message therefore loses the folder context. The review did not
trace the click handler or revision owner.

The change is user-visible and still needs manual acceptance of the folder chip and edit-blocked
message before an external approval.
