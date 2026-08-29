# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/2965 — `chore(runtime): retire the Claude subscription OAuth path`
- Author: Joob1n
- Target base head: `26817cb7b671c52b83d2d9cffad4e4627bbf6121`
- Comparison base: `d29569d250e92a124eb9e6544501a28b7c821c5a`
- Exact source head: `7c6cc8e5bdeafc1a8152621adec19bd1d859b366`
- Diff: 558 additions, 2509 deletions, 60 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

The Claude subscription path authenticated as the Claude Code client and
shaped every request to look like that client: its `client_id`, its
`User-Agent`, a `You are Claude Code` system block injected ahead of the
caller's own prompt, and a synthesized `x-anthropic-billing-header`. The
module that assembled it was named for what it did —
`subscription-cloaked-request`.

Removed, in the order a request met them:

| Removed | Effect |
|---|---|
| OAuth login contract | No authorize URL carries that client id |
| Login provider in the wire enum | A Client asking to start one is refused by the protocol, not a later guard |
| Paste-code presentation flow | Served no other provider |
| `subscription-cloaked-request.ts` | The request cloak itself |
| `claudeSubscriptionHeaders` | The user agent and `claude-code-*` betas |
| `claude-subscription-usage.ts` | Read quota under the same identity |
| Runtime adapter (now `unavailable`) | No Session can send with it, and the pickers filter it out of selection |
| Credential refresh | A stored token is inert |

`connection.test` also stopped reporting a resolved token as a verified
connection. That shortcut is why a workspace could show "Claude OAuth 已登录"
on a connection that could not answer a single turn.

Callers keep Claude models through an Anthropic API key connection.

## Why the provider type stays registered

`connection-catalog.json` decodes its connections with a plain `map`, and
`decodeProviderType` throws on an unregistered type. Removing the type would
therefore not skip one entry — it would fail the whole document, and a
workspace that ever signed in would lose **every other connection with it**
(API keys, Codex, Copilot).

So the type stays registered and unwired. `gemini-cli` already models exactly
this shape: registered, `runtimeAdapter: unavailable`, not offered as a usable
model.

The settings row stays for the same reason, now carrying what happened and
where to go instead. A row that simply disappears leaves an affected user to
work out on their own why their model stopped answering — which is the failure
mode this change is trying not to create.

## Verification

`lint`, `format:check`, `build`, `typecheck`, `knip` (desktop + ui) and
`astryx:theme` pass.

| suite | result |
|---|---|
| `@maka/core` | 538 / 538 |
| `@maka/storage` | 769 / 769 |
| `@maka/runtime-host` | 890 / 890 |
| `@maka/desktop` | 790 / 790 |
| `@maka/runtime` | 2769 pass, 5 fail |

Those 5 runtime failures are file-tool path containment and Grep sandbox
tests. I ran the suite on this branch and on a clean tree and diffed the
failing test names: **identical sets, no new failure**.

That diff earned its keep. A first pass showed one extra failure —
`OpenCode connection probes follow each selected model protocol` — because
removing the `claude-subscription` case from `testConnectionModel` had also
taken the `anthropic` case's return statement, silently routing every
Anthropic API key connection test at `/chat/completions`. Fixed here.

Tests whose subject was the removed behavior are gone (the cloak shape, the
always-verified test shortcut, the paste-code presentation). Tests that used
this provider only as a convenient OAuth fixture now run on `openai-codex`.
One in `provider-auth` was dropped outright: it asserted the behavior of a
wired OAuth provider with fallback-only discovery, and after this change the
registry has no such provider.

## Retirement is now an explicit registry fact

A retired provider and an unwired preview provider look identical from
`runtimeAdapter: 'unavailable'`, but only one of them was ever available to a
user. The registry entry carries `retired: true` and `isRetiredProvider()`
reads it, so the connection detail page and `deriveProviderAuthContract` can
tell "this was taken away" from "this has not arrived yet". Without it the
detail page told these users to go reauthorize — an instruction whose only
destination is the retirement notice — and the auth sheet read
`账号登录预览`.

`ProviderAuthState` gains `retired` and `ProviderAuthSetupMode` gains
`oauth_retired`. Both are exhaustively switched, so the compiler named every
surface that had to answer for the new state.

## Compatibility

