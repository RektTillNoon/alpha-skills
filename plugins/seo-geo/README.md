# SEO/GEO Plugin

Public-safe SEO and GEO audit workflows for any project. The plugin is designed
to be installable by Codex and Claude Code from the same package.

## What It Provides

- A reusable `seo-geo-audit` skill for SEO, GEO, AI-search visibility, content
  readiness, and evidence-bundle reviews.
- A thin Claude Code slash command at `/seo-geo-audit` that routes to the same
  canonical workflow.
- Codex metadata at `.codex-plugin/plugin.json`.
- Claude Code metadata at `.claude-plugin/plugin.json`.
- Project-neutral instructions that avoid hard-coded brands, local paths,
  private URLs, credentials, or proprietary evidence.

## Layout

```text
seo-geo/
├── .codex-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── seo-geo-audit.md
├── docs/
│   └── provider-setup.md
├── examples/
│   └── sanitized-basic/
├── SECURITY.md
├── README.md
└── skills/
    └── seo-geo-audit/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```

## Public-Safe Operating Model

The skill must treat every project as unknown until it inspects local evidence.
It must not assume a specific company, product, site, analytics provider,
repository layout, or connector availability.

When credentials, analytics exports, logs, search-console exports, crawl data,
or internal planning docs are present, the skill should summarize findings
without copying sensitive values into reports. Outputs should cite evidence by
file type, source, and date when available, not by embedding raw credentials,
tokens, cookies, private URLs, customer data, or personal data.

## Claude Code Compatibility

Claude Code discovers plugin skills from `skills/<skill-name>/SKILL.md` under a
plugin root with `.claude-plugin/plugin.json`. This plugin keeps the same
`skills/` path for Codex and Claude Code so there is one canonical skill body.

The repository root also contains `.claude-plugin/marketplace.json`, which lets
the public repository act as a Claude Code plugin marketplace. Once that
marketplace is added in Claude Code, install with:

```bash
/plugin install seo-geo@alpha-skills
```

For local development before publishing, load the plugin directory directly:

```bash
cc --plugin-dir /absolute/path/to/alpha-skills/plugins/seo-geo
```

After installation, run:

```bash
/seo-geo-audit
```

## Codex Compatibility

Codex metadata lives at `.codex-plugin/plugin.json`. The repository root also
contains `.agents/plugins/marketplace.json`, which points Codex at this nested
plugin directory:

```text
./plugins/seo-geo
```

For local development, load that plugin directory directly or add the repository
as a local plugin marketplace. The collection-level `npx skills@latest add`
workflow installs top-level skills, not this nested plugin package by itself.

## Provider Setup

Provider setup is optional and external to this plugin. Credentials live in the
host agent, MCP server, connector, browser profile, provider CLI, or user-owned
project environment. See `docs/provider-setup.md` for supported evidence source
types and missing-evidence behavior.

## Security

See `SECURITY.md` for redaction rules and repeatable publish-safety checks. This
plugin must not contain real credentials, `.env` files, `.mcp.json`, connector
state, private URLs, customer data, or provider-specific secret templates.

## Example

See `examples/sanitized-basic/` for a fake evidence bundle and expected report
using `example.invalid`.

## Local Validation

Run the public contract test:

```bash
python3 -m unittest tests.test_seo_geo_plugin_public_contract
```

Run all plugin contract tests:

```bash
python3 -m unittest discover -s tests
```
