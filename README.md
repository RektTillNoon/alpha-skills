# Alpha Skills

A public skill collection for agent workflows.

## Install The Collection

Install from this collection:

```bash
npx skills@latest add RektTillNoon/alpha-skills
```

Preview available skills without installing:

```bash
npx skills@latest add RektTillNoon/alpha-skills --list
```

Check global installs from any directory before adding a skill again:

```bash
npx skills@latest list --global --json
```

Update installed skills instead of re-adding them:

```bash
npx skills@latest update
```

## Skills

## Plugins

### seo-geo

Provides a public-safe SEO/GEO audit plugin that can be used from Codex and
Claude Code. The plugin keeps one canonical skill body at
`plugins/seo-geo/skills/seo-geo-audit/SKILL.md` and exposes both
`.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` manifests.

The repo also includes `.claude-plugin/marketplace.json` so the public
repository can act as a Claude Code plugin marketplace. After the marketplace is
published and added in Claude Code, the plugin is intended to install as:

```bash
/plugin install seo-geo@alpha-skills
```

For local Claude Code development before publishing:

```bash
cc --plugin-dir /absolute/path/to/alpha-skills/plugins/seo-geo
```

After installation, Claude Code users can run:

```bash
/seo-geo-audit
```

For Codex plugin use, the repo includes `.agents/plugins/marketplace.json`
pointing at `./plugins/seo-geo`. In local development, add this repository as a
local plugin marketplace or load the plugin directory directly from:

```text
/absolute/path/to/alpha-skills/plugins/seo-geo
```

The top-level `npx skills@latest add RektTillNoon/alpha-skills` flow installs
top-level skills from this collection. It does not install the `seo-geo` plugin,
because `seo-geo` is intentionally packaged as a plugin, not a standalone skill.

Run the plugin contract test:

```bash
python3 -m unittest tests.test_seo_geo_plugin_public_contract
```

Provider credentials live in the host agent, MCP server, connector, browser
profile, provider CLI, or user-owned project environment. The plugin documents
provider setup in `plugins/seo-geo/docs/provider-setup.md` and security policy
in `plugins/seo-geo/SECURITY.md`.

### clean

Runs a constrained, behavior-preserving cleanup pass for existing codebases. It focuses on semantic clarity, dead-code removal, leaner APIs, nearby test cleanup, and narrow verification without turning cleanup into product work.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill clean
```

### clean-commit

Runs the same cleanup discipline with an intentional git commit workflow. It inspects unstaged work, avoids accidental staging, runs the discovered verification gate, and commits only when explicitly requested.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill clean-commit
```

### owner-check

Runs a representation-first ownership check for architecture-sensitive edits, canonical path cleanup, duplicated state, cache/lifecycle authority, render authority, and similar "who owns this behavior?" questions.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill owner-check
```

### technical-design-dossier

Creates decision-complete TeX Technical Design Dossiers and phased implementation plans grounded in the current repository state. Every `.tex` deliverable must include a rendered `.pdf` companion.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill technical-design-dossier
```

Remove the skill:

```bash
npx skills@latest remove technical-design-dossier
```

Alias:

```bash
npx skills@latest rm technical-design-dossier
```

## Repository Layout

```text
alpha-skills/
├── README.md
├── LICENSE
├── plugins/
│   └── seo-geo/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       │   └── seo-geo-audit.md
│       ├── docs/
│       │   └── provider-setup.md
│       ├── examples/
│       │   └── sanitized-basic/
│       ├── SECURITY.md
│       ├── README.md
│       └── skills/
│           └── seo-geo-audit/
│               ├── SKILL.md
│               └── agents/
│                   └── openai.yaml
├── clean/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
├── clean-commit/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── scripts/
│   │   └── inspect_unstaged_changes.py
│   └── tests/
│       ├── __init__.py
│       └── test_inspect_unstaged_changes.py
├── owner-check/
│   └── SKILL.md
└── technical-design-dossier/
    ├── assets/
    │   └── technical-design-dossier-template.tex
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        └── golden-example.md
```

This follows the public skill collection pattern used by repositories such as `mattpocock/skills`, where each skill is a top-level directory with a `SKILL.md` file and optional supporting files.

## Compatibility

- Codex: uses `.codex-plugin/plugin.json`; `.agents/plugins/marketplace.json`
  exposes repo-local plugin marketplace metadata; `SKILL.md` and
  `agents/openai.yaml` provide skill metadata where supported.
- Claude Code: uses `SKILL.md`; supporting files are optional.

## Local Development

Validate the skill structure with your local skill validator if available. For Codex:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py technical-design-dossier
```

## License

MIT
