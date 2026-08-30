# Frozen pull request snapshot

- PR: https://github.com/grafana/grafana/pull/131692 — `Alerting: Fix negative triage filters being cancelled out by alias expansion`
- Author: gillesdemey
- Target base head: `345e03d588cae57fe98d08219a99dab584bf35c8`
- Comparison base: `aa5d48b19807b369967fcd2ab01b182a94e6948a`
- Exact source head: `7386912384e4e4a21066c482a23d2bf3cb2e95eb`
- Diff: 132 additions, 16 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## What is this feature?

Fixes exclusion filters (`!=`, `!~`, and the multi-value `!=|`) on the Alerts activity page silently doing nothing.

The page lets a single filter key stand for several real label names — `cluster` covers `cluster` and `cluster_name`, `namespace` covers `namespace`, `exported_namespace` and `namespace_extracted`, `service` and `severity` likewise. Until now every matcher on such a key was expanded into one selector per backing label, joined with `or`.

That's right for `=` and `=~`, but it undoes `!=` and `!~`. Prometheus treats a label the series doesn't have as empty, so a series with `cluster="prod-me-central-1"` and no `cluster_name` still matches the `cluster_name!="prod-me-central-1"` branch, and the `or` unions it right back in.

Filtering `namespace = alloy-otlp` and `cluster != prod-me-central-1` used to build:

```promql
count by (alertstate) ((
  GRAFANA_ALERTS{cluster!="prod-me-central-1",namespace="alloy-otlp"} or
  GRAFANA_ALERTS{cluster!="prod-me-central-1",exported_namespace="alloy-otlp"} or
  GRAFANA_ALERTS{cluster!="prod-me-central-1",namespace_extracted="alloy-otlp"} or
  GRAFANA_ALERTS{cluster_name!="prod-me-central-1",namespace="alloy-otlp"} or       ← brings them back
  GRAFANA_ALERTS{cluster_name!="prod-me-central-1",exported_namespace="alloy-otlp"} or
  GRAFANA_ALERTS{cluster_name!="prod-me-central-1",namespace_extracted="alloy-otlp"}
))
```

and now builds:

```promql
count by (alertstate) ((
  GRAFANA_ALERTS{cluster!="prod-me-central-1",cluster_name!="prod-me-central-1",namespace="alloy-otlp"} or
  GRAFANA_ALERTS{cluster!="prod-me-central-1",cluster_name!="prod-me-central-1",exported_namespace="alloy-otlp"} or
  GRAFANA_ALERTS{cluster!="prod-me-central-1",cluster_name!="prod-me-central-1",namespace_extracted="alloy-otlp"}
))
```

Exclusions now go into every selector together instead of being split across `or` branches. Inclusions keep branching exactly as before.

One exception, in the second commit: `cluster!=""` isn't excluding a value — since Prometheus reads an absent label as empty, it's asking whether the series has a cluster at all. That's a question about *any* backing label, so it keeps branching. ANDed it would mean "has both `cluster` and `cluster_name`", which almost nothing does. Not reachable from the value dropdown (`label_values` never returns an empty value), but external integrations can link into the page with a hand-built URL.

## Why do we need this feature?

Reported internally: filtering `cluster != prod-me-central-1` on the Alerts activity page returned prod-me-central-1 alerts anyway. Any exclusion on `cluster`, `namespace`, `service`, or `severity` is affected. Regression from #121410.

## Testing

Eight new cases in `queries.test.ts`, asserting full expressions rather than substrings — substring matching is what let the original bug through. Covers exclusion-only, the reported include+exclude combination, include and exclude on the same key, `!~` across all seven severity aliases, multi-value `!=|` fed through `prometheusExpressionBuilder`, non-combined keys left alone, empty-value exclusions still branching, and exclusions flowing into the deduplicated `last_over_time` query.

Six of them fail against the old builder. The existing alias-expansion tests are untouched and still pass, so inclusion behaviour is unchanged.

## Which issue(s) does this PR fix?

