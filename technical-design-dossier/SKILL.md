---
name: technical-design-dossier
description: Create repo-grounded TeX Technical Design Dossiers and companion PDFs. Use for LaTeX technical design dossiers, formal specifications, algorithm-heavy plans, and phased implementation documents.
---

# TeX Technical Design Dossier Writer

Use this skill to create or revise decision-complete TeX Technical Design Dossiers grounded in the actual repository state.

The goal is a durable, citable artifact, not a chat-only plan. Every TeX source deliverable must come with a rendered PDF companion. Every TeX source deliverable must also include a captured preparation timestamp with day, month, year, exact local time, and timezone. The document should let a later engineer implement, review, test, and validate the work without reconstructing missing decisions from the conversation.

## Execution Requirement

Creation requests require file-producing work.

A creation pass is complete only when one of these is true:

- A `.tex` source artifact has been written in the canonical repo location and a companion `.pdf` has been rendered.
- A concrete blocker prevents artifact creation or PDF rendering, and the blocker is reported with the exact command, path, or missing prerequisite.

If the user asks only for naming advice, scoping advice, or a review, do not create files unless they also ask for the artifact.

## Bundled Resources

- Use `assets/technical-design-dossier-template.tex` as the default TeX starting point when the repository has no stronger local template.
- Read `references/golden-example.md` only when calibrating style, recovering from a too-chat-only output, or creating the first dossier in a repository.

The template follows professional technical-report structure while preserving this skill's implementation-readiness requirements: ownership, contracts, alternatives, TDD proof, validation, exact next sequence, and exit rule.

## When To Use

Use this skill when the user asks for:

- a detailed spec in `.tex`
- a TeX Technical Design Dossier
- a technical dossier, design dossier, or formal technical memorandum
- a formal specification in `.tex`
- a LaTeX implementation plan
- an algorithm-heavy design document
- a research-backed technical plan
- a phased plan that should be checked into a repo
- a rewrite or hardening pass on an existing TeX design artifact or formal specification

Do not use this skill for short markdown plans, ordinary code review, or one-off explanation unless the user wants a TeX artifact.

## Document Form and Naming

Use **Technical Design Dossier** as the default artifact name. Do not force every artifact to call itself a "spec." Pick a narrower subtype only when the work clearly calls for it:

- **Technical Design Dossier**: the default for broad documents that combine evidence, architecture decisions, algorithms, implementation sequencing, and validation.
- **Formal specification**: use when the artifact is primarily normative API, data-contract, protocol, or behavior definition.
- **Architecture memorandum**: use when the artifact is mainly a decision record with alternatives, tradeoffs, and ownership boundaries.
- **Research note**: use when the artifact is exploratory and should separate evidence from recommendations.

Use "Technical Design Dossier" as the natural user-facing artifact form in headings, metadata, and final handoff language unless a narrower subtype is more accurate. Prefer filenames such as `*-technical-design-dossier.tex` when no repo convention exists. Only use `*-spec.tex` filenames if the repo already has that convention or the artifact is actually a formal specification.

Keep TeX and PDF titles very concise. The main title should be a short subject noun phrase, usually 2 to 6 words and under 50 characters, such as "Renderer Backpressure" or "Invoice Sync Cutover." Do not use sentence-style titles, implementation summaries, phase labels, dates, repository paths, or phrases like "A Technical Design Dossier for..." in the title. Set the PDF metadata title to the same concise main title. Put the artifact form in the subtitle or metadata, and put scope detail in the abstract, purpose, or section headings.

## Timestamp Requirement

Before writing a TeX source artifact, capture the current local timestamp from the machine. Do not rely on `\today`, stale conversation dates, or model memory.

Preferred shell command:

```sh
date '+%A, %d %B %Y, %H:%M:%S %Z (%z)'
```

Include the captured value in the TeX front matter, title block, or document metadata. Use a clear label such as:

```tex
\date{Prepared Friday, 22 May 2026, 14:37:09 EDT (-0400)}
```

If the document has a revision table, include the same timestamp there for the initial entry. If a repo-specific document template already has metadata fields, preserve that template and add the timestamp to the canonical metadata field instead of creating a parallel authority.

## Academic Style Bar

Write in a professional, academic register:

