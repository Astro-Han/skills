---
name: shape
description: "Interview the user to resolve material branches of a decision tree and converge on a shared plan before acting. Use when multiple reasonable choices would materially change scope, cost, reversibility, or outcome, or when the user asks to brainstorm, shape, or grill an idea. Do not use when facts can resolve the ambiguity or a reversible assumption would not materially affect the result."
---

# Shape

Walk down each material branch of the decision tree until you reach a shared understanding, resolving dependencies between decisions one by one. For each question, provide your recommended answer.

Ask questions one at a time, waiting for feedback before continuing. Asking multiple questions at once is bewildering.

Look up *facts* in the environment—filesystem, tools, or available sources—instead of asking. *Decisions* belong to the user: put each one to them and wait for their answer.

Use the environment's structured question tool for every user-facing question: Codex `request_user_input`, Claude Code `AskUserQuestion`, Pi/OpenCode `question`. Use plain text only when no such tool is available or it is rejected.

For a visual-taste decision, render minimal HTML variants side by side and let the user judge them. Do not build a visual aid for a conceptual question.

Cut scope and process until another cut would damage the goal, coherence, reversibility, or ability to improve later. Stop asking when the remaining ambiguity is reversible and would not materially change the result.

Synthesize the shortest coherent plan, including material assumptions and exclusions. Do not act on it until the user confirms you have reached a shared understanding.
