# Golden Example: Technical Design Dossier

Use this reference only when style calibration is needed, when a prior output was too chat-only, or when creating the first dossier in a repository. Do not treat the domain content below as repository fact.

## Research Direction

The template follows standard engineering report guidance: front matter, summary or abstract, body, references, and appendices. It also adds design-document sections that make implementation review practical: goals and non-goals, alternatives, ownership, contracts, validation, and an exact next sequence.

Useful external references:

- IEEE Professional Communication Society, "Write Effective Reports": https://procomm.ieee.org/communication-resources-for-engineers/written-reports/write-effective-reports/
- IET, "A guide to technical report writing": https://www.theiet.org/media/5182/technical-report-writing.pdf

## Example Prompt

Create the Technical Design Dossier for this recommendation: replace the static-field-plus-dynamic-overlay split with one canonical effective-field compute pass. Keep the static cache only as an optimization path, not as the semantic owner.

## Expected Agent Behavior

1. Inspect the live repository before choosing the path.
2. Capture the local timestamp with:

```sh
date '+%A, %d %B %Y, %H:%M:%S %Z (%z)'
```

3. Write the `.tex` artifact in the canonical repo documentation path.
4. Render the companion PDF.
5. Report both paths and the validation command.

## Example Artifact Shape

Title:

```text
Canonical Effective Field Compute: Technical Design Dossier
```

Metadata:

```tex
\date{Prepared Saturday, 23 May 2026, 00:30:53 EDT (-0400)}
```

Abstract:

```text
This dossier specifies the replacement of a two-owner field evaluation model with a canonical effective-field compute pass. The selected design assigns semantic ownership of Phi(p,t), grad Phi(p,t), and signed cancellation to the effective-field stage. The static field cache remains an optimization and fallback path only. Acceptance requires a failing proof for the current ownership split, a canonical owner change, removal or boundary-justification of stale competing paths, and validation through focused runtime tests plus the repository's broader verification lane.
```

Decision table:

```text
Concern                         Canonical owner                   Reason
Field semantics                 Effective-field compute pass       The rendered field is time-dependent when phase authority is active.
Static cache                    Optimization/fallback              It cannot own Phi(p,t) without preserving the semantic split.
Render-visible cancellation     Effective-field output contract    Downstream render code should consume one field contract.
```

Cutover policy:

```text
Surface                         Policy                            Removal condition
Field semantic owner             Hard cutover                      Not applicable; one semantic owner is required.
Static cache access              Boundary optimization only         Delete any semantic alias after consumers read the canonical field.
Legacy debug fields              Remove unless externally consumed  Keep only with a named consumer and deletion proof.
```

Implementation plan:

```text
1. Add or identify a failing proof that shows the static cache and phase overlay can diverge.
2. Move Phi(p,t) and grad Phi(p,t) ownership into the effective-field compute pass.
3. Make render/runtime consumers read the canonical effective-field output.
4. Remove stale semantic aliases; keep static cache access only behind an optimization or fallback boundary.
5. Validate focused field tests, render-visible proof, and the broader repo verification lane.
```

Exit rule:

```text
The work is complete only when the effective-field compute pass is the sole semantic owner, stale competing paths are removed or boundary-justified, focused and broad validation pass, and the dossier PDF is regenerated from the current TeX source.
```

Example final response after a successful creation pass:

```text
Created the Technical Design Dossier and rendered the companion PDF.

TeX: /abs/path/documentation/internal/reference/canonical-effective-field-compute-technical-design-dossier.tex
PDF: /abs/path/documentation/internal/reference/canonical-effective-field-compute-technical-design-dossier.pdf

Validation: latexmk -pdf -interaction=nonstopmode -halt-on-error ...
```
