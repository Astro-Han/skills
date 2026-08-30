# Frozen pull request snapshot

- PR: https://github.com/grafana/grafana/pull/127870 — `Revert "DataPro (migration): Migrate `core/utils/explore.ts` (#127578)"`
- Author: gtk-grafana
- Target base head: `52b21b516f6533d4498b8b9a5117f716a624f7e2`
- Comparison base: `52b21b516f6533d4498b8b9a5117f716a624f7e2`
- Exact source head: `7fda5faeaeb53556a412ab6499d0764f6b3d25c2`
- Diff: 6 additions, 23 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This reverts commit 3103327a3f9e8444a6345039cf66e6987fbe07da from https://github.com/grafana/grafana/pull/127578 which introduced the bug addressed by https://github.com/grafana/grafana/pull/127857.

**Special notes for your reviewer:**
Reverting the earlier PR is probably less risky over a holiday weekend, especially because it was supposed to be a noop migration to a new API.

Should follow up with investigating upstream fix in `getDataSourceInstance` as it doesn't have functional parity with `getDataSourceSrv`

Please check that:
- [ ] It works as expected from a user's perspective.
- [ ] If this is a pre-GA feature, it is behind a feature toggle.
- [ ] The docs are updated, and if this is a [notable improvement](https://grafana.com/docs/writers-toolkit/contribute/release-notes/#how-to-determine-if-content-belongs-in-whats-new), it's added to our [What's New](https://grafana.com/docs/writers-toolkit/contribute/release-notes/) doc.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- trigger: SKIPPED
- Setup and establish latest: SKIPPED
- main: SUCCESS
- main: SUCCESS
- Detect whether code changed: SUCCESS
- Detect whether code changed: SUCCESS
- Setup opted-in teams: SUCCESS
- codeowners-validator: SUCCESS
- dispatch-job: SUCCESS
- Detect whether code changed: SUCCESS
- detect-changes: SUCCESS
- handle-ephemeral-instances: SUCCESS
- Detect whether code changed: SUCCESS
- Detect whether code changed: SUCCESS
- Detect whether code changed: SUCCESS
- Detect whether code changed: SUCCESS
- check-separation: SUCCESS
- main: SUCCESS
- main: SUCCESS
- Detect whether code changed: SUCCESS
- reject-gh-secrets: SUCCESS
- Detect whether code changed: SUCCESS
- dashboard-schema-v2-e2e: SUCCESS
- Shellcheck scripts: SUCCESS
- Detect whether code changed: SUCCESS
- build / full source (alpine): SUCCESS
- TruffleHog Secret Scan / trufflehog-scan: SUCCESS
- Run Trufflehog: SUCCESS
- check-separation: SUCCESS
- verify-i18n / verify-i18n: SUCCESS
- Detect whether code changed: SUCCESS
- Check whether there are things to scan: SUCCESS
- Validate Backend Configs: SKIPPED
- Grafana (${{ matrix.shard }}): SKIPPED
- dispatch-job-fork: SKIPPED
- Publish metrics: SKIPPED
- Feature toggles documentation is in sync with source: SKIPPED
- Go Workspace Check: SKIPPED
- Verify API clients: SKIPPED
- Create next release branch (Grafana): SKIPPED
- Verify committed API specs match: SKIPPED
- go-fmt: SKIPPED
- Detect changed files: SUCCESS
- check-endpoint-migration: SUCCESS
- Generate golden files: SUCCESS
- setup: SUCCESS
- Run Storybook a11y tests (light theme): SUCCESS
- build / frontend: SUCCESS
- TruffleHog Secret Scan / Send TruffleHog metrics to Prometheus via Grafana Bench: SUCCESS
- Run zizmor / job-workflow-ref: SUCCESS
- Run Storybook a11y tests (dark theme): SUCCESS
- Run Storybook a11y tests (deut_prot_light theme): SUCCESS
- Run Storybook a11y tests (deut_prot_dark theme): SUCCESS
- Run Storybook a11y tests (tritanopia_light theme): SUCCESS
- Run Storybook a11y tests (tritanopia_dark theme): SUCCESS
- Grafana Enterprise (${{ matrix.shard }}): SKIPPED
- Check Wire Changes: SKIPPED
- Create next release branch (Grafana Enterprise): SKIPPED
- lint-go: SKIPPED
- Clear skip warning: SUCCESS
- Build backend: SUCCESS
- endpoint-toggle-result: SUCCESS
- Decoupled plugin tests: SUCCESS
- Verify API clients (enterprise): SUCCESS
- build frontend: SUCCESS
- Storybook a11y tests: SUCCESS
- build / backend (linux-amd64): SUCCESS
- Run zizmor / Generate and upload zizmor results 🌈: SUCCESS
- Cleanup coverage comments: SKIPPED
- Lint: SKIPPED
- Create security branch (Grafana Security Mirror): SKIPPED
- All backend unit tests complete: SUCCESS
- Build frontend: SUCCESS
- Packages unit tests: SUCCESS
- All Go Workspace Checks complete: SUCCESS
- build backend: SUCCESS
- build / source tarball: SUCCESS
- Run zizmor / Send zizmor metrics to Prometheus via Grafana Bench: SUCCESS
- Unit tests (${{ matrix.shard }} / ${{ matrix.total }}): SKIPPED
- Create security branch (Enterprise): SKIPPED
- Run zizmor / Delete branch with dangerous-trigger vulnerability: SKIPPED
- Coverage - @grafana/datapro: SUCCESS
- Verify Storybook (Playwright): SUCCESS
- Lint: SUCCESS
- build targz: SUCCESS
- build / variants (targz) / alpine: SUCCESS
- Coverage - @grafana/dataviz-squad: SUCCESS
- build / variants (targz) / alpine-slim: SUCCESS
- Coverage - @grafana/grafana-operator-experience-squad: SUCCESS
- build / variants (targz) / ubuntu: SUCCESS
- Coverage - @grafana/grafana-frontend-navigation: SUCCESS
- build / variants (targz) / ubuntu-slim: SUCCESS
- build / variants (targz) / distroless: SUCCESS
- build / variants (targz) / distroless-slim: SUCCESS
- Post skip warning: SKIPPED
- Typecheck: SKIPPED
- create_github_release: SKIPPED
- Playwright E2E tests (1/8): SUCCESS
- Unit tests (1 / 16): SUCCESS
- build docker: SUCCESS
- Playwright E2E tests (2/8): SUCCESS
- Unit tests (2 / 16): SUCCESS
- Playwright E2E tests (3/8): SUCCESS
- Unit tests (3 / 16): SUCCESS
- Playwright E2E tests (4/8): SUCCESS
- Unit tests (4 / 16): SUCCESS
- Playwright E2E tests (5/8): SUCCESS
- Unit tests (5 / 16): SUCCESS
- Playwright E2E tests (6/8): SUCCESS
- Unit tests (6 / 16): SUCCESS
- Playwright E2E tests (7/8): SUCCESS
- Unit tests (7 / 16): SUCCESS
- Playwright E2E tests (8/8): SUCCESS
- Unit tests (8 / 16): SUCCESS
- Unit tests (9 / 16): SUCCESS
- Unit tests (10 / 16): SUCCESS
- Unit tests (11 / 16): SUCCESS
- Unit tests (12 / 16): SUCCESS
- Unit tests (13 / 16): SUCCESS
- Unit tests (14 / 16): SUCCESS
- Unit tests (15 / 16): SUCCESS
- Unit tests (16 / 16): SUCCESS
- All coverage checks pass: SUCCESS
- All Playwright tests complete: SUCCESS
- All frontend unit tests complete: SUCCESS
- Typecheck: SUCCESS
- Push PR Docker image: SUCCESS
- Report Playwright benchmarks: SUCCESS
- Typecheck (TSGO/TS7): SUCCESS
- Run Meticulous tests: SUCCESS
- post_on_slack: SKIPPED
- All E2E tests complete: SUCCESS
- Verify OpenAPI specs: SUCCESS
- Verify packed frontend packages: SKIPPED
- migrate_prs_grafana: SKIPPED
- migrate_prs_enterprise: SKIPPED
- Check circular dependencies: SUCCESS
- Attach Linux packages to the GitHub release: SKIPPED
- lint-knip: SUCCESS
- Validate yarn install: SKIPPED
- zizmor: NEUTRAL
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- semgrep-cloud-platform/scan: SUCCESS

## Changed files

- `public/app/core/utils/explore.test.ts`: +0/-6
- `public/app/core/utils/explore.ts`: +6/-6
- `public/app/features/explore/state/query.test.ts`: +0/-11
