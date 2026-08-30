# Frozen pull request snapshot

- PR: https://github.com/astral-sh/uv/pull/21144 — `Do not treat a URL ending in `.py` as a script path`
- Author: Kayvan-Zahiri
- Target base head: `7ae99e21bbc6176cbd23cb9abc7b7e3fb507bdf9`
- Comparison base: `7ae99e21bbc6176cbd23cb9abc7b7e3fb507bdf9`
- Exact source head: `e9b370ece55957369f2319383fc03b5aa5d7e0ff`
- Diff: 94 additions, 6 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

`uvx git+https://github.com/uPesy/easyeda2kicad.py` fails with "Not a valid package or extra name".

`has_python_script_ext` calls `Path::extension()` on the raw argument, so any URL whose last segment ends in `.py` is read as a script path. uv then parses the whole URL as a package name, which is where the message comes from.

This skips the script check when the argument carries a scheme `Scheme::parse` recognises. Pairing `split_scheme` with `Scheme::parse` is deliberate and matches the existing use in `verbatim_url.rs`: a bare `split_scheme` would read the `C:` in `C:\script.py` as a scheme and break script detection on Windows.

Before:

```console
$ uv tool run --offline git+https://github.com/uPesy/easyeda2kicad.py
error: Not a valid package or extra name: "git+https://github.com/uPesy/easyeda2kicad.py"
```

After, it reaches the git fetch and stops only on `--offline`:

```console
Updating https://github.com/uPesy/easyeda2kicad.py (HEAD)
error: ... Remote Git fetches are not allowed because network connectivity is disabled
```

Two tests added beside the existing script tests. They use `--offline`, so they exercise the parse without touching the network. Both fail without the change with the exact error above. The existing `script.py`, missing-`script.py` and `--from script.py` behaviours are unchanged.

Closes #21141

## Linked issues

### https://github.com/astral-sh/uv/issues/21141 — uvx: git url is rejected when the repository name ends in .py

### Summary

Using `uvx` with a git repo url that ends with `.py` causes an error:
```
$ uvx git+https://github.com/uPesy/easyeda2kicad.py
error: Not a valid package or extra name: "git+https://github.com/uPesy/easyeda2kicad.py". Names must start and end with
       a letter or digit and may only contain -, _, ., and alphanumeric characters.
```

Same behavior when using `--from`:
```
$ uvx --from git+https://github.com/uPesy/easyeda2kicad.py easyeda2kicad
error: Not a valid package or extra name: "git+https://github.com/uPesy/easyeda2kicad.py". Names must start and end with
       a letter or digit and may only contain -, _, ., and alphanumeric characters.
```

Here is the check that causes the issue:
https://github.com/astral-sh/uv/blob/210d1f6785e95a8c8c0d53e284408c9be1134700/crates/uv/src/commands/tool/run.rs#L127-L130

...which is invoked from here:
https://github.com/astral-sh/uv/blob/210d1f6785e95a8c8c0d53e284408c9be1134700/crates/uv/src/commands/tool/run.rs#L175-L193

### Platform

OpenSuse Tumbleweed 7.1.3-1-default x86_64 GNU/Linux

### Version

0.12.4

### Python version

Python 3.12.13

## Exact-head checks

