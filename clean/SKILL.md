---
name: clean
description: "Project-agnostic, behavior-preserving cleanup, semantic clarity refactor, codebase slimming, and test audit pass for existing codebases. Use when Codex needs to clean up a changed area, make code leaner without product changes, reduce ambiguity in names, types, fields, status objects, or string unions, remove dead or misleading code, cut bloat and excess indirection, collapse duplicate branches, align nearby tests with the real contract, trim brittle or duplicate tests, or add focused regression coverage without broadening into product changes or architecture work. Trigger on requests like 'clean this up', 'make this leaner', 'cut bloat', 'simplify this without changing behavior', or 'remove dead code.'"
---

# Clean

## Goal

Run one constrained, behavior-preserving cleanup pass. Prefer less code, fewer concepts, narrower APIs, clearer names, and tests that describe the real contract.

Do not turn cleanup into product work, architecture redesign, dependency churn, or style-only sweeping across unrelated files.

## Ownership-Sensitive Cleanup

If cleanup involves canonical paths, duplicated state, fallback behavior, compatibility shims, cache/state ownership, lifecycle authority, sync/reconnect authority, render authority, or any question of who should own a behavior, perform one `owner-check` pass before editing, then resume this cleanup workflow.

Use the ownership decision to rank pruning candidates: false owners, duplicate representations, downstream heuristics, stale aliases, obsolete wrappers, and compatibility paths with no named external boundary should be removed in the cleanup pass.

## Before Editing

Work through this five-step frame explicitly:

1. Goal: what the cleanup should improve.
2. Problems: what blocks that outcome in the current code.
3. Root cause: why the ambiguity, bloat, dead seam, or test drift exists.
4. Design: the smallest behavior-preserving change that addresses it.
5. Implementation: the exact edit and verification sequence.

Use test-driven cleanup:

- For bug-risk or behavior-risk cleanup, write or identify a focused failing or characterization test before changing implementation.
- For pure refactor, run the narrowest existing contract test first, then keep it green.
- If no useful test exists, add one focused regression only when it protects real behavior better than nearby coverage.

## Discover The Project

Before broad searching, discover the current repo's rules and tools:

- Read local instructions such as `AGENTS.md`, `CLAUDE.md`, `.github/CONTRIBUTING.md`, `README*`, and nearby package docs when present.
- Inspect manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, `build.gradle`, `Makefile`, `justfile`, `Taskfile*`, or CI configs.
- Prefer repo-provided navigation, dependency, xref, dead-code, rename, typecheck, lint, format, and test commands over generic guesses.
- Use project-specific tools only when the current repo exposes them or local instructions require them.
- If the repo has no obvious tools, fall back to `rg`, language-native tests, and direct call-site inspection.

## Scope

Keep the cleanup radius to touched files, immediate callers or callees, shared types or status objects, and closest tests. Go wider only when a shared semantic helper, public boundary, or compatibility layer forces it.

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

Before deleting, de-exporting, or renaming a symbol, check:

- import and text consumers
- runtime string references, subprocess entrypoints, worker paths, plugin hooks, config-discovered files, CSS-only usage, binaries, migrations, and out-of-repo boundaries
- nearest tests and fixtures that may encode the boundary

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

If no real boundary consumer can be named, delete it in the cleanup pass.

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

- main thread: contract inference, cleanup ranking, rename strategy, integration, final verification
- sidecar 1: consumer/dead-code/test-boundary map
- sidecar 2: one disjoint cleanup slice or nearby test cleanup

Do not delegate the main semantic judgment call, final verification summary, or scope decision. If not launching sidecars, say whether the surface is too small, too sequential, or delegation is unavailable.

## Verification

Use the discovered project tools. Prefer this ladder:

1. narrow characterization or regression test
2. narrow touched-surface test
3. narrow typecheck or build
4. lint or format check when the repo treats it as correctness
5. repo-wide gate only when shared behavior changed, local instructions require it, or the user asks

When deleting dead code, include any build, config, binary, CLI, or runtime command needed to prove non-import edges still resolve.

If verification cannot run, state the exact command that was unavailable and the remaining risk.

## Report Back

Cover only what applies:

- semantic ambiguities found
- bloat or indirection removed
- clarifying helper or normalization introduced
- code and test cleanup performed
- compatibility shims removed or boundary-scoped
- verification run
- tempting cleanup left out of scope and why