- Prefer neutral, evidence-backed claims over promotional or conversational phrasing.
- Define specialized terms before relying on them.
- Separate observed repository facts, assumptions, decisions, and recommendations.
- Use precise verbs: "requires," "constrains," "implies," "invalidates," "verifies," and "falsifies."
- Avoid hype language, rhetorical emphasis, and unexplained metaphors.
- Use section titles that would be acceptable in an engineering design review or academic technical report.
- When a claim depends on source inspection, cite the file, test, config, report, or command output that supports it.
- When evidence is missing, state the gap explicitly and describe the validation needed to close it.

## Physics Consistency Pass

For any physics-facing, simulation, signal-processing, graphics, audio, robotics, controls, scientific-computing, or other model-heavy dossier, run a physics consistency pass before finalizing the design.

The principle is: **classify the quantity, then the owner, then the allowed transformations.** Do not accept a physically named variable until its dimensional meaning is explicit.

For every proposed state variable, buffer, field, equation, shortcut, cache, or scheduler behavior, answer:

- What quantity is this: amplitude, coefficient, energy, power, phase, frequency, damping, support, probability, color, radiance, resource budget, or diagnostic?
- What are its units or implied dimensions?
- Is the proposed equation correct for that quantity? For example, amplitude and stored energy may have different decay constants.
- Has the state already been summed, projected, normalized, clamped, cached, filtered, quantized, or converted?
- Does the proposed operation commute with that transformation, or must it happen before the transformation?
- Who is the deepest valid behavior owner for this quantity?
- Is any category, bucket, mode label, threshold, visual floor, scheduler cadence, or debug convenience standing in for a continuous physical variable?
- Can the behavior be tested across old threshold boundaries and under dense, sparse, silent, and retained-state conditions?
- Does static search prove old names are gone from behavior owners, not merely hidden from public fields?

When this pass identifies a mismatch, the dossier must either correct the design or explicitly document the mismatch as a blocker. Do not leave a physically suspect shortcut in the plan because it is easier to implement.

## Core Workflow

1. **Clarify the deliverable**
   - Identify whether the user wants a new Technical Design Dossier, formal specification, architecture memorandum, research note, revision, or only a review.
   - Treat a requested `.tex` deliverable as requiring a companion `.pdf`.
   - If they ask for code implementation too, keep the TeX artifact and implementation steps separate.
   - Capture the local timestamp before drafting TeX metadata.
   - If the user used a creation verb, proceed to artifact creation.

2. **Find the canonical location**
   - Inspect the repo before choosing paths.
   - Prefer existing plan/spec directories and naming conventions.
   - Do not invent parallel doc trees when a canonical path exists.

3. **Read the real source of truth**
   - Inspect current code, tests, README/docs, reports, prior specs, artifacts, and configs.
   - Treat previous specs as references, not proof that the live repo matches them.
   - If a report or existing TeX file is the user's source, read it directly.

4. **Diagnose before writing**
   - State the actual problem the artifact must solve.
   - Push back if the requested angle is too narrow, stale, or aimed at the wrong failure mode.
   - Identify what is in scope, out of scope, and already implemented.

5. **Run the physics consistency pass when applicable**
   - For model-heavy dossiers, classify every proposed quantity before writing final contracts.
   - Check unit/dimension correctness, transformation order, ownership, and whether any discrete category is replacing a continuous physical variable.
   - Add tests or acceptance criteria for threshold-boundary continuity, retained-state behavior, dense/sparse input, silence, and cache/scheduler interactions when relevant.
   - If the artifact is not physics-facing or model-heavy, skip this step explicitly in your reasoning rather than adding irrelevant content.

6. **Write a decision-complete TeX artifact**
   - Start from the bundled template unless the repo already has a canonical TeX template.
   Include the sections that fit the task:
   - Title block with document form and captured timestamp
   - Abstract or executive summary written in neutral technical language
   - Purpose
   - Glossary for new readers, when the domain is specialized
   - Current status and source evidence
   - Problem diagnosis
   - Product or system definition
   - Goals and non-goals
   - Assumptions, constraints, and exclusions
   - Canonical ownership boundaries
   - Cutover and compatibility policy
   - Data/model/runtime contracts
   - Required algorithms with LaTeX math or pseudocode
   - Phased implementation plan
   - File-level implementation map
   - Test-driven development contract
   - Metrics and promotion/acceptance rules
   - Risks and failure modes
   - References or evidence appendix, when source-backed claims are numerous
   - Exact next sequence
   - Exit rule

