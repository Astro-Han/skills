# Frozen pull request snapshot

- PR: https://github.com/tailscale/tailscale/pull/20841 — `feature/conn25: expire connector state`
- Author: franbull
- Target base head: `902f5c414a3e0324c934222048779062ae136ee5`
- Comparison base: `902f5c414a3e0324c934222048779062ae136ee5`
- Exact source head: `c53c21cd4fb270ab75cc659807376efb6bb71202`
- Diff: 211 additions, 15 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

The connector struct holds a map of peer+transitIP -> destinationIP that it uses for routing traffic. The client registers new entries in the map over the peer API.

Stop the transitIPs map from growing indefinitely by expiring entries after 1 hour.

Updates tailscale/corp#38261

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

## Changed files

- `feature/conn25/conn25.go`: +112/-13
- `feature/conn25/conn25_test.go`: +99/-2
