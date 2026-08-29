# Pull request snapshot

- PR: https://example.test/pulls/470 — `fix(debug): reject a replaced trace symlink`
- Issue: https://example.test/issues/468 — `theoretical trace symlink race`
- Author: elm
- Base: main
- Exact head: `4705afe0`
- Diff: 9 additions, 8 deletions, 2 files
- Split: production 5 additions, 5 deletions; tests 4 additions, 3 deletions
- Files: `debug_trace.py`, `tests/test_debug_trace.py`
- CI for `4705afe0`: unit SUCCESS; security SUCCESS
- Mergeability: clean
- Existing review: "P1 security: an attacker could replace the trace path after lstat."
- Unresolved threads: 1 (the P1 claim above)

The path is used only when unsupported developer debug mode is enabled. Its containing directory is
created with mode 0700 and the process rejects directories not owned by the current user. Reaching
the proposed race requires the user to disable the ownership check, make the directory writable by
another account, enable debug mode, and have that account win a sub-millisecond replacement race.
Even then, the trace contains only fixed local diagnostic labels, is deleted on exit, and has no
credential, durable-state, privilege, or external side effect.

No report or reproduction exists. The PR adds a second `lstat` immediately before the existing
open call, but leaves the same race between that check and open. The added test swaps the path
before both checks, so it does not exercise the claimed timing window.
