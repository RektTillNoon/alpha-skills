---
name: evolutionary-5-step
description: "Use for one bounded Dalio-style improvement pass on non-trivial work: define a clear goal, identify specific problems, diagnose root causes, design the smallest entropy-reducing plan, do the work, verify it, and name the next target."
---

# Evolutionary 5-Step

Use this skill to run one bounded improvement pass. It adapts Ray Dalio's sequence — Goals -> Problems -> Diagnosis -> Design -> Do/Tasks — to agentic work. The point is disciplined progress with a stop condition, not an endless optimization loop.

## Operating Contract

- Run one local pass by default. Recurse only when verification exposes a problem that prevents the stated goal from being satisfied.
- Keep the goal concrete and local to the current request. Do not expand it into adjacent cleanup. Treat the user's request as the value signal unless the goal itself is unclear.
- Treat problems as specific gaps between current reality and the goal. Do not tolerate them, but do distinguish real problems from vague discomfort.
- Keep blockers separate from problems: a blocker is only something that prevents this pass without user input, credentials, approval, or an external state change.
- Prefer the smallest change that reduces system entropy: fewer concepts, fewer paths, clearer ownership, stronger invariants.
- Separate observations, inferences, and assumptions when they affect the solution.
- End by naming the next best target. Do not start that target unless it is required for the current goal or the user asks.

## The Pass

1. **Define the clear goal**
   - State the user-visible outcome.
   - State the success condition and the smallest useful proof.
   - If goals compete, prioritize one concrete outcome rather than trying to satisfy everything at once.

2. **Identify and don't tolerate problems**
   - List the specific problems standing between current reality and the goal.
   - Distinguish big problems from small ones; carry forward only problems that matter for this pass.
   - Do not mistake a cause for the problem. Capture symptoms clearly, but do not jump to solutions yet.

3. **Diagnose root causes**
   - Focus on what is true before deciding what to do about it.
   - Trace each significant problem to the deepest practical cause.
   - Identify whether the failure sits in goal selection, problem identification, diagnosis, design, or execution.
   - Distinguish true causes from visible symptoms, stale names, duplicated paths, and test-only scaffolding.

4. **Design the smallest entropy-reducing plan**
   - Choose the narrowest edit layer that owns the behavior.
   - Go backward before going forward: explain how the current machine produced the bad outcome, then how the changed machine should produce the desired outcome.
   - Prefer hard cutovers over compatibility layers unless an external boundary still requires old behavior.
   - Remove obsolete paths in the same pass when the boundary allows it.
   - For substantial work, write the plan as concrete steps with the expected proof for each step.

5. **Do, measure, and verify**
   - Make scoped edits or execute the necessary tasks.
   - Push through to the success condition rather than stopping at the design.
   - Validate canonical behavior, not implementation trivia.
   - If verification fails, diagnose that failure before adding more changes.

## Output Shape

For substantial work, use this compact structure before coding or in the final handoff:

```text
5-step pass:
- Goal:
- Problems:
- Root cause:
- Solution:
- Proof:
Next target:
```

Whenever the five points are listed out, format those five points as bullets. Keep `Next target:` separate from the five-point list.

For small work, compress the same reasoning into a few sentences.

## Stop Conditions

Stop the pass when one of these is true:

- The success condition is verified.
- A real blocker needs user input or an external state change.
- The remaining work is a separate target that is not required for the current goal.
- Further cleanup would broaden the blast radius without improving the current invariant.
