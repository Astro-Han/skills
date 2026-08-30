# Frozen pull request snapshot

- PR: https://github.com/caddyserver/caddy/pull/7809 — `caddyhttp: restore allow_underscore_in_headers server option`
- Author: bluegate-studio
- Target base head: `55b3397a2da2af0a8d567b63460af1be8e6820a7`
- Comparison base: `55b3397a2da2af0a8d567b63460af1be8e6820a7`
- Exact source head: `7f2024df34402501bd2ec1a617becc44cded6faf`
- Diff: 606 additions, 26 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Ref: #7808

This restores the `allow_underscore_in_headers` opt-in flag that was implemented and tested in `3eb8e48` but removed before merge.

## What it does

Adds a boolean `allow_underscore_in_headers` global server option. When set, incoming HTTP request headers containing underscores are preserved instead of being dropped. When unset (the default), the v2.11.4 drop behaviour is unchanged.

```caddyfile
{
    servers {
        allow_underscore_in_headers
    }
}
```

## What it doesn't do

- Does **not** change the default behaviour — underscore headers are still dropped unless the operator explicitly opts in.
- Does **not** weaken the security posture for any deployment that doesn't set the flag.
- Does **not** introduce new dependencies, new packages, or new test infrastructure.

## Why

Some deployments use underscore-named headers with backends that have no CGI/FastCGI ambiguity (Bun, Deno, Node, Go's own `net/http`). For those, the drop is a breaking change with no migration path — especially when immutable clients (deployed mobile apps) cannot be updated to use hyphenated names.

NGINX solves this identically: `underscores_in_headers off` by default, `on` as an explicit opt-in.

## Implementation

Follows the exact pattern of `enable_full_duplex`:

| File | Change |
|------|--------|
| `modules/caddyhttp/server.go` | `AllowUnderscoreInHeaders bool` field on `Server` struct; gate the drop loop |
| `caddyconfig/httpcaddyfile/serveroptions.go` | Field on `serverOptions` struct; Caddyfile parsing; wiring in `applyServerOptions` |

2 files changed, +24 / −5. The existing tests (drop, debug log, RFC-7230 space rejection, fastcgi replacer, forward_auth integration) all pass — the default path is unaffected.

## Testing

- `go test -race -short ./...` — all packages pass
- Deployed and verified in a production environment serving multiple backends

## Assistance Disclosure

AI-assisted (Opus 4.6). Used for code search and pattern matching against existing conventions. All code drafted, written, reviewed, and tested by the human operator.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Track Maintainer Approvals: SKIPPED
- Track Maintainer Approvals: SKIPPED
- Track Maintainer Approvals: SKIPPED
- Track Maintainer Approvals: SKIPPED
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
- Handle PR Closed Without Tag: SKIPPED
- Handle PR Closed Without Tag: SKIPPED
- Handle PR Closed Without Tag: SKIPPED
- Handle PR Closed Without Tag: SKIPPED
- test (s390x on IBM Z): SKIPPED
- govulncheck: SUCCESS
- goreleaser-check: SKIPPED
- dependency-review: SUCCESS
- Scorecard: NEUTRAL
- unnamed: SUCCESS

## Changed files

- `caddyconfig/httpcaddyfile/serveroptions.go`: +30/-21
- `modules/caddyhttp/app.go`: +5/-0
- `modules/caddyhttp/server.go`: +144/-5
- `modules/caddyhttp/server_test.go`: +427/-0
