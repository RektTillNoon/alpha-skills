# Alpha Skills

A public skill collection for agent workflows.

## Skills

### tex-spec-writer

Creates decision-complete TeX specs and phased implementation plans grounded in the current repository state. Every `.tex` deliverable must include a rendered `.pdf` companion.

Install the skill:

```bash
npx skills@latest add RektTillNoon/alpha-skills --skill tex-spec-writer
```

Check whether it is already installed before adding it again:

```bash
npx skills@latest list --json
```

Update an existing install instead of re-adding it:

```bash
npx skills@latest update tex-spec-writer
```

## Repository Layout

```text
alpha-skills/
├── README.md
├── LICENSE
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