7. **Make the artifact implementable**
   - Prefer concrete constants, thresholds, states, interfaces, and acceptance criteria over broad intent.
   - Prefer hard cutovers inside the repo's semantic core. Allow compatibility only at verified external boundaries, with a removal condition.
   - Do not recommend preserving old field names for "debug stability" by default; debug and audit fields are not compatibility boundaries unless the repo has a documented external consumer.
   - Include validation commands and expected artifacts, including the PDF path.
   - Distinguish process completion from outcome success.
   - Name what evidence would falsify or block the plan.

8. **Validate TeX and render PDF**
   - Compile with the repo's existing command if one exists.
   - Otherwise use `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=<output-dir> <file>.tex` when available.
   - If `latexmk` is unavailable, use `pdflatex -interaction=nonstopmode -halt-on-error -output-directory <output-dir> <file>.tex`.
   - Fix fatal errors before claiming the artifact is valid.
   - Fix formatting warnings that indicate clipped or unreadable output before claiming the artifact is complete. At minimum, search the final `.log` for `Overfull`, `Underfull`, `LaTeX Warning`, `Package .* Warning`, and `Error`; resolve any overfull boxes caused by long code identifiers, paths, equations, tables, or commands.
   - Use breakable TeX constructs for long technical content:
     - define `\code` with a URL-style command such as `\DeclareUrlCommand{\code}{\urlstyle{tt}}` rather than unbreakable `\texttt{\detokenize{...}}`;
     - use `\path{...}` or another breakable path command for file paths;
     - wrap long data-flow equations in `aligned`, `split`, or `multline` instead of a single display line;
     - split long shell commands inside `verbatim` blocks across multiple lines with continuation characters;
     - size `longtable` columns so their total width leaves margin for intercolumn spacing, and narrow dense metric tables before rendering.
   - Visually inspect at least one rendered PDF page that contains the densest table, longest equation, or widest command block. When available, render the page to an image with a local tool such as `pdftoppm` and verify that right-edge content is not clipped.
   - Do not finish a TeX-writing pass without either producing the companion PDF or clearly reporting the compile blocker.

9. **Clean artifacts**
   - Remove generated sidecars such as `.aux`, `.log`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `.synctex.gz` unless the repo intentionally tracks them.
   - Always keep the rendered `.pdf` next to the `.tex` source, unless the repo has a stricter documented artifact location.
   - Keep the `.tex` source as the canonical artifact.

10. **Handoff**
   - Report exact `.tex` and `.pdf` artifact paths.
   - Report validation commands run and whether they passed.
   - State any unresolved risks or manual next steps.

## Generalization Rules

- Keep domain facts out of the reusable workflow. Trading, math, product, backend, frontend, and research specs should use the same process but different evidence.
- Use old TeX artifacts as format examples only after verifying the current repo.
- Do not preserve legacy commands, names, fields, or duplicate paths unless a real external boundary still consumes them.
- If a canonical path replaces an old one, remove or clearly retire the old path when the task boundary allows it.
- Translate legacy names at the boundary only; do not keep duplicate semantic paths in the core.

## Quality Bar

A good TeX artifact has enough detail that a future implementation pass can:

- identify the exact files to change
- write focused tests first
- know the acceptance criteria
- understand what not to build
- run the validation commands
- decide whether the work is done
- cite the document date, time, evidence base, and revision state unambiguously
- for physics-facing work, identify each physical quantity, its owner, its valid transformations, and tests that would catch dimensional or ordering mistakes

A weak TeX artifact usually lacks timestamped metadata, source evidence, definitions, thresholds, file mapping, test strategy, or an exit rule. For physics-facing work, it is also weak if it uses physically named variables without dimensional meaning, conflates amplitude/energy/power/support/diagnostic state, applies transformations after the state has already been summed or cached, or allows buckets and scheduler policy to stand in for continuous physical variables. Tighten those before finishing.
