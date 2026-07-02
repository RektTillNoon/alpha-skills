---
name: stateful-planning-protocol
description: Use when the user asks for a technical plan, PR breakdown, rollout plan, or refactor plan for stateful systems, especially ones involving authoritative ownership, mirrored state, reconnect behavior, transport protocols, React effects, cached bootstrap payloads, or cross-process/window sync. This skill hardens plans by forcing explicit ownership boundaries, allowed and forbidden triggers, reconnect/cache rules, negative invariants, and loop-prevention regressions.
---

# Stateful Planning Protocol

Use this skill when writing plans for systems where state can be:

- authoritative vs mirrored
- cached vs actively sent
- steady-state vs startup/recovery
- local vs transported across process, window, worker, or device boundaries

This is a planning skill, not an implementation skill. The point is to stop plans from being technically plausible but trigger-ambiguous.

## Repo Orientation

Before writing the plan, orient on the actual ownership surfaces in the repo instead of relying on memory.

When a repo exposes local navigation helpers, prefer this sequence:

1. repo map or architecture map
2. dependency graph for package and ownership boundaries
3. repo nav helper for entrypoints and scripts
4. saved structural-search recipes for state, effects, transport, or protocol seams

## Core Rule

Every plan must make it obvious:

1. who owns a piece of state
2. who may mirror it
3. who may command it
4. who may initialize or reset it
5. which signals may retrigger each of those actions

If a plan cannot answer those questions, it is not ready.

## Required Plan Sections

Include these sections, even if they are brief.

### 1. Goal And Scope

State what is changing and what is explicitly not changing.

Always include:

- architectural boundaries that stay fixed
- runtime modes that stay unchanged
- out-of-scope optimizations or future follow-ups

### 2. Ownership Model

Name the single writer for each critical state domain.

At minimum, identify:

- startup owner
- steady-state owner
- mirror-only consumers
- command-only producers
- cache-only holders

If ownership changes by mode, say so explicitly.

Use wording like:

- `The stage owns steady-state live-input runtime once authoritative mode is active.`
- `The desktop may cache reconnect bootstrap payloads but must not reinitialize the live stage during steady state.`

### 3. Allowed Triggers

List the signals that are allowed to cause each of these:

- bootstrap or initialization
- steady-state command send
- cache refresh
- reconnect replay
- recovery or repaint
- UI recomposition if relevant

Be specific about trigger source, not just event name.

Example:

- `Entering performer-output-authoritative mode may send bootstrap.`
- `Transport reconnect may replay the cached bootstrap.`
- `Authoritative status updates may refresh reconnect cache inputs but must not send bootstrap immediately.`

### 4. Forbidden Triggers

For stateful or bidirectional systems, this section is mandatory.

List what must *not* retrigger startup or reset paths.

Common forbidden triggers:

- mirrored status updates
- mirrored telemetry updates
- render acknowledgements
- derived UI state
- effect dependency churn from subordinate state
- stale cached payload changes that should be reconnect-only

Example:

- `Steady-state authoritative status must not retrigger bootstrap send.`
- `Telemetry changes must not affect transport initialization.`

### 5. Cache And Reconnect Semantics

If the plan mentions bootstrap, replay, reconnect, or recovery, explicitly separate:

- cache update
- active send
- replay on reconnect

Never allow the plan to blur these into one action.

If the implementation will keep a cached payload, specify:

- what updates the cache
- what sends immediately
- what replays on reconnect only

### 6. Effect Dependency Audit

If React effects, subscriptions, observers, or callbacks are involved, list:

- effects that are mode-entry only
- effects that may depend on mirrored state
- effects that must not depend on mirrored state

This section exists to catch feedback loops before implementation.

Examples of risky dependencies:

- stage-owned status inside a desktop bootstrap effect
- telemetry inside initialization effects
- render ack inside steady-state command construction

### 7. Positive And Negative Invariants

Do not stop at “what should happen.” Also state “what must never happen.”

Include both:

- positive invariants
- negative invariants

Examples:

- `Bootstrap carries explicit cadence config.`
- `Output-config sync updates cadence without reconnect.`
- `Authoritative status updates do not emit another bootstrap.`
- `Mirrored state cannot re-enter startup paths.`

### 8. Regression Shape

The test plan must include:

- one positive path that proves the intended behavior
- one negative path that proves a loop, echo, or re-bootstrap cannot happen

When relevant, also require:

- reconnect replay test
- stale-session rejection test
- mode transition test
- user-visible smoke on the affected runtime mode

## Planning Checklist

Before finalizing the plan, check:

- Did I orient on the current repo seams using the available repo-local tools instead of relying on memory?
- Did I separate initialization, steady state, reconnect, and recovery?
- Did I identify the single writer for each critical state domain?
- Did I name at least one forbidden trigger?
- Did I distinguish cache refresh from active send?
- Did I include at least one “must not loop” regression?
- Did I identify any effect dependency that could turn mirrored state into a reset path?

If any answer is no, revise the plan.

## Output Template

Use this structure when the skill applies:

1. Summary
2. Ownership Model
3. Allowed Triggers
4. Forbidden Triggers
5. Cache / Reconnect Behavior
6. Key Changes
7. Positive Invariants
8. Negative Invariants
9. Test Plan
10. Assumptions

Keep sections short, but do not omit them.

## Notes

- Prefer explicit boundaries over clever wording.
- Plans for authoritative or mirrored systems should bias toward single-writer clarity.
- If a plan touches bootstrap, replay, reconnect, mirrored status, or effect-driven orchestration, use this skill by default.
