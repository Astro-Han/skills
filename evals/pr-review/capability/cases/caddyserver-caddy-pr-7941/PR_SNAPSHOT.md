# Frozen pull request snapshot

- PR: https://github.com/caddyserver/caddy/pull/7941 — `caddyhttp: fix url_pattern authorization bypass via encoded-slash traversal`
- Author: dunglas
- Target base head: `50e54ee279aa1e504fe218ca49ab6ae16c100410`
- Comparison base: `50e54ee279aa1e504fe218ca49ab6ae16c100410`
- Exact source head: `9355e8b2bbf6c2cebff7e05cd4202a2ed4d96d0c`
- Diff: 86 additions, 4 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Advisory: [GHSA-m8m5-v4jf-3wcm](https://github.com/caddyserver/caddy/security/advisories/GHSA-m8m5-v4jf-3wcm)
Reported by [@z3k0sec](https://github.com/z3k0sec).

## Affected versions

No released version is affected. `url_pattern` support was added in #7787 and has not been part of a tagged release; the bug only exists on `master`.

## Problem

The `http.matchers.url_pattern` matcher evaluated the raw, percent-encoded request URI (`r.URL.RequestURI()`), while every path-consuming handler resolves the decoded, cleaned `r.URL.Path`. An encoded-slash payload like `..%2f` stays a single opaque segment for the WHATWG `URLPattern` parser, so:

- `/public/..%2fadmin/secret` **matches** an allow-list pattern of `/public/*`
- handlers decode `%2f` to `/` and resolve `/admin/secret`

Matcher and handler ran two different path models on the same request, so any route ACL built with `url_pattern` could be bypassed by an unauthenticated request (`file_server`, `reverse_proxy`, `php_fastcgi`, internal routes).

The classic `path` matcher is unaffected; it already compares the cleaned, decoded path (#4407).

## Fix

Match against the same path model the handlers resolve:

1. decode via `r.URL.Path`
2. `normalizeWindowsPath` + `CleanPath` (collapses `..` and, per the pattern, doubled slashes, mirroring `MatchPath`)
3. re-encode through `url.URL` to a canonical escaped form before `Exec`

`mergeSlashes` is derived once in `Provision` from the pattern's path part, matching the path matcher's `//` rule.

The `github.com/dunglas/go-urlpattern` library is spec-correct: keeping `%2F` encoded is required by RFC 3986 and matches browser `URLPattern` behavior. The defect is in the integration, so the fix stays in Caddy. This PR also bumps go-urlpattern from its pseudo-version to the first tagged release, `v1.0.0`.

## Tests

Added regression cases: encoded-slash (`..%2f`, `..%2F`), encoded dots (`%2e%2e`), raw dots (`../`), positive re-match on the real decoded target, slash collapsing, empty-segment preservation, and encoded-character decode. Verified against the advisory's live reproduction: all three payloads now return `403`, control paths still serve.

## Assistance Disclosure

Patched by Claude, reviewed by me.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

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
- test (s390x on IBM Z): SKIPPED
- govulncheck: SUCCESS
- goreleaser-check: SKIPPED
- dependency-review: SUCCESS
- Scorecard: NEUTRAL

## Changed files

- `go.mod`: +1/-1
- `go.sum`: +2/-2
- `modules/caddyhttp/urlpatternmatcher.go`: +27/-1
- `modules/caddyhttp/urlpatternmatcher_test.go`: +56/-0
