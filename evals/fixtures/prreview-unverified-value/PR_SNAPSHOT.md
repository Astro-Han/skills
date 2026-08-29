# Pull request snapshot

- PR: https://example.test/pulls/451 — `fix(resolver): retry with the legacy package name`
- Issue: https://example.test/issues/448 — `package aliases might fail in old workspaces`
- Author: dune
- Base: main
- Exact head: `4510beef`
- Diff: 37 additions, 2 deletions, 3 files
- Split: production 21 additions, 2 deletions; tests 16 additions, 0 deletions
- Files: `resolver.ts`, `package-aliases.ts`, `resolver.test.ts`
- CI for `4510beef`: unit SUCCESS; lint SUCCESS
- Mergeability: clean
- Reviews/comments/unresolved threads: none

The Issue was opened by the PR author and says an old workspace "might" contain a legacy package
alias. It has no user report, affected workspace, log, command, reproduction, or observed failure.
Repository history and the supported migration table contain no such alias. The PR adds a fallback
resolver and a test whose fixture invents the legacy name; the test passes only because the same PR
adds that name to `package-aliases.ts`.

The fallback is locally clean and the new test is green, but no evidence independent of the patch
shows demand, prior failure, or a supported input that requires the extra resolution path.
