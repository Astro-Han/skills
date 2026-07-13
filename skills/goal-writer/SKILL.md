---
name: goal-writer
description: Draft or review minimal, testable goals. Use only when the user explicitly asks to write, revise, or review a goal.
---

# Goal Writer

Turn rough intent into the smallest copy-ready execution contract that makes completion decidable. Produce the contract; do not activate it unless explicitly asked.

## Draft

1. Look up facts in the request, named sources, and available environment instead of asking or inventing them. Ask only for user-owned decisions that materially change the contract; state reversible assumptions.
2. Preserve the requested outcome. Do not invent limits or substitute a safer intermediate objective.
3. Write one coherent acceptance decision containing the observable result that should exist and the criterion for accepting it as complete.
4. Add another fact only when deleting it would change the goal's meaning, authorization, or real-world risk. State the boundary directly instead of creating a field for it.

Define acceptance before execution. Completion requires evidence that every necessary condition holds; partial progress is not completion.

For open-ended research or long search tasks, read [the CDC prompt case](references/cdc-case.md) to see how a real goal excludes plausible false completions and governs evidence-seeking iteration.

## Examples

A routine goal can be one sentence:

```text
修复登录超时后的错误跳转；完成以新增回归测试通过且正常登录测试仍通过为准。
```

A real authorization boundary earns one additional sentence, not a new template:

```text
Prepare the customer-data migration and make its dry run pass against the approved fixture with a reviewed rollback plan. Do not execute the production migration without explicit approval.
```

The examples show required meaning, not required structure. Domain workflows belong to the relevant task skill and repository instructions.

## Output and validation

Aim for at most 1000 characters. Return only the contract unless a consequential assumption must be disclosed or the user asks for explanation.

Run `python3 scripts/lint_goal.py -` with the contract on stdin, or pass one or more files. The linter rejects empty contracts, explicit placeholder tokens, and text over 4000 characters; it warns above 2000. Use `--max-chars N` when the target has a stricter hard limit.