- plan / plan: SUCCESS
- check-fmt / rust: SUCCESS
- check-fmt / prettier: SUCCESS
- check-fmt / python: SUCCESS
- review: SKIPPED
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
- test / cargo test on macos: SUCCESS
- test / cargo test on windows 1 of 3: SUCCESS
- test / cargo test on windows 2 of 3: SUCCESS
- test / cargo test on windows 3 of 3: SUCCESS
- test-windows-trampolines / check windows crate version: SUCCESS
- test-windows-trampolines / check binary: SKIPPED
- test-windows-trampolines / check on x86_64: SUCCESS
- test-windows-trampolines / check on i686: SUCCESS
- test-windows-trampolines / check on aarch64: SUCCESS
- test-windows-trampolines / test on x86_64: SUCCESS
- test-windows-trampolines / test on i686: SUCCESS
- test-windows-trampolines / test on aarch64: SUCCESS
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
- build-release-binaries / sdist: SUCCESS
- build-release-binaries / x86_64-apple-darwin: SUCCESS
- build-release-binaries / aarch64-apple-darwin: SUCCESS
- build-release-binaries / x86_64-pc-windows-msvc: SUCCESS
- build-release-binaries / i686-pc-windows-msvc: SUCCESS
- build-release-binaries / aarch64-pc-windows-msvc: SUCCESS
- build-release-binaries / i686-unknown-linux-gnu: SUCCESS
- build-release-binaries / x86_64-unknown-linux-gnu: SUCCESS
- build-release-binaries / aarch64-unknown-linux-gnu: SUCCESS
- build-release-binaries / armv7-unknown-linux-gnueabihf: SUCCESS
- build-release-binaries / arm-unknown-linux-musleabihf: SUCCESS
- build-release-binaries / s390x-unknown-linux-gnu: SUCCESS
- build-release-binaries / powerpc64le-unknown-linux-gnu: SUCCESS
- build-release-binaries / riscv64gc-unknown-linux-gnu: SUCCESS
- build-release-binaries / x86_64-unknown-linux-musl: SUCCESS
- build-release-binaries / i686-unknown-linux-musl: SUCCESS
- build-release-binaries / aarch64-unknown-linux-musl: SUCCESS
- build-release-binaries / armv7-unknown-linux-musleabihf: SUCCESS
- build-release-binaries / riscv64gc-unknown-linux-musl: SUCCESS
- build-release-binaries / check wheel contents: SUCCESS
- build-docker / plan: SUCCESS
- build-docker / build uv: SUCCESS
- build-docker / build alpine:3.23,alpine3.23,alpine: SUCCESS
- build-docker / build alpine:3.22,alpine3.22: SUCCESS
- build-docker / build debian:trixie-slim,trixie-slim,debian-slim: SUCCESS
- build-docker / build buildpack-deps:trixie,trixie,debian: SUCCESS
- build-docker / build python:3.14-alpine3.23,python3.14-alpine3.23,python3.14-alpine: SUCCESS
- build-docker / build python:3.13-alpine3.23,python3.13-alpine3.23,python3.13-alpine: SUCCESS
- build-docker / build python:3.12-alpine3.23,python3.12-alpine3.23,python3.12-alpine: SUCCESS
- build-docker / build python:3.11-alpine3.23,python3.11-alpine3.23,python3.11-alpine: SUCCESS
- build-docker / build python:3.10-alpine3.23,python3.10-alpine3.23,python3.10-alpine: SUCCESS
- build-docker / build python:3.9-alpine3.22,python3.9-alpine3.22,python3.9-alpine: SUCCESS
- build-docker / build python:3.14-trixie,python3.14-trixie: SUCCESS
- build-docker / build python:3.13-trixie,python3.13-trixie: SUCCESS
- build-docker / build python:3.12-trixie,python3.12-trixie: SUCCESS
- build-docker / build python:3.11-trixie,python3.11-trixie: SUCCESS
- build-docker / build python:3.10-trixie,python3.10-trixie: SUCCESS
- build-docker / build python:3.9-trixie,python3.9-trixie: SUCCESS
- build-docker / build python:3.14-slim-trixie,python3.14-trixie-slim: SUCCESS
- build-docker / build python:3.13-slim-trixie,python3.13-trixie-slim: SUCCESS
- build-docker / build python:3.12-slim-trixie,python3.12-trixie-slim: SUCCESS
- build-docker / build python:3.11-slim-trixie,python3.11-trixie-slim: SUCCESS
- build-docker / build python:3.10-slim-trixie,python3.10-trixie-slim: SUCCESS
- build-docker / build python:3.9-slim-trixie,python3.9-trixie-slim: SUCCESS
- build-docker / annotate uv: SKIPPED
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

- `crates/uv/src/commands/tool/run.rs`: +23/-6
- `crates/uv/tests/tool/tool_run.rs`: +71/-0
