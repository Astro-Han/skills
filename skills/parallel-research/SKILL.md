---
name: parallel-research
description: Research with parallel agents, independent evidence angles, and cross-validation. Use when the user explicitly asks for parallel or delegated research, or when a high-cost question materially benefits from independent evidence.
---

# Parallel Research

Split a research question only when independent searches are likely to reduce blind spots enough to justify the coordination cost.

## Shape the search

Define the question, the decision it informs, required recency, exclusions, and every material, non-overlapping evidence angle. Ask the user only when the scope is materially ambiguous; otherwise state any consequential assumption and proceed.

Assign one researcher per material, non-overlapping evidence angle. Run as many researchers concurrently as available subagent slots allow. When angles outnumber slots, launch the remainder as slots open until every material angle is covered. Every researcher is a leaf: it must not spawn, delegate, or invoke another research workflow.

## Research in parallel

Each researcher should:

- Search current public sources and prefer primary evidence.
- Vary queries enough to test the angle rather than repeat one search.
- Open key pages and return direct citations, not search snippets.
- Separate sourced facts from inferences and name important gaps or uncertainty.
- Stop when added searching is unlikely to change the conclusion.

## Validate in the main thread

The main thread coordinates, verifies decision-critical claims, resolves conflicts, and synthesizes the answer; it does not take a research angle. Compare results for agreement, contradiction, and missing coverage. Check numbers, dates, policies, availability, and technical behavior against the strongest primary sources. Downgrade stale, indirect, or single-source claims.

Synthesize the answer around verified findings, unresolved uncertainty, and the decision they support. Cite the underlying sources, never the agents. Save a durable report only when the user asks for one.
