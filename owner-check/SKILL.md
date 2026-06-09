---
name: owner-check
description: Use for representation-first ownership checks on architecture-sensitive edits, state/cache/lifecycle/reconnect/sync work, render/physics/audio/shader systems, canonical path cleanup, or when the user asks who should own a behavior. Guides quantity classification, transformation tracing, deepest valid owner selection, deletion of false owners, and invariant proof.
---

# Owner Check

Use this skill when the risk is that behavior is being patched at the visible symptom layer instead of the layer that owns the state.

## Owner Ledger

Before changing behavior, identify:

1. The state representation and its units or semantics.
2. Whether it is a field, mode parameter, coefficient, amplitude, energy/power measure, support/domain mask, diagnostic, cache, serialized value, mirrored value, or rendered projection.
3. Transformations already applied: summing, normalization, damping, projection, thresholding, clamping, quantization, serialization, mirroring, rendering, or scheduler cadence.
4. Transformations still valid at this layer.
5. The invariant that must hold.
6. The deepest valid behavior owner.
7. The correct edit layer.
8. Why that layer owns the behavior and why the fix addresses the root cause.
9. Whether any downstream layer is reinterpreting the quantity through a proxy instead of consuming the owner-owned representation.

## Refinement Workflow

1. **Observe current behavior**
   - Inspect the live code path and tests before proposing edits.
   - Separate observations from inferences and assumptions.

2. **Classify the quantity**
   - Name what the value physically or semantically represents.
   - Reject vague labels such as "intensity", "amount", or "level" unless the code defines their units.
   - Separate source evidence, stored state, projected state, visibility, authority, diagnostics, and cache/replay data before comparing them.

3. **Trace transformations**
   - Follow the value from source to consumer.
   - Mark where it is cached, mirrored, normalized, clamped, rendered, serialized, or replayed.
   - Note where a continuous physical or semantic variable becomes categorical, thresholded, or quantized.

4. **Choose the deepest valid owner**
   - Behavior belongs where the canonical state is created or transformed, not where symptoms are easiest to hide.
   - Buckets, slots, scheduler cadence, render defaults, diagnostics, CSS, mirrored status, and legacy names are not behavior owners unless they are the actual external boundary.
   - Projection layers can map owner-owned state into a target representation, but cannot decide whether upstream state or authority is real.

5. **Delete false owners**
   - Remove obsolete wrappers, duplicate pathways, stale aliases, compatibility shims, and heuristic overrides when no external contract still needs them.
   - If an external contract still needs a legacy name or shape, translate at the boundary only.
   - Remove downstream liveness, authority, pruning, or cache heuristics that duplicate an upstream owner.
   - If this check was invoked from an active `clean` or `clean-commit` pass, return to that same pass for bounded pruning, verification, and staging or commit work; do not restart either skill.
   - If there is no active cleanup pass and the user asks for pruning or test cleanup beyond the ownership decision, use `clean` for the edit and verification discipline.

6. **Prove the invariant**
   - Prefer tests for canonical behavior.
   - Use static search to prove old paths or names are gone.
   - Use visual, screenshot, or pixel checks when the behavior is render-facing.
   - Assert conservation across the owner seam: valid upstream state should not vanish downstream unless an explicit boundary owner closes it.

## High-Risk System Checks

- For authoritative sync, identify startup state, steady-state state, mirrored state, reset behavior, cached-state updates, active sends, and reconnect replay separately.
- Do not use mirrored status, telemetry, render acknowledgements, or cache snapshots as React effect dependencies unless they are explicitly valid triggers.
- If a continuous physical or semantic variable is represented categorically, justify the boundary or replace it with a continuous descriptor.
- Prefer one canonical internal name per concept. Keep legacy translation at system boundaries only.
- Do not use one global threshold across distinct physical or semantic regimes unless they have first been normalized into the same representation.
- For layered physical systems, keep layer-local pruning and normalization local to comparable quantities. For example, low-Q/source-coupled energy must not prune high-Q/resonant energy before both have been transformed into a shared energy representation.
- Caches may retain topology, structure, and diagnostics, but current evidence and current authority must be recomputed by their owners.
- Render authority, transport authority, source evidence, modal energy, and visibility are separate quantities. Do not let projection slots, debug state, retained field state, or observer continuity authorize output unless that is the explicit owner contract.
- For render/audio/shader paths, add at least one invariant test that proves owner-owned state survives downstream projection while closed boundaries still fail closed.

## Output Shape

Use this compact form when documenting the decision:

```text
Observations:
Inferences:
Assumptions:
Owner:
Invariant:
Change:
Proof:
```

If the request is tiny, compress this to the minimum needed to make the ownership decision auditable.
