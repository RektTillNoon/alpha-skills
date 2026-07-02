---
name: investigate-fix
description: Investigate a concrete bug report, isolate the failing seam, carry the work through the smallest defensible fix, add focused regression coverage, and verify the affected path before broadening validation. Use when a user reports a bug, regression, flaky behavior, broken interaction, or "this stopped working" symptom and wants diagnosis plus an actual landed fix, not just speculation or a likely cause.
---

# Investigate Fix

Use this workflow to take a reported bug from symptom to verified repair without widening into unrelated refactors.

## Resolution Bar

Stay on the task until one of these is true:

- the root cause is evidenced, the owning seam is fixed, and the changed path is verified
- a concrete external blocker remains and you can name exactly what is blocked
- the user redirects the work

Do not stop at "likely cause found", "symptom stopped happening", "left notes", "partial patch applied", or "tests not yet run" if you can continue yourself.
Do not treat a disappearing symptom as resolved until you can point to the concrete causal break in code, state, configuration, data, or runtime behavior and show that the fix closes that break.

## Workflow

1. Re-state the symptom and the user-visible done condition.
2. Orient in the repo before deep tracing. Prefer any repo-local map, graph, nav, or structural-search helpers over raw file wandering.
3. Reproduce the issue or add the smallest probe that can prove or falsify the leading theories.
4. Write the investigation split explicitly: one immediate blocking main thread plus 1 to 3 bounded sidecar threads.
5. If subagents are permitted by the current session policy and useful for independent search surfaces, deploy 1 to 3 subagents for bounded sidecar investigation work. Otherwise keep the sidecar split internal and continue locally.
6. If you apply temporary containment to reduce noise or stop damage, label it as containment and continue toward the underlying cause unless the user explicitly asked for mitigation only.
7. Trace the event, state, or transport path end-to-end before editing code.
8. Name the owning seam, identify the concrete root cause at that seam, and capture a failing proof before patching whenever feasible.
9. Patch the smallest fix at the owning seam instead of layering workarounds on top.
10. Add or tighten focused regression coverage for the exact failure mode.
11. Re-run the narrowest affected checks first, then broaden validation only after the targeted path is green.
12. Finish by stating root cause, fix, verification, and any remaining bounded risk.

The owning seam is the narrowest boundary responsible for preserving the broken invariant. It may not be the first file where the symptom appears.

## Repo Orientation

When a repo exposes local navigation tooling, use it early.

Prefer this order:

1. generated repo map or architecture map
2. dependency graph for workspace/package boundaries
3. repo-local nav helper for files, entrypoints, and scripts
4. saved structural-search recipes before writing a one-off search

## Operating Rules

- Keep moving unless a real blocker requires user input, missing credentials, or risky approval.
- If exact reproduction is hard, create the smallest reliable proof with a focused test, probe, log point, or failing assertion.
- Remove local blockers yourself when reasonable: stale dev server, bad cache, missing test fixture, broken seed data, wrong command, or narrow environment drift.
- Do not present a handoff as progress if you can still patch or verify the fix in the current turn.
- Do not stop at seam-level understanding if the causal chain is still ambiguous. Keep tracing until you can name why the bug exists, not only where it surfaced.
- Keep a lightweight evidence ledger while investigating:
  - observation: directly seen in code, logs, tests, runtime state, or docs
  - inference: conclusion drawn from observations
  - assumption: unverified belief that still needs proof or a risk note
  - proof: executable check, deterministic probe, or concrete artifact that confirms or falsifies the issue
- Record the work split in plain terms before you fan out:
  - main thread: the immediate blocking question you will own locally
  - sidecar 1 to 3: bounded adjacent questions that can be answered independently
- Treat the sidecar split as internal planning unless you are actually delegating. User-facing progress updates should name the current blocking seam and the next concrete check, not the bookkeeping around skipped delegation.

## Containment Versus Resolution

- A guard, retry, debounce, dedupe, null-check, feature flag, or fallback may be valid containment, but it is not resolution by default.
- If you add containment first, say exactly what it contains and continue investigating until the causal break is concrete.
- Only stop at containment when the user explicitly asks for mitigation only or when a named external blocker prevents deeper repair.

## Subagent Deployment

Use subagents for investigation coverage when the environment allows it, session policy permits delegation, and there are at least two independent seams, histories, or proof surfaces to inspect.

- Do the first orientation and choose the immediate blocking thread yourself before delegating anything.
- After the blocking seam is identified, default to launching 1 to 3 bounded sidecar subagents only when independent sidecar work can run without blocking the next local proof step.
- Use actual delegated subagents for sidecar work. Parallel local reads or batched shell commands are useful, but they do not satisfy this step when real subagents are available.
- Spawn subagents for bounded sidecar work that can run in parallel without blocking the next local step:
  - tracing one candidate producer or consumer path
  - checking recent history for the introducing change
  - reproducing the bug in an alternate test harness
  - locating the highest-signal existing test seam
  - validating a suspected fix against a nearby codepath
