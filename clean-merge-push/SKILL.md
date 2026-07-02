---
name: clean-merge-push
description: Use when the user asks to run owner-clean on your work, commit the bounded work, merge develop or the current branch into main/master, run pnpm verify or the repository's release gate, push main/master plus develop/current branch to remote, and end back on develop when available. Applies across software repositories. Requires a clean worktree after the owned commit before branch switching, merging, verifying release, or pushing. Keeps unrelated work out of the commit, prefers fast-forward merges, allows normal merge commits when the repo's branch history requires them, verifies before/after commit, and reports exact branch/push state.
---

# Clean Merge Push

## Goal

Run an owner-clean finishing pass, turn a bounded local software change into an intentional commit, carry it through the repository's established integration path, verify the release branch, and push the branches that policy allows.

## Principles

- Preserve unrelated user work. Never stage unrequested files, generated churn, local lockfiles, logs, or editor metadata unless they are part of the requested change.
- Start from the completed work, not a whole-tree cleanup. Use `$owner-clean` first when available, then commit only the owned slice.
- After the owned commit, require a clean worktree before continuing. Do not switch branches, merge, run the release verification gate, or push while `git status --short` shows staged, unstaged, or untracked entries.
- Prefer fast-forward merges when the branch graph allows them. Normal merge commits are allowed for integration or release branch merges when the repository's existing branch history requires them, or when the user explicitly approves them. Never use merge commits to paper over unrelated dirty work, stale upstream refs, or unresolved branch divergence.
- Honor the repository's branch flow before generic defaults. If the repo uses `develop`, the normal path is `feature -> develop -> main/master`; never skip directly from feature to `main` or `master` unless the user explicitly asks.
- Do not rebase, force-push, reset, checkout files, or delete changes without explicit user approval.
- Verify the smallest meaningful test lane first, then broaden when the change touches shared contracts or the user asks for a full gate.
- Treat toolchain drift separately from the commit slice. Report stale global tools or pre-existing lint failures without mixing broad cleanup into the commit.

## Workflow

1. Inspect the repository:
   - `git status --short --branch`
   - `git log --oneline --decorate -5`
   - `git remote -v`
   - `git branch --show-current`
   - `git branch --list main master develop`
   - If available, run the project or user clean-commit inspector.

2. Run the owner-clean pass:
   - If `$owner-clean` is installed, read and follow it for one bounded pass over the current work before staging.
   - Record the owner decision, any cleanup performed, and any unrelated changes intentionally left alone.
   - Treat cleanup edits as part of the owned commit slice. Do not continue to branch synchronization or merging until those edits are committed.
   - If `$owner-clean` is unavailable or ownership is irrelevant, state that as an assumption and continue without inventing a replacement workflow.

3. Identify the source, integration, and release branches:
   - Source branch is usually the current branch.
   - Integration branch is `develop` when it exists, unless repo evidence clearly says otherwise.
   - Release branch is `main` if it exists, otherwise `master`.
   - If `develop` exists and the source branch is not `develop`, merge source into `develop` first. Only after `develop` contains the source commit may you merge `develop` into `main` or `master`.
   - If both `main` and `master` exist and the target is ambiguous, inspect upstream/default branch evidence before choosing. Ask only if evidence is unclear.
   - The intended endpoint is a pushed release branch. After the source has reached `develop` when applicable, merge `develop` into `main` or `master` and attempt to push the release branch. If hooks or branch protection block that push, report the exact blocker and the required manual/PR step. Do not bypass the hook.

4. Bound the commit slice:
   - Review unstaged, staged, and untracked files.
   - If staged changes already exist before this workflow, stop and ask how to handle them.
   - Stage only intended paths with `git add -- <paths>`.
   - Leave unrelated untracked files alone.

5. Verify before committing:
   - Run focused tests for touched code.
   - Run typecheck/build/lint when the project treats them as correctness gates or the change crosses shared boundaries.
   - Run `git diff --check` before staging or `git diff --cached --check` after staging.
   - If a needed command is blocked by sandbox permissions, rerun with escalation rather than silently skipping it.

