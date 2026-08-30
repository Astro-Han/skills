# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/4024 — `feat(ui): add UI and terminal font size settings to Appearance`
- Author: liugddx
- Target base head: `c8410c53b52e1ab3d19fc1fff45c90885a853862`
- Comparison base: `76adbdb20b58a4c1287c9272d006db65ea65830d`
- Exact source head: `d32399b12308323b38d7fa54832ba192503df13d`
- Diff: 372 additions, 10 deletions, 12 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Screenshot

Settings → Appearance → 字号 (Font size), presented as Codex-style numeric px steppers — an independent **UI font size** and **terminal font size**, each with a description and a `px` stepper:

![Font size controls](https://raw.githubusercontent.com/liugddx/maka-agent/pr4024-assets/assets/font-size-section.png)

<details><summary>Full Appearance page</summary>

![Appearance page](https://raw.githubusercontent.com/liugddx/maka-agent/pr4024-assets/assets/font-size-appearance-full.png)

</details>

<details><summary>Boundary: 22px (max)</summary>

![Appearance page at 22px](https://raw.githubusercontent.com/liugddx/maka-agent/pr4024-assets/assets/font-size-appearance-22px.png)

</details>

<details><summary>Boundary: 11px (min)</summary>

![Appearance page at 11px](https://raw.githubusercontent.com/liugddx/maka-agent/pr4024-assets/assets/font-size-appearance-11px.png)

</details>

## Summary

Appearance settings only exposed *theme* and *palette* — there was no in-app way to change font size. The renderer type scale was fixed at `base: 14` and both xterm.js terminals hardcoded `fontSize: 12`, so users on large / high-DPI displays had to fall back to coarse OS-level scaling.

This adds two controls to the Appearance page, mirroring Codex Desktop's *UI Font* / *Code Font* but deliberately kept as **separate** knobs:

- **UI font size** — an integer px value (11–22, default 14 = the type-scale base). Applied as a document-root font-size of `16px × size / base`: every `--font-size-*` token is `rem`, so this scales what is rem-derived — text and Astryx's rem-based icon atoms — while px-literal spacing and control widths stay fixed. That is why the range is clamped tightly around the base rather than offered as a free zoom; the boundary screenshots above show the layout absorbing the max/min sizes by wrapping, not clipping. It is **not** the old `html { font-size }` density hack removed in `makaTheme.ts`. Restored before first paint in `cached-theme-bootstrap` to avoid a resize flash.
- **Terminal font size** — an integer px value (9–24, default 12) fed via `getTerminalFontSize()` into both `Terminal` instances; open terminals subscribe and re-fit (re-emitting geometry to the PTY) on change.

Both persist under `appearance` (already client-owned) and **fail closed** to their defaults on any malformed/out-of-range value — so a bad persisted value can't drive an arbitrary root size (the failure mode that made Codex's font size unusable).

Refs #4021

## Verification

- `npm --workspace @maka/core run typecheck` — pass
- `npm --workspace @maka/desktop run typecheck` — pass (preload/main/renderer/storybook)
- `node --test packages/core/dist/__tests__/settings.test.js` — 20/20 pass, including a new test covering the fail-closed normalize (wrong types → defaults, out-of-range → clamped) for `uiFontSize` / `terminalFontSize`
- `biome check` on all changed files — clean
- Manual: launched the desktop app on this branch (isolated `--user-data-dir` profile), changed both values in Settings → Appearance — UI rescales and open terminals re-fit immediately, values persist across relaunch. Screenshots above are from that run.

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: Claude Opus 4.8 — codebase investigation, implementation across settings schema / theme apply layer / terminal wiring / settings UI + i18n, and the added unit test. Commit carries a `Generated-by` trailer.

## Checklist

- [x] Tests cover the change and fail without it
- [x] Lint, format, typecheck and the affected suites pass locally

Does this PR entail a change in behavior?

- [x] Yes — described under Summary above
- [ ] No




## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- test: SUCCESS
- windows_recovery: SUCCESS

## Changed files

- `apps/desktop/src/main/__tests__/font-size-type-scale.test.ts`: +40/-0
- `apps/desktop/src/renderer/astryx-theme/makaTheme.ts`: +2/-1
- `apps/desktop/src/renderer/astryx-theme/type-scale.ts`: +32/-0
- `apps/desktop/src/renderer/cached-theme-bootstrap.ts`: +5/-0
- `apps/desktop/src/renderer/features/workbar/tools/terminal/session-terminal-panel.tsx`: +12/-1
- `apps/desktop/src/renderer/locales/settings-preferences-copy.ts`: +12/-1
- `apps/desktop/src/renderer/settings/appearance-settings-page.tsx`: +74/-2
- `apps/desktop/src/renderer/settings/runtime-host-ssh-terminal-dialog.tsx`: +7/-1
- `apps/desktop/src/renderer/theme.ts`: +80/-2
- `apps/desktop/src/renderer/use-shell-appearance.ts`: +13/-2
- `packages/core/src/__tests__/settings.test.ts`: +44/-0
- `packages/core/src/settings.ts`: +51/-0
