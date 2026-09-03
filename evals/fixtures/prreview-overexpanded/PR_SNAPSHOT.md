# Pull request snapshot

- PR: https://example.test/pulls/702 — `fix(scheduler): apply config changes to queued jobs via settings bus`
- Issue: https://example.test/issues/697 — `config change not applied until scheduler restart`
- Author: rowan
- Base: main
- Exact head: `702c0ffe`
- Diff: 412 additions, 9 deletions, 9 files
- Split: production 268 additions, 6 deletions; tests 144 additions, 3 deletions
- Files: `scheduler/settings_bus.py` (new), `scheduler/generation.py` (new), `scheduler/worker.py`, `scheduler/config.py`, `scheduler/registry.py`, `scheduler/sweep.py` (new), `tests/test_settings_bus.py` (new), `tests/test_generation.py` (new), `tests/test_reload.py` (new)
- CI for `702c0ffe`: unit SUCCESS; lint SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Issue 697 is a user report with a reproduction: an operator changes `max_retries` while jobs are
queued; jobs that start after the change still run with the old value until the scheduler process
restarts. The issue states its acceptance plainly: "a config change is observed by the next job
that starts after it, without a restart."

Current behavior on `main`: `Worker.__init__` copies `Config.snapshot()` into `self._settings`
once at construction, and `Job.run` reads `worker._settings`. `Config.current()` already returns
the live validated mapping, is the single write point for config updates, and is safe to call from
any thread.

What the PR adds: a new `SettingsBus` with subscribe/publish and per-worker subscriptions; a
`Generation` module that assigns a monotonic revision to every config write; workers subscribe on
construction and replace `self._settings` when a publish arrives; `registry.py` tracks
subscriptions so dead workers are unsubscribed; a timer-driven reconciliation sweep re-publishes
the latest generation in case a publish was missed. The new tests cover subscribe/publish
ordering, generation monotonicity, sweep timing, unsubscribe on worker shutdown, and the
issue's reload scenario end to end.
