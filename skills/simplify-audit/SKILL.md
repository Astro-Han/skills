---
name: simplify-audit
description: Audit an existing repository or scoped architecture area for actionable and decision-gated simplification opportunities. Use when asked to find what can be removed or consolidated, reduce codebase-wide maintenance complexity, or identify obsolete or duplicated authorities, states, paths, contracts, or representations. Do not use to implement an already chosen change, fix a bug, optimize performance, or perform general code review without a simplification goal.
---

# Simplification Audit

Find removals and consolidations whose maintenance cost exceeds their present value. The unit of simplification is a concept, authority, state, path, contract, coordination mechanism, or representation that can disappear — not a line count.

Discover aggressively: the audit's value is the provably deletable surface it uncovers, not the safety of its report. Audit only: do not edit production code or turn the report into an implementation plan; naming a decisive verification step is fine.

## Establish coverage

Read repository instructions and sources of current architectural authority. Enumerate the surfaces where behavior enters, leaves, or persists — shipped deliverables, entry points and startup composition; configuration, environment variables, feature flags, and deployment manifests; dynamic wiring such as DI, registries, reflection, dynamic import, string lookup, generated code, and serialization hooks; persisted artifacts, queues, events, and replay/resume inputs; public APIs, CLIs, file formats, protocols, webhooks, extension contracts, and operational tooling. Trace each maintained top-level surface to the shipped behavior, contract, or operational obligation sustaining it. Slice by responsibility and authority, not file count; mark each slice **Reviewed**, or name the gap that keeps it from being Reviewed. Independent slices may be investigated in parallel; the primary agent owns the final evidence check and cross-slice synthesis. Keep the requested boundary as candidate scope; read adjacent producers and consumers as evidence without silently widening it.

## Presume suspicion

Assume accidental complexity is widespread. An internal concept is presumptively suspicious unless current evidence ties it to at least one of: a demand chain ending in shipped behavior; a supported external or extension contract with actual demand; a boundary carrying real ownership, isolation, policy, security, or invariants; a persisted-data, deployed-version, or compatibility obligation; a current operational obligation (observability, recovery, rate limiting, audit, compliance).

These are retention claims, never retention proof: code exists and is called; internal modules call each other; tests cover it; documentation restates the implementation; naming or architectural symmetry implies it belongs; hypothetical reuse or future flexibility; the pattern is widely copied; deletion would touch many call sites.

Treat something as an explicit design decision only when current architectural authority states its rationale, constraints, and intended ownership — never infer one from prevalence, tests, or naming. Do not reopen a valid explicit decision unless present evidence changes a premise, reveals an unconsidered material cost, or shows the promised demand or ownership is gone. Missing rationale weakens the retention case but does not alone justify deletion.

## Hunt

Derive per deliverable the smallest set of concepts, states, and contracts that satisfies its evidenced behavior and obligations; investigate the largest gaps between that minimum and the current composition first. The minimum is a discovery lens, not a target design. A chain that ends inside a group of mutually supporting internal consumers establishes no independent demand.

Actively search for (each is a lead, not a conclusion):

- duplicate authorities or representations of one fact; mirrored or derivable-but-persisted state; parallel paths kept consistent only by synchronization;
- interface, factory, registry, strategy, or plugin machinery with one implementation or one semantic consumer;
- layers that mostly delegate — services, facades, adapters, or wrappers passing calls through unchanged; a few non-trivial methods do not justify the layer: propose folding it into its natural owner and rehoming the exceptions;
- duplicated domain models, DTOs, or schemas with mapper chains; serialize-then-reparse or convert-and-reconvert paths; one business rule repeatedly validated, defaulted, or translated;
- feature flags, config branches, fallback or old/new paths, and migration scaffolding with only one proven live value or no supported producer;
- production APIs, hooks, or helper layers whose only consumer is tests; complexity kept alive only by tests, docs, or historical machinery;
- abstractions justified only by future reuse, symmetry, or "may swap later"; product-shaped generality — multi-backend, multi-tenant, live reconfiguration, pluggability — that no product owner currently demands; escape hatches added to bypass another abstraction; responsibilities implemented outside their natural owner;
- defensive copies, freezes, and validators at same-process trusted boundaries — name where each value comes from and who owns it next; tests built on hostile getters or post-handoff mutation evidence a speculative contract, not a reason to keep it;
- several mechanisms mirroring one liveness, settlement, or lifecycle fact in async code — propose a single owner, but preserve machinery protecting rollback, callback containment, first-terminal-outcome arbitration, or dispose-to-quiescence;
- hand-rolled infrastructure (retry, parsing, framing, globbing, diffing) that a well-maintained dependency or platform builtin already provides — a dependency swap is a valid simplification when net deletion (implementation + dedicated tests + docs − remaining glue) is real.

