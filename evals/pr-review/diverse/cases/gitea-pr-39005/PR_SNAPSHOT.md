# Frozen pull request snapshot

- PR: https://github.com/go-gitea/gitea/pull/39005 — `fix(actions): enforce fork pull request trust boundaries`
- Author: bircni
- Target base head: `a52e5f53c096961b61e4016a35b693aa72b51339`
- Comparison base: `a52e5f53c096961b61e4016a35b693aa72b51339`
- Exact source head: `071a6aafa52f624519c26f4953342d4d2a44c136`
- Diff: 85 additions, 3 deletions, 7 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Preserve fork pull request restrictions across review-triggered workflows, reusable workflow access, job scheduling, and filtered workflow statuses.

This prevents untrusted fork workflow content from bypassing approval, accessing private reusable workflows, or satisfying protected status checks.


_Assisted-by: Codex:GPT-5_


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

- `models/perm/access/actions_repo_permission_test.go`: +12/-0
- `models/perm/access/repo_permission.go`: +1/-1
- `services/actions/job_emitter.go`: +5/-0
- `services/actions/job_emitter_test.go`: +29/-0
- `services/actions/notifier.go`: +1/-2
- `services/actions/notifier_helper.go`: +13/-0
- `services/actions/notifier_helper_test.go`: +24/-0
