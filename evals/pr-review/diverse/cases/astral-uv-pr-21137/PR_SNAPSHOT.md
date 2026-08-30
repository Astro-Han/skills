# Frozen pull request snapshot

- PR: https://github.com/astral-sh/uv/pull/21137 — `Consistently use creation time for directory `cache-keys` entries regardless of libc`
- Author: EliteTK
- Target base head: `728a70d25c0889d9aaa53776256c3a843eea67a6`
- Comparison base: `3a76e496e36783371a6d91a8f4834478964d36ca`
- Exact source head: `1b97033d572f915260a81b149a2e973b55e8e6f3`
- Diff: 52 additions, 2 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

When using musl we would fall back to using the inode, which would cause churn when going between musl backed and glibc backed uv versions on the same host.

Using rustix, this remains consistent as long as the underlying OS supports the call for the specific filesystem.

This will cause a small bit of churn on musl systems, but that churn will just be in the form of a cache invalidation when updating uv.

## Test Plan

Existing coverage for the functionality. Manual tests for checking musl and linux now work the same (but we bypass glibc/musl so it didn't feel worth it to try to come up with an automated regression test here).

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- plan / plan: SUCCESS
- check-fmt / rust: SUCCESS
- check-fmt / prettier: SUCCESS
- check-fmt / python: SUCCESS
- review / security review: SUCCESS
- review / prepare: SUCCESS
- review / report: SKIPPED
- check-lint / ruff: SUCCESS
- check-lint / ty: SUCCESS
- check-lint / shellcheck: SUCCESS
- check-lint / validate-pyproject: SUCCESS
- check-lint / readme: SUCCESS
- check-lint / clippy on linux: SUCCESS
- check-lint / clippy on windows: SUCCESS
- check-lint / hawk: SUCCESS
- check-lint / cargo shear: SUCCESS
- check-lint / typos: SUCCESS
- check-docs / mkdocs: SUCCESS
- check-zizmor / zizmor: SUCCESS
- check-publish / cargo publish dry-run: SUCCESS
- check-release / dist plan: SUCCESS
- check-lock / uv lockfiles: SUCCESS
- check-generated-files / cargo dev generate-all: SUCCESS
- test / cargo test on linux: SUCCESS
- test / cargo test on macos: SKIPPED
- test / cargo test on windows 1 of 3: SUCCESS
- test / cargo test on windows 2 of 3: SUCCESS
- test / cargo test on windows 3 of 3: SUCCESS
- test-windows-trampolines: SKIPPED
- build-dev-binaries / linux libc: SUCCESS
- build-dev-binaries / linux aarch64: SUCCESS
- build-dev-binaries / linux armv7 gnueabihf: SUCCESS
- build-dev-binaries / linux musl: SUCCESS
- build-dev-binaries / macos aarch64: SUCCESS
- build-dev-binaries / macos x86_64: SUCCESS
- build-dev-binaries / windows x86_64: SUCCESS
- build-dev-binaries / windows aarch64: SUCCESS
- build-dev-binaries / msrv: SUCCESS
- build-dev-binaries / android aarch64: SUCCESS
- build-dev-binaries / freebsd: SUCCESS
- build-release-binaries: SKIPPED
- build-docker: SKIPPED
- bench / walltime build: SUCCESS
- bench / simulated: SUCCESS
- bench / walltime on aarch64 linux: SUCCESS
- test-smoke / linux: SUCCESS
- test-smoke / linux aarch64: SUCCESS
- test-smoke / linux musl: SUCCESS
- test-smoke / macos: SUCCESS
- test-smoke / windows x86_64: SUCCESS
- test-smoke / windows aarch64: SUCCESS
- test-integration: SKIPPED
- test-system: SKIPPED
- test-ecosystem / prefecthq/prefect: SUCCESS
- test-ecosystem / pallets/flask: SUCCESS
- test-ecosystem / pydantic/pydantic-core: SUCCESS
- test uv publish: SKIPPED
- all required jobs passed: SUCCESS
- CodSpeed Performance Analysis: SUCCESS
- zizmor: SUCCESS

## Changed files

- `crates/uv-cache-info/src/cache_info.rs`: +2/-2
- `crates/uv-fs/src/lib.rs`: +50/-0
