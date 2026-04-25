---
name: clean-commit
description: "Project-agnostic, behavior-preserving cleanup, semantic clarity refactor, codebase slimming, test audit, and intentional git commit workflow for existing codebases. Use when Codex needs to clean up a changed area, make code leaner without product changes, reduce ambiguity in names, types, fields, status objects, or string unions, remove dead or misleading code, cut bloat and excess indirection, collapse duplicate branches, align nearby tests with the real contract, trim brittle or duplicate tests, add focused regression coverage, or commit the resulting unstaged work with a well-scoped commit message. Trigger on requests like 'clean this up and commit it', 'make this leaner then commit', 'remove dead code and commit', 'commit current unstaged work', 'clean-commit all unstaged', or 'simplify this without changing behavior.'"
---

# Clean Commit

## Goal

Run one constrained, behavior-preserving cleanup pass and, only when the user asks for a commit, create one intentional git commit from the intended work.

Prefer less code, fewer concepts, narrower APIs, clearer names, and tests that describe the real contract. Do not turn cleanup into product work, architecture redesign, dependency churn, or style-only sweeping across unrelated files.

## Before Editing

Work through this five-step frame explicitly:

1. Goal: what the cleanup and commit should accomplish.
2. Problems: what blocks that outcome in the current code or diff.
3. Root cause: why the ambiguity, bloat, dead seam, test drift, or staging risk exists.
4. Design: the smallest behavior-preserving change that addresses it.
5. Implementation: the exact edit, verification, staging, and commit sequence.

Use test-driven cleanup:

- For bug-risk or behavior-risk cleanup, write or identify a focused failing or characterization test before changing implementation.
- For pure refactor, run the narrowest existing contract test first, then keep it green.
- If no useful test exists, add one focused regression only when it protects real behavior better than nearby coverage.

## Discover The Project

Before broad searching, discover the current repo's rules and tools:

- Read local instructions such as `AGENTS.md`, `CLAUDE.md`, `.github/CONTRIBUTING.md`, `README*`, and nearby package docs when present.
- Inspect manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, `build.gradle`, `Makefile`, `justfile`, `Taskfile*`, or CI configs.
- Inspect commit and push hooks such as `.husky/*`, `.git/hooks/*`, `lint-staged`, `pre-commit`, `lefthook`, `overcommit`, `pre-push`, and language-native hook config when present.
- Prefer repo-provided navigation, dependency, xref, dead-code, rename, typecheck, lint, format, and test commands over generic guesses.
- Use project-specific tools only when the current repo exposes them or local instructions require them.
- If the repo has no obvious tools, fall back to `rg`, language-native tests, and direct call-site inspection.

## Scope

Keep the cleanup radius to the existing diff or requested files, immediate callers or callees, shared types or status objects, and closest tests. Go wider only when a shared semantic helper, public boundary, or compatibility layer forces it.

If the user says `all unstaged`, treat the full unstaged tree as the intended review surface. Keep a cohesive slice together when the changes form one contract, and do not split it into conceptual commits unless the user asks or the diff contains unrelated work.

Make the top 1-3 highest-signal improvements and stop unless verification exposes a directly related issue.

Rank candidates by:

- semantic confusion
- dead code or stale protocol vocabulary
- excess indirection
- duplicate branches
- branch complexity
- stale or misleading tests
- brittle assertions
- duplicate coverage
- missing high-value regressions

## Contract Inference

Infer the contract in this order:

1. focused tests and observed runtime behavior
2. public types, schemas, and wire or persistence contracts
3. repeated production usage
4. docs and comments

Treat static dead-code tools as candidate generators, not proof.

Before deleting, de-exporting, or renaming a symbol, check import consumers, text consumers, runtime string references, subprocess entrypoints, worker paths, plugin hooks, config-discovered files, CSS-only usage, binaries, migrations, out-of-repo boundaries, and nearest tests.

If code is still used only inside its own module or package, prefer removing unnecessary exports over deleting live behavior.

## Semantic Cleanup

Separate concepts before renaming or extracting:

- product label vs internal behavior
- display wording vs behavior switch
- runtime phase vs transport or persistence value
- platform/device term vs domain concept
- one field, status object, or union carrying multiple meanings
- repeated ad hoc checks spread across files

Prefer one canonical internal name per concept. If an external boundary still needs a legacy name or value, translate it at ingress or egress only.

Avoid keeping old and new names live together inside the same semantic layer.

## Implementation Moves

Prefer these in order:

1. Delete dead code, stale comments, obsolete branches, invalidated tests, and fallback paths with no real boundary consumer.
2. Inline or remove pass-through wrappers and low-value indirection.
3. Rename misleading concepts toward semantic roles.
4. Flatten control flow and merge duplicate paths.
5. Move tightly related logic together.
6. Introduce shared constants, predicates, type aliases, normalization helpers, or a small semantics module only when reuse is real and ambiguity is reduced.
7. Narrow accidental API surface by reducing unnecessary exports, helper visibility, parameters, or return-shape width.

Do not add abstraction just for style or DRY instinct.

## Compatibility

