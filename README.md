# Astro Skills

[中文](README.zh.md)

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

## Origins and acknowledgements

These skills mix original work with ideas learned from other skill authors:

- `learn-anything` and `wrap-up` are original skills developed from my own workflows.
- `shape` is inspired by Matt Pocock's [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me).
- `tdd` is inspired by Matt Pocock's [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).
- `debug` draws from Matt Pocock's [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs), Superpowers' [`systematic-debugging`](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging), and Waza's [`hunt`](https://github.com/tw93/Waza/tree/main/skills/hunt). It deliberately reduces those approaches to a smaller evidence-driven core.
- `review-feedback` began with ideas from Superpowers' [`receiving-code-review`](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review), but has since been substantially rewritten around evidence, ownership, scope, and system cost.

The linked projects remain the canonical sources for their skills. This repository contains my own adaptations, not vendored copies.

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
- Credit adapted ideas while keeping external skills at their canonical source.

The English `SKILL.md` files are the canonical agent instructions.

## License

MIT
