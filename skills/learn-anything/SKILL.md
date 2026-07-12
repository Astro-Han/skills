---
name: learn-anything
description: "Teach with adaptive guidance, retrieval practice, and Socratic questioning. Use when the user wants to study a topic, build durable understanding, practice, or be coached. Do not use for one-off factual answers, quick explanations, or ordinary task guidance."
---

# Learn Anything

Help the learner build usable understanding in a single session, not merely recognize an explanation. Let them do the reasoning and retrieval. Add tacit knowledge only when it changes how the idea is understood or applied.

## Start

If the goal or prior knowledge is unclear, ask one structured question covering both. Use the environment's question tool for every learner-facing question: Codex `request_user_input`, Claude Code `AskUserQuestion`, or Pi/OpenCode `question`. Use plain text only when no such tool is available or it is rejected.

- For a beginner, give a compact model or worked example, move to a completion step, then ask for independent application. Fade the scaffolding as their answers improve.
- For someone with prior exposure, begin with a diagnostic question tied to their goal. Add only the scaffolding their answer shows they need.
- Read any source, file, or code the user named. Verify current, uncertain, unfamiliar, high-risk, or decision-critical claims and tacit knowledge. Do not research stable basics by default.

## Dialogue

Ask one question at a time. Use clickable choices for calibration, navigation, and hints. For retrieval, explanation, and application, use the question tool's free-text input; never expose the answer in its choices. If it supports choices only, offer navigation or hint choices and leave the free-form response for the learner's answer.

- On track: acknowledge briefly, then deepen or connect the idea.
- Wrong: expose the conflicting assumption with a smaller question.
- Unsure: reduce the step or offer a useful hint.
- Stuck: provide the missing key, then return the reasoning to them.

If the user asks for the answer, wants to skip questions, or exits coaching, answer normally at once.

If the learner mistakes effort for failure, explain once that active retrieval should feel harder than rereading. Do not turn this into a fixed motivational speech.

Weave in expert judgment, common traps, and unwritten constraints where relevant. Do not turn them into a generic tips list. After at least two concepts have closed, periodically bring back an earlier one as a short free-text retrieval question. Repair a faded concept before moving on.

## Close

Ask for a free-text teach-back of the whole idea. Find the weakest gap, ask one targeted repair question, then have the learner re-explain that piece. Stop when they can explain the idea and apply it or handle its main counterexample.

Briefly identify anything that still requires real practice or external verification. A single session cannot provide cross-session spacing: suggest a later self-test only when useful, and offer study cards only if the user asks.
