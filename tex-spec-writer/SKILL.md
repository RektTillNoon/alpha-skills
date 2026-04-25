---
name: tex-spec-writer
description: Create repo-grounded TeX specs and companion PDFs. Use for LaTeX technical specs, algorithm-heavy plans, and phased implementation docs.
---

# TeX Spec Writer

Use this skill to create or revise decision-complete TeX specs and phased implementation plans grounded in the actual repository state.

The goal is a durable artifact, not a chat-only plan. Every TeX source deliverable must come with a rendered PDF companion. The spec should let a later engineer implement, review, test, and validate the work without reconstructing missing decisions from the conversation.

## When To Use

Use this skill when the user asks for:

- a detailed spec in `.tex`
- a LaTeX implementation plan
- an algorithm-heavy design document
- a research-backed technical plan
- a phased plan that should be checked into a repo
- a rewrite or hardening pass on an existing TeX spec

Do not use this skill for short markdown plans, ordinary code review, or one-off explanation unless the user wants a TeX artifact.

## Core Workflow

1. **Clarify the deliverable**
   - Identify whether the user wants a new spec, a revision, or only a review.
   - Treat a requested `.tex` deliverable as requiring a companion `.pdf`.
   - If they ask for code implementation too, keep the TeX spec and implementation steps separate.

2. **Find the canonical location**
   - Inspect the repo before choosing paths.
   - Prefer existing plan/spec directories and naming conventions.
   - Do not invent parallel doc trees when a canonical path exists.

3. **Read the real source of truth**
   - Inspect current code, tests, README/docs, reports, prior specs, artifacts, and configs.
   - Treat previous specs as references, not proof that the live repo matches them.
   - If a report or existing TeX file is the user's source, read it directly.

4. **Diagnose before writing**
   - State the actual problem the spec must solve.
   - Push back if the requested angle is too narrow, stale, or aimed at the wrong failure mode.
   - Identify what is in scope, out of scope, and already implemented.

5. **Write a decision-complete TeX spec**
   Include the sections that fit the task:
   - Purpose
   - Glossary for new readers, when the domain is specialized
   - Current status and source evidence
   - Problem diagnosis
   - Product or system definition
   - Goals and non-goals
   - Canonical ownership boundaries
   - Data/model/runtime contracts
   - Required algorithms with LaTeX math or pseudocode
   - Phased implementation plan
   - File-level implementation map
   - Test-driven development contract
   - Metrics and promotion/acceptance rules
   - Risks and failure modes
   - Exact next sequence
   - Exit rule

6. **Make the spec implementable**
   - Prefer concrete constants, thresholds, states, interfaces, and acceptance criteria over broad intent.
   - Include validation commands and expected artifacts, including the PDF path.
   - Distinguish process completion from outcome success.
   - Name what evidence would falsify or block the plan.

7. **Validate TeX and render PDF**
   - Compile with the repo's existing command if one exists.
   - Otherwise use `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=<output-dir> <file>.tex` when available.
   - If `latexmk` is unavailable, use `pdflatex -interaction=nonstopmode -halt-on-error -output-directory <output-dir> <file>.tex`.
   - Fix fatal errors before claiming the artifact is valid.
   - Do not finish a TeX-writing pass without either producing the companion PDF or clearly reporting the compile blocker.

8. **Clean artifacts**
   - Remove generated sidecars such as `.aux`, `.log`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `.synctex.gz` unless the repo intentionally tracks them.
   - Always keep the rendered `.pdf` next to the `.tex` source, unless the repo has a stricter documented artifact location.
   - Keep the `.tex` source as the canonical artifact.

9. **Handoff**
   - Report exact `.tex` and `.pdf` artifact paths.
   - Report validation commands run and whether they passed.
   - State any unresolved risks or manual next steps.

## Generalization Rules

- Keep domain facts out of the reusable workflow. Trading, math, product, backend, frontend, and research specs should use the same process but different evidence.
- Use old specs as format examples only after verifying the current repo.
- Do not preserve legacy commands, names, fields, or duplicate paths unless a real external boundary still consumes them.
- If a canonical path replaces an old one, remove or clearly retire the old path when the task boundary allows it.

## Quality Bar

A good TeX spec has enough detail that a future implementation pass can:

- identify the exact files to change
- write focused tests first
- know the acceptance criteria
- understand what not to build
- run the validation commands
- decide whether the work is done

A weak TeX spec usually lacks thresholds, file mapping, test strategy, or an exit rule. Tighten those before finishing.
