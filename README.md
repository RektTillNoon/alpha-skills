# Alpha Skills

A public skill collection for agent workflows.

## Install The Collection

Install any skill from this collection with:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill <skill-name>
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

### tex-spec-writer

Creates decision-complete TeX specs and phased implementation plans grounded in the current repository state. Every `.tex` deliverable must include a rendered `.pdf` companion.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill tex-spec-writer
```

Remove the skill:

```bash
npx skills@latest remove tex-spec-writer
```

Alias:

```bash
npx skills@latest rm tex-spec-writer
```

## Repository Layout

```text
alpha-skills/
├── README.md
├── LICENSE
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
└── tex-spec-writer/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

This follows the public skill collection pattern used by repositories such as `mattpocock/skills`, where each skill is a top-level directory with a `SKILL.md` file and optional supporting files.

## Compatibility

- Codex: uses `SKILL.md`; `agents/openai.yaml` provides UI metadata where supported.
- Claude Code: uses `SKILL.md`; supporting files are optional.

## Local Development

Validate the skill structure with your local skill validator if available. For Codex:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py tex-spec-writer
```

## License

MIT