Simplifications compose. After closing a finding, re-derive the minimum for its neighbors: a layer that becomes pure delegation, a state that becomes derivable, or a contract that loses its last consumer once another finding lands is itself a finding — report it with its prerequisite named and size the chain's disappearance surface together. Do not let early strong findings end the hunt; the largest wins often sit in the biggest, most defended surfaces.

## Trace demand

Use demand chains for surface-sized leads and exact-symbol, exact-string, or representation searches for local ones. Before concluding absence, confirm the search tool does not silently skip files (binary detection, ignore rules, unindexed paths), then check the enumerated surfaces for a connection a static call graph misses — dynamic wiring, configuration, persistence, replay/resume, and published contracts all reach code that nothing appears to call.

Usage is retention evidence, not proof; architecture states intended ownership; resolve conflicts among ownership, demand, and usage. For a compatibility path, absence of a current writer is insufficient — check supported persisted artifacts, deployed versions, replay/resume, rolling upgrades, and third-party producers before its reader can disappear. Public and extension contracts require checking ecosystem demand; existence or documentation alone establishes none.

Do not read every file. A slice is Reviewed when its top-level surfaces, demand chains, and dynamic connections have been investigated far enough to disposition credible leads.

## Prove

A lead becomes a **Candidate** only when its deletion proof establishes: the current authority, production consumers, demand chain, and strongest retention reason stated in its most favorable form; the whole-system disappearance surface; what is added or moved and why the result is still a strict net reduction; why the strongest retention reason no longer applies; and the capability given up, impact radius, and material uncertainty. The proof is closed only when the retention reason is resolved and net reduction does not depend on a future implementation choice.

The burden is asymmetric: for a bounded internal lead, exhaustive evidence within the affected boundary suffices — do not demand nonexistent historical rationale or refutation of purely theoretical uses. Public contracts, supported extensions, persisted representations, deployed-version compatibility, replay/resume paths, and third-party producers always require the full proof.

Behavior preservation is not a proof requirement: a candidate may change behavior slightly when the new behavior is still reasonable and easier to explain — record the difference as capability given up.

## Report in three tiers

**Candidate** — closed proof; eligible for implementation priority.

**Deletion probe** — likely accidental complexity with a clear disappearance surface and one or few bounded, decisively checkable uncertainties. Do not drop a high-signal lead just because one bounded verification is missing. State: the suspected disappearing concept and why it reads as accidental; observed consumers and traced demand; the strongest plausible retention reason; the single decisive check; and how a failed check downgrades it. Report at most 10; no implementation priority — state expected leverage only.

**Decision gate** — a genuinely open product or architecture choice. A gap closable by searching, tracing, or reading configuration and artifacts is an evidence gap or a probe, not a gate. State: the decision, what each choice keeps or removes, the disappearance surface, the strongest retention reason, and the missing evidence or policy. Never an implementation recommendation.

Omit observations that only say code looks complex, layered, or inelegant. Cosmetic defects, naming, mechanical file merges, like-for-like abstraction swaps, and pure line-count wins are out of scope unless they embody a recurring maintenance obligation or a duplicate authority.

## Prioritize

Priorities apply to Candidates only and describe when implementation is worth it, not defect severity: **P0** active harm, blocked work, or spreading complexity; **P1** high leverage, real current cost, sufficient evidence; **P2** worthwhile, ordinary urgency; **P3** modest value, opportunistic. Any priority may be empty; no ranking within a priority; no quota.

## Close

Merge findings that share one underlying simplification: report the concept once, the rest as impact surface. Return:

1. a coverage table with every slice, its status, and remaining gaps;
2. Candidates grouped P0–P3;
3. Deletion probes;
4. Decision gates.

If evidence or access blocks closure, report a partial audit without full-scope claims. Stop when the coverage table accounts for the requested scope; every claim traces to production evidence rather than tests or restated docs; no underlying simplification is reported twice; no uncertainty is hidden as certainty; and no material high-signal lead was omitted merely because absolute certainty was unreachable.
