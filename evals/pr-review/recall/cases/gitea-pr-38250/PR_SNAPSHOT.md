# Frozen pull request snapshot

- PR: https://github.com/go-gitea/gitea/pull/38250 — `build(sign): move to sigstore`
- Author: TheFox0x7
- Target base head: `cc1df1976be3593c93cdcd28b9b4fba6cb23a6ec`
- Comparison base: `cc1df1976be3593c93cdcd28b9b4fba6cb23a6ec`
- Exact source head: `e834a07354e69e4d499746344d2b70a26d65b634`
- Diff: 12 additions, 30 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

drops signing with gpg in favor of sigstore based artifact signing

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- labeler: SUCCESS
- test-pgsql-shard-1: SKIPPED
- container-amd64: SKIPPED
- test-e2e: SKIPPED
- lint-backend: SUCCESS
- pr-title: SUCCESS
- test-pgsql-shard-2: SKIPPED
- container-arm64: SKIPPED
- lint-on-demand: SUCCESS
- container-riscv64: SKIPPED
- checks-backend: SUCCESS
- test-sqlite: SUCCESS
- test-unit: SKIPPED
- frontend: SUCCESS
- test-mysql: SKIPPED
- backend: SUCCESS
- test-mssql: SKIPPED
- unnamed: SUCCESS

## Changed files

- `.github/workflows/release-nightly.yml`: +4/-10
- `.github/workflows/release-tag-rc.yml`: +4/-10
- `.github/workflows/release-tag-version.yml`: +4/-10
