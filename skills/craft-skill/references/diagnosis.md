# Diagnose a skill

Load this reference only when an existing skill behaves incorrectly or costs more than its value. Start from the observed symptom; do not apply every remedy.

| Symptom | Check | Smallest useful move |
| --- | --- | --- |
| The skill is missed or called on adjacent tasks | Metadata does not name a real branch, or ignores the platform's invocation model | Rewrite the disputed trigger and its closest non-trigger; do not add synonyms without a new branch |
| The agent follows the description but skips the body | The description leaks a usable process summary | Keep identity and triggers in metadata; move execution into the body |
| A conditional path bloats every run | Branch-only reference is inline, or its pointer is vague | Move it behind a direct condition-bearing pointer |
| The agent drifts between approaches | The target behavior or leading concept is weak | Name the desired process with a precise concept already understood by the model |
| A step ends early | Its completion criterion is vague while later steps pull attention forward | Make done/not-done checkable first; split the sequence only if the criterion cannot be sharpened and rushing is observed |
| The agent finishes the steps but does too little work | The criterion is checkable but undemanding | Require the observable coverage the task actually needs |
| The skill keeps prohibiting the same failure | The unwanted behavior is repeatedly activated by negation | State the positive target and reserve prohibitions for irreducible guardrails |
| Multiple runs rediscover the same facts | Stable knowledge has no owner | Move it once into a reference and point to it from the branch that needs it |
| Multiple runs rewrite the same fragile operation | Deterministic work is expressed as prose | Bundle and test the smallest script that owns the operation |
| The skill works only on the examples used to revise it | Acceptance reused its training cases | Check untouched or newly generated cases before claiming general improvement |
| The skill grows without a clear new behavior | Sediment, duplication, sprawl, or no-op instructions have accumulated | Apply the sentence-level removal test; restore a single source of truth and disclose branch-only detail |
| The skill is rigid where context should decide | Degrees of freedom are lower than task fragility requires | Replace needless procedure with the principle and completion criterion that matter |

Use observed transcripts only when they can locate wasted steps, ignored instructions, or repeated work worth extracting. A plausible diagnosis without discriminating evidence is not a reason to add text.
