# Frozen pull request snapshot

- PR: https://github.com/tailscale/tailscale/pull/20388 — `go.mod: Update vulnerable dependencies`
- Author: jentfoo
- Target base head: `7965d496a687919ae38078f9a0428b87eaa5f854`
- Comparison base: `7965d496a687919ae38078f9a0428b87eaa5f854`
- Exact source head: `1ba1d565edbc691a1fb01e7c9d48f21f3bd80217`
- Diff: 320 additions, 267 deletions, 11 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This change updates vulnerable dependencies with a direct fix path. Updated:
* github.com/prometheus/prometheus@v0.311.3 - Direct dependency addressing https://pkg.go.dev/vuln/GO-2026-5710 and https://pkg.go.dev/vuln/GO-2026-5662
* github.com/go-openapi/swag@v0.27.0 - Needed to fix mutal dependency on github.com/go-openapi/testify/v2 after prometheus update
* github.com/go-git/go-git/v5@v5.19.1 - Addresses https://pkg.go.dev/vuln/GO-2026-5496
* helm.sh/helm/v3@v3.21.1 - Root update to address most containerd CVEs
* github.com/containerd/containerd@v1.7.33 - Addresses remaining containerd CVEs, in total: https://pkg.go.dev/vuln/GO-2026-5758 https://pkg.go.dev/vuln/GO-2026-5475 https://pkg.go.dev/vuln/GO-2026-5378

Not addressed are containerd CVE's which require a `v2` update, or have no patch:
* https://pkg.go.dev/vuln/GO-2026-5064
* https://pkg.go.dev/vuln/GO-2026-5338
* https://pkg.go.dev/vuln/GO-2026-5622
* https://pkg.go.dev/vuln/GO-2026-5932

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- prepare: SKIPPED
- Request K8s Review: SKIPPED
- gomod-cache: SUCCESS
- Analyze (go): SUCCESS
- deploy: SUCCESS
- testchart: SUCCESS
- lint: SUCCESS
- EasyEasy: SUCCESS
- policybot-test: SUCCESS
- Request K8s Review: SUCCESS
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

- `cmd/k8s-operator/depaware.txt`: +27/-17
- `cmd/k8s-operator/deploy/crds/tailscale.com_dnsconfigs.yaml`: +2/-1
- `cmd/k8s-operator/deploy/crds/tailscale.com_proxyclasses.yaml`: +2/-1
- `cmd/k8s-operator/deploy/crds/tailscale.com_recorders.yaml`: +2/-1
- `cmd/k8s-operator/deploy/manifests/operator.yaml`: +6/-3
- `cmd/tailscaled/depaware.txt`: +1/-1
- `flake.nix`: +1/-1
- `flakehashes.json`: +2/-2
- `go.mod`: +71/-63
- `go.sum`: +205/-176
- `shell.nix`: +1/-1
