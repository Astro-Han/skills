# Frozen pull request snapshot

- PR: https://github.com/apache/maka/pull/4073 — `fix(desktop): state a failed turn's outcome where it happened`
- Author: Astro-Han
- Target base head: `4b202615f1b2aec5018dfa52cdc4650c4a9ec8e9`
- Comparison base: `4b202615f1b2aec5018dfa52cdc4650c4a9ec8e9`
- Exact source head: `c8e78ded56391423889b4a502486892260dfdda5`
- Diff: 210 additions, 217 deletions, 15 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Summary

A failed turn's banner made three promises it could not keep.

**It named an action that does not exist.** The banner joins `describeTurnErrorClass()` and `deriveFailedTurnRecovery()` with a CSS `::before` dot, so a rate limit rendered as 「触发模型速率限制 · 已保留部分输出，可从这里继续」. There is no "here" to continue from — `partialOutputRetained` only records that the turn produced assistant text or a tool result, and the one real resume path is `app_restarted`'s safe resume, gated on `latestInterruptedResumeTurnId`. `FailedTurnRecoveryAction`'s four values were never read by any renderer, only `label` was, so the recovery layer existed solely to phrase guidance no surface could honor. It is deleted. Each `turnError` string now says what happened and what to do in one sentence, and what it asks for — send another message — always works.

**It painted its own error surface.** `Marker variant="failed-banner"` plus hand-rolled `oklch(from var(--destructive) …)` borders reimplemented Astryx's `Banner`, which this same file already uses for the provider retry indicator and which the app uses in ~50 other places. Reason → `title`, park diagnostic → `description`, safe resume → `endContent`. Three `MarkerVariant`s, the bespoke `AlertOctagon`, and the shell CSS go with it. Severity follows the app's existing `tone === 'destructive' ? 'error' : 'warning'` grading, so "restarted, press continue" stops looking as severe as blocked billing.

**It rendered above the work it described.** The banner sat at the head of `maka-assistant-answer-content`, before `segment.items.map()` — an outcome reading as a header on reasoning and tool calls that had all succeeded. It now follows the timeline it concludes.

Safe resume is kept: it is the only recovery with a real backend, replaying an interrupted turn's own context instead of asking the user to restate it. Its button and the strings around it move from 「安全恢复」 to 「继续这一轮」 so the control, its pending state, its park description, and its toasts stop describing one act four ways.

Net −122 lines.

## Verification

- `npm --workspace @maka/ui run build` — pass
- `npm --workspace @maka/desktop run typecheck` (preload + main + renderer + storybook) — pass
- `npm run format:check` — clean
- `node --test` on the three affected files (`session-status-presentation`, `session-error-presentation`, `chat-turn-steering-order`) — 7/7 pass
- Not run: the full repository suite, left to CI.

Rendered through the real `TurnView` + Astryx CSS. Banner now follows the answer; app-restart is `warning` with the resume button, rate limit and auth are `error` with copy only:

![image](https://github.com/user-attachments/assets/9a971846-313b-4645-980a-5004ffddc77f)

![image](https://github.com/user-attachments/assets/80f37020-2aac-415f-bd7c-f4ea328ff992)

## Review focus

The copy is the substance of this change — every `turnError` string in both locales was rewritten. Worth reading as user-facing text rather than as a diff.

## AI use

Select exactly one:

- [ ] No generative tool made a substantive contribution
- [x] Generative tooling made a substantive contribution

Tool(s) and scope: Claude Code (Opus 5) — traced the three defects to their sources, wrote the change, and rewrote the copy under review by the contributor of record, who chose the approach at each branch (drop the unbacked recovery layer rather than build buttons for it; keep safe resume; grade severity in two tiers).

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

## Changed files

- `apps/desktop/src/main/__tests__/session-error-presentation.test.ts`: +4/-10
- `apps/desktop/src/main/__tests__/session-status-presentation.test.ts`: +54/-67
- `apps/desktop/src/renderer/app-shell-turn-view-model.ts`: +20/-8
- `apps/desktop/src/renderer/features/workbar/tools/side-chat/quote-companion-panel.tsx`: +2/-1
- `apps/desktop/src/renderer/locales/conversation-copy.ts`: +3/-3
- `apps/desktop/src/renderer/locales/shell-copy.ts`: +6/-6
- `apps/desktop/src/renderer/session-status-presentation.ts`: +40/-48
- `apps/desktop/src/renderer/styles/chat-detail.css`: +5/-5
- `packages/ui/src/__tests__/chat-turn-steering-order.test.ts`: +4/-0
- `packages/ui/src/chat-turn.tsx`: +53/-32
- `packages/ui/src/chat-view.tsx`: +4/-1
- `packages/ui/src/conversation-copy.ts`: +2/-2
- `packages/ui/src/primitives/chat.tsx`: +4/-10
- `packages/ui/src/runtime-resume-copy.ts`: +5/-5
- `packages/ui/src/styles.css`: +4/-19
