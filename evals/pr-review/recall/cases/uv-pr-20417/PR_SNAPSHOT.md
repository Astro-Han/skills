# Frozen pull request snapshot

- PR: https://github.com/astral-sh/uv/pull/20417 — `Revert "Add `--cert` support to `uv pip`"`
- Author: charliermarsh
- Target base head: `a2af4cb54a708c10e731b3a1c3a5c3ff13832b47`
- Comparison base: `a2af4cb54a708c10e731b3a1c3a5c3ff13832b47`
- Exact source head: `89354ed862c88f465dd1086c8bf7bfb12e61c97d`
- Diff: 53 additions, 201 deletions, 11 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Revert #20367. Supporting `--cert` changes certificate-trust behavior for existing `uv pip` invocations, so it is breaking and should not land in a non-breaking release.

Move the change to the 0.12 release line in #20418.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- plan: SUCCESS
- review: SUCCESS
- check-fmt / rust: SUCCESS
- prepare: SUCCESS
- check-fmt / prettier: SUCCESS
- report: SUCCESS
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

- `crates/uv-cli/src/compat.rs`: +18/-0
- `crates/uv-cli/src/lib.rs`: +0/-6
- `crates/uv-client/src/base_client.rs`: +5/-15
- `crates/uv-client/src/lib.rs`: +0/-1
- `crates/uv-client/src/tls.rs`: +5/-46
- `crates/uv-client/tests/it/ssl_certs.rs`: +12/-66
- `crates/uv/src/lib.rs`: +1/-28
- `crates/uv/tests/it/help.rs`: +0/-23
- `crates/uv/tests/pip/pip_sync.rs`: +6/-5
- `crates/uv/tests/pip_compile/pip_compile.rs`: +6/-5
- `docs/concepts/authentication/certificates.md`: +0/-6
