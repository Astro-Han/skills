# Pull request snapshot

- PR: https://example.test/pulls/84 — `fix(discovery): support linked extensions`
- Issue: https://example.test/issues/79 — `linked extensions are missing`
- Author: river
- Base: main
- Exact head: `84ca11ab`
- Diff: 42 additions, 9 deletions, 3 files
- Split: production 14 additions, 5 deletions; tests 24 additions, 2 deletions; docs 4 additions, 2 deletions
- Files: `discovery.py`, `tests/test_discovery.py`, `docs/extensions.md`
- CI for `84ca11ab`: unit SUCCESS; lint SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

Issue evidence: a user keeps extensions in `/srv/shared/extensions` and links one into
`~/.tool/extensions`. The linked extension is missing. The target is outside the configured
discovery root. The report includes the exact command and before/after catalog output.

The PR description says links are now supported when their canonical target remains inside the
configured discovery root. Links whose targets escape the root are still rejected. The added
positive test creates both the link and target beneath one temporary discovery root.
