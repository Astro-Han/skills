---
name: simplify-audit
description: Audit an existing repository or scoped architecture area for simplification opportunities, separating proven removals from those still blocked on a fact or a decision. Use when asked to find what can be removed or consolidated, reduce codebase-wide maintenance complexity, or identify obsolete or duplicated authorities, states, paths, contracts, or representations. Do not use to implement an already chosen change, fix a bug, optimize performance, or perform general code review without a simplification goal.
---

# Simplification Audit

Find removals and consolidations whose maintenance cost exceeds their present value. The unit is a concept, authority, state, path, contract, or representation that can disappear — not a line count. Discover aggressively: the audit's value is the deletable surface it uncovers, not the safety of its report. Audit only — do not edit production code or turn the report into an implementation plan.

## Establish coverage

Read repository instructions and current architectural authority. Enumerate the surfaces where behavior enters, leaves, or persists: entry points and startup composition; configuration, flags, and deployment manifests; dynamic wiring (DI, registries, reflection, dynamic import, string lookup, generated code, serialization); persisted artifacts, queues, events, and replay/resume inputs; public APIs, CLIs, formats, protocols, and extension contracts. Slice by responsibility and authority, not file count; mark each slice **Reviewed**, or name the gap. Keep the requested boundary as candidate scope; read adjacent producers and consumers as evidence without widening it.

## Presume suspicion

Assume accidental complexity is widespread. An internal concept is suspicious unless current evidence ties it to: a demand chain ending in shipped behavior; an external or extension contract with actual demand; a boundary carrying ownership, isolation, policy, security, or invariants; a persisted-data, deployed-version, or compatibility obligation; an operational obligation (observability, recovery, rate limiting, audit, compliance).

These are retention claims, never proof: code exists and is called; internal modules call each other; tests cover it; docs restate the implementation; naming or symmetry implies it belongs; hypothetical reuse; the pattern is widely copied; deletion would touch many call sites.

Treat something as an explicit design decision only when current architectural authority states its rationale and ownership — never infer one from prevalence, tests, or naming, and never read an unmade decision as absent demand. Do not reopen one unless evidence changes a premise or shows the promised demand is gone.

## Hunt

Derive per deliverable the smallest set of concepts, states, and contracts its evidenced behavior and obligations require; investigate the largest gaps first. A chain ending inside a group of mutually supporting internal consumers establishes no independent demand.

Search for (each a lead, not a conclusion):

- duplicate authorities or representations of one fact; mirrored or derivable-but-persisted state; parallel paths kept consistent only by synchronization;
- interface, factory, registry, strategy, or plugin machinery with one implementation or one semantic consumer;
- layers that mostly delegate — services, facades, adapters, wrappers; a few non-trivial methods do not justify the layer: fold it into its natural owner and rehome the exceptions;
- duplicated domain models, DTOs, or schemas with mapper chains; serialize-then-reparse paths; one business rule repeatedly validated, defaulted, or translated;
- feature flags, config branches, fallback or old/new paths, and migration scaffolding with one proven live value or no supported producer;
- production APIs or helpers whose only consumer is tests; complexity kept alive only by tests, docs, or historical machinery;
- abstractions justified only by future reuse, symmetry, or "may swap later"; product-shaped generality no owner currently demands; escape hatches bypassing another abstraction; responsibilities implemented outside their natural owner;
- defensive copies, freezes, and validators at same-process trusted boundaries — name where each value comes from and who owns it next;
- several mechanisms mirroring one liveness or lifecycle fact in async code — propose a single owner, but preserve machinery protecting rollback, callback containment, first-terminal-outcome arbitration, or dispose-to-quiescence;
- hand-rolled infrastructure (retry, parsing, framing, globbing, diffing) a maintained dependency or platform builtin already provides, when net deletion is real.

Simplifications compose. After closing a finding, re-derive the minimum for its neighbors: a layer that becomes pure delegation, a state that becomes derivable, or a contract left without consumers is itself a finding — report it with its prerequisite named. Do not let early strong findings end the hunt.

## Trace demand

Use demand chains for surface-sized leads and exact-symbol or exact-string searches for local ones. Before concluding absence, confirm the search tool does not silently skip files (binary detection, ignore rules, unindexed paths), then check the enumerated surfaces: every one of them reaches code nothing appears to call.

Architecture states intended ownership; resolve conflicts between it and observed usage. For a compatibility path, absence of a current writer is insufficient — check persisted artifacts, deployed versions, replay/resume, rolling upgrades, and third-party producers before its reader can disappear. Public and extension contracts require ecosystem demand; documentation alone establishes none.

Do not read every file: a slice is Reviewed once its surfaces and demand chains are investigated far enough to disposition credible leads.

## Prove

A lead is **Ready to cut** only when its deletion proof establishes: the current authority, production consumers, and strongest retention reason in its most favorable form; the whole-system disappearance surface; what is added or moved and why the result is still a net reduction; why the retention reason no longer applies; and the capability given up. The proof is closed only when net reduction does not depend on a future implementation choice.

The burden is asymmetric: for a bounded internal lead, exhaustive evidence within the affected boundary suffices — do not demand nonexistent historical rationale or refutation of theoretical uses. Public contracts, supported extensions, persisted representations, deployed-version compatibility, and replay/resume paths always require the full proof.

A ready-to-cut finding may change behavior slightly when the new behavior is still reasonable and easier to explain — record the difference as capability given up.

## Report in three tiers

A tier says what is still missing before the concept can disappear: nothing, one fact, or one decision.

**Ready to cut** — closed proof. Prioritize by when implementation is worth it, not defect severity: **P0** active harm, blocked work, or spreading complexity; **P1** high leverage, real current cost; **P2** ordinary urgency; **P3** opportunistic. Any priority may be empty; no quota.

**Needs one check** — likely accidental complexity with a clear disappearance surface, blocked on a single fact. Settle that fact yourself whenever the repository can answer it; a check you can run is not a finding. This tier is for facts the repository cannot reach — ecosystem demand, deployed versions, third-party producers, an owner's intent — and no high-signal lead is dropped because one is out of reach. State the suspected concept and why it reads as accidental, observed consumers and traced demand, the strongest retention reason, the open fact, and who can settle it. At most 10; no priority — state expected leverage.

**Needs a decision** — an open product or architecture choice no amount of reading settles. Anything a check could close belongs to a tier above. State the decision, what each choice keeps or removes, the disappearance surface, and the missing policy. Never an implementation recommendation.

Omit observations that only say code looks complex or inelegant. Cosmetic defects, naming, mechanical file merges, and pure line-count wins are out of scope unless they embody a recurring maintenance obligation or a duplicate authority.

## Close

Merge findings that share one underlying simplification: report the concept once, the rest as impact surface. Return a coverage table with every slice and its gaps, then the three tiers in order. If evidence or access blocks closure, report a partial audit without full-scope claims. Every claim must trace to production evidence rather than tests or restated docs, and no high-signal lead may be dropped merely because certainty was unreachable.
