# Frozen pull request snapshot

- PR: https://github.com/vercel/next.js/pull/97902 — `Guard filesystem reads against unresolved symlinks`
- Author: sokra
- Target base head: `d352f1740a870d2dcf84f367019dfe7fe033646c`
- Comparison base: `d352f1740a870d2dcf84f367019dfe7fe033646c`
- Exact source head: `24d05ce8c2decf918bb59036e85dd539c0d18dec`
- Diff: 527 additions, 46 deletions, 13 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

### What?

Adds debug-only OS realpath validation to successful `DiskFileSystem` file and directory reads. When a successfully canonicalized path differs from the supplied path, the read returns a normal task error naming both paths.

Fixes pattern/glob traversal and NFT tracing so physical filesystem access uses resolved paths while logical paths remain available for user-visible specifiers and complete symlink-chain recovery.

### Why?

Reading through an unresolved symlink parent gives the same filesystem object multiple path identities. That can make Turbo Tasks dependency tracking and invalidation inconsistent and can produce invalid deployment ZIPs when NFT output contains files below unresolved links.

The checks return errors rather than asserting because paths can disagree temporarily under eventual consistency. Propagating a task error avoids panicking a worker thread while still exposing invalid callers during development.

### How?

The validation lives directly in `DiskFileSystem::read` and `DiskFileSystem::raw_read_dir`. It calls the OS canonicalization API inline instead of the Turbo Tasks realpath task, keeping the diagnostic out of the task dependency graph. The guard runs only after the OS read succeeds, so missing/non-directory probes preserve their existing behavior.

`read_matches` resolves each physical directory immediately before enumeration while retaining logical `PatternMatch` paths.

`read_glob` and `track_glob` now resolve their initial directory before enumeration. Symlinks discovered later through wildcard segments are also traversed through resolved targets. `ReadGlobResult` deliberately retains logical paths rooted at the supplied base, allowing consumers to call `realpath_with_links` and recover the complete symlink chain.

Consumers follow that contract explicitly:

- NFT includes expand each logical match with `realpath_with_links`, emit resolved files and every traversed symlink, skip resolved directory targets, and deterministically deduplicate/sort output.
- `import.meta.glob` uses recursive logical keys as the source of user-visible requests, while module resolution follows and tracks symlinks.
- the hash-glob example resolves returned logical paths before reading.

Webpack-loader context dependencies are covered for both `path/to/symlink/inner/path/*` and `path/to/*/inner/path/*`. The loader fixture performs its directory read with Node `fs`, reports the directory using `addContextDependency`, and Turbopack tracks the resolved target.

### Verification

- `cargo fmt -p turbo-tasks-fs -p turbopack-ecmascript -p next-api -- --check`
- `cargo clippy -p turbo-tasks-fs -p turbopack-ecmascript -p next-api --all-targets`
- `cargo test -p turbo-tasks-fs` (128 passed)
- `cargo test -p next-api` (7 passed)
- `cargo check -p turbo-tasks-fs --examples`
- `import.meta.glob` symlink execution fixture (1 passed)
- Nine targeted node-file-trace CI cases with `release-with-assertions` (9 passed)
- `pnpm build-all`
- `webpack-loader-fs` Turbopack dev e2e (1 passed)
- `build-trace-extra-entries-turbo` Turbopack production e2e (1 passed)
- twoslash Turbopack production, normal mode (4 passed)
- twoslash Turbopack production, cache-components mode (4 passed)
- `bench/heavy-npm-deps` Turbopack development smoke test (HTTP 200)

### Notes

The disk guard is cross-platform, while its symlink-parent regression test is Unix-only, matching neighbouring symlink tests. On Windows, OS canonicalization can also normalize casing and 8.3 short names; a debug read using a non-canonical spelling will therefore return the same diagnostic error.

<!-- NEXT_JS_LLM -->


