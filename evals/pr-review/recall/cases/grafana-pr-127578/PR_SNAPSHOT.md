# Frozen pull request snapshot

- PR: https://github.com/grafana/grafana/pull/127578 — `DataPro (migration): Migrate `core/utils/explore.ts``
- Author: nicwestvold
- Target base head: `e9f875e65dd5474c3912ad11eb35c9750c5ae10d`
- Comparison base: `818e7ef255cdb8367e7940a9057a54d6ce6f0806`
- Exact source head: `ce8866912070d3b64d26101c947aed543eebbe81`
- Diff: 23 additions, 6 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Description
Migrate `core/utils/explore.ts` off the deprecated synchronous `getDataSourceSrv()` API to the new async `getDataSourceInstance()` from `@grafana/runtime/unstable`.

## Changes
* Replaced all five `getDataSourceSrv().get(...)` calls with `getDataSourceInstance(...)`:
  * `getExploreUrl` - resolves each query's datasource before interpolation.
  * `generateEmptyQuery` - resolves the default datasource and the datasource for a given ref.
  * `ensureQueries` - validates a query's datasource and resolves the default datasource ref.
* All call sites were already `await`ed, so these are 1:1 replacements. `getDataSourceInstance` preserves the existing semantics: returns the same `DataSourceApi`, returns the default datasource when no ref is given, and throws when a datasource cannot be resolved (the `ensureQueries` try/catch behaviour is unchanged).
* Updated `explore.test.ts` to mock `getDataSourceInstance` on `@grafana/runtime/unstable`, delegating to the existing `DatasourceSrvMock`.

## Risks
* Low. Behavior is unchanged - the same datasource instances are resolved, just via the new API. `getDataSourceInstance` falls back to the legacy service if its cache is empty. No function signatures changed (all were already async).

## Demo
N/A - no user-facing changes.

## Testing Instructions
* `yarn jest public/app/core/utils/explore.test.ts` — all tests pass.
* Optionally, in a dashboard panel use the "Explore" menu action and confirm the Explore URL opens with the correct datasource and queries; in Explore, switch datasources and confirm new/empty queries initialise correctly.

## Reviewer Checklist
- [ ] Tests are added where applicable
- [ ] Issue is linked to PR
- [ ] Code pulled and tested
- [ ] Code is meaningfully improved if applicable

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- trigger: SKIPPED
- Setup and establish latest: SKIPPED
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
- semgrep-cloud-platform/scan: SUCCESS

## Changed files

- `public/app/core/utils/explore.test.ts`: +6/-0
- `public/app/core/utils/explore.ts`: +6/-6
- `public/app/features/explore/state/query.test.ts`: +11/-0
