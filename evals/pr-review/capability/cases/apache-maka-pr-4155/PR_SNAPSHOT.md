# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/4155 — `fix(desktop): truncate long file paths in the changes panel`
- Author: liuxiaocs7
- Target base head: `b16376d782a2c7d3540a67708851f9256d87dde6`
- Comparison base: `b16376d782a2c7d3540a67708851f9256d87dde6`
- Exact source head: `085682665bb12ee16fd224bcb6fc17667c47dd4a`
- Diff: 28 additions, 0 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

In the workbar **变更 / Changes** panel, a long, deeply-nested file path did not truncate: it overflowed the narrow panel and pushed the change counts (`新增 N` / `删除 N`) and the collapse chevron off the right edge, where the list's `overflow: hidden` clipped them — with no `…` ellipsis.

The panel already has a truncation chain (`.maka-session-review-file-path` `min-width:0; flex:1` + `Text maxLines={1}`), but the width constraint never reaches it. Astryx `Collapsible` wraps each trigger row in an intermediate flex `<span>` that keeps the browser default `min-width: auto`, so it refuses to shrink below the full nowrap path width and overflows the button. This constrains that label span (`min-width: 0; flex: 1 1 auto; overflow: hidden`) so the path ellipsizes and the stats + chevron stay in view. `flex: 1 1 auto` keeps the stats right-aligned for short paths; `min-width: 0` lets it shrink for long ones. The rule lives in unlayered `review.css` and `triggerLabel` sets no competing `flex`/`min-width`, so it overrides cleanly.

Fixes #4154

## Verification

- `npx tsc -p apps/desktop/tsconfig.storybook.json --noEmit` — no errors
- `npx biome check` + `npx biome format` on the two touched files — pass
- Added a deep-path fixture (`.scratch/pyclient/gen/client/Comparator_pb2.py`) to the `Product/Session Workbar → Changes` story and captured before/after from the built Storybook at a ~360px docked-panel width.

Not run (scope): full-repo `npm run lint` / `typecheck` / `build` / `knip`.

### Screenshots (Changes panel, ~360px)

| Before (clipped, no ellipsis) | After (path truncates, stats + chevron visible) |
|---|---|
| ![before](https://raw.githubusercontent.com/liuxiaocs7/maka/pr-4155-assets/changes-before.png) | ![after](https://raw.githubusercontent.com/liuxiaocs7/maka/pr-4155-assets/changes-after.png) |

### Review focus

CSS-only layout fix plus a story fixture; no behavior change to data or IPC. The one thing to sanity-check visually is that short-path rows still right-align their change counts.

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: Claude Code (Opus 4.8) — diagnosed the root cause and wrote the CSS fix and the story fixture. Author reviewed. The fix commit carries a `Generated-by` trailer.

## Checklist

- [ ] Tests cover the change and fail without it
- [ ] Lint, format, typecheck and the affected suites pass locally

<!-- Note: this is a CSS-layout fix; the Changes story now renders a long path so
the case is visible for review, but the visual smoke only gates on console errors,
so no automated assertion fails without the change. Affected checks (storybook
typecheck, biome on the touched files) pass; full-repo checks were not run. -->

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No

## Linked issues

### https://github.com/apache/maka/issues/4154 — Long file paths in the Changes panel are clipped instead of truncated

### What happened

In the workbar **变更 / Changes** panel (`SessionReviewPanel`), when a changed file has a long, deeply-nested path, the row does not truncate the path. Instead the path overflows the narrow panel and pushes the change counts (`新增 N` / `删除 N`) and the collapse chevron off the right edge, where they get clipped by the panel. For the longest paths even the path text itself is cut mid-word, with no `…` ellipsis.

Expected: the file path ellipsizes to fit the panel width, and the change counts + chevron stay visible on the right — as already happens for short paths.

Root cause: each row is rendered with Astryx `Collapsible`, whose trigger wraps the row content in a flex `<span>`. That span keeps the browser default `min-width: auto`, so it refuses to shrink below the full (nowrap) path width and overflows the button; the list's `overflow: hidden` then clips it. The panel's own truncation chain (`.maka-session-review-file-path` with `min-width: 0; flex: 1` + `Text maxLines={1}`) never receives a width constraint because it stops at that intermediate span.

### How to reproduce

1. Open a session whose Git working tree has many changes, including files with long, deeply-nested paths (e.g. `.scratch/pyclient/gen/client/Comparator_pb2.py`).
2. Open the 任务工作栏 → **变更** tab (dock it on the right so the panel is at its narrower width).
3. Observe rows with long paths: the path runs off the right edge and the `新增 N` count and chevron are clipped, instead of the path truncating with `…`.

### Environment

- Maka commit: `b16376d78`
- OS and version: macOS (Darwin 24.6.0)
- Surface: Desktop
- Node.js version: v24.14.0

### Logs, screenshots, or additional context

Reproduced in the `Product/Session Workbar → Changes` Storybook story once a long-path file is present in the fixture. Screenshot showing the clipping is available and can be attached to this issue. A fix is in progress.

## Exact-head checks

- test: SUCCESS
- label: SUCCESS

## Changed files

- `apps/desktop/src/renderer/styles/workbar/review.css`: +11/-0
- `apps/desktop/stories/session-workbar.stories.tsx`: +17/-0