6. Commit:
   - Use Conventional Commits when the repo does not specify another format.
   - Keep the subject under 72 characters where practical.
   - Write non-trivial messages to a temporary file and commit with `git commit -F <file>`.
   - Verify the commit with `git show --stat --summary --format=fuller -1`.
   - Run `git status --short` immediately after committing. If anything remains, stop before branch switching or merging. Commit owned residue when it belongs to the current work; otherwise report the unrelated dirty state and ask before continuing.

7. Sync and merge:
   - Before every branch switch, merge, release verification, and push, confirm `git status --short` is empty. Stop on any staged, unstaged, or untracked entry; do not stash, discard, or sweep it into the commit without explicit approval.
   - Fetch the remote before merging: `git fetch origin`. If fetch is unavailable, stop before touching integration/release branches unless the user explicitly accepts stale remote knowledge.
   - Check every branch that will be touched against its upstream before merging:
     - Source: if `origin/<source-branch>` exists and local source is behind or diverged, fast-forward/pull only when clean and safe; never rebase or force.
     - Integration: before merging into `develop`, switch to `develop` and fast-forward from `origin/develop` first: `git merge --ff-only origin/develop`.
     - Release: before merging into `main` or `master`, switch to the release branch and fast-forward from `origin/<release-branch>` first: `git merge --ff-only origin/<release-branch>`.
   - If any touched branch cannot fast-forward from upstream, stop and report the divergence; do not publish until the user chooses a merge/rebase/PR strategy.
   - Ensure the source branch contains the intended commit after the upstream check.
   - If `develop` exists and source is not `develop`, switch to `develop` after syncing it from upstream and fast-forward only: `git merge --ff-only <source-branch>`.
   - Only after the integration branch contains the commit, switch to the release branch after syncing it from upstream: `git switch main` or `git switch master`.
   - Merge from the integration branch when it exists: first try `git merge --ff-only develop`; if that fails because the release branch already has prior integration merge commits and the user has approved normal merge commits, use a regular `git merge develop`. If there is no integration branch, apply the same rule to the source branch.
   - If the commit was created directly on the release branch, switch back to the source/integration branch and fast-forward it from the release branch when the user asked to push both.

8. Verify the release branch:
   - After switching to `main` or `master` and merging the intended source/integration branch, run the repository's release gate before pushing.
   - If the user specifically asked for `pnpm verify` and the repository has pnpm metadata, run `pnpm verify`.
   - If `pnpm verify` is absent, run the closest documented verification command and report the substitution as an assumption.
   - If verification fails because of the current work, switch back to the owning branch when needed, fix the owned slice, recommit, repeat the integration path, and rerun verification.
   - If verification fails for unrelated or pre-existing reasons, stop before pushing release branches and report the exact blocker.

9. Push branches in policy order:
   - `git push origin <source-branch>`
   - If an integration branch exists: `git push origin develop`
   - Always attempt the release push after the integration branch is updated: `git push origin <release-branch>`.
   - If a hook blocks the release push, do not retry or bypass; report the exact hook message and the PR/manual step needed.
   - Confirm with `git rev-parse HEAD <source-branch> <integration-branch-if-any> <release-branch> origin/<source-branch> origin/<integration-branch-if-any> origin/<release-branch>`.

10. Return to the working branch:
   - If `develop` exists, end by switching back to it: `git switch develop`.
   - If there is no `develop`, switch back to the original source branch.
   - If switching back is blocked by local changes or hooks, report the exact blocker and the branch you are still on.

11. Final status:
   - Run `git status --short --branch`.
   - Report any remaining untracked or unstaged files separately from the published work.

## Reporting

Include:

- Commit hash and subject.
- Source, integration, and release branch state. Say explicitly whether the release branch was pushed, blocked, or needs PR/manual approval.
- Verification commands that passed.
- Checks that could not run and exact reason.
- Remaining local changes or untracked files.
- Current checked-out branch.
