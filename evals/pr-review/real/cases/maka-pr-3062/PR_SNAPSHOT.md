# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3062 — `refactor: retire Gemini CLI account preview`
- Author: Astro-Han
- Target base head: `820a47b90ff052a726997819539fc382efa31ace`
- Comparison base: `820a47b90ff052a726997819539fc382efa31ace`
- Exact source head: `06f1f908f7425d043ab6e768e42abfc608248b50`
- Diff: 219 additions, 871 deletions, 42 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

- remove the non-executable `gemini-cli` provider from Core, generated metadata, Desktop settings, preload, and OAuth IPC
- remove the provider-wide preview/unavailable adapter contract that lost its only consumer; every maintained OAuth provider now uses the normal executable auth and readiness paths
- reject new Gemini CLI account connections while preserving the ordinary `google` Gemini API-key provider
- filter legacy persisted `gemini-cli` entries from the active connection catalog and clear a retired default target; the next catalog mutation writes the maintained set
- preserve retired connection identities during migration so duplicate ids or slugs still fail closed before credential resolution
- update current credential-boundary documentation while retaining historical/upstream-only references

Fixes #3054

## Verification

- `node --test packages/storage/dist/__tests__/runtime-policy-stores.test.js` — 41 passed
- focused Core suites for codecs, auth, readiness, onboarding, and task submission — 39 passed
- focused Runtime provider/conformance suites — 152 passed
- focused Desktop readiness and model-catalog suites — 22 passed
- `npm run typecheck --workspace=@maka/core`
- `npm run typecheck --workspace=@maka/runtime`
- `npm run typecheck --workspace=@maka/runtime-host`
- `npm run typecheck --workspace=@maka/desktop`
- Biome check on all 24 files in the follow-up simplification commit
- `git diff --check`

The create-boundary test failed before removal because `gemini-cli` was still registered. The duplicate-identity migration test then failed before the follow-up fix because retired records were filtered before uniqueness validation.

## Migration

Older `connection-catalog.json` files may contain a `gemini-cli` entry. Reads validate its persisted id and slug, preserve catalog-wide identity uniqueness, omit the retired entry from the active snapshot, and clear the default target only when it referenced the retired connection. The raw file remains recoverable until the next catalog mutation writes the canonical supported set.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No

## AI assistance

Codex implemented the change, added the focused tests, and ran the checks listed above. Three independent AI reviewers performed adversarial deletion, migration, and holistic architecture reviews; Codex reproduced and fixed the concrete identity-collision finding and removed the now-unneeded preview contract. The human contributor approved the retirement decision and will review the final diff and commit messages before merge.


## Linked issues

### https://github.com/apache/maka/issues/3054 — Retire the Gemini CLI / Antigravity preview

## Problem

Maka still maintains a Gemini CLI / Antigravity account-provider surface that has never been executable. The provider has no Runtime OAuth enrollment contract or runnable adapter, and Desktop only retains disabled IPC, preload, copy, metadata, and compatibility branches.

The project has decided to retire this preview instead of completing it.

## Scope

- Remove `gemini-cli` from the maintained provider registry and generated metadata.
- Remove the Antigravity Desktop IPC, preload bridge, typed contract, settings branches, fixtures, and current documentation.
- Reject creation of new `gemini-cli` connections.
- Retire legacy persisted `gemini-cli` entries without preventing the remaining connection catalog from loading; clear the default target when it referenced a retired entry.
- Preserve the ordinary `google` Gemini API-key provider unchanged.

## Acceptance criteria

- [ ] `gemini-cli` is no longer a supported provider type.
- [ ] No Antigravity login or disabled preview bridge remains in current product surfaces.
- [ ] A legacy persisted entry cannot block supported connections from loading.
- [ ] The ordinary Google Gemini API-key path remains available.
- [ ] Focused tests, affected typechecks, and formatting checks pass.

## Non-goals

