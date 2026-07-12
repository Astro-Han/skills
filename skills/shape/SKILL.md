---
name: shape
description: "Interview the user to resolve material user-owned decisions before acting. Use when multiple reasonable choices would materially change scope, cost, reversibility, or outcome, or when the user asks to brainstorm, shape, or grill an idea. Do not use when facts can resolve the ambiguity or a reversible assumption would not materially affect the result."
---

# Shape

Interview the user until we reach a shared understanding. Walk down each material branch of the design tree, resolving dependencies between decisions one by one. For each question, provide your recommended answer.

Ask questions one at a time, waiting for feedback before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found in the codebase or available sources, look it up rather than asking. The *decisions*, though, belong to the user: put each one to them and wait for their answer.

When the environment provides a structured question tool, use it for every user-facing question: Codex `request_user_input`, Claude Code `AskUserQuestion`, Pi/OpenCode `question`. Use plain text only when no such tool is available or the tool is rejected.

For a genuine visual-taste decision, render minimal HTML variants side by side and let the user judge them. Do not build a visual aid for a conceptual question.

Reason from first principles. Cut scope and process until another cut would damage the goal, coherence, reversibility, or ability to improve later. Stop asking when the remaining ambiguity is reversible and would not materially change the result.

Synthesize the shortest coherent plan, including material assumptions and exclusions. Do not act on the plan until we reach a shared understanding.