`RUNTIME_HOST_COMPATIBILITY_EPOCH` goes 19 → 20. Narrowing
`OAUTH_LOGIN_PROVIDERS` is a decode change in the new-Client-against-old-Host
direction — a `claude-subscription` projection from an older Host now throws
`invalidProtocolFrame` where it used to decode. This repo bumps for that class
(#2633, #2625).

`oauth.account.usage.fetch` stays on the wire and answers
`unsupported_provider` unconditionally, reading no state. The
`request_authorization_code` presentation chain is unreachable after the epoch
bump but is left in place; removing it is a second protocol narrowing and is
clearer as its own change.

## Testing

Each line that enforces the retirement is pinned by an assertion that was
mutation-checked against the revert it is meant to catch:

| Pinned | Reverting it |
|---|---|
| `runtimeAdapter.kind === 'unavailable'`, `isWiredOAuthProvider === false` | `provider-catalog-contract` fails |
| `retired: true` on the registry entry | `provider-catalog-contract` fails |
| A retired connection cannot begin an interactive login | `runtime-policy-stores` fails once both gates are removed |
| `oauth.account.usage.fetch`'s constant reason | `oauth-coordinator` fails |
| Commit excludes overlapping backend activations | `oauth-coordinator` fails |

The last one is re-landed from the Claude fixture this PR removed — what it
asserts is provider-agnostic (`oauth-coordinator.ts` wraps every commit in
`#activation.runMutation`), so it now runs on Codex.

Note on the storage row: removing `'claude-subscription'` from
`isInteractiveOAuthLoginProvider` *alone* leaves the suite green, because
`deriveProviderAuthContract` now refuses independently. The assertion pins the
end-to-end verdict rather than either gate.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck, the full test suite and the Storybook smoke pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- changes: SUCCESS
- audit: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS

## Changed files

- `README.md`: +1/-1
- `README.zh-CN.md`: +1/-1
- `SECURITY.md`: +11/-8
- `apps/desktop/src/main/__tests__/chat-readiness.test.ts`: +4/-4
- `apps/desktop/src/main/__tests__/runtime-host-oauth-ipc-main.test.ts`: +9/-14
- `apps/desktop/src/main/oauth-connection-identities.ts`: +0/-1
- `apps/desktop/src/main/runtime-host-oauth-ipc-main.ts`: +0/-16
- `apps/desktop/src/preload/bridge-contract.d.ts`: +0/-14
- `apps/desktop/src/preload/preload.ts`: +6/-47
- `apps/desktop/src/renderer/locales/settings-provider-copy.ts`: +18/-38
- `apps/desktop/src/renderer/settings/claude-subscription-card.tsx`: +9/-482
- `apps/desktop/src/renderer/settings/provider-connection-detail.tsx`: +4/-1
- `apps/desktop/src/renderer/settings/provider-oauth-section.tsx`: +45/-43
- `apps/desktop/src/renderer/settings/use-connection-detail.ts`: +14/-6
- `apps/desktop/stories/settings/provider-settings.stories.tsx`: +7/-16
- `apps/desktop/stories/settings/settings-pages.stories.tsx`: +2/-10
- `docs/astryx-surface-file-inventory.md`: +1/-1
- `packages/core/src/__tests__/oauth-subscription.test.ts`: +1/-92
- `packages/core/src/__tests__/onboarding.test.ts`: +2/-2
- `packages/core/src/__tests__/provider-auth.test.ts`: +1/-21
- `packages/core/src/__tests__/provider-catalog-contract.test.ts`: +54/-1
- `packages/core/src/llm-connections.ts`: +2/-0
- `packages/core/src/oauth-subscription.ts`: +16/-115
- `packages/core/src/provider-auth.ts`: +43/-1
- `packages/core/src/provider-contract-matrix.ts`: +1/-1
- `packages/core/src/provider-registry.ts`: +27/-6
- `packages/runtime-host/src/__tests__/execution-model-composition.test.ts`: +17/-28
- `packages/runtime-host/src/__tests__/oauth-coordinator.test.ts`: +112/-224
- `packages/runtime-host/src/__tests__/oauth-execution-authority.test.ts`: +23/-173
- `packages/runtime-host/src/__tests__/oauth-protocol.test.ts`: +3/-3
- `packages/runtime-host/src/__tests__/oauth-two-client-uds.test.ts`: +19/-11
- `packages/runtime-host/src/protocol/index.ts`: +1/-1
- `packages/runtime-host/src/protocol/oauth.ts`: +1/-1
- `packages/runtime-host/src/server/execution-composition.ts`: +0/-5
- `packages/runtime-host/src/server/execution-model-authority.ts`: +0/-6
- `packages/runtime-host/src/server/execution-model-composition.ts`: +0/-3
- `packages/runtime-host/src/server/oauth-coordinator.ts`: +17/-142
- `packages/runtime-host/src/server/oauth-execution-authority.ts`: +0/-19
- `packages/runtime/package.json`: +0/-1
- `packages/runtime/src/__tests__/claude-subscription-runtime.test.ts`: +0/-29
- `packages/runtime/src/__tests__/claude-subscription-usage.test.ts`: +0/-30
- `packages/runtime/src/__tests__/oauth-login.test.ts`: +31/-124
- `packages/runtime/src/__tests__/subscription-credentials.test.ts`: +24/-24
- `packages/runtime/src/__tests__/subscription-model-fetch.test.ts`: +0/-85
- `packages/runtime/src/claude-subscription-usage.ts`: +0/-64
- `packages/runtime/src/codex-oauth-enrollment.ts`: +1/-1
- `packages/runtime/src/model-factory.ts`: +2/-11
- `packages/runtime/src/model-fetcher.ts`: +3/-16
- `packages/runtime/src/model-runtime.ts`: +0/-1
- `packages/runtime/src/oauth-login.ts`: +0/-248
- `packages/runtime/src/oauth-provider-contracts.ts`: +1/-16
- `packages/runtime/src/subscription-auth.ts`: +0/-13
- `packages/runtime/src/subscription-cloaked-request.ts`: +0/-143
- `packages/runtime/src/subscription-credentials.ts`: +2/-41
- `packages/runtime/src/subscription-model-fetch.ts`: +0/-71
- `packages/runtime/src/test-connection.ts`: +5/-25
- `packages/runtime/src/xai-oauth-enrollment.ts`: +1/-1
- `packages/storage/src/__tests__/runtime-policy-stores.test.ts`: +14/-1
- `packages/storage/src/runtime-policy/coordinator.ts`: +1/-5
- `packages/storage/src/runtime-policy/operations.ts`: +1/-1
