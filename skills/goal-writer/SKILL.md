---
name: goal-writer
description: Draft or review bounded, testable goals. Use only when the user explicitly asks to create, revise, or review a goal, invokes `/goal`, or asks to use the goal feature.
---

# Goal Writer

Turn rough intent into the smallest copy-ready execution contract that makes completion decidable. Produce the contract; do not activate it unless explicitly asked.

## Draft

1. Choose the target surface. Use `/goal` only for Codex or a product that supports it; otherwise use `Goal:` or the product's native format. Match the user's language.
2. Read cheap, relevant context first: the request, named sources, repo instructions, current state, and known verification commands. Distinguish facts from assumptions.
3. Ask only when missing information materially changes scope, risk, ownership, cost, or product direction. State low-risk assumptions and continue.
4. Preserve the requested ambition. Do not silently reduce a complete product to a demo, invent a quota or time limit, or turn a risky final objective into discovery only.
5. Write one coherent acceptance decision containing:
   - the observable result that should exist; and
   - the criterion for accepting that result as complete.
6. Add another fact only when deleting it would change the goal's meaning, authorization, or real-world risk. State the specific boundary directly; do not add empty headings or a standard field list.
7. Run the linter before returning the contract. The linter catches mechanical defects; it does not prove that the result or acceptance criterion is sufficient.

The acceptance criterion is the rule defined before execution. Tests, screenshots, logs, diffs, artifacts, or external state observed afterward are evidence used to apply that rule. One acceptance decision may require several conditions to hold together; partial progress is not completion.

## Examples

A routine goal can be one line:

```text
/goal 修复登录超时后的错误跳转；完成以新增回归测试通过且正常登录测试仍通过为准。
```

A real authorization boundary earns one additional sentence, not a new template:

```text
Goal: Prepare the customer-data migration and make its dry run pass against the approved fixture with a reviewed rollback plan. Do not execute the production migration without explicit approval.
```

These examples demonstrate the required meaning, not a required structure. Context, scope, non-goals, constraints, iteration instructions, pause conditions, and report formats belong in a goal only when the specific task needs them to prevent a different interpretation, an unauthorized action, or a false completion claim. Otherwise omit them. Domain workflows belong to the relevant task skill and repository instructions.

## Output

Keep the contract within the target product's limit; use 4000 characters as the default hard ceiling. Return the contract first. Add only short notes explaining a consequential assumption or boundary. If the user asks for just the goal, return only the contract.

## Validate

Resolve paths relative to this file:

```bash
python3 scripts/lint_goal.py <goal-file.md>
```

Use `python3 scripts/lint_goal.py -` for stdin and `--max-chars N` for a stricter product limit.
