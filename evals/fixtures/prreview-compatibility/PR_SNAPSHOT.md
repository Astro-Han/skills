# Pull request snapshot

- PR: https://example.test/pulls/318 — `refactor(credentials): remove duplicate legacy token`
- Issue: https://example.test/issues/315 — `rotation can leave credential representations stale`
- Author: west
- Base: main
- Exact head: `318feed0`
- Diff: 24 additions, 37 deletions, 4 files
- Split: production 14 additions, 30 deletions; tests 10 additions, 7 deletions
- Files: `credential.py`, `rotate.py`, `reader_v1.py`, `tests/test_rotate.py`
- CI for `318feed0`: unit SUCCESS; integration SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Issue evidence: during rolling upgrades, rotation can update `token` without updating
`legacy_token`, and an older deployed reader then rejects the credential. Deployment logs and a
mixed-version reproduction demonstrate the failure.

The PR removes `legacy_token` from the model and updates current-version tests. The deployment
contract states that version N must remain readable by deployed N-1 workers during the supported
rolling-upgrade window. `reader_v1.py` is the deployed N-1 reader and still consumes
`legacy_token`. The compatibility owner is the credential's atomic `rotate()` transition until
that window expires.