<!-- fleet 1d32e12c-f4ec-4f22-862a-c85f0005805c -->

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- deploy-target: SKIPPED
- deploy-target: SUCCESS
- optimize-ci / PR Stack Optimizer: SUCCESS
- build: SKIPPED
- build: SUCCESS
- Determine changes: SUCCESS
- generate-native-matrix: SKIPPED
- generate-native-matrix: SUCCESS
- Upload PR CI metadata: SUCCESS
- build-wasm: SKIPPED
- build-wasm (web): SUCCESS
- build-next / build: SUCCESS
- build-wasm (nodejs): SUCCESS
- stable - ${{ matrix.target }} - node@20: SKIPPED
- stable - x86_64-unknown-linux-gnu - node@20: SUCCESS
- validate-docs-links: SUCCESS
- Prepare preview tarball: SKIPPED
- Prepare preview tarball: SUCCESS
- build-native / build: SUCCESS
- Potentially publish release: SKIPPED
- Potentially publish release: SKIPPED
- build-native-windows / build: SUCCESS
- thank you, build: SKIPPED
- thank you, build: SUCCESS
- fetch test timings: SUCCESS
- Upload Turbopack Bytesize metrics to Datadog: SKIPPED
- Upload Turbopack Bytesize metrics to Datadog: SKIPPED
- test devlow package / build: SUCCESS
- report publish failure to slack: SKIPPED
- report publish failure to slack: SKIPPED
- Wait for preview tarball: SUCCESS
- lint / build: SUCCESS
- test cargo unit / build: SUCCESS
- test cargo benches / Test: SUCCESS
- rust check / build: SUCCESS
- rustdoc check / build: SUCCESS
- ast-grep lint: SUCCESS
- test next-swc wasm / build: SUCCESS
- test next-swc wasi: SKIPPED
- types and precompiled / build: SUCCESS
- Run devlow benchmarks: SKIPPED
- test unit (20) / build: SUCCESS
- test unit (22) / build: SUCCESS
- test next-config-ts-native-ts dev (22) / build: SUCCESS
- test next-config-ts-native-ts dev (24.15.0) / build: SUCCESS
- test next-config-ts-native-ts prod (22) / build: SUCCESS
- test next-config-ts-native-ts prod (24.15.0) / build: SUCCESS
- Test new and changed tests for flakes (dev) (1/5) / build: SUCCESS
- Test new and changed tests for flakes (dev) (2/5) / build: SUCCESS
- Test new and changed tests for flakes (dev) (3/5) / build: SUCCESS
- Test new and changed tests for flakes (dev) (4/5) / build: SUCCESS
- Test new and changed tests for flakes (dev) (5/5) / build: SUCCESS
- Test new and changed tests for flakes (prod) (1/5) / build: SUCCESS
- Test new and changed tests for flakes (prod) (2/5) / build: SUCCESS
- Test new and changed tests for flakes (prod) (3/5) / build: SUCCESS
- Test new and changed tests for flakes (prod) (4/5) / build: SUCCESS
- Test new and changed tests for flakes (prod) (5/5) / build: SUCCESS
- test firefox and safari / build: SUCCESS
- test unit windows (20) / build: SUCCESS
- test unit windows (22) / build: SUCCESS
- test dev windows / build: SUCCESS
- test integration windows / build: SUCCESS
- test prod windows / build: SUCCESS
- test turbopack dev (1/7) / build: SUCCESS
- test turbopack dev (2/7) / build: SUCCESS
- test turbopack dev (3/7) / build: SUCCESS
- test turbopack dev (4/7) / build: SUCCESS
- test turbopack dev (5/7) / build: SUCCESS
- test turbopack dev (6/7) / build: SUCCESS
- test turbopack dev (7/7) / build: SUCCESS
- test turbopack production (1/7) / build: SUCCESS
- test turbopack production (2/7) / build: SUCCESS
- test turbopack production (3/7) / build: SUCCESS
- test turbopack production (4/7) / build: SUCCESS
- test turbopack production (5/7) / build: SUCCESS
- test turbopack production (6/7) / build: SUCCESS
- test turbopack production (7/7) / build: SUCCESS
- test rspack dev: SKIPPED
- test rspack production: SKIPPED
- test dev (1/10) / build: SUCCESS
- test dev (2/10) / build: SUCCESS
- test dev (3/10) / build: SUCCESS
- test dev (4/10) / build: SUCCESS
- test dev (5/10) / build: SUCCESS
- test dev (6/10) / build: SUCCESS
- test dev (7/10) / build: SUCCESS
- test dev (8/10) / build: SUCCESS
- test dev (9/10) / build: SUCCESS
- test dev (10/10) / build: SUCCESS
- test prod (1/10) / build: SUCCESS
- test prod (2/10) / build: SUCCESS
- test prod (3/10) / build: SUCCESS
- test prod (4/10) / build: SUCCESS
- test prod (5/10) / build: SUCCESS
- test prod (6/10) / build: SUCCESS
- test prod (7/10) / build: SUCCESS
- test prod (8/10) / build: SUCCESS
- test prod (9/10) / build: SUCCESS
- test prod (10/10) / build: SUCCESS
- test cache components dev (1/6) / build: SUCCESS
- test cache components dev (2/6) / build: SUCCESS
- test cache components dev (3/6) / build: SUCCESS
- test cache components dev (4/6) / build: SUCCESS
- test cache components dev (5/6) / build: SUCCESS
- test cache components dev (6/6) / build: SUCCESS
- test cache components prod (1/7) / build: SUCCESS
- test cache components prod (2/7) / build: SUCCESS
- test cache components prod (3/7) / build: SUCCESS
- test cache components prod (4/7) / build: SUCCESS
- test cache components prod (5/7) / build: SUCCESS
- test cache components prod (6/7) / build: SUCCESS
- test cache components prod (7/7) / build: SUCCESS
- Test new and changed tests when deployed (1/5) / build: SUCCESS
- Test new and changed tests when deployed (2/5) / build: SUCCESS
- Test new and changed tests when deployed (3/5) / build: SUCCESS
- Test new and changed tests when deployed (4/5) / build: SUCCESS
- Test new and changed tests when deployed (5/5) / build: SUCCESS
- Test new and changed tests when deployed (cache components) (1/5) / build: SUCCESS
- Test new and changed tests when deployed (cache components) (2/5) / build: SUCCESS
- Test new and changed tests when deployed (cache components) (3/5) / build: SUCCESS
- Test new and changed tests when deployed (cache components) (4/5) / build: SUCCESS
- Test new and changed tests when deployed (cache components) (5/5) / build: SUCCESS
- thank you, next: SUCCESS
- Socket Security: Project Report: SUCCESS
- Vercel Agent Review: SUCCESS
- Vercel – Code Owners: SUCCESS
- Docs Link Validation: SUCCESS

