# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/3046 — `fix(runtime): reject truncated history-compact summaries at load time (#3041)`
- Author: me2seeks
- Target base head: `820a47b90ff052a726997819539fc382efa31ace`
- Comparison base: `2f76c310944c13791657c17ef491c4ed127eb30d`
- Exact source head: `621f1d535556c3a4cbdb356904cec97b778f39bf`
- Diff: 519 additions, 29 deletions, 13 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

Closes #3041. #3029 (PR #3040) added validation at the two checkpoint **write** gates, but a checkpoint whose truncated summary was persisted **before** that gate — incident checkpoint `hcheckpoint-981ceab8…` in session `fbdb3fd3`, plus two more in `d282f6ac` — still loads and replays. This PR closes the load side.

## What changed

- Extracts a writer-agnostic `isHistoryCompactSummaryTruncated` from `validateHistoryCompactSummary` (fence count + tail punctuation).
- Applies it in **both** load paths of `loadLatestHistoryCompactCheckpointFromRunLedger`: the bounded projection fast path and the canonical ledger recovery path.
- A rejected checkpoint falls back to the previous valid checkpoint (or raw events when none), and the stale projection is repaired via `repairEventProjection`. No data is lost: raw events are append-only, and the next high-water fold rewrites a fresh checkpoint.
- **Deliberately does NOT apply the `missing_sections` check at load**: legacy checkpoints predate the sectioned summarizer contract and remain usable without sections. Only truncation is load-bearing regardless of writer era.

## Review fixes (first-principles + Occam double review)

- **MAJOR**: the shared tail heuristic counted a trailing backtick as truncation, which would also match a *closed* ``` fence. At load time that would reject complete legacy summaries ending in a code fence and force a re-compaction. Dropped the backtick from the tail class (the even fence count already proves a closed block), added the `…` signal, and renamed the predicate to `isHistoryCompactSummaryTruncated`.
- Trimmed lockstep unit tests to three distinct contract points.

## Validation

- runtime suite: **2816 tests, 2810 pass, 0 fail, 6 skipped**; biome + tsc clean.
- New tests cover: ledger fallback on a truncated checkpoint, projection repair from the canonical ledger, and the closed-fence false-positive regression.

## Stacking

Stacked on **#3040** (`maka/history-compact-summary-validation`), which is not yet merged; this branch contains those 3 commits plus 2 new ones. Merge **after** #3040, at which point the diff reduces to the 2 new commits.

## Linked issues

### https://github.com/apache/maka/issues/3041 — Validate history-compact checkpoint summaries at load time (repair poisoned sessions)

## Background

#3029 added validation at the two checkpoint **write** gates: a malformed/truncated LLM summary can no longer replace folded history going forward. The fix is write-only.

## Gap

A checkpoint whose summary was persisted **before** the gate (e.g. the incident checkpoint `hcheckpoint-981ceab8…` in session `fbdb3fd3`) still loads and replays: `loadLatestHistoryCompactCheckpointFromRunLedger` only checks `validateHistoryCompactCheckpointShape` (non-empty summary), not the summary contract. The already-poisoned session keeps serving the fragment until a later successful fold happens to supersede it.

## Why not just reuse the same validator

Load-time validation is **asymmetric** to write-time: at write time the summary was just produced by the sectioned summarizer prompt, so a missing `## Goal` heading means degraded output. At load time the ledger may contain checkpoints written by older binaries whose summaries never followed the sectioned contract but are still usable. Applying `validateHistoryCompactSummary` verbatim would silently discard those and force a fallback to raw events (safe but wasteful/surprising), or loop re-compaction.

## Suggested direction

- Only validate checkpoints whose shape/metadata indicates the sectioned writer (e.g. a schema `version` bump or an explicit `summaryFormat` field), leaving legacy checkpoints to the existing shape check.
- Or validate but treat "section-less yet non-trivially-long" as a distinct case from "fragment/truncated" and migrate rather than discard.
- Add load-path tests mirroring the existing `history-compact-checkpoint.test.ts` fixtures (which currently use section-less synthetic summaries — they would all need to keep passing for legacy).

## Related

- #3029 (write-gate validation, merged in PR #3040)
- #3030 (parallel tool-call message merge)

## Exact-head checks

- request-review: SUCCESS
- unnamed: SUCCESS

## Changed files

- `packages/runtime/src/__tests__/ai-sdk-backend.test.ts`: +91/-0
- `packages/runtime/src/__tests__/history-compact-checkpoint.test.ts`: +63/-0
- `packages/runtime/src/__tests__/history-compact-summary-validation.test.ts`: +135/-0
- `packages/runtime/src/__tests__/mid-turn-capacity-backend.test.ts`: +40/-4
- `packages/runtime/src/__tests__/mid-turn-capacity-compact.test.ts`: +20/-2
- `packages/runtime/src/__tests__/overflow-reactive-recovery.test.ts`: +3/-1
- `packages/runtime/src/__tests__/session-manager.test.ts`: +6/-1
- `packages/runtime/src/ai-sdk-compaction.ts`: +7/-0
- `packages/runtime/src/history-compact-error.ts`: +4/-1
- `packages/runtime/src/history-compact-ledger.ts`: +21/-2
- `packages/runtime/src/history-compact-summarizer.ts`: +24/-18
- `packages/runtime/src/history-compact-summary-validation.ts`: +94/-0
- `packages/runtime/src/mid-turn-capacity-compact.ts`: +11/-0