- Changing the ordinary Google Gemini API-key provider.
- Adding a replacement Google account OAuth integration.
- Removing historical references that only document upstream Gemini CLI behavior or archived architecture.

---

*This issue was identified and updated with AI assistance (Codex). A human contributor reviewed the decision and owns the submission.*

## Exact-head checks

- request-review: SKIPPED
- changes: SUCCESS
- request-review: SUCCESS
- changes: SUCCESS
- windows_recovery: SUCCESS
- typecheck: SUCCESS
- windows_baseline (non-blocking): SUCCESS
- test_workspaces: SUCCESS
- test_runtime_host: SUCCESS
- e2e: SUCCESS
- storybook: SUCCESS
- test: SUCCESS
- unnamed: SUCCESS

## Changed files

- `README.md`: +1/-1
- `README.zh-CN.md`: +1/-1
- `SECURITY.md`: +2/-2
- `apps/desktop/src/main/__tests__/runtime-host-oauth-ipc-main.test.ts`: +0/-12
- `apps/desktop/src/main/chat-readiness.ts`: +0/-2
- `apps/desktop/src/main/runtime-host-oauth-ipc-main.ts`: +0/-30
- `apps/desktop/src/preload/bridge-contract.d.ts`: +0/-20
- `apps/desktop/src/preload/preload.ts`: +3/-37
- `apps/desktop/src/renderer/locales/conversation-copy.ts`: +0/-4
- `apps/desktop/src/renderer/locales/settings-provider-copy.ts`: +8/-12
- `apps/desktop/src/renderer/model-catalog-choices.ts`: +0/-4
- `apps/desktop/src/renderer/settings/provider-add-form.tsx`: +3/-7
- `apps/desktop/src/renderer/settings/provider-brand-marks.tsx`: +0/-1
- `apps/desktop/src/renderer/settings/provider-connection-detail.tsx`: +1/-3
- `apps/desktop/src/renderer/settings/provider-display-copy.ts`: +0/-4
- `apps/desktop/src/renderer/settings/use-connection-detail.ts`: +4/-14
- `apps/desktop/src/renderer/settings/use-oauth-login-flow.ts`: +1/-2
- `apps/desktop/stories/settings/provider-settings.stories.tsx`: +0/-4
- `packages/core/src/__tests__/onboarding.test.ts`: +1/-1
- `packages/core/src/__tests__/provider-auth.test.ts`: +3/-23
- `packages/core/src/__tests__/runtime-policy-codec.test.ts`: +17/-0
- `packages/core/src/chat-model-choice.ts`: +1/-8
- `packages/core/src/connection-error-copy.ts`: +0/-2
- `packages/core/src/connection-readiness.ts`: +7/-16
- `packages/core/src/llm-connections.ts`: +0/-2
- `packages/core/src/model-metadata.generated.ts`: +0/-552
- `packages/core/src/model-metadata.ts`: +0/-7
- `packages/core/src/model-web-search.ts`: +0/-2
- `packages/core/src/onboarding.ts`: +0/-1
- `packages/core/src/provider-auth.ts`: +15/-42
- `packages/core/src/provider-contract-matrix.ts`: +1/-1
- `packages/core/src/provider-registry.ts`: +1/-27
- `packages/core/src/task-submission-readiness.ts`: +0/-1
- `packages/runtime-host/src/server/execution-model-authority.ts`: +1/-1
- `packages/runtime/src/__tests__/responses-wire-contract.test.ts`: +0/-1
- `packages/runtime/src/model-factory.ts`: +0/-3
- `packages/runtime/src/model-runtime.ts`: +1/-5
- `packages/runtime/src/test-connection.ts`: +0/-2
- `packages/storage/src/__tests__/runtime-policy-stores.test.ts`: +106/-7
- `packages/storage/src/runtime-policy/connection-catalog-document.ts`: +40/-4
- `packages/ui/src/chat-model-helpers.ts`: +1/-1
- `scripts/sync-model-metadata.mjs`: +0/-2
