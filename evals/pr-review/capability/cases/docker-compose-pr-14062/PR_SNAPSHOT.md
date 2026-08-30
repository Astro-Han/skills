# Frozen pull request snapshot

- PR: https://github.com/docker/compose/pull/14062 — `refactor: one handler per container event in monitor.Start, add tests`
- Author: ndeloof
- Target base head: `d254e7d062592834e9328a3b8c756025323cc754`
- Comparison base: `d254e7d062592834e9328a3b8c756025323cc754`
- Exact source head: `42fb13fa81c511ccdfb1569eb05d0ae677fc9ea1`
- Diff: 326 additions, 76 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

**What I did**

Restructured `monitor.Start` (cognitive complexity 77 → 19), the event loop driving `up`/`logs` termination: each container action moves to an `onContainerX` handler and the recurring bits get names (`watched`, `notify`, `initialContainers`). The tracking sets stay explicit parameters so data flow remains visible. No behavior change: same events, same ordering, same termination conditions.

Since the monitor had no unit test, the refactor ships with a suite covering the full container lifecycle, restart detection through both engine states (`Restarting`, and `Running` per moby/moby#45538), the already-removed-on-die path, service filtering, events stream errors, context cancellation, and exit-code parse errors. `monitor.go` functions are now 75–100% covered.

**Related issue**

n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Analyze (actions): SUCCESS
- AI disclosure gate: SUCCESS
- validate (lint): SUCCESS
- zizmor / zizmor: SUCCESS
- Analyze (go): SUCCESS
- validate (validate-go-mod): SUCCESS
- validate (validate-headers): SUCCESS
- validate (validate-docs): SUCCESS
- binary / registry-identities / setup-registry-identities: SUCCESS
- binary / prepare: SUCCESS
- binary / build (0, darwin/amd64, ubuntu-24.04): SUCCESS
- binary / build (1, darwin/arm64, ubuntu-24.04): SUCCESS
- binary / build (2, linux/amd64, ubuntu-24.04): SUCCESS
- binary / build (3, linux/arm/v6, ubuntu-24.04): SUCCESS
- binary / build (4, linux/arm/v7, ubuntu-24.04): SUCCESS
- binary / build (5, linux/arm64, ubuntu-24.04): SUCCESS
- binary / build (6, linux/ppc64le, ubuntu-24.04): SUCCESS
- binary / build (7, linux/riscv64, ubuntu-24.04): SUCCESS
- binary / build (8, linux/s390x, ubuntu-24.04): SUCCESS
- binary / build (9, windows/amd64, ubuntu-24.04): SUCCESS
- binary / build (10, windows/arm64, ubuntu-24.04): SUCCESS
- binary / finalize: SUCCESS
- bin-image-test / registry-identities / setup-registry-identities: SUCCESS
- bin-image-test / prepare: SUCCESS
- bin-image-test / build (0, darwin/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (1, darwin/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / build (2, linux/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (3, linux/arm/v6, ubuntu-24.04): SUCCESS
- bin-image-test / build (4, linux/arm/v7, ubuntu-24.04): SUCCESS
- bin-image-test / build (5, linux/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / build (6, linux/ppc64le, ubuntu-24.04): SUCCESS
- bin-image-test / build (7, linux/riscv64, ubuntu-24.04): SUCCESS
- bin-image-test / build (8, linux/s390x, ubuntu-24.04): SUCCESS
- bin-image-test / build (9, windows/amd64, ubuntu-24.04): SUCCESS
- bin-image-test / build (10, windows/arm64, ubuntu-24.04): SUCCESS
- bin-image-test / finalize: SUCCESS
- test: SUCCESS
- e2e (plugin, stable, graphdriver): SUCCESS
- e2e (plugin, stable, containerd): FAILURE
- e2e (standalone, stable, graphdriver): FAILURE
- e2e (standalone, stable, containerd): SUCCESS
- e2e (plugin, oldstable, graphdriver): SUCCESS
- e2e (standalone, oldstable, graphdriver): SUCCESS
- binary-finalize: SUCCESS
- coverage: SKIPPED
- release: SKIPPED
- CodeQL: SUCCESS
- zizmor: SUCCESS
- DCO: SUCCESS

## Changed files

- `pkg/compose/monitor.go`: +102/-76
- `pkg/compose/monitor_test.go`: +224/-0
