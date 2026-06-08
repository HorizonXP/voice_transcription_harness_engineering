# Agent Operating Rules

This repository is intended to be developed through coordinated agent work.

## Repository Mission

The repository demonstrates harness engineering for a native Windows 11 voice transcription app. The app implementation should be built incrementally through GitHub Issues, GitHub Pull Requests, GitHub Projects, CI, Greptile review, tmux sessions, and coordinated Codex/Claude Code agents.

Do not jump straight to building the app unless assigned a specific generated issue. The harness and requirements are the source of truth for sequencing.

## Human Attention

Treat human attention as the scarcest resource in the project.

Agents should use sound engineering judgment for simple, reversible, low-risk decisions instead of interrupting the user. Ask the user only for decisions that materially affect product direction, privacy, cost, security, architecture, or user experience.

When making a judgment call, document the decision in the relevant artifact and keep the implementation easy to revise.

## Pull Request Discipline

From this point forward, repository changes should go through pull requests.

- Create a branch for every coherent change.
- Use a separate Git worktree for each parallel worker/issue whenever possible.
- Use the repository pull request template.
- Keep each PR scoped to one issue or one explicit harness task.
- Run relevant validation before opening the PR.
- Do not bypass Greptile review.
- Reply to Greptile findings with the exact fix commit and concise explanation.
- Resolve review threads when GitHub permissions allow it.
- Keep `main` clean and protected once branch protection is enabled.

## Worktree Isolation

Parallel workers must avoid sharing the same checkout.

Use Git worktrees for issue work whenever possible:

```sh
git fetch origin
git worktree add ../voice-transcription-worktrees/<branch-name> -b <branch-name> origin/main
cd ../voice-transcription-worktrees/<branch-name>
```

Recommended branch naming:

```text
work/<harness-id>-short-title
review/<harness-id>-short-title
fix/<pr-number>-greptile
```

Rules:

- One issue branch per worktree.
- One tmux worker session per worktree.
- Do not run multiple implementation agents in the same checkout.
- Do not reuse another worker's worktree unless explicitly assigned a review/fix task for that branch.
- Before starting, verify the worktree branch and status with `git status --short --branch`.
- After pushing and opening a PR, leave the worktree intact until review and CI repair are complete.
- Remove worktrees only after the PR is merged or abandoned.

Worktree cleanup:

```sh
git worktree list
git worktree remove ../voice-transcription-worktrees/<branch-name>
git branch -d <branch-name>
```

## GitHub Formatting Standard

Issues, PRs, generated plans, and review replies should be beautiful, human-readable, and agent-readable.

Use GitHub-supported formatting when it improves comprehension:

- Alerts for critical instructions.
- Tables for metadata.
- Tasklists for executable work and acceptance criteria.
- Mermaid diagrams for dependency or status flow.
- Fenced code blocks for commands, prompts, and expected output.
- Collapsed `<details>` blocks for long logs, review details, or escalation rules.
- Autolinks for issues, PRs, commits, and docs.

Do not create ad hoc plain-text PR bodies when a template exists.

## Planning Loop

The deterministic generated plan is a sample and regression fixture. Production planning should use:

1. Codex as the primary planner with extra-high reasoning.
2. Claude Code as the critic planner with extra-high reasoning.
3. Codex as the reconciler with extra-high reasoning.
4. Claude Code verifies that the reconciliation addressed the critique or reports remaining gaps.
5. Harness validation and rendering before any GitHub apply step.

The critic should critique the plan, not rewrite it directly. The reconciler should preserve stable issue IDs where possible.

If the critic reports unresolved gaps after reconciliation, the coordinator must halt GitHub apply mode until Codex reconciles those gaps or records a documented reason for deferring them.

Do not use paid model API calls for orchestration. Use local CLI/subscription tools available on this machine. If the requested model or effort is unavailable, stop and report the limitation instead of silently downgrading.

## Worker Expectations

Generated issues should carry enough detail that low or medium reasoning workers can execute safely.

Workers should:

- Work from their assigned issue worktree, not the coordinator checkout.
- Read `docs/requirements.md`, relevant ADRs, and the assigned issue before editing.
- Follow the prescribed implementation plan and constraints.
- Keep changes focused.
- Run listed checks.
- Open a PR using the template.
- Report completion in the required `HARNESS_STATUS` format when operating through tmux.

## Review Expectations

- Codex reviews Claude Code work for architecture, correctness, maintainability, tests, Windows integration, and security.
- Claude Code reviews Codex work for UX, visual design, interaction clarity, native Windows feel, and user-facing copy.
- Greptile review findings are first-class work items.
- CI failures should be handled from machine-readable summaries first, then full logs only when needed.

## Defaults

- Prefer current official documentation over memory for time-sensitive platform, framework, model, API, pricing, or packaging choices.
- Prefer native Windows 11 implementation choices over cross-platform shortcuts.
- Prefer small, reviewable changes with clear commits.
- Preserve user changes and do not rewrite unrelated work.
- Prefer deterministic, idempotent scripts for GitHub setup and apply operations.
- Prefer documenting low-risk judgment calls over asking the user to make every minor choice.
