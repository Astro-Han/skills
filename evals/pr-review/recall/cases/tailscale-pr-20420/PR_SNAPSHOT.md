# Frozen pull request snapshot

- PR: https://github.com/tailscale/tailscale/pull/20420 — `Revert "go.mod: Update vulnerable dependencies (#20388)"`
- Author: fserb
- Target base head: `125fd88c305b296717019bb8b9867b0973c06ec7`
- Comparison base: `125fd88c305b296717019bb8b9867b0973c06ec7`
- Exact source head: `22a93c1476526e46a8e5ba6914bcdfc58053243a`
- Diff: 267 additions, 320 deletions, 11 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This reverts commit ca9f6971e542a0c2df6e756e2b28f1bde945cf89 (#20388)

The dependency updates broke the K8s E2E tests. Reverting so the updates can be re-landed with the tests passing.

flake.nix, shell.nix, and flakehashes.json were regenerated with tool/updateflakes rather than reverted, since a later commit (6fdffd9e5) also updated them for the gowebdav bump.

Change-Id: Id4afd7788d305a674841168e2a66a0009212ffd3

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- gomod-cache: SUCCESS
- Analyze (go): SUCCESS
- deploy: SUCCESS
- testchart: SUCCESS
- lint: SUCCESS
- EasyEasy: SUCCESS
- policybot-test: SUCCESS
- Request K8s Review: SUCCESS
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
- vm: SUCCESS
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

- `cmd/k8s-operator/depaware.txt`: +17/-27
- `cmd/k8s-operator/deploy/crds/tailscale.com_dnsconfigs.yaml`: +1/-2
- `cmd/k8s-operator/deploy/crds/tailscale.com_proxyclasses.yaml`: +1/-2
- `cmd/k8s-operator/deploy/crds/tailscale.com_recorders.yaml`: +1/-2
- `cmd/k8s-operator/deploy/manifests/operator.yaml`: +3/-6
- `cmd/tailscaled/depaware.txt`: +1/-1
- `flake.nix`: +1/-1
- `flakehashes.json`: +2/-2
- `go.mod`: +63/-71
- `go.sum`: +176/-205
- `shell.nix`: +1/-1
