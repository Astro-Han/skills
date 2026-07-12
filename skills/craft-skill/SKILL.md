---
name: craft-skill
description: "Create or improve agent skills from concrete behavior and evidence. Use when building or revising SKILL.md, or testing whether a skill earns its context. Do not use for ordinary documentation or one-off prompts."
---

# Craft Skill

A skill should be called for the right task, steer the agent to genuine completion, and make every token earn its place.

## Establish the job

Read the request, conversation, existing skill, repository conventions, and target platform's authoritative skill specification.

Define the useful behavior with realistic examples: what should call the skill, what should not, what the agent should do differently, and what observable evidence means it finished. Ask only about user-owned choices that materially change those answers. When revising a skill, preserve its name and inspect observed failures before editing.

## Call

- Follow the platform's metadata and invocation contract. Test triggering only when automatic invocation exists.
- Make the description identify the skill and its distinct trigger branches without leaking enough procedure to skip the body. One trigger per real branch; synonyms are not branches.
- Keep what every branch needs in `SKILL.md`. Put branch-specific knowledge behind a direct pointer that states when to load it.

Call is complete when every intended branch and close non-trigger has one clear owner, and the metadata passes the platform's validator when one exists.

## Steer

Use the lightest reliable medium:

- Put non-obvious judgment and sequence in instructions.
- Put knowledge the agent would rediscover in references.
- Put repeated, fragile, or deterministic operations in scripts.
- Put material copied into outputs in assets.

Match freedom to fragility. Use principles where several approaches work; tighten procedure or code only where variance causes failure.

Define completion from the requested outcome, not the procedure. Exhaustive means every decision-relevant item is accounted for, not every discoverable source or intermediate step is performed. End each step with a completion criterion the agent can check, with honest terminal states for missing evidence, unavailable input, and blocked actions. End with an overall postcondition that inspects the resulting artifact or state; completed steps are not final evidence.

## Earn

- Delete any sentence whose removal changes neither invocation nor execution.
- Keep each meaning in one authoritative place. Remove stale branches, duplication, and abstractions without present demand.
- Add code only when it makes repeated or error-prone work more reliable than instructions can; test it through its public seam.
- Evaluate only when the result can change a decision; otherwise stop.

When evidence could change the decision, read [references/evaluation.md](references/evaluation.md) before evaluating. When an existing skill misbehaves and the cause is unclear, read [references/diagnosis.md](references/diagnosis.md).

## Finish

Run the platform validator and relevant script tests. Confirm every resource has a condition-bearing pointer. Report the evidence and what remains unverified.

Stop when the concrete examples work and another deletion would damage Call, Steer, or the evidence needed to judge them.
