# Astro Skills

Skills I use to make coding agents reason more carefully, learn from evidence, and finish work cleanly.

These are not prompt collections or exhaustive playbooks. Each skill exists because a recurring failure survived ordinary prompting: agents acted before resolving a real decision, patched symptoms without proving a cause, wrote tests after the implementation, obeyed review comments without checking them, or left a session half-finished.

The skills are intentionally small. They encode only the behavior that has proved useful in repeated work, including trials with smaller models where the skill—not the base model—has to carry more of the result.

## Skills

| Skill | Use it when you need to… |
| --- | --- |
| [`learn-anything`](skills/learn-anything/) | Build durable understanding through adaptive teaching and retrieval practice. |
| [`shape`](skills/shape/) | Resolve material user-owned decisions before implementation. |
| [`debug`](skills/debug/) | Reproduce a failure, isolate its cause, and verify the original symptom. |
| [`tdd`](skills/tdd/) | Change production behavior through a reliable red-green-refactor loop. |
| [`review-feedback`](skills/review-feedback/) | Evaluate review feedback with evidence before accepting or rejecting it. |
| [`wrap-up`](skills/wrap-up/) | Close a work session without leaving session-owned loose ends. |

## Install

Install all skills:

```bash
npx skills add Astro-Han/skills
```

Install one skill:

```bash
npx skills add Astro-Han/skills --skill debug
```

See the [Skills CLI](https://skills.sh/docs) for supported agents and additional options.

## Design principles

- Start from a failure an agent actually exhibits.
- State when the skill should and should not trigger.
- Add only instructions the model cannot reliably infer on its own.
- Prefer evidence and observable outcomes over ritual.
- Test demanding skills with smaller models when practical.
- Keep external skills at their source instead of vendoring them here.

The English `SKILL.md` files are the canonical agent instructions. [中文说明](README.zh.md).

## License

MIT
