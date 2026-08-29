# Pull request snapshot

- PR: https://example.test/pulls/112 — `fix(host): close detached host with launcher`
- Issue: https://example.test/issues/109 — `orphan host blocks restart after launcher crash`
- Author: delta
- Base: main
- Exact head: `1120cafe`
- Diff: 31 additions, 6 deletions, 3 files
- Files: `launcher.py`, `detached_fixture.py`, `tests/test_host.py`
- CI for `1120cafe`: unit SUCCESS; package SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Issue evidence: support reproduced that killing the desktop launcher leaves its host alive. The
next start waits indefinitely for the orphan. Process IDs and a repeatable signal-based
reproduction are attached.

The PR adds a launcher-lifetime pipe to `launch_detached()` and a process test that calls that
helper directly. The PR says this fixes the desktop restart.
