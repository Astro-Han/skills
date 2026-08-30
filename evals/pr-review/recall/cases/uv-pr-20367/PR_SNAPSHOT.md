# Frozen pull request snapshot

- PR: https://github.com/astral-sh/uv/pull/20367 — `Add `--cert` support to `uv pip``
- Author: charliermarsh
- Target base head: `3d92ddb084041992ba92bc64ef0bff549a10b048`
- Comparison base: `2937610e418bf5bb8e8922f5c935e67215d4f8c1`
- Exact source head: `a9c7c42fb6c7294dad0f49cb4364307a6651cb8d`
- Diff: 201 additions, 53 deletions, 11 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

Add pip-compatible `--cert <path>` support to all `uv pip` commands. The option is scoped to the `uv pip` namespace, so other uv commands continue to reject it.

An explicit certificate bundle replaces uv's default, system, and `SSL_CERT_FILE` / `SSL_CERT_DIR` trust sources for that invocation, matching pip's behavior without modifying the environment inherited by child processes.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- plan: SUCCESS
- check-fmt / rust: SUCCESS
- check-fmt / prettier: SUCCESS
- check-fmt / python: SUCCESS
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

- `crates/uv-cli/src/compat.rs`: +0/-18
- `crates/uv-cli/src/lib.rs`: +6/-0
- `crates/uv-client/src/base_client.rs`: +15/-5
- `crates/uv-client/src/lib.rs`: +1/-0
- `crates/uv-client/src/tls.rs`: +46/-5
- `crates/uv-client/tests/it/ssl_certs.rs`: +66/-12
- `crates/uv/src/lib.rs`: +28/-1
- `crates/uv/tests/it/help.rs`: +23/-0
- `crates/uv/tests/pip/pip_sync.rs`: +5/-6
- `crates/uv/tests/pip_compile/pip_compile.rs`: +5/-6
- `docs/concepts/authentication/certificates.md`: +6/-0
