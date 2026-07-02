---
name: owner-clean
description: "Post-change ownership and cleanup pass for Codex's own work. Use when the user asks to run owner-check and clean on your work, audit recent edits before finishing, patch bugs found during verification, make a completed change leaner without product drift, or ensure an implementation is owned at the right seam before reporting done."
---

# Owner Clean

## Goal

Run a finishing pass over the current work: verify the intended edit is owned at the right layer, perform one bounded behavior-preserving cleanup pass, patch bugs found by that process, and report the proof.

This skill composes `$owner-check` and `$clean`; it does not replace either skill or copy their full workflows. Read and follow those installed skills when they are available.

## Workflow

1. Discover the active work surface.
   - Inspect the current branch or working tree when there is a repo.
   - Identify the files, tests, generated artifacts, and user-requested scope that belong to the current task.
   - Preserve unrelated user edits.

2. Run one ownership lens.
   - Use `owner-check` before cleanup when the work touches canonical paths, duplicated state, lifecycle authority, cache/sync/reconnect behavior, render authority, or semantic ownership.
   - Keep it non-recursive: perform one owner-check pass, record the owner decision, then resume this same owner-clean pass.
   - If ownership is not relevant, state that as an assumption and continue to cleanup.

3. Run bounded cleanup.
   - Use `clean` for the cleanup discipline: smallest behavior-preserving edits, narrow scope, nearby tests, and no product expansion.
   - Prefer deleting false owners, stale aliases, duplicate paths, misleading names, brittle tests, and low-value indirection found during the owner lens.
   - Stop after the highest-signal 1-3 improvements unless verification exposes directly related bugs.

4. Patch bugs found in the process.
   - Treat failing tests, type errors, broken docs checks, invalid generated artifacts, or owner-invariant violations as part of the current pass when they are caused by the current work.
   - Do not broaden into unrelated failures. Separate observation, inference, and assumption before deciding a failure belongs to the current work.

5. Verify with the cheapest sufficient proof.
   - Prefer the narrowest relevant test, typecheck, lint, build, screenshot, link check, or static reference search that proves the touched contract.
   - Run broader gates only when shared behavior changed, local instructions require them, or the user asked.

## Reporting

Use this compact shape when useful:

```text
Observations:
Inferences:
Assumptions:
Owner:
Cleanup:
Proof:
Left out:
```

Keep the report direct. Include commands actually run and failures actually observed. Do not claim a clean result unless verification ran or the remaining risk is explicitly stated.
