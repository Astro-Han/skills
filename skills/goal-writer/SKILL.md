---
name: goal-writer
description: Draft or review bounded, testable goals. Use only when the user explicitly asks to create, revise, or review a goal, invokes `/goal`, or asks to use the goal feature.
---

# Goal Writer

Turn rough intent into a copy-ready execution contract. Preserve the user's ambition while making progress observable, reversible, and reviewable. Produce the contract; do not activate it unless explicitly asked.

## Draft

1. Choose the target surface. Use `/goal` only for Codex or a product that supports it; otherwise use `Goal:` or the product's native format. Match the user's language.
2. Read cheap, relevant context first: the request, named files or links, repo instructions, current state, and known verification commands. Distinguish facts from assumptions.
3. Ask only when missing information materially changes scope, risk, ownership, cost, or product direction. State low-risk assumptions and continue.
4. Keep the requested outcome. Do not silently turn a complete product into a demo, an open production window into an arbitrary quota, or a risky objective into discovery only. Gate risky execution instead.
5. Draft the smallest contract that changes agent behavior. Run the linter before returning it.

## Contract

Use one compact line per field when possible:

```text
/goal [one concrete outcome].
Context: [minimum sources and current state to inspect first].
Scope: [desired outcome, allowed work, and meaningful boundaries].
Non-goals: [plausible adjacent work that is intentionally excluded].
Constraints: [non-obvious contracts, safety rules, or topology limits].
Verification: [commands and observable evidence that prove completion].
Iteration: [how to narrow failures and continue using new evidence].
Stop when: [mechanically checkable completion or exhaustion condition].
Pause if: [external decision, access, ownership, or high-risk gate].
Final report: [artifacts changed, checks run, risks, and manual next steps].
```

## Judgment

- Make the outcome concrete. Reject vague goals such as “improve everything” until completion can be observed.
- Keep context minimal. If a command is unknown, require discovery instead of inventing it.
- Include only non-goals a reasonable agent might otherwise attempt and constraints that alter behavior.
- Name verification evidence such as tests, screenshots, logs, diffs, artifacts, or external state. Never weaken validators to make the goal pass.
- Make iteration evidence-seeking, not “keep trying.” Ordinary difficulty and test failures belong here or in `Stop when`, not `Pause if`.
- Reserve `Pause if` for human choices, credentials, production data, destructive or public actions, paid services, unclear ownership, and comparable external gates.
- Preserve user-supplied counts or time windows. Do not invent caps. Bound open-ended work by candidate exhaustion, verification, conflicts, ownership, review overhead, or repeated non-narrowing failure.
- Default PR work to independent, reviewable changes. Do not authorize review, approval, merge, release, force-push, or remote deletion unless explicitly requested and appropriately gated.

Read only the matching section of [references/patterns.md](references/patterns.md) for PR batches, product/UI builds, bug fixes, high-risk work, or skill creation.

## Length and output

Keep the pasteable contract within the target product's limit. Treat 4000 characters as the default hard ceiling; aim for six to ten short lines and preserve `Stop when` and `Pause if` when trimming.

Return the contract first. Add only short design notes that explain consequential scope, verification, or gates. If the user asks for just the goal, return only the contract.

## Validate

Resolve paths relative to this file:

```bash
python3 scripts/lint_goal.py <goal-file.md>
```

Use `python3 scripts/lint_goal.py -` for a contract from stdin. Use `--max-chars N` for a stricter product limit.
