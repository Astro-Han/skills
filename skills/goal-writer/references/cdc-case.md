# OpenAI CDC Prompt: A Real Goal Case

Use this case when drafting an open-ended research or long search goal where plausible partial results could look like completion.

Source: OpenAI, [Prompt used for “A Proof of the Cycle Double Cover Conjecture”](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf), two pages.

## What the goal does well

- It defines the requested result precisely enough to decide success: a complete proof of the stated conjecture for the full graph class.
- It names attractive but insufficient outcomes, including special cases, fixed-size computation, weaker covers, and reductions to another unproved conjecture. These exclusions matter because each could otherwise be mistaken for progress sufficient to return.
- It makes audit part of acceptance. Candidate proofs must survive checks against task-specific failure modes rather than a generic request to "verify carefully."
- It governs search by new evidence. Several independent routes stay alive; a blocked route reopens only after a materially new mechanism, invariant, or construction appears.
- It rejects status reports and vague optimism in favor of concrete lemmas, constructions, equations, or counterexamples.

The reusable lesson is not its length or headings. It is the tight connection between one non-degradable acceptance decision, the exact false completions most likely to fool the search, and an iteration rule that requires new information.

## What not to copy by default

- The 64-agent orchestration policy belongs to that execution environment, not to the mathematical goal itself.
- The eight-hour minimum is a time instruction, not evidence of completion, and may not be enforceable by the target runtime.
- The assumption that an affirmative proof exists is benchmark-specific and would bias ordinary research.
- Its public-search restriction protects that benchmark; it is not a general research rule.
- Repeated return prohibitions are justified only when the runtime is otherwise likely to stop at partial progress.

Do not turn these observations into a research template. Add a false-completion exclusion, audit condition, or iteration rule only when removing it would change what the agent accepts as complete or how it responds to new evidence.