n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- trigger: SKIPPED
- Check PR is eligible: SKIPPED
- signed-commits: SKIPPED
- Setup and establish latest: SKIPPED
- main: SUCCESS
- Detect whether code changed: SUCCESS
- Detect whether code changed: SUCCESS
- Detect frontend changes: SUCCESS
- Setup opted-in teams: SUCCESS
- codeowners-validator: SUCCESS
- dispatch-job: SUCCESS
- signed-commits: SUCCESS
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
- Detect whether the Docker image build is affected: SUCCESS
- TruffleHog Secret Scan / trufflehog-scan: SUCCESS
- Run Trufflehog: SUCCESS
- check-separation: SUCCESS
- verify-i18n / verify-i18n: SUCCESS
- Detect whether code changed: SUCCESS
- Check whether there are things to scan: SUCCESS
- Validate Backend Configs: SKIPPED
- Grafana (${{ matrix.shard }}): SKIPPED
- Label PR for future deploys: SKIPPED
- dispatch-job-fork: SKIPPED
- Feature toggles documentation is in sync with source: SKIPPED
- Go Workspace Check: SKIPPED
- Verify API clients: SKIPPED
- Create next release branch (Grafana): SKIPPED
- Verify committed API specs match: SKIPPED
- go-fmt: SKIPPED
- Build base frontend: SUCCESS
- Detect changed files: SUCCESS
- Build backend: SUCCESS
- check-endpoint-migration: SUCCESS
- Generate golden files: SUCCESS
- setup: SUCCESS
- Run Storybook a11y tests (light theme): SUCCESS
- build / full source (alpine): SUCCESS
- TruffleHog Secret Scan / Send TruffleHog metrics to Prometheus via Grafana Bench: SUCCESS
- Run zizmor / job-workflow-ref: SUCCESS
- Build pr frontend: SUCCESS
- Run Storybook a11y tests (dark theme): SUCCESS
- Run Storybook a11y tests (deut_prot_light theme): SUCCESS
- Run Storybook a11y tests (deut_prot_dark theme): SUCCESS
- Run Storybook a11y tests (tritanopia_light theme): SUCCESS
- Run Storybook a11y tests (tritanopia_dark theme): SUCCESS
- Grafana Enterprise (${{ matrix.shard }}): SKIPPED
- Comment that the build started: SKIPPED
- Check Wire Changes: SKIPPED
- Create next release branch (Grafana Enterprise): SKIPPED
- lint-go: SKIPPED
- Check bundle size impact: SUCCESS
- Coverage - @grafana/datapro: SUCCESS
- Build frontend: SUCCESS
- endpoint-toggle-result: SUCCESS
- Decoupled plugin tests: SUCCESS
- Verify API clients (enterprise): SUCCESS
- build frontend: SUCCESS
- Storybook a11y tests: SUCCESS
- build / frontend: SUCCESS
- Run zizmor / Generate and upload zizmor results 🌈: SUCCESS
- Coverage - @grafana/dataviz-squad: SUCCESS
- Coverage - @grafana/grafana-operator-experience-squad: SUCCESS
- Coverage - @grafana/grafana-frontend-navigation: SUCCESS
- Build frontend: SKIPPED
- Lint: SKIPPED
- Create security branch (Enterprise): SKIPPED
- All backend unit tests complete: SUCCESS
- All coverage checks pass: SUCCESS
- Verify Storybook (Playwright): SUCCESS
- Rspack plugin tests: SUCCESS
- All Go Workspace Checks complete: SUCCESS
- build backend: SUCCESS
- build / backend (linux-amd64): SUCCESS
- Run zizmor / Send zizmor metrics to Prometheus via Grafana Bench: SUCCESS
- Deploy preview assets: SKIPPED
- create_github_release: SKIPPED
- Run zizmor / Delete branch with dangerous-trigger vulnerability: SKIPPED
- Playwright E2E tests (1/8): SUCCESS
- Packages unit tests: SUCCESS
- Lint: SUCCESS
- build targz: SUCCESS
- build / source tarball: SUCCESS
- Playwright E2E tests (2/8): SUCCESS
- Playwright E2E tests (3/8): SUCCESS
- Playwright E2E tests (4/8): SUCCESS
- Playwright E2E tests (5/8): SUCCESS
- Playwright E2E tests (6/8): SUCCESS
- Playwright E2E tests (7/8): SUCCESS
- Playwright E2E tests (8/8): SUCCESS
- Comment that the deploy failed: SKIPPED
- Unit tests (${{ matrix.shard }} / ${{ matrix.total }}): SKIPPED
- Typecheck: SKIPPED
- Diagnostics e2e (on-prem) / Download diagnostics e2e (on-prem): SUCCESS
- build docker: SUCCESS
- build / variants (targz) / alpine: SUCCESS
- build / variants (targz) / alpine-slim: SUCCESS
- build / variants (targz) / ubuntu: SUCCESS
- build / variants (targz) / ubuntu-slim: SUCCESS
- build / variants (targz) / distroless: SUCCESS
- build / variants (targz) / distroless-slim: SUCCESS
- Comment that the deploy was cancelled: SKIPPED
- Publish metrics: SKIPPED
- Unit tests (1 / 16): SUCCESS
- Typecheck: SUCCESS
- Push PR Docker image: SUCCESS
- Unit tests (2 / 16): SUCCESS
- Unit tests (3 / 16): SUCCESS
- Unit tests (4 / 16): SUCCESS
- Unit tests (5 / 16): SUCCESS
- Unit tests (6 / 16): SUCCESS
- Unit tests (7 / 16): SUCCESS
- Unit tests (8 / 16): SUCCESS
- Unit tests (9 / 16): SUCCESS
- Unit tests (10 / 16): SUCCESS
- Unit tests (11 / 16): SUCCESS
- Unit tests (12 / 16): SUCCESS
- Unit tests (13 / 16): SUCCESS
- Unit tests (14 / 16): SUCCESS
- Unit tests (15 / 16): SUCCESS
- Unit tests (16 / 16): SUCCESS
- post_on_slack: SKIPPED
- All Playwright tests complete: SUCCESS
- All frontend unit tests complete: SUCCESS
- Verify OpenAPI specs: SUCCESS
- Run Meticulous tests: SUCCESS
- Verify packed frontend packages: SKIPPED
- migrate_prs_grafana: SKIPPED
- Report Playwright benchmarks: SUCCESS
- migrate_prs_enterprise: SKIPPED
- All E2E tests complete: SUCCESS
- Check circular dependencies: SUCCESS
- Export SBOM and attach to the GitHub release: SKIPPED
- lint-knip: SUCCESS
- Validate yarn install: SKIPPED
- Attach Linux packages to the GitHub release: SKIPPED
- zizmor: NEUTRAL
- Cursor Bugbot: SUCCESS
- Socket Security: Project Report: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- semgrep-cloud-platform/scan: SUCCESS

## Changed files

- `public/app/features/alerting/unified/triage/scene/queries.test.ts`: +86/-0
- `public/app/features/alerting/unified/triage/scene/queries.ts`: +46/-16
