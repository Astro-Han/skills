# Frozen pull request snapshot

- PR: https://github.com/caddyserver/caddy/pull/7826 — `tracing: fix BatchSpanProcessor goroutine leak on config reload`
- Author: Dean2026
- Target base head: `d2e0ad1e92329d841a3a12e9ec7935afb30ce246`
- Comparison base: `d2e0ad1e92329d841a3a12e9ec7935afb30ce246`
- Exact source head: `16709990f5cb7de802bde301073a051d6fb453a0`
- Diff: 98 additions, 18 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

tracing: fix BatchSpanProcessor goroutine leak on config reload

## Description

When the `tracing` directive is enabled, each config reload leaks one
`go.opentelemetry.io/otel/sdk/trace.(*batchSpanProcessor).processQueue`
goroutine. On a server that reloads frequently (e.g. polling a remote
config source every few seconds) this accumulates into tens of thousands
of leaked goroutines over time.

A goroutine dump shows many identical stacks:

```
goroutine ... [select]:
go.opentelemetry.io/otel/sdk/trace.(*batchSpanProcessor).processQueue(...)
	.../sdk/trace/batch_span_processor.go:327
go.opentelemetry.io/otel/sdk/trace.NewBatchSpanProcessor.func2()
	.../sdk/trace/batch_span_processor.go:129
created by go.opentelemetry.io/otel/sdk/trace.NewBatchSpanProcessor
	.../sdk/trace/batch_span_processor.go:127
```

## Root cause

`tracing` keeps a global, reference-counted `TracerProvider` so it can be
reused across reloads (`tracerProvider.getTracerProvider`). Caddy reloads
provision the new config *before* cleaning up the old one, so the counter
never drops to 0 and the provider is correctly reused — `Shutdown` is
never called, by design.

The problem is on the caller side in `newOpenTelemetryWrapper`:

```go
traceExporter, err := autoexport.NewSpanExporter(ctx)
...
tracerProvider := globalTracerProvider.getTracerProvider(
    sdktrace.WithBatcher(traceExporter),   // evaluated on every reload
    sdktrace.WithResource(res),
)
```

`sdktrace.WithBatcher(e)` is `WithSpanProcessor(NewBatchSpanProcessor(e))`,
and `NewBatchSpanProcessor` **starts its `processQueue` goroutine eagerly at
construction time** — not when the option is applied. The option is built
on every `Provision` (every reload), but `getTracerProvider` only applies
it when it actually creates a new provider (`t.tracerProvider == nil`). On
the reuse path the option is silently discarded, so the just-started
BatchSpanProcessor goroutine is orphaned: it is never registered with any
provider and therefore never shut down. Result: one leaked goroutine (plus
a leaked exporter) per reload.

## Fix

Defer construction of the exporter/batcher until a new provider is actually
needed. `getTracerProvider` now takes a `buildOpts` factory that is invoked
only on the create path, so nothing with a side effect is built on the
reuse path.

The reference counter is now incremented only after the provider is
successfully obtained, preserving the previous semantics where a failed
exporter creation did not affect the counter.

## Testing

- `Test_tracersProvider_buildOptsOnlyOnCreate` — asserts `buildOpts` runs
  exactly once across one create + five reuses (the regression guard).
- `Test_tracersProvider_buildOptsError` — asserts that on a build error the
  provider stays nil and the counter is not incremented.
- Existing tracing tests updated for the new signature and still pass.

Verified manually with a reload loop: before the fix, 50 reloads leaked 50
`processQueue` goroutines; after the fix, 0 are leaked while the provider is
still reused (counter stays at 1).

----

🤖 AI Disclosure: Claude Opus 4.8 was used to generate the patch, and verified at the staging deployment.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Track Maintainer Approvals: SKIPPED
- Track Maintainer Approvals: SKIPPED
- build (aix, 1.26): SUCCESS
- lint (linux): SUCCESS
- Scorecard analysis: SUCCESS
- test (linux, 1.26): SUCCESS
- build (linux, 1.26): SUCCESS
- lint (mac): SUCCESS
- test (mac, 1.26): SUCCESS
- build (solaris, 1.26): SUCCESS
- lint (windows): SUCCESS
- test (windows, 1.26): SUCCESS
- build (illumos, 1.26): SUCCESS
- build (dragonfly, 1.26): SUCCESS
- build (freebsd, 1.26): SUCCESS
- build (openbsd, 1.26): SUCCESS
- build (windows, 1.26): SUCCESS
- build (darwin, 1.26): SUCCESS
- build (netbsd, 1.26): SUCCESS
- Handle PR Closed Without Tag: SKIPPED
- Handle PR Closed Without Tag: SKIPPED
- test (s390x on IBM Z): SKIPPED
- govulncheck: SUCCESS
- goreleaser-check: SKIPPED
- dependency-review: SUCCESS
- Scorecard: NEUTRAL
- unnamed: SUCCESS

## Changed files

- `modules/caddyhttp/tracing/tracer.go`: +19/-9
- `modules/caddyhttp/tracing/tracerprovider.go`: +15/-5
- `modules/caddyhttp/tracing/tracerprovider_test.go`: +64/-4
