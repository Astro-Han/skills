# Astro Skills

English | [中文](README.zh.md)

![Every token should change behavior.](assets/astro-skills-hero.png)

## Every token should change behavior.

Small skills that help coding agents make better decisions: clarify before building, prove before fixing, verify before accepting, and close the loop before stopping.

## Why I made these

I started with [Superpowers](https://github.com/obra/superpowers). It showed me how much a structured workflow can improve agentic coding. But I also found its full spec → plan → development process too heavy for much of my daily work. Even a change of a few lines could pull in the whole ceremony.

Then I found Matt Pocock's [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me). It was strikingly short, yet it changed the conversation in exactly the right place. That was the lesson: a skill is not valuable because it says more. It is valuable when a small instruction reliably changes an important behavior.

Astro Skills grew from that standard. I keep only the constraints that earn their place in the model's context—one recurring failure, one behavioral correction, as few tokens as the job allows.

## The skills

| Skill | Use it when | What you get |
| --- | --- | --- |
| [`goal-writer`](skills/goal-writer/) | You have an ambitious or long-running task, but the finish line is still vague. | A minimal execution contract that states the observable result, its acceptance criterion, and only the boundaries the task truly needs. |
| [`shape`](skills/shape/) | A plan, decision, or idea needs stress-testing because choosing silently would change the outcome. | A shared plan you have actually agreed on, reached one consequential branch of the decision tree at a time. |
| [`craft-skill`](skills/craft-skill/) | You want to create or improve a reusable agent skill and need to know whether its instructions earn their context. | A platform-valid skill shaped through Call and Steer, with every token, evaluation, and line of code held to Earn. |
| [`parallel-research`](skills/parallel-research/) | A high-cost question needs broad, current, trustworthy evidence. | A faster, better-supported answer: independent evidence angles run in parallel, then the main agent cross-checks critical claims and conflicts. |
| [`learn-anything`](skills/learn-anything/) | You want to genuinely learn or practise something, not just receive an explanation. | Adaptive coaching that uses retrieval, application, and teach-back to build understanding you can actually use. |
| [`tdd`](skills/tdd/) | You are adding or changing production behavior and need fast, trustworthy feedback. | Small, verified increments: one predicted RED, the minimum GREEN, then safe refactoring before the next behavior. |
| [`debug`](skills/debug/) | A bug or performance regression needs investigation, not a plausible guess. | A reproducible signal, discriminating evidence, and a root cause checked against the original symptom. |
| [`review-feedback`](skills/review-feedback/) | Code-review feedback may lead to changes and needs to be evaluated before acting. | An evidence-backed decision for every claim—fix, simplify, defer, or reject it at the layer that actually owns the problem. |
| [`wrap-up`](skills/wrap-up/) | The work is ending and you want the result finished, not merely summarized. | A closed workstream: promised outcomes verified, session-owned loose ends resolved, and the real final state reported. |

`shape` is the clearest example of the design. Its core is a **decision tree**: whenever a branch would materially change the outcome, the agent discusses that branch with the user instead of silently choosing. When the decision is genuinely visual, it renders the alternatives in HTML because seeing them is more useful than describing them.

## Install

### GitHub CLI

With [GitHub CLI](https://cli.github.com/manual/gh_skill) v2.90.0 or later, install all skills for Codex:

```bash
gh skill install Astro-Han/skills --all --agent codex --scope user
```

Or install one:

```bash
gh skill install Astro-Han/skills shape --agent codex --scope user
```

Replace `codex` with your agent host, or use `--scope project` for a repository-local installation.

### Skills CLI

Install all skills:

```bash
npx skills add Astro-Han/skills
```

Or install one:

```bash
npx skills add Astro-Han/skills --skill shape
```

See the [Skills CLI documentation](https://skills.sh/docs) for supported agents and other options.

## The rule

- Start with a failure agents actually repeat.
- Find the smallest instruction that changes that behavior.
- Keep evidence and observable outcomes; remove ceremony.
- Test demanding skills with smaller models when practical. If the skill only works because the base model is strong, the skill has not proved much.

Every line competes for limited context. If removing it does not make the agent worse at the job, it does not belong in the skill.

## Origins and acknowledgements

- `learn-anything` and `wrap-up` are original skills developed from my own workflows.
- `craft-skill` draws from [OpenAI's `skill-creator`](https://github.com/openai/skills/tree/main/skills/.system/skill-creator), [Anthropic's `skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator), Matt Pocock's [`writing-great-skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills), and Superpowers' [`writing-skills`](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills). It rebuilds their strongest ideas around three constraints: call the right skill, steer the agent to genuine completion, and make every token earn its place.
- `shape` is inspired by Matt Pocock's [`grilling`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling). Its visual-decision rule also carries forward an idea from Superpowers' [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming) workflow.
- `tdd` is inspired by Matt Pocock's [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).
- `debug` draws from Matt Pocock's [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs), Superpowers' [`systematic-debugging`](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging), and Waza's [`hunt`](https://github.com/tw93/Waza/tree/main/skills/hunt). It deliberately reduces those approaches to a smaller evidence-driven core.
- `review-feedback` began with ideas from Superpowers' [`receiving-code-review`](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review), but has since been substantially rewritten around evidence, ownership, scope, and system cost.

The linked projects remain the canonical sources for their skills. This repository contains my own adaptations, not vendored copies. The English `SKILL.md` files are the canonical instructions for Astro Skills.

## License

MIT
