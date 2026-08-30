# Frozen pull request snapshot

- PR: https://github.com/tokio-rs/tokio/pull/8300 — `signal: restore MSRV by removing OnceLock::wait from the Windows handler`
- Author: jensholdgaard
- Target base head: `eb4988dc2ecb85d2617971fbbabc84938c141bfd`
- Comparison base: `eb4988dc2ecb85d2617971fbbabc84938c141bfd`
- Exact source head: `ac09983cf50ed0d46678e7fef373143562ab9cdd`
- Diff: 21 additions, 10 deletions, 1 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Motivation

Fixes #8299: tokio 1.53.0 declares `rust-version = "1.71"` but uses `OnceLock::wait` — stabilized in Rust **1.86** — in the Windows console ctrl handler (`src/signal/windows/sys.rs`), so any `cargo check` of a Windows target with a toolchain in the declared-supported `1.71..1.86` range fails:

```
error[E0599]: no method named `wait` found for struct `OnceLock` in the current scope
```

This began breaking downstream MSRV CI on Windows the day 1.53.0 published (e.g. opentelemetry-rust's `msrv (windows-latest)` job — diagnosis in open-telemetry/opentelemetry-rust#3600).

## Solution

The `wait()` existed only because `SetConsoleCtrlHandler` was called **inside** `REGISTRY`'s `get_or_init` closure — i.e. before the `OnceLock` was actually initialized — leaving a window where an invoked handler could observe an uninitialized `REGISTRY` (the comment in `handler` documented exactly that window).

This PR removes the window instead of blocking on it: initialize the registry first, then register the OS handler (exactly once, through a second `OnceLock` that also caches a registration failure so every subsequent `new()` reports the same error — identical semantics to before). The handler can then rely on plain `get()`: registration happens-after initialization, so an invoked handler always finds the registry. The defensive `else` arm is kept (returns 0, letting the OS run the next handler) with an updated comment.

No behavior change intended beyond restoring the MSRV: same one-time registration, same cached-failure semantics, same handler behavior; the existing tests in the module (which drive `handler` directly after creating signals through the public API) are unchanged and still compile for the Windows target.

Verification (done from a non-Windows host — `cargo check` needs no linker):

- `cargo +1.71 check -p tokio --features full --target x86_64-pc-windows-msvc` — **fails with the reported E0599 before this change, clean after** (1.71 = the declared MSRV).
- `cargo check -p tokio --features full --target x86_64-pc-windows-msvc --all-targets` on stable — clean (includes the module's test targets).

Disclosure: this fix was developed with AI assistance under my direction; I reviewed the change and the verification above was run as described.


## Linked issues

### https://github.com/tokio-rs/tokio/issues/8299 — tokio 1.53.0 breaks its declared MSRV (1.71) on Windows: OnceLock::wait (Rust 1.86) in signal/windows/sys.rs

**Version**

tokio v1.53.0 (crates.io, published 2026-07-17)

**Platform**

Windows (x86_64-pc-windows-msvc) — the affected code is behind `cfg(windows)`; other platforms are unaffected.

**Description**

tokio 1.53.0 declares `rust-version = "1.71"` in its manifest, but `src/signal/windows/sys.rs:112` (at tag `tokio-1.53.0`) calls [`OnceLock::wait`](https://doc.rust-lang.org/std/sync/struct.OnceLock.html#method.wait):

```rust
let Ok(registry) = REGISTRY.wait().as_ref() else {
```

`OnceLock::wait` was stabilized in **Rust 1.86**, so any Windows build of tokio 1.53.0 with a toolchain in the declared-supported range `1.71..1.86` fails:

```
error[E0599]: no method named `wait` found for struct `OnceLock` in the current scope
   --> tokio-1.53.0/src/signal/windows/sys.rs:112:33
    |
112 |     let Ok(registry) = REGISTRY.wait().as_ref() else {
    |                                 ^^^^ method not found in `OnceLock<Result<Registry, i32>>`
```

I expected `cargo check` with any toolchain ≥ the declared `rust-version` to succeed; instead it fails on Windows for every toolchain below 1.86. Since the code path is `cfg(windows)`-gated, I suspect the MSRV CI job doesn't cover the Windows signal module.

Observed in the wild: this began breaking downstream MSRV CI on Windows the day 1.53.0 published (e.g. open-telemetry/opentelemetry-rust's `msrv (windows-latest)` job, verifying an example against Rust 1.75 — [failing job](https://github.com/open-telemetry/opentelemetry-rust/actions/runs/29684156505/job/88185441506), diagnosis in [open-telemetry/opentelemetry-rust#3599 (comment)](https://github.com/open-telemetry/opentelemetry-rust/pull/3599#issuecomment-5015466054)).

(Disclosure: this report was drafted with AI assistance; the source facts — the tag's manifest `rust-version`, the `sys.rs` call site, and the publish date — were verified directly against the `tokio-1.53.0` tag and crates.io.)


## Exact-head checks

- loom tokio::runtime::spawn_blocking: SKIPPED
- minrust: SUCCESS
- triage: SUCCESS
- Stress Test (simple_echo_tcp): SUCCESS
- loom tokio::sync: SKIPPED
- fmt: SUCCESS
- loom time driver: SKIPPED
- clippy: SUCCESS
- loom current-thread scheduler: SKIPPED
- docs (windows-latest, tracing): SUCCESS
- docs (ubuntu-latest, tracing,io-uring,taskdump): SUCCESS
- loom multi-thread scheduler: SKIPPED
- Check README: SUCCESS
- loom tokio-util: SKIPPED
- test tokio for wasm32-wasip2: SUCCESS
- get-latest-kernel-version: SUCCESS
- basic checks: SUCCESS
- test tokio full (windows-latest): SUCCESS
- test tokio full (ubuntu-latest): SUCCESS
- test tokio full (macos-latest): SUCCESS
- test all crates in the workspace with all features (windows-latest): SUCCESS
- test all crates in the workspace with all features (ubuntu-latest): SUCCESS
- test all crates in the workspace with all features (macos-latest): SUCCESS
- test all crates in the workspace with all features and panic=abort (windows-latest): SUCCESS
- test all crates in the workspace with all features and panic=abort (ubuntu-latest): SUCCESS
- test all crates in the workspace with all features and panic=abort (macos-latest): SUCCESS
- Run integration tests for each feature (windows-latest): SUCCESS
- Run integration tests for each feature (ubuntu-latest): SUCCESS
- Run integration tests for each feature (macos-latest): SUCCESS
- compile tests with parking lot send guards: SUCCESS
- valgrind: SUCCESS
- test tokio full --unstable (windows-latest): SUCCESS
- test tokio full --unstable (ubuntu-latest): SUCCESS
- test tokio full --unstable (ubuntu-latest, io-uring): SUCCESS
- test tokio full --unstable (macos-latest): SUCCESS
- test tokio full --unstable --taskdump (ubuntu-latest): SUCCESS
- check tokio full --internal-mt-counters (ubuntu-latest): SUCCESS
- miri-lib: SUCCESS
- miri-test: SUCCESS
- miri-doc: SUCCESS
- asan: SUCCESS
- semver: SUCCESS
- cross-check (powerpc-unknown-linux-gnu): SUCCESS
- cross-check (powerpc64-unknown-linux-gnu): SUCCESS
- cross-check (arm-linux-androideabi): SUCCESS
- cross-check-tier3 (x86_64-unknown-haiku, taskdump): SUCCESS
- cross-test-with-parking_lot (i686-unknown-linux-gnu, ubuntu-latest, taskdump): SUCCESS
- cross-test-with-parking_lot (armv5te-unknown-linux-gnueabi, ubuntu-latest): SUCCESS
- cross-test-with-parking_lot (armv7-unknown-linux-gnueabihf, ubuntu-24.04-arm): SUCCESS
- cross-test-with-parking_lot (aarch64-unknown-linux-gnu, ubuntu-24.04-arm, io-uring,taskdump): SUCCESS
- cross-test-with-parking_lot (aarch64-pc-windows-msvc, windows-11-arm): SUCCESS
- cross-test-without-parking_lot (i686-unknown-linux-gnu, ubuntu-latest, taskdump): SUCCESS
- cross-test-without-parking_lot (armv5te-unknown-linux-gnueabi, ubuntu-latest): SUCCESS
- cross-test-without-parking_lot (armv7-unknown-linux-gnueabihf, ubuntu-24.04-arm): SUCCESS
- cross-test-without-parking_lot (aarch64-unknown-linux-gnu, ubuntu-24.04-arm, io-uring,taskdump): SUCCESS
- cross-test-without-parking_lot (aarch64-pc-windows-msvc, windows-11-arm): SUCCESS
- Test tokio --all-features on i686-unknown-linux-gnu without AtomicU64: SUCCESS
- Check tokio --feature-powerset --depth 2 on i686-unknown-linux-gnu without AtomicU64: SUCCESS
- features exclude: SUCCESS
- features exclude --unstable: SUCCESS
- features exclude --unstable io-uring,taskdump,schedule-latency: SUCCESS
- minimal-versions: SUCCESS
- build loom tests: SUCCESS
- Test hyper (windows-latest): SUCCESS
- Test hyper (ubuntu-latest): SUCCESS
- Test hyper (macos-latest): SUCCESS
- Test Quinn (windows-latest): SUCCESS
- Test Quinn (ubuntu-latest): SUCCESS
- Test Quinn (macos-latest): SUCCESS
- build tokio for x86_64-fortanix-unknown-sgx: SUCCESS
- build tokio for redox-os: SUCCESS
- test tokio for wasm32-unknown-unknown (macros sync): SUCCESS
- test tokio for wasm32-unknown-unknown (macros sync rt): SUCCESS
- test tokio for wasm32-unknown-unknown (macros sync time rt): SUCCESS
- wasm32-wasip1: SUCCESS
- wasm32-wasip1-threads: SUCCESS
- check-external-types (windows-latest): SUCCESS
- check-external-types (ubuntu-latest): SUCCESS
- check-fuzzing: SUCCESS
- check-spelling: SUCCESS
- Test io_uring on Linux 7.1.4 / build: SUCCESS
- Test io_uring on Linux 4.19.325 / build: SUCCESS
- FreeBSD x86_64: SUCCESS
- FreeBSD docs: SUCCESS
- FreeBSD i686: SUCCESS
- Header rules - tokio-rs: NEUTRAL
- Pages changed - tokio-rs: NEUTRAL
- *control: SUCCESS
- Redirect rules - tokio-rs: SUCCESS
- unnamed: SUCCESS

## Changed files

- `tokio/src/signal/windows/sys.rs`: +21/-10
