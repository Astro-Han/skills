# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3958 — `fix(runtime): avoid OpenAI tool_search name collision`
- Author: liugddx
- Target base head: `4b745fc56734ef3e80cf45d318c12af288cfff63`
- Comparison base: `4b745fc56734ef3e80cf45d318c12af288cfff63`
- Exact source head: `166204c59e10d3ecfe7047a52d1cbab5bf7007f2`
- Diff: 304 additions, 8 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

Fixes #3939

Maka's deferred-tool connector keeps the internal name `tool_search`, but the provider-bound OpenAI Responses request uses the collision-free alias `maka_tool_search`. Provider-facing system text, replayed tool call/result names, repair callbacks, and streamed provider tool results are mapped consistently at the adapter boundary. The alias is reserved so a real tool cannot shadow it.

## Verification

- `npm --workspace @maka/core run build`
- `npm --workspace @maka/storage run build`
- `npm --workspace @maka/mcp run build`
- `npm --workspace @maka/computer-use run build`
- `npm --workspace @maka/runtime run build`
- `node --test "packages/runtime/dist/__tests__/deferred-tools-wire.test.js" "packages/runtime/dist/__tests__/responses-wire-contract.test.js"` (20 passed)
- Biome format/check passed for all changed files

The Responses wire regression uses the real `openai-codex` / `gpt-5.6-sol` adapter and `@ai-sdk/openai` converter. It proves the historical `{ activated: [...] }` result is sent as a generic function output under `maka_tool_search`, and that provider tool calls/results map back to Maka's internal `tool_search` identity.

## Review focus

The provider alias is a transport-only projection. Runtime persistence, UI copy, activation payloads, and existing history remain on the internal name. A real `maka_tool_search` tool is rejected at catalog construction to preserve bijective mapping.

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: Codex authored the implementation, tests, and review follow-up; the human contributor reviewed the changes and owns the submission.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — provider-bound tool naming changes to avoid an SDK reserved-name collision; internal behavior is unchanged.
- [ ] No


## Linked issues

### https://github.com/apache/maka/issues/3939 — Runtime tool_search conflicts with OpenAI Responses native tool_search

## Summary

Maka's runtime-defined deferred-tool connector is named `tool_search`. When a session uses an OpenAI Responses model (for example `codex-subscription` / `gpt-5.6-sol`), the current `@ai-sdk/openai` adapter treats that name as the provider-native `openai.tool_search` tool.

Maka returns a client tool result shaped like:

```json
{"activated":["mcp__desktop_browser__browser_click"]}
```

The OpenAI Responses adapter validates native `tool_search` output as:

```json
{"tools":[...]}
```

and rejects the Maka result before the next model request is sent.

## Reproduction

1. Run the latest `main` desktop app on Windows.
2. Use the `codex-subscription` connection with `gpt-5.6-sol`.
3. Send a request that requires a deferred client capability, such as desktop browser tools.
4. The run fails immediately with:

```text
Type validation failed: Value: {"kind":"json","value":{"activated":[...]}}
Error message:
[
  {
    "expected": "array",
    "code": "invalid_type",
    "path": ["tools"],
    "message": "Invalid input: expected array, received undefined"
  }
]
```

## Evidence

The failure is produced while converting a local tool result in `@ai-sdk/openai`'s Responses input converter. The runtime's connector is defined in `packages/runtime/src/tool-availability.ts` and uses the reserved provider name `tool_search`.

## Expected behavior

Deferred tool activation should complete and the next model step should receive the activated Maka tools.

## Proposed fix

Use a Maka-specific provider-visible connector name that cannot collide with OpenAI's reserved `tool_search` name, while preserving the internal activation semantics and updating history/replay, prompts, UI copy, and regression tests.


## Exact-head checks

- test: SUCCESS
- label: SUCCESS
- windows_recovery: SUCCESS

## Changed files

- `packages/runtime/src/__tests__/deferred-tools-wire.test.ts`: +108/-0
- `packages/runtime/src/__tests__/responses-wire-contract.test.ts`: +86/-0
- `packages/runtime/src/model-adapter.ts`: +105/-8
- `packages/runtime/src/tool-availability.ts`: +5/-0
