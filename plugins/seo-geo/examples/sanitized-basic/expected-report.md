# SEO/GEO Audit Example

## Executive Summary

`example.invalid` has a crawlable two-page baseline with clear home-page entity
language. The docs page needs a meta description and stronger internal links.

## Evidence Used

- Local sanitized crawler fixture from `evidence/crawl-summary.json`
- No connector-backed data was used

## Missing Evidence

- Search Console export
- Analytics export
- Live search benchmark

## Scores

- Technical SEO: 3/5
- Content SEO: 2/5
- GEO readiness: 2/5

## Top Findings

- The docs page has an empty meta description.
- Internal linking is thin on the docs page.
- There is not enough evidence to score query demand or answer-engine visibility.

## Priority Backlog

- Add a concise docs-page meta description.
- Add contextual links from the homepage to the docs page and from docs back to
  the primary product page.
- Provide a Search Console export or connector result before treating query
  performance as evidence-backed.

## Assumptions

- This is a local-only example report.
- Missing provider data is treated as missing evidence, not poor performance.
