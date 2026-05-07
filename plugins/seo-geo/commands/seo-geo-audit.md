---
name: seo-geo-audit
description: Run the public-safe SEO/GEO audit workflow for the current project.
argument-hint: "[project root or site URL]"
---

Use the canonical workflow in `plugins/seo-geo/skills/seo-geo-audit/SKILL.md`.

Run an SEO/GEO audit for `$ARGUMENTS` when provided, otherwise use the current
project. Classify evidence as `local`, `connector`, `live web`, or `inference`
before scoring. Redact credentials, tokens, cookies, private URLs, customer data,
personal data, and proprietary excerpts before quoting or writing any output.

If configured providers or evidence exports are missing, report the gap as
`missing evidence`; do not infer fake results or treat unavailable data as poor
performance.