## Changed files

- `crates/next-api/src/nft.rs`: +93/-6
- `test/e2e/app-dir/webpack-loader-fs/app/glob-target/inner/path/one.txt`: +1/-0
- `test/e2e/app-dir/webpack-loader-fs/app/path/to/symlink`: +1/-0
- `test/e2e/app-dir/webpack-loader-fs/test-file-loader.js`: +10/-1
- `test/e2e/app-dir/webpack-loader-fs/webpack-loader-fs.test.ts`: +1/-1
- `test/production/build-trace-extra-entries-turbo/build-trace-extra-entries-turbo.test.ts`: +18/-2
- `turbopack/crates/turbo-tasks-fs/examples/hash_glob.rs`: +3/-0
- `turbopack/crates/turbo-tasks-fs/src/disk.rs`: +110/-2
- `turbopack/crates/turbo-tasks-fs/src/read_glob.rs`: +192/-24
- `turbopack/crates/turbopack-core/src/resolve/pattern.rs`: +77/-6
- `turbopack/crates/turbopack-ecmascript/src/references/import_meta_glob.rs`: +8/-4
- `turbopack/crates/turbopack-tests/tests/execution/turbopack/resolving/import-meta-glob/input/index.js`: +12/-0
- `turbopack/crates/turbopack-tests/tests/execution/turbopack/resolving/import-meta-glob/input/linked`: +1/-0