Default to deleting compatibility aliases, dormant commands, noop fallbacks, and test-only protocol names once the canonical path is proven.

Keep a compatibility shim only for a named external boundary such as public APIs, wire contracts, persisted data, migrations in flight, plugin surfaces, or caller-owned integration points. Make the boundary explicit and state the removal condition.

For each legacy seam, answer:

1. Who still calls or consumes it in production?
2. Is that caller inside the current semantic layer or at a true external boundary?
3. If it stays, what exact boundary requires it?

If no real boundary consumer can be named, delete it before commit.

## Tests

Audit nearby tests as part of cleanup:

- keep tests that prove public behavior, product-critical paths, bug fixes, or meaningful edge cases
- tighten tests that over-specify incidental markup, ordering, timing, formatting, or snapshots
- collapse duplicate tests that cover the same contract
- delete tests for removed code or obsolete behavior
- rename tests so failures describe the contract, not the implementation step

Do not weaken assertions just to pass. Do not replace meaningful behavioral tests with larger snapshots.

## Parallel Fanout

When the surface is large enough and the user explicitly allows subagents, write a split before delegating:

- main thread: contract inference, cleanup ranking, rename strategy, integration, verification, staging choices, and commit authorship
- sidecar 1: consumer/dead-code/test-boundary map
- sidecar 2: one disjoint cleanup slice or nearby test cleanup

Do not delegate the main semantic judgment call, final verification summary, staging choices, commit message, or final commit command. If not launching sidecars, say whether the surface is too small, too sequential, or delegation is unavailable.

## Verification

Use the discovered project tools. Prefer this ladder:

1. narrow characterization or regression test
2. narrow touched-surface test
3. narrow typecheck or build
4. lint or format check when the repo treats it as correctness
5. repo-wide gate when committing, when shared behavior changed, when local instructions require it, or when the user asks

When deleting dead code, include any build, config, binary, CLI, or runtime command needed to prove non-import edges still resolve.

If verification cannot run, state the exact command that was unavailable and the remaining risk.

## Hook-Mutating Repos

If commit hooks can modify files, make those mutations happen before the final expensive verification gate:

- Identify hook-time mutators such as formatters, eslint/autofix, `lint-staged`, generated lockfile refreshes, codegen, or import sorting.
- Prefer running the repo's explicit formatter/fixer/check command before final verification. If the only documented mutator is a hook runner, run the narrow hook-equivalent command directly when it is safe and project-local.
- Restage only the intended paths after the mutator runs, then run the final verification gate against that stable staged/worktree state.
- Do not rely on `git commit` hooks to make first-time changes after the final verification gate; that can invalidate verify stamps, pre-push caches, build artifacts, or tree hashes and force duplicate verification.
- If no safe pre-commit mutator command is discoverable, proceed normally but treat a post-commit verification-cache mismatch as expected and rerun only the smallest cache-producing gate needed.

## Commit Workflow

Only commit when the user explicitly asks.

1. Run `git rev-parse --show-toplevel`.
2. Run `python3 scripts/inspect_unstaged_changes.py` from this skill's directory.
3. If the index already contains staged changes, stop and ask how to handle the pre-existing staged state.
4. If there are no unstaged tracked files and no untracked files, report that there is nothing to commit and stop.
5. Identify generated artifacts, local metadata, large files, binary files, renames, copies, submodule changes, and unrelated paths before staging.
6. Infer the commit intent from the diff, tests, docs, and user context. Do not invent motivation or claim a larger scope than the diff supports.
7. Run narrow characterization or regression verification before cleanup edits when behavior risk exists.
8. Stage only intended tracked and untracked paths with `git add -- <paths>`. Avoid `git commit -am`.
9. If the repo has hook-time mutators, run the project-local mutator command now and restage only the intended paths it changed.
10. Run the discovered repo-wide verification gate after staging and after hook-time mutators have already made their changes. If no repo-wide gate exists, run the strongest relevant narrow verification and say why it is sufficient.
11. Confirm the staged diff still matches the intended commit slice.
12. Write the message to a temporary file and commit with `git commit -F <file>`.
13. Verify the result with `git show --stat --summary --format=fuller -1`.
14. If the repo has a verify cache, stamp, or pre-push skip mechanism, compare it to the final committed `HEAD` state. If it no longer matches because the commit hook mutated files, rerun only the smallest cache-producing verification gate required by that mechanism.

Commit message:

- use an imperative subject, preferably 72 characters or fewer
- describe the main behavioral, architectural, or user-visible outcome
- add a body unless the change is trivially small
- use concrete nouns and verbs from the diff, not generic phrases like `update files`

For non-trivial commits:

```text
<imperative subject>

Explain why these changes belong together.

- Summarize the first concrete change group.
- Summarize the second concrete change group.
- Note tests, docs, or caveats when material.
```

## Report Back

Cover only what applies:

- semantic ambiguities found
- bloat or indirection removed
- clarifying helper or normalization introduced
- code and test cleanup performed
- compatibility shims removed or boundary-scoped
- verification run
- commit created, if any
- tempting cleanup left out of scope and why
