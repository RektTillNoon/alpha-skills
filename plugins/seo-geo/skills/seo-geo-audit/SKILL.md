---
name: seo-geo-audit
description: Run public-safe SEO and GEO audits for any project using local evidence first, then optional current external evidence when available.
---

# SEO/GEO Audit

Use this skill when the user asks for an SEO audit, GEO audit, AI-search
visibility review, content opportunity map, answer-engine readiness review,
Search Console analysis, crawl analysis, log analysis, or reusable search
briefing for any project.

## First Principles

- Start from the current project, not a remembered brand or prior audit.
- Treat every project as prelaunch or evidence-limited until local evidence
  proves otherwise.
- Separate first-party evidence, live external evidence, and inference.
- Prefer entity clarity, answerability, proof, crawlability, internal linking,
  technical accessibility, and content usefulness over keyword stuffing.
- Keep search overlap separate from direct product competition.
- Never silently treat missing connectors, missing exports, or blocked crawls as
  poor performance.

## Public-Safe Rules

- Do not copy raw credentials, tokens, cookies, private keys, analytics IDs,
  private URLs, customer records, email addresses, personal data, or internal
  planning excerpts into the final report.
- Refer to sensitive sources by role and path shape, such as `analytics export`,
  `access log sample`, `crawl export`, or `local planning document`.
- Redact sensitive substrings before quoting a file path, URL, header, query
  string, log line, or environment variable.
- If a finding depends on sensitive evidence, summarize the behavior and cite
  the evidence category instead of pasting the raw evidence.
- Do not write audit artifacts outside the user-selected project or output
  directory.
- Do not create project-specific defaults in this skill. Project packs belong in
  project repositories, not in the public plugin.

## Workflow

1. Discover context:
   - Identify the project root, site URL if provided, app framework, generated
     site output, sitemap, robots file, routes, content directories, docs, and
     available evidence exports.
   - If the user provides a GitHub URL, inspect the local read-only mount first
     when available, and use a writable checkout only for edits.
2. Classify evidence:
   - Mark each source as `local`, `connector`, `live web`, or `inference`.
   - Mark the audit as `draft`, `prelaunch`, `local-only`, or `evidence-backed`.
3. Check safety:
   - Scan planned citations and report snippets for credentials, customer data,
     private paths, query strings, and proprietary excerpts.
   - Redact before writing or presenting results.
4. Audit:
   - Technical SEO: crawlability, indexability, canonical URLs, metadata,
     structured data, sitemap, robots rules, page status, performance signals,
     and accessibility blockers.
   - Content SEO: topic coverage, page intent, information gain, internal links,
     proof points, comparisons, glossary needs, and conversion paths.
   - GEO readiness: entity definitions, answerable questions, concise claims,
     citation-worthy proof, source clarity, author or organization clarity,
     schema support, and retrieval-friendly page structure.
5. Produce outputs:
   - Keep reports concise and evidence-labeled.
   - Include assumptions and manual next steps when evidence is missing.
   - Save artifacts only when the user asks for files or the workflow requires
     checked-in deliverables.

## Output Contract

Use these sections unless the user requests a different format:

- Executive Summary
- Evidence Used
- Evidence Bundle Readiness
- Scores
- Top Findings
- Priority Backlog
- Page Briefs
- GEO Benchmark
- Assumptions
- Next Steps

## Scoring Contract

Use a 0-5 scale when scoring:

- `0`: no usable evidence or severe blocker
- `1`: present but broken or misleading
- `2`: partial, thin, or inconsistent
- `3`: adequate baseline
- `4`: strong with minor gaps
- `5`: best-in-class for the project stage

Always explain when a score is capped by missing evidence.

## Next Steps

After each pass, tell the user:

- what was actually inspected
- what was inferred
- which evidence would improve confidence
- what they need to do manually, if anything
