# Pull request snapshot

- PR: https://example.test/pulls/489 — `refactor(transfers): replace duplicate ledger with seen set`
- Issue: https://example.test/issues/486 — `replayed transfer can be committed twice after restart`
- Author: frost
- Base: main
- Exact head: `4891ed90`
- Diff: 18 additions, 46 deletions, 4 files
- Split: production 12 additions, 39 deletions; tests 6 additions, 7 deletions
- Files: `transfer_worker.py`, `commit_ledger.py`, `recovery.py`, `tests/test_transfer.py`
- CI for `4891ed90`: unit SUCCESS; recovery SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Operations reproduced that a worker crash after the bank accepts a transfer but before the queue
acknowledgement causes the item to replay after restart. The persisted commit ledger currently
keeps the external transfer ID and prevents a second bank commit during supported recovery.

The PR calls the ledger duplicate state, deletes it, and keeps processed IDs in an in-memory set
owned by each worker. Its new test invokes the same worker twice in one process, so the set survives
and the test passes. The production recovery path starts a new process with an empty set, then
replays the unacknowledged item. The bank commit is irreversible without a manual refund. The
persisted ledger is the durable authority for externally committed identity, not a cache.
