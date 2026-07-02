#!/usr/bin/env python3
"""Install alpha-skills without re-adding skills that are already installed."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = "RektTillNoon/alpha-skills"
SKIP_DIRS = {".agents", ".claude-plugin", ".git", ".github", "plugins", "scripts", "tests"}


def discover_skill_names(repo_root: Path = REPO_ROOT) -> list[str]:
    return sorted(
        path.name
        for path in repo_root.iterdir()
        if path.is_dir() and path.name not in SKIP_DIRS and (path / "SKILL.md").is_file()
    )


def collect_installed_skill_names(payload: object) -> set[str]:
    names: set[str] = set()

    def visit(value: object) -> None:
        if isinstance(value, dict):
            for key in ("name", "skill", "skillName", "slug", "id"):
                candidate = value.get(key)
                if isinstance(candidate, str) and candidate:
                    names.add(candidate)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(payload)
    return names


def list_installed_skill_names(global_scope: bool) -> set[str]:
    command = ["npx", "skills@latest", "list", "--json"]
    if global_scope:
        command.append("--global")

    result = subprocess.run(command, check=True, capture_output=True, text=True)
    if not result.stdout.strip():
        return set()

    return collect_installed_skill_names(json.loads(result.stdout))


def install_skill(skill: str, source: str, global_scope: bool, yes: bool, agents: Iterable[str]) -> None:
    command = ["npx", "skills@latest", "add", source, "--skill", skill]
    if global_scope:
        command.append("--global")
    if yes:
        command.append("--yes")
    for agent in agents:
        command.extend(["--agent", agent])

    subprocess.run(command, check=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install only missing alpha-skills, skipping skills already present in the selected scope."
    )
    parser.add_argument("skills", nargs="*", help="Specific skills to install. Defaults to every skill in this repo.")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help=f"Skill source passed to skills add. Default: {DEFAULT_SOURCE}")
    parser.add_argument("--project", action="store_true", help="Use project scope instead of global scope.")
    parser.add_argument("--yes", action="store_true", help="Pass --yes to the skills CLI.")
    parser.add_argument("--agent", action="append", default=[], help="Forward one target agent to the skills CLI.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    requested = args.skills or discover_skill_names()
    known = set(discover_skill_names())
    unknown = sorted(set(requested) - known)
    if unknown:
        print(f"Unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    global_scope = not args.project
    installed = list_installed_skill_names(global_scope)
    missing = [skill for skill in requested if skill not in installed]

    for skill in requested:
        if skill in installed:
            print(f"skip {skill}: already installed")

    if not missing:
        print("All requested skills are already installed; nothing to download.")
        return 0

    for skill in missing:
        print(f"install {skill}")
        install_skill(skill, args.source, global_scope, args.yes, args.agent)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
