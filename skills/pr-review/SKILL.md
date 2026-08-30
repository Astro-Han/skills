---
name: pr-review
description: "Review a pull request or queue from problem value through code correctness. Use for new review, rereview, batch review, or deciding findings and next steps. Do not use to implement feedback, report status, draft, merge, or monitor checks."
---

# PR Review

Review the production contract, not just the patch. Decide what must change, what must stay true, and who owns both. Stay read-only unless authorized.

## Identify the reviewed change

Read repository rules. Identify the patch, snapshot, or checkout; prefer the exact head SHA and state any mismatch. Gather available PR/Issue links, `+A/-D`, files, production/test split, CI, mergeability, and review state. Never mix versions. Name gaps, which do not block analysis.

## Check the problem first

Ask first:

> What problem does this PR solve? How does it solve it? Is the problem defined correctly? Do the problem definition and solution follow first principles and Occam's razor?

Seek a report, reproduction, log, or failing check; an Issue is optional. A new test proves neither demand nor prior failure. Call the problem **demonstrated**, **plausible but unverified**, **disproved**, or **mismatched**. Compare its scenario and expected result with PR coverage; do not accept a different scenario or unknown value.

## Follow the real code path

Turn the problem and solution into a falsifiable production contract: supported entry, changed result, preserved results, and responsible owner. Trace the shortest supported path that could prove the solution wrong before adjacent risks. Compare old and new behavior at the actual producer-consumer boundary, beyond helpers and fixtures.

Check whether the change:

- fixes one owner or adds copied state, synchronization, another loop, or a second source of truth;
- preserves supported callers and later use of changed data or state, including reachable failure, retry, concurrency, restart, and recovery;
- uses an extension point or adds an implementation, wrapper, state machine, or compatibility path;
- proves the real path: fixtures do not prove launchers, helpers do not prove callers, and in-process tests do not prove process races.

## Simplify the change

Every added path, test, owner, stored state, synchronization point, contract, and wrapper must justify its cost or disappear. Regression tests must fail on old behavior through the production owner, not a bypassed fixture. Prefer the fewest tests proving distinct obligations over a matrix. Before reporting no findings, require the smallest complete solution. Preserve live obligations until evidence proves they ended.

> Is this the smallest complete solution? What low-value tests, code, wrappers, states, or old paths can disappear? Can the result converge on one owner without losing required behavior?

Judge concepts, not lines; one process test can outweigh a fixture matrix.

## Report only real findings

Before P0–P3, show a supported entry reaching an observable consequence in production. If a link is unproven or blocked, record an evidence gap or **No finding**.

Classify the path:

1. normal or supported operation;
2. reasonable failure, reconnect, concurrency, or recovery;
3. attacker-controlled input or trust boundary;
4. several unsupported premises.

Category 4 is normally **No finding**, except for irreversible data loss, privilege breach, loss of a core source of truth, or broad outage. Grade reachable impact and recovery; low probability does not erase proof, and possibility is not proof.

- **P0** — blocks release.
- **P1** — fix before merge: reachable security exposure, data loss, money movement, sustained outage, wrong committed state, or unusable core workflow.
- **P2** — bounded or recoverable wrong behavior; usually non-blocking.
- **P3** — minor complexity without meaningful wrong behavior.

Give each finding's category, trigger, consequence, evidence, location, and smallest fix. Merge duplicates; report none.

## Give the conclusion

Use this order:

1. **Facts** — content, links, head, numeric `+A/-D`, production/test split, live facts, and gaps.
2. **Problem** — evidence, truth classification, and scenario match.
3. **Solution** — operation, owner, production path, necessities, and removals.
4. **Findings** — P0–P3 or none.
5. **Next step** — say plainly what should happen next and why.

Start with Facts. Never label the conclusion Approve, Comment, or Wait. Keep findings separate from merge and publication conditions; put pending CI, stale head, human approval, or manual acceptance under Next step. If content is unverified, name the snapshot and require refresh before action; never call it approvable. For user-visible changes, name manual checks, including Astryx primitives when standard.

For a queue, delegation, rereview, or public review, read [references/queue-and-publication.md](references/queue-and-publication.md) first.

Done means the review states its evidence boundary, judges value, follows production code, accounts for changes and removals, and calibrates findings.
