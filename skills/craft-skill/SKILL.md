---
name: craft-skill
description: "Create or improve agent skills from concrete behavior and evidence. Use when the user wants to build a reusable skill, revise an existing SKILL.md, or determine whether a skill changes agent behavior enough to justify its context. Do not use for ordinary documentation or one-off prompts that are not meant to become skills."
---

# Craft Skill

A skill should be called for the right task, steer the agent to genuine completion, and make every token earn its place.

## Establish the job

Read the request, conversation, existing skill, and nearby repository conventions. Find the target platform's authoritative skill specification and invocation model instead of assuming one platform's frontmatter works everywhere.

Define the useful behavior with realistic examples: what should call the skill, what should not, what the agent should do differently, and what observable evidence means it finished. Ask only about user-owned choices that materially change those answers.

For an existing skill, preserve its name and inspect actual failures or inefficiencies before editing. For a new skill, run a clean default-behavior baseline before drafting only when its result could change the design.

## Call

Call the right skill for the right task.

- Follow the target platform's metadata and invocation contract. Distinguish automatic from explicit invocation; test triggering only when the platform supports it.
- Make the description identify the skill and its distinct trigger branches without summarizing enough procedure for the agent to skip the body. One trigger per real branch; synonyms are not branches.
- Keep what every branch needs in `SKILL.md`. Put branch-specific knowledge behind a direct pointer that says when to load it.

Call is complete when every intended branch and close non-trigger has one clear owner, and the produced metadata passes the platform's validator when one exists.

## Steer

Steer the agent's action to genuine completion using the lightest reliable medium:

- Put non-obvious judgment and sequence in instructions.
- Put knowledge the agent would otherwise rediscover in references.
- Put repeated, fragile, or deterministic operations in scripts.
- Put material copied into outputs in assets.

Match freedom to fragility. Prefer principles where several approaches work; use tighter procedures or code only where variance causes failure. Define scope from the requested outcome before defining the procedure. Exhaustive means every decision-relevant item is accounted for, not every discoverable source or intermediate step is performed.

State positive target behavior, co-locate rules needed together, and end each step with a completion criterion the agent can check. The criterion proves the required outcome, not that the procedure was followed. It must admit an honest terminal state for missing evidence, unavailable input, and blocked actions instead of requiring the agent to wish them away. End the skill with one overall postcondition that inspects the resulting artifact or state; completed intermediate steps are not final evidence.

Steer is complete when the realistic examples reach their observable outcomes without relying on unstated knowledge or unnecessary ceremony.

## Earn

Earn is the value test across Call and Steer, not a third phase.

- For every sentence, ask whether removing it changes invocation or execution. Delete the whole sentence when it does not.
- Keep each meaning in one authoritative place. Remove stale branches, duplicated rules, and abstractions without present demand.
- Add code only when it makes repeated or error-prone work more reliable than instructions can. Test it through its stable public seam.
- Evaluate only when the result can change a decision. Before evaluating, state that decision, the success criteria, and what each possible result changes. If those cannot be stated, stop.

When evidence can change the decision, read [references/evaluation.md](references/evaluation.md) before running anything. When an existing skill misbehaves and the cause is unclear, read [references/diagnosis.md](references/diagnosis.md).

## Finish

Run the target platform's validator and every bundled script's relevant tests. Confirm each resource is pointed to from the skill under the condition that needs it. Report what evidence was obtained and what remains unverified; do not turn absence of evidence into proof of no value.

Stop when the skill handles its concrete examples and another deletion would damage Call, Steer, or the evidence needed to judge them.
