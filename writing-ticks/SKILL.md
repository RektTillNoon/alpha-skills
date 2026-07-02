---
name: writing-ticks
description: Audit writing for signs commonly associated with AI-generated or machine-edited prose. Use when reviewing drafts, articles, docs, comments, PR text, marketing copy, or pasted writing to identify AI-writing tells, separate observations from inferences, and revise toward natural, specific prose without making unsupported authorship claims.
---

# Writing Ticks

## Overview

Use this skill to audit prose for AI-writing signals, weigh those signals cautiously, and revise the text so it reads more specific, grounded, and human.

## Workflow

1. Establish the writing context: audience, venue, purpose, desired voice, and whether the user wants an audit, a rewrite, or both.
2. Read the text once for meaning before marking any signals.
3. Read `references/ai-writing-signs.md` when the request asks for an AI-writing audit, AI tell review, detector-style pass, or cleanup of "AI-sounding" prose.
4. Separate observations, inferences, and assumptions. Never present a stylistic pattern as proof of authorship.
5. Classify signals by weight:
   - **Mechanical artifact**: visible model residue, placeholders, refusal/apology scaffolding, malformed markup, fabricated citations, or instruction leakage.
   - **Strong signal**: multiple concrete issues such as generic filler, unsupported confident claims, abrupt context drift, mismatched citations, or tone shifts.
   - **Soft signal**: polished but generic rhythm, stock transitions, balanced-summary structure, or bland abstractions.
6. Revise the prose by preserving meaning, cutting generic scaffolding, adding concrete detail, verifying claims, and making rhythm fit the author's actual context.
7. Return the cleanest useful output for the user's request: findings only, rewrite only, or findings plus rewrite.

## Output Standard

Lead with the practical judgment. Use plain language such as "This has a few AI-writing tells" or "I do not see strong AI-writing signals." Avoid saying "this is AI-written" unless the text contains explicit machine artifacts.

For audits, use this shape:

```markdown
Judgment: [none / light / moderate / strong / mechanical artifact]

Observations:
- [Weight] Concrete issue and why it matters.

Inference:
- What the pattern suggests, stated cautiously.

Fix:
- Specific edit direction or rewritten passage.
```

For rewrites, keep the author's intent and useful quirks. Do not sand the prose into generic professionalism.

## Guardrails

- Do not accuse a person of using AI from style alone.
- Do not optimize for passing commercial AI detectors; improve prose quality, specificity, and evidence.
- Do not remove all personality. Preserve precise, odd, or local phrasing when it helps.
- Do not over-weight punctuation, tidy structure, or formal grammar. Humans use those too.
- Fact-check citations and named claims when possible before treating them as evidence.
