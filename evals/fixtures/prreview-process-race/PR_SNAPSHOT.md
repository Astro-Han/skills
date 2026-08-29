# Pull request snapshot

- PR: https://example.test/pulls/401 — `fix(host): bind worker lifetime before spawn`
- Issue: https://example.test/issues/397 — `worker survives a launcher crash in CI`
- Author: ash
- Base: main
- Exact head: `401a11ce`
- Diff: 27 additions, 3 deletions, 2 files
- Split: production 12 additions, 3 deletions; tests 15 additions, 0 deletions
- Files: `owned_host_supervisor.py`, `tests/test_launcher_lifetime.py`
- CI for `401a11ce`: unit SUCCESS; process SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

CI logs and a local script demonstrate a race: if the launcher is killed after creating the
worker but before publishing the lifetime lease, the worker remains alive and the next CI job
cannot bind its port. The failure requires two operating-system processes and is reproducible
about one run in twenty; an in-process fake cannot reproduce it.

`OwnedHostSupervisor` already owns worker creation and lifetime. The PR creates and transfers the
existing lease before spawning, without adding another state or owner. Its regression test starts
the real launcher and worker as separate processes, kills the launcher at the synchronization
point, and verifies that the worker exits. The test is 15 focused lines and replaces a helper-only
assertion that could not exercise process inheritance.
