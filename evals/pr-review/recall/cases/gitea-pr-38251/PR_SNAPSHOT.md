# Frozen pull request snapshot

- PR: https://github.com/go-gitea/gitea/pull/38251 — `revert(sign): restore gpg`
- Author: TheFox0x7
- Target base head: `4812e354866a066dcb899af667b0fad5fa094065`
- Comparison base: `4812e354866a066dcb899af667b0fad5fa094065`
- Exact source head: `47a47cefdd730f41071b0308006d2fef6113a63e`
- Diff: 30 additions, 0 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

partially revert sigstore signing to avoid causing breaking change for v1.27


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

- `.github/workflows/release-nightly.yml`: +10/-0
- `.github/workflows/release-tag-rc.yml`: +10/-0
- `.github/workflows/release-tag-version.yml`: +10/-0
