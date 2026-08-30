# Frozen pull request snapshot

- PR: https://github.com/tailscale/tailscale/pull/20673 — `feature/conn25: clear address assignments, flow tables on profile switch`
- Author: tendstofortytwo
- Target base head: `d4dce809278ecc0bfc50ea2d376459c66f2f3a66`
- Comparison base: `514e50bd1bd0f0689f87ffb3a7adc306150290c8`
- Exact source head: `0905f9e2f93796c169f07ca66fa7e33669a58d29`
- Diff: 118 additions, 4 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

On switching from one tailnet with Connectors 2025 enabled to another, clear the address assignments and flow tables from the previous tailnet. They will not be useful in the new one (since the tailnet configuration and nodes are different), and could blackhole traffic if both tailnets happen to have a connector for the same domain.

Fixes tailscale/corp#45619.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- prepare: SKIPPED
- gomod-cache: SUCCESS
- Analyze (go): SUCCESS
- deploy: SUCCESS
- checklocks: SUCCESS
- lint: SUCCESS
- EasyEasy: SUCCESS
- vet: SUCCESS
- matrix.test: SKIPPED
- fuzz: SUCCESS
- race-root-integration (1/4): SUCCESS
- race-root-integration (2/4): SUCCESS
- race-root-integration (3/4): SUCCESS
- race-root-integration (4/4): SUCCESS
- test (amd64): SUCCESS
- test (amd64, -race, 1/3): SUCCESS
- test (amd64, -race, 2/3): SUCCESS
- test (amd64, -race, 3/3): SUCCESS
- test (386): SUCCESS
- Windows (benchmarks): SUCCESS
- Windows (1/2): SUCCESS
- Windows (2/2): SUCCESS
- macos: SUCCESS
- privileged: SUCCESS
- cross (linux, arm64): SUCCESS
- cross (linux, 386): SUCCESS
- cross (linux, loong64): SUCCESS
- cross (linux, arm, 5): SUCCESS
- cross (linux, arm, 7): SUCCESS
- cross (darwin, amd64): SUCCESS
- cross (darwin, arm64): SUCCESS
- cross (windows, amd64): SUCCESS
- cross (windows, arm64): SUCCESS
- cross (freebsd, amd64): SUCCESS
- cross (openbsd, amd64): SUCCESS
- ios: SUCCESS
- crossmin (plan9, amd64): SUCCESS
- crossmin (aix, ppc64): SUCCESS
- crossmin (solaris, amd64): SUCCESS
- crossmin (illumos, amd64): SUCCESS
- android: SUCCESS
- wasm: SUCCESS
- tailscale_go: SUCCESS
- depaware: SUCCESS
- go_generate: SUCCESS
- make_tidy: SUCCESS
- licenses: SUCCESS
- staticcheck (macOS): SUCCESS
- staticcheck (Windows): SUCCESS
- staticcheck (Linux): SUCCESS
- staticcheck (Portable (1/4)): SUCCESS
- staticcheck (Portable (2/4)): SUCCESS
- staticcheck (Portable (3/4)): SUCCESS
- staticcheck (Portable (4/4)): SUCCESS
- notify_slack: SUCCESS
- merge_blocker: SUCCESS
- check_mergeability_strict: SUCCESS
- check_mergeability: SUCCESS
- CodeQL: SUCCESS
- DCO: SUCCESS
- unnamed: SUCCESS

## Changed files

- `feature/conn25/conn25.go`: +54/-4
- `feature/conn25/datapath.go`: +8/-0
- `feature/conn25/flowtable.go`: +17/-0
- `feature/conn25/flowtable_test.go`: +39/-0
