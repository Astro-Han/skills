# Frozen pull request snapshot

- PR: https://github.com/prometheus/prometheus/pull/19461 — `tsdb: stabilize the XOR2 float chunk encoding`
- Author: roidelapluie
- Target base head: `a70bacac22231ab4cf87e7bc4115582f5b824f5f`
- Comparison base: `a70bacac22231ab4cf87e7bc4115582f5b824f5f`
- Exact source head: `c1f3939425a41e4d4ed596327ed7a519197cb324`
- Diff: 125 additions, 119 deletions, 15 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Deprecate the --enable-feature=xor2-encoding flag. It now only sets the default for storage.tsdb.chunk_encoding.floats and will become a no-op in a future major version; select xor2 directly in the config instead.

<!--
    - Please give your PR a title in the form "area: short description".  For example "tsdb: reduce disk usage by 95%"

    - Please sign CNCF's Developer Certificate of Origin and sign-off your commits by adding the -s / --signoff flag to `git commit`. See https://github.com/apps/dco for more information.

    - If the PR adds or changes a behaviour or fixes a bug of an exported API it would need a unit/e2e test.

    - Where possible use only exported APIs for tests to simplify the review and make it as close as possible to an actual library usage.

    - Performance improvements would need a benchmark test to prove it.

    - All exposed objects should have a comment.

    - All comments should start with a capital letter and end with a full stop.
 -->

#### Which issue(s) does the PR fix:
<!--
If it applies.
Automatically closes linked issue when PR is merged.
Usage: `Fixes #<issue number>`, or `Fixes (paste link of issue)`.
More at https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword
-->

#### Release notes for end users (**ALL** commits must be considered).
*Reviewers should verify clarity and quality.*

<!--
Write NONE only if there is no user-facing change.

Otherwise use one of: [FEATURE] [ENHANCEMENT] [PERF] [BUGFIX] [SECURITY] [CHANGE]
Following the pattern `[TYPE] Component: description.`

Example: [FEATURE] API: Add `/api/v1/features` endpoint.

Refer to the existing CHANGELOG for inspiration:  https://github.com/prometheus/
prometheus/blob/main/CHANGELOG.md
-->
```release-notes
[ENHANCEMENT] TSDB: Stabilize the XOR2 float chunk encoding. `--enable-feature=xor2-encoding` is deprecated; use `storage.tsdb.chunk_encoding.floats: xor2` instead. Check that other software reading the TSDB directly (e.g. Thanos sidecar) supports XOR2 before enabling.
```


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- dependabot: SKIPPED
- Go tests: SUCCESS
- check: SUCCESS
- Scorecards analysis: SUCCESS
- More Go tests: SUCCESS
- Go tests for 32-bit x86: SUCCESS
- List active LTS releases: SUCCESS
- Go tests with previous Go version: SUCCESS
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

- `cmd/prometheus/main.go`: +11/-4
- `cmd/prometheus/main_test.go`: +36/-4
- `cmd/prometheus/testdata/features.json`: +1/-1
- `config/config.go`: +3/-3
- `docs/configuration/configuration.md`: +14/-8
- `docs/feature_flags.md`: +4/-19
- `promql/functions_test.go`: +0/-1
- `promql/promqltest/test.go`: +0/-1
- `promql/promqltest/test_test.go`: +0/-1
- `scrape/scrape_test.go`: +0/-1
- `tsdb/db.go`: +25/-31
- `tsdb/db_append_v2_test.go`: +0/-2
- `tsdb/db_test.go`: +30/-41
- `tsdb/docs/format/chunks.md`: +1/-1
- `tsdb/querier_test.go`: +0/-1
