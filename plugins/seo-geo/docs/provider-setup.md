# Provider Setup

The SEO/GEO plugin does not ship credentials, connector state, `.env` files, or
provider-specific secret templates. Credentials live in the host agent, MCP
server, connector, browser profile, or user-selected project environment.

## Optional Evidence Sources

Use any combination of these sources. A complete audit is not required to have
all of them.

| Source | Typical Input | Credential Location |
| --- | --- | --- |
| Built site | local `dist`, `out`, or generated pages | none |
| Sitemap and robots | public URL or local files | none |
| Crawl export | JSON, CSV, or report from a crawler | none in plugin |
| Analytics export | redacted CSV or report | host connector or user export |
| Search Console | export or configured connector | host connector |
| Access logs | redacted sample or aggregate report | user-provided local evidence |
| Third-party SEO tools | Ahrefs, Semrush, DataForSEO, or similar exports | provider tool or MCP server |
| Live web/search | browser, search, or Exa-style tool | host tool configuration |

## Missing Evidence Behavior

When an evidence source or credential-backed provider is unavailable, the agent
must mark it as `missing evidence`. It must not fabricate traffic, rankings,
queries, crawl results, competitor data, or GEO benchmark results.

## Safe Output Rules

- Summarize sensitive evidence by category, not by raw value.
- Redact private paths, query strings, headers, cookies, user identifiers, and
  credential-like substrings before citing evidence.
- Keep provider setup instructions generic. Do not commit real keys, account
  IDs, analytics IDs, client IDs, client secrets, or refresh tokens.
