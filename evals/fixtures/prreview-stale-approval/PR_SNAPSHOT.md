# Pull request snapshot

- PR: https://example.test/pulls/612 — `fix(cache): keep an explicit zero timeout`
- Author: vale
- Base: main
- Reviewed snapshot head: `6120beef`
- Current live head: unavailable; the PR may have advanced after export
- Linked Issue: none; the PR description contains the user report below
- Current CI, mergeability, reviews, and unresolved threads: unavailable
- Diff: 5 additions, 1 deletion, 2 files
- Split: production 1 addition, 1 deletion; tests 4 additions, 0 deletions

The PR description reproduces the problem with `timeoutMs: 0`: the settings loader replaces zero
with the 30-second default, so callers cannot disable waiting. The patch uses a nullish fallback
instead and adds a regression for zero. The user asks whether the current PR can be approved, but
only this exported snapshot is available.
