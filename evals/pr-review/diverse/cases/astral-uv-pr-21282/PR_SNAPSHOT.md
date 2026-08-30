# Frozen pull request snapshot

- PR: https://github.com/astral-sh/uv/pull/21282 — `Return errors for invalid bearer authorization headers`
- Author: konstin
- Target base head: `26a9dd4b2125bc271b47855e1fa0c49af3365db5`
- Comparison base: `26a9dd4b2125bc271b47855e1fa0c49af3365db5`
- Exact source head: `d174a7af1829e4761bb0faec62f9391401e9ee93`
- Diff: 68 additions, 36 deletions, 6 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Bearer tokens can contain bytes that are invalid in an HTTP header, including newlines supplied through `PYX_AUTH_TOKEN` or `UV_AUTH_TOKEN`. Header construction previously assumed those bytes were valid and panicked, now they return errors.

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
- test uv publish: SUCCESS
- all required jobs passed: SUCCESS
- CodSpeed Performance Analysis: SUCCESS
- zizmor: SUCCESS

## Changed files

- `crates/uv-auth/src/credentials.rs`: +21/-24
- `crates/uv-client/src/base_client.rs`: +6/-1
- `crates/uv-publish/src/lib.rs`: +15/-10
- `crates/uv/src/commands/auth/helper.rs`: +1/-0
- `crates/uv/src/commands/auth/logout.rs`: +1/-1
- `crates/uv/tests/it/auth.rs`: +24/-0
