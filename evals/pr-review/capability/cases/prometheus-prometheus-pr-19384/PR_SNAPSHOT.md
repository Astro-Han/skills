# Frozen pull request snapshot

- PR: https://github.com/prometheus/prometheus/pull/19384 — `ui: show effective scrape pool configuration`
- Author: fzlzjerry
- Target base head: `3d36e183cd78c9e71be3e6a200a583f5b76f79c9`
- Comparison base: `3d36e183cd78c9e71be3e6a200a583f5b76f79c9`
- Exact source head: `e3d37797c51598b686602bab6d4b5aa06eed62fe`
- Diff: 551 additions, 6 deletions, 16 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Fixes #12591

## Summary

- expose the effective configuration for one scrape pool through an on-demand, experimental API endpoint
- add a compact, link-like configuration toggle to each parent pool header on the Targets and Service Discovery pages
- render the configuration in the pool content pane, fetch it only when expanded, and retain YAML secret redaction
- document the endpoint and add it to the OpenAPI specification

## Validation

- `go test ./web/api/v1 -count=1`
- `go vet ./web/api/v1`
- `go build ./cmd/prometheus`
- `golangci-lint run --timeout 4m ./...`
- `pnpm --filter @prometheus-io/mantine-ui test --run`
- `pnpm --filter @prometheus-io/mantine-ui run lint`
- `pnpm --filter @prometheus-io/mantine-ui run build`
- ran the built server with an imported `scrape_config_files` job and verified that the pool is returned while its authorization credentials remain redacted

```release-notes
[ENHANCEMENT] UI: Show the effective configuration for each scrape pool on the Targets and Service Discovery pages.
```


## Linked issues

### https://github.com/prometheus/prometheus/issues/12591 — Expand scrape_config_files in the /config web UI endpoint

### Proposal

Being able to quickly see the running configuration on a Prometheus instance using the `/config` UI endpoint is a really convenient feature of Prometheus. However, with the recent addition of being able to separate scrape configs into multiple files with `scrape_config_files`, you lose the ability to see exactly what the full running config actually is when using it. This can make it more difficult to easily see what relabeling is happening on individual scrape jobs. 

Instead, you just see which paths are being included in the main config file, like so:
![Screenshot 2023-07-21 at 11 20 34 AM](https://github.com/prometheus/prometheus/assets/11506822/4314228b-2716-48f9-bedc-c93df0f65c5f)

I'd propose that the contents in the `/config` endpoint be expanded to show the contents of the included `scrape_config_files`.

In order to do so, I'm not sure if the best way would be to just include it in the box that is there now or create a new section named something like "Running Configuration" that has all of the scrape config files expanded. Or to create a new endpoint entirely just for scrape configs, similar to `/rules`.

Regardless, I believe it's an important feature and wanted to put this out there for ideas and tracking.

## Exact-head checks

- Go tests: FAILURE
- dependabot: SKIPPED
- check: SUCCESS
- check: SUCCESS
- Scorecards analysis: SUCCESS
- More Go tests: SUCCESS
- Go tests for 32-bit x86: SUCCESS
- List active LTS releases: SUCCESS
- Go tests with previous Go version: FAILURE
- UI tests: SUCCESS
- Go tests on Windows: SUCCESS
- Mixins tests: SUCCESS
- Compliance testing: SUCCESS
- Check generated parser: SUCCESS
- golangci-lint: SUCCESS
- fuzzing / Run Go Fuzz Tests (FuzzParseMetricText, FuzzParseOpenMetric): SUCCESS
- fuzzing / Run Go Fuzz Tests (FuzzParseMetricSelector, FuzzParseExpr): SUCCESS
- fuzzing / Run Go Fuzz Tests (FuzzXORChunk, FuzzXOR2Chunk): SUCCESS
- fuzzing / Run Go Fuzz Tests (FuzzParseProtobuf): SUCCESS
- fuzzing / Fuzzing: SUCCESS
- codeql / Analyze (javascript): SUCCESS
- Go tests for Prometheus upgrades and downgrades (3.13.2): SUCCESS
- Go tests for Prometheus upgrades and downgrades (3.5.5): SUCCESS
- Build Prometheus for common architectures (0): SUCCESS
- Build Prometheus for common architectures (1): SUCCESS
- Build Prometheus for common architectures (2): SUCCESS
- Build Prometheus for all architectures: SKIPPED
- Publish UI on npm Registry: SUCCESS
- Report status of build Prometheus for all architectures: SKIPPED
- Publish main branch artifacts: SKIPPED
- Publish release artefacts: SKIPPED
- CodeQL: NEUTRAL
- Scorecard: NEUTRAL
- Header rules - prometheus-react: NEUTRAL
- Pages changed - prometheus-react: NEUTRAL
- DCO: SUCCESS
- Redirect rules - prometheus-react: SUCCESS
- unnamed: SUCCESS

## Changed files

- `docs/querying/api.md`: +30/-0
- `web/api/v1/api.go`: +21/-0
- `web/api/v1/api_scenarios_test.go`: +34/-0
- `web/api/v1/api_test.go`: +51/-3
- `web/api/v1/openapi.go`: +1/-0
- `web/api/v1/openapi_examples.go`: +17/-0
- `web/api/v1/openapi_paths.go`: +15/-0
- `web/api/v1/openapi_schemas.go`: +15/-0
- `web/api/v1/openapi_test.go`: +1/-0
- `web/api/v1/testdata/openapi_3.1_golden.yaml`: +86/-0
- `web/api/v1/testdata/openapi_3.2_golden.yaml`: +86/-0
- `web/ui/mantine-ui/src/api/responseTypes/config.ts`: +1/-2
- `web/ui/mantine-ui/src/components/ScrapePoolConfig.test.tsx`: +81/-0
- `web/ui/mantine-ui/src/components/ScrapePoolConfig.tsx`: +55/-0
- `web/ui/mantine-ui/src/pages/service-discovery/ServiceDiscoveryPoolsList.tsx`: +28/-0
- `web/ui/mantine-ui/src/pages/targets/ScrapePoolsList.tsx`: +29/-1
