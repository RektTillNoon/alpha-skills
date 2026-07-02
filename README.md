# Alpha Skills

A public skill collection for agent workflows.

## Install The Collection

Install missing top-level skills from this collection without re-downloading
skills that are already installed:

```bash
python3 scripts/install_missing_skills.py --yes
```

Install only specific missing skills:

```bash
python3 scripts/install_missing_skills.py clean owner-check --yes
```

The installer checks `npx skills@latest list --global --json`, skips matching
skill names that are already installed, and only calls `npx skills@latest add`
for missing skills. Use `--project` when you intentionally want project-scoped
installs instead of global installs.

Direct install from the collection is still available:

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

Install any top-level skill from this collection with:

```bash
python3 scripts/install_missing_skills.py <skill-name> --yes
```

| Skill | Use |
| --- | --- |
| `clean` | Behavior-preserving cleanup and simplification for existing codebases. |
| `clean-commit` | Cleanup plus an intentional, scoped git commit workflow. |
| `clean-merge-push` | Owner-clean, commit, merge, verify, push, and return-to-branch workflow. |
| `evolutionary-5-step` | Run one bounded goals/problems/diagnosis/design/do improvement pass. |
| `investigate-fix` | Take a concrete bug from symptom to root cause, fix, regression, and proof. |
| `owner-check` | Find the real owner of architecture-sensitive behavior before patching. |
| `owner-clean` | Post-change owner-check plus cleanup pass for Codex's own work. |
| `stateful-planning-protocol` | Harden plans for systems with authoritative, mirrored, cached, or transported state. |
| `technical-design-dossier` | Create repo-grounded TeX technical design dossiers and companion PDFs. |
| `tty-design` | Design and refine terminal TTY/TUI command flows. |
| `writing-ticks` | Audit writing for AI-like tells and revise toward natural prose. |

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

## Repository Layout

```text
alpha-skills/
├── README.md
├── LICENSE
├── <skill-name>/
│   ├── SKILL.md
│   └── agents/                 # optional Codex metadata
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
├── tests/
└── .github/workflows/
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
