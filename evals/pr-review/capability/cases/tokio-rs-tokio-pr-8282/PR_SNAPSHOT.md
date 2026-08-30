# Frozen pull request snapshot

- PR: https://github.com/tokio-rs/tokio/pull/8282 — `runtime: expose schedule latency in TaskMeta / Task Hooks`
- Author: rcoh
- Target base head: `ecd621dd2c1a5205a84f579225e1454b62af211c`
- Comparison base: `ecd621dd2c1a5205a84f579225e1454b62af211c`
- Exact source head: `52014fdb6ce1c2764b556e882eab8212df6ffcf5`
- Diff: 472 additions, 82 deletions, 15 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body



<!--
Thank you for your Pull Request. Please provide a description above and review
the requirements below.

Bug fixes and new features should include tests.

Contributors guide: https://github.com/tokio-rs/tokio/blob/master/CONTRIBUTING.md

The contributors guide includes instructions for running rustfmt and building the
documentation, which requires special commands beyond `cargo fmt` and `cargo doc`.
-->

## Motivation

#7986 exposes a task-schedule-latency histogram and metric. For tools like dial9, it is very helpful to have this statistic available on a per-poll basis.


<!--
Explain the context and why you're making that change. What is the problem
you're trying to solve? In some cases there is not a problem and this can be
thought of as being the motivation for your change.
-->

## Solution

Expose `schedule_latency() -> Option<Duration>` on `TaskMeta`.

This is off by default. When disabled, schedule_latency returns `None`. It is enabled by calling `track_task_schedule_latency()`; happy to workshop the name. It can be enabled separately from the histogram: if you are tracking the individual latencies there's no specific need to also put them in a histogram. Enabling the histogram also exposes it to `TaskMeta`.

_Assisted by GPT 5.6 Sol_

<!--
Summarize the solution and provide any necessary context needed to understand
the code change.
-->


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- loom tokio::runtime::spawn_blocking: SKIPPED
- minrust: SUCCESS
- triage: SUCCESS
- Stress Test (simple_echo_tcp): SUCCESS
- loom tokio::sync: SKIPPED
- fmt: SUCCESS
- loom time driver: SKIPPED
- clippy: SUCCESS
- docs (windows-latest, tracing): SUCCESS
- loom current-thread scheduler: SUCCESS
- docs (ubuntu-latest, tracing,io-uring,taskdump): SUCCESS
- Check README: SUCCESS
- loom multi-thread scheduler (loom_multi_thread::group_a): SUCCESS
- loom multi-thread scheduler (loom_multi_thread::group_b): SUCCESS
- loom multi-thread scheduler (loom_multi_thread::group_c): SUCCESS
- loom multi-thread scheduler (loom_multi_thread::group_d): SUCCESS
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
- Test io_uring on Linux 7.1.7 / build: SUCCESS
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

- `tokio/src/runtime/builder.rs`: +58/-0
- `tokio/src/runtime/config.rs`: +4/-0
- `tokio/src/runtime/metrics/batch.rs`: +77/-14
- `tokio/src/runtime/metrics/mod.rs`: +2/-2
- `tokio/src/runtime/metrics/schedule_latency.rs`: +1/-1
- `tokio/src/runtime/metrics/schedule_latency_mock.rs`: +0/-9
- `tokio/src/runtime/scheduler/current_thread/mod.rs`: +17/-19
- `tokio/src/runtime/scheduler/multi_thread/handle.rs`: +2/-0
- `tokio/src/runtime/scheduler/multi_thread/stats.rs`: +13/-2
- `tokio/src/runtime/scheduler/multi_thread/worker.rs`: +29/-26
- `tokio/src/runtime/task/harness.rs`: +2/-0
- `tokio/src/runtime/task/mod.rs`: +13/-9
- `tokio/src/runtime/task_hooks.rs`: +31/-0
- `tokio/tests/rt_unstable_metrics.rs`: +51/-0
- `tokio/tests/task_hooks.rs`: +172/-0
