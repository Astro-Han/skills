# Frozen pull request snapshot

- PR: https://github.com/go-gitea/gitea/pull/39026 — `fix(packages): bound Alpine metadata entries`
- Author: bircni
- Target base head: `ad05aaee800a7d1180e325957a37998e6c6c30c5`
- Comparison base: `ad05aaee800a7d1180e325957a37998e6c6c30c5`
- Exact source head: `35e2ae33d1a9745210bb82f3395358bc8544d85e`
- Diff: 22 additions, 3 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Limit retained dependency and provision metadata while parsing Alpine package information.

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
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- labeler: SUCCESS
- container-amd64: SKIPPED
- lint-backend: SUCCESS
- test-pgsql-shard-1: SUCCESS
- test-e2e: SUCCESS
- pr-title: SUCCESS
- container-arm64: SKIPPED
- lint-on-demand: SUCCESS
- test-pgsql-shard-2: SUCCESS
- container-riscv64: SKIPPED
- checks-backend: SUCCESS
- test-sqlite: SUCCESS
- frontend: SKIPPED
- test-unit: SUCCESS
- backend: SUCCESS
- test-mysql: SUCCESS
- test-mssql: SUCCESS
- unnamed: SUCCESS

## Changed files

- `modules/packages/alpine/metadata.go`: +12/-3
- `modules/packages/alpine/metadata_test.go`: +10/-0
