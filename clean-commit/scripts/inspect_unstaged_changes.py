#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path

LARGE_FILE_BYTES = 1024 * 1024

GENERATED_OR_BUILD_PARTS = {
    ".cache",
    ".next",
    ".nuxt",
    ".parcel-cache",
    ".pytest_cache",
    ".ruff_cache",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "out",
    "target",
    "tmp",
    "venv",
}

LOCAL_METADATA_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
}

GENERATED_SUFFIXES = {
    ".min.css",
    ".min.js",
    ".map",
    ".pyc",
    ".pyo",
}


def run_git(repo_root, args, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=False,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr}")
    return result


def decode_zlist(blob):
    return [entry.decode("utf-8", "replace") for entry in blob.split(b"\0") if entry]


def trim_lines(text, max_lines):
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text.rstrip()
    trimmed = "\n".join(lines[:max_lines]).rstrip()
    omitted = len(lines) - max_lines
    return f"{trimmed}\n... ({omitted} more lines omitted)"


def is_text_file(path):
    try:
        with path.open("rb") as handle:
            chunk = handle.read(8192)
    except OSError:
        return False
    return b"\0" not in chunk


def is_generated_or_build_path(rel_path):
    path = Path(rel_path)
    parts = set(path.parts)
    if parts & GENERATED_OR_BUILD_PARTS:
        return True
    return any(rel_path.endswith(suffix) for suffix in GENERATED_SUFFIXES)


def classify_path_metadata(rel_path, abs_path, exists=None):
    labels = []
    path = Path(rel_path)
    if path.name in LOCAL_METADATA_NAMES:
        labels.append("local-metadata")
    if is_generated_or_build_path(rel_path):
        labels.append("generated-or-build-artifact")

    file_exists = abs_path.exists() if exists is None else exists
    if not file_exists:
        labels.append("missing")
        return labels
    if abs_path.is_dir():
        labels.append("directory")
        return labels

    try:
        size = abs_path.stat().st_size
    except OSError:
        labels.append("unreadable")
        return labels
    if size > LARGE_FILE_BYTES:
        labels.append("large-file")
    if not is_text_file(abs_path):
        labels.append("binary-or-non-text")
    return labels


def list_section(title, items):
    print(f"\n{title}:")
    if not items:
        print("(none)")
        return
    for item in items:
        print(item)


def main():
    parser = argparse.ArgumentParser(
        description="Summarize unstaged git changes for commit-message drafting."
    )
    parser.add_argument("--max-tracked-lines", type=int, default=400)
    parser.add_argument("--max-untracked-lines", type=int, default=120)
    args = parser.parse_args()

    try:
        repo_root = (
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            .stdout.strip()
        )
    except subprocess.CalledProcessError:
        print("Not inside a git repository.", file=sys.stderr)
        sys.exit(1)

    staged_paths = decode_zlist(
        run_git(repo_root, ["diff", "--cached", "--name-only", "-z"]).stdout
    )
    unstaged_paths = decode_zlist(
        run_git(repo_root, ["diff", "--name-only", "-z"]).stdout
    )
    untracked_paths = decode_zlist(
        run_git(repo_root, ["ls-files", "--others", "--exclude-standard", "-z"]).stdout
    )

    diff_stat = run_git(repo_root, ["diff", "--stat", "--"]).stdout.decode(
        "utf-8", "replace"
    )
    diff_name_status = run_git(
        repo_root,
        ["diff", "--name-status", "--find-renames", "--find-copies", "--"],
    ).stdout.decode("utf-8", "replace")
    diff_summary = run_git(repo_root, ["diff", "--summary", "--"]).stdout.decode(
        "utf-8", "replace"
    )
    submodule_diff = run_git(
        repo_root,
        ["diff", "--submodule=short", "--"],
    ).stdout.decode("utf-8", "replace")
    tracked_diff = run_git(repo_root, ["diff", "--no-ext-diff", "--"]).stdout.decode(
        "utf-8", "replace"
    )

    print(f"REPO_ROOT: {repo_root}")
    print(f"HAS_STAGED_CHANGES: {'yes' if staged_paths else 'no'}")

    list_section("STAGED_PATHS", staged_paths)
    list_section("UNSTAGED_TRACKED_PATHS", unstaged_paths)
    list_section("UNTRACKED_PATHS", untracked_paths)

    print("\nUNSTAGED_DIFF_STAT:")
    print(diff_stat.rstrip() or "(none)")

    print("\nUNSTAGED_NAME_STATUS:")
    print(diff_name_status.rstrip() or "(none)")

    print("\nUNSTAGED_SUMMARY:")
    print(diff_summary.rstrip() or "(none)")

    print("\nUNSTAGED_SUBMODULE_DIFF:")
    print(submodule_diff.rstrip() or "(none)")

    print("\nUNTRACKED_CLASSIFICATION:")
    if not untracked_paths:
        print("(none)")
    else:
        for rel_path in untracked_paths:
            abs_path = Path(repo_root) / rel_path
            labels = classify_path_metadata(rel_path, abs_path)
            print(f"{rel_path}: {', '.join(labels) if labels else 'ordinary-text-file'}")

    print("\nUNSTAGED_TRACKED_DIFF:")
    print(trim_lines(tracked_diff, args.max_tracked_lines) or "(none)")

    print("\nUNTRACKED_FILE_PREVIEWS:")
    if not untracked_paths:
        print("(none)")
        return

    for rel_path in untracked_paths:
        abs_path = Path(repo_root) / rel_path
        print(f"\n=== {rel_path} ===")
        labels = classify_path_metadata(rel_path, abs_path)
        print(f"(classification: {', '.join(labels) if labels else 'ordinary-text-file'})")
        if not abs_path.exists():
            print("(file no longer exists)")
            continue
        if abs_path.is_dir():
            print("(directory; preview skipped)")
            continue
        if not is_text_file(abs_path):
            size = abs_path.stat().st_size
            print(f"(binary or non-text file; size={size} bytes)")
            continue

        preview = run_git(
            repo_root,
            ["diff", "--no-index", "--", os.devnull, rel_path],
            check=False,
        ).stdout.decode("utf-8", "replace")
        if not preview.strip():
            try:
                preview = abs_path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                preview = f"(unable to read file: {exc})"
        print(trim_lines(preview, args.max_untracked_lines) or "(empty file)")


if __name__ == "__main__":
    main()
