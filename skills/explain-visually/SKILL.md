---
name: explain-visually
description: "Turn complex technical work or decisions into audience-calibrated explanations, using a visual artifact when it materially helps. Use when the user asks for an explanation for a PM or non-expert, an ELI5-style explanation, an illustrated explainer, infographic, mobile long image, or HTML-to-image artifact. Do not use for ordinary factual answers, study or coaching, implementation documentation, or presentation decks."
---

# Explain Visually

Make the important idea easy to grasp without making it less true.

## Find the story

Identify the audience, the decision or question they need answered, and the verified facts that constrain the answer. Infer an explicit audience; ask only when different audiences would need materially different stories. Check named code, PRs, incidents, or sources before simplifying them.

Write the one-sentence takeaway first. Build the explanation around the user's experience and consequences, not the implementation order. Use technical details as evidence. Replace jargon with plain language or define the smallest necessary term. Never turn unknown or conditional behavior into certainty.

Choose only the structure the idea needs:

- an intuition or analogy when the user needs to feel why a mechanism works;
- a flow or state diagram when sequence, ownership, or boundaries matter;
- a comparison when scenarios, options, or tradeoffs matter;
- prose alone when a visual would only decorate the answer.

For a substantial explainer, a reliable arc is: why it matters, the mental model, the old problem, the new rule, representative scenarios, and what to remember. Delete any stage that does not change understanding.

## Make the artifact

Use the environment's visual or design guidance when available. For information-bearing diagrams or dense text, prefer deterministic HTML/CSS or SVG over generated imagery so wording, layout, and relationships stay exact. Use image generation only when real illustration materially carries the explanation, never to render critical text.

For a shareable mobile long image, produce an editable HTML source and render it at a fixed mobile-friendly width, normally 1080 px. Give the piece one visual metaphor or organizing idea; do not stack generic cards. Keep body text readable after phone scaling, use color to encode meaning, and preserve a clear hierarchy.

## Prove it works

Inspect the rendered artifact, not only its source. Check the full image and representative crops for text rendering, line breaks, clipping, overflow, contrast, diagram continuity, and accidental density. Iterate until it reads cleanly on a phone.

Deliver the explanation plus the final artifact and editable source. Done means the intended audience can tell what changed, why it matters, how common scenarios behave, and which limits remain—without needing the original technical material.