- Keep the main thread on the critical path: reproduction, owning-seam judgment, fix integration, and final verification.
- Give each subagent a concrete question, clear ownership, and a disjoint scope. Ask for evidence, not guesses.
- Do not delegate the immediate blocking step if your next action depends on that result.
- Do not wait idly on subagents. Continue local tracing or implementation while they run.
- When subagents disagree, trust the strongest evidence and reconcile the conflict in the main thread before editing.
- If you choose not to launch sidecar subagents, say why the surface is too narrow or too sequential for parallel work to help.
- Only skip sidecar subagents when there is genuinely one actionable seam, no independent adjacent question to split off, or the environment or session policy does not allow delegation.
- If delegation is unavailable, keep the sidecar split internal. Do not emit user-facing lines such as "sidecar 1/2/3 I'm handling locally instead of spawning." Report the blocking seam you are checking and the next concrete proof step instead.
- Useful default sidecar shapes:
  - transport or state bugs: trace producer path, trace consumer path, inspect reconnect or bootstrap history
  - UI event bugs: inspect event source, inspect state transition path, locate the narrowest user-visible test seam
  - data or backend bugs: inspect write path, inspect read path, inspect the contract or schema boundary
  - regressions: search for the introducing change, inspect neighboring tests, inspect the boundary that should have caught it

## Investigation Rules

- Separate symptoms from guesses. Do not commit to a cause until a concrete path in code or runtime data supports it.
- Prefer reading the producer and consumer of a signal together: sender and receiver, caller and callee, UI event and state reducer, transport source and sink.
- If the repo has saved structural-search recipes for the domain, run the closest one first and only widen into custom search if needed.
- If multiple theories exist, choose the one you can disprove fastest with a focused probe.
- If the suspected seam depends on current third-party library, framework, SDK, developer API, CLI, or cloud-service behavior, verify the current documentation before patching.
- Treat stale dev processes, cached builds, and HMR gaps as possible confounders, but do not stop there unless the evidence supports it.
- Keep tightening the explanation until the root issue is concrete enough that you can answer both "why did the bug happen?" and "why does this patch prevent it from happening again?"

## False Root Cause Traps

- stale process or stale build output that hides the real codepath
- cached payload, bootstrap snapshot, or replay buffer that makes a fix look effective when the source is unchanged
- duplicated send or replay paths where the first visible seam is not the owner
- broken fixture, seed data, or environment setup that mimics a product bug
- logging, timing, or retry behavior that changes the race and makes the bug disappear during investigation

## Fix Rules

- Patch the real seam that owns the broken invariant.
- Preserve existing architecture unless the bug proves the boundary is wrong.
- Do not broaden into cleanup or redesign unless the current structure prevents a correct fix.
- When a bug involves authoritative or mirrored state, restore a single-writer model where possible.
- Prefer one good fix over stacked defensive tweaks across multiple layers.
- If a patch only masks the symptom, keep going. Temporary guards are not the finish line unless the user explicitly asks for containment only.

## Regression Rules

- Add one regression per bug shape, not a broad speculative suite.
- Capture the failing proof before the fix whenever the environment allows it, then keep or translate that proof into durable regression coverage.
- Prefer the highest-signal layer that catches the failure reliably:
  - unit test for pure logic or protocol contracts
  - integration test for state reconciliation and transport
  - smoke/e2e test for user-visible regressions
- Assert the behavior that matters to the user, not just implementation detail.

## Verification Order

1. Run targeted unit or integration checks for the changed seam.
2. Run the narrowest smoke or end-to-end case that proves the reported fix.
3. Run broader lint, typecheck, or verify steps only after the focused path passes.
4. If a check cannot run, say why and use the next best concrete validation you can perform.

## Minimum Proof

- Prefer one artifact that fails before the fix and passes after it: test, probe, log assertion, or deterministic reproduction step.
- If the environment prevents a before-and-after proof, say exactly what blocked it and provide the strongest concrete substitute you could run.
- Do not present code inspection alone as sufficient proof when executable validation was possible.

## Response Pattern

- Tell the user what seam you are checking first.
- Share the first concrete thing learned, not generic progress.
- If no subagents are being launched, do not narrate skipped sidecars or justify non-delegation in routine progress updates.
- After the fix, explain root cause, user-visible impact, and why the chosen seam was the right place to patch.
- Call out any remaining known gaps separately from the fixed issue.
- End with a short proof statement covering:
  - symptom
  - causal break
  - why the patch closes it
  - what regression or probe proves it
