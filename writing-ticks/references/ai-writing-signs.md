# AI Writing Signals Reference

Source basis: Wikipedia's "Signs of AI writing" page, reviewed 2026-06-27. Treat this as a practical audit rubric, not a detector.

## Core Principle

Look for clusters and contradictions. One polished sentence, one em dash, or one generic phrase is weak evidence. A combination of machine residue, context drift, invented support, and generic phrasing is much stronger.

## Mechanical Artifacts

Give these the most weight:

- Visible assistant residue: refusals, apologies, disclosure-like phrases, task framing, or "here is the revised..." scaffolding left in final prose.
- Unresolved placeholders: bracketed notes, TODO-like fragments, missing names, copied prompt instructions, or template variables.
- Broken or inappropriate markup: fenced code in prose, raw HTML/XML/reference syntax, malformed Markdown, table syntax pasted into normal text, or stray editor annotations.
- Citation artifacts: invented titles, impossible dates, mismatched author/source details, URLs that do not support the claim, or references that look plausible but cannot be verified.
- Context contradictions: a paragraph confidently says something that conflicts with the surrounding document, the topic, the date, or the cited source.
- Abrupt register shifts: a human first-person voice suddenly becomes a neutral encyclopedia voice, customer-support voice, or policy-summary voice without a reason.

## Strong Prose Signals

Treat these as meaningful when several appear together:

- Generic framing that sounds useful but does not commit to a concrete point.
- Symmetrical summaries that cover "both sides" without source-specific stakes.
- Excessive hedging or universally true caveats where the context needs a decision.
- Repeated abstract nouns instead of exact actors, objects, dates, numbers, or mechanisms.
- Promotional uplift language, especially when the topic is mundane or factual.
- List-heavy structure that feels generated from the prompt rather than selected by an author.
- Explanations that restate the question, define obvious terms, or add filler before answering.
- Paragraphs that are locally fluent but do not advance the argument.

## Soft Signals

Use these only as supporting context:

- Very even sentence lengths and paragraph shapes.
- Stock transitions such as "however," "moreover," or "in conclusion" when they stack up.
- Formulaic contrast patterns such as "not just X, but Y."
- Over-neat summaries, generic examples, and context-free recommendations.
- Smooth tone that lacks the author's normal preferences, constraints, or irritations.
- Punctuation habits, including frequent em dashes or semicolons.

## Human Signals

These reduce concern when they are real, not pasted in mechanically:

- Specific tradeoffs, local constraints, and awkward-but-true details.
- Source-grounded claims with citations that actually support the sentence.
- Uneven but purposeful rhythm: short assertions mixed with longer explanation.
- Distinct author priorities, taste, humor, impatience, or domain vocabulary.
- Admissions of uncertainty tied to a concrete missing fact.
- Clear decisions about what to omit.

## Review Questions

Ask these while auditing:

1. What concrete claim does this sentence add?
2. Could this paragraph fit almost any topic if a few nouns changed?
3. Are the citations real, relevant, and sufficient?
4. Does the voice match the stated author, audience, and venue?
5. Is the structure earned by the material, or does it look like prompt fulfillment?
6. Are caveats useful, or are they generic safety padding?
7. Where would a knowledgeable human have used a sharper example, exception, or number?

## Revision Moves

- Cut throat-clearing and generic setup.
- Replace abstract categories with exact nouns, actions, dates, numbers, and constraints.
- Make the first sentence do real work.
- Prefer one clear claim over a balanced but empty paragraph.
- Keep useful roughness: directness, specificity, and personal priority often read more human than polished neutrality.
- Vary rhythm only where meaning benefits.
- Remove assistant scaffolding, placeholder text, and copied prompt language.
- Verify or remove unsupported citations and named claims.
- For comments or reviews, answer the point directly before adding context.

## Reporting Language

Use careful labels:

- **None**: no notable AI-writing signals.
- **Light**: a few soft signals, no mechanical artifacts.
- **Moderate**: several soft or strong signals that affect trust or voice.
- **Strong**: clustered generic prose, drift, unsupported claims, or repeated machine-like patterns.
- **Mechanical artifact**: visible model residue or verifiable fabricated support.

Prefer "This reads AI-shaped because..." over "This is AI-written."
