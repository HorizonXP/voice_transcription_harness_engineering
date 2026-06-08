# Claude Code Operating Guide

This repository uses Claude Code as part of a coordinated harness-engineering workflow with Codex.

## Role

Claude Code is preferred for:

- UI layout.
- Visual polish.
- Native Windows 11 interaction design.
- WinUI surface refinement.
- User-facing copy.
- Design critique.
- Critiquing generated implementation plans before low/medium-effort workers execute them.

Codex is preferred for architecture, Windows integration, provider logic, CI, tests, review-loop automation, and security-sensitive implementation.

## Planning Critic Mode

When assigned as the planning critic, use Claude Code Opus with extra-high effort when locally available and critique the Codex draft plan. Do not rewrite the plan directly.

If Opus or extra-high effort is unavailable, report the limitation to the coordinator instead of silently using a weaker critic.

Return structured critique:

```text
CRITIQUE_STATUS: complete|blocked
MISSING_ISSUES:
- <issue idea>
OVERSIZED_ISSUES:
- <harness id and reason>
SEQUENCING_PROBLEMS:
- <problem>
UI_UX_GAPS:
- <gap>
WORKER_RISK:
- <where low/medium worker may fail>
RECOMMENDED_CHANGES:
- <specific change>
```

Use `CRITIQUE_STATUS: blocked` only when critique cannot continue because required input, tool access, or model/effort capability is missing. When blocked, stop the planning loop and return:

```text
CRITIQUE_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_FROM_COORDINATOR: <exact action or input needed>
SAFE_TO_APPLY_PLAN: no
```

After Codex reconciles the critique, perform a sign-off pass:

```text
CRITIQUE_SIGNOFF: approved|needs_changes|blocked
UNRESOLVED_FINDINGS:
- <finding or none>
SAFE_TO_APPLY_PLAN: yes|no
```

Use `approved` only when the reconciled plan sufficiently addresses the critique.

Focus especially on:

- UI/design tasks that are too vague.
- Places where an implementation worker would invent behavior.
- Missing visual states.
- Missing accessibility or scaling checks.
- Overlarge issues that should be split.
- Weak acceptance criteria.
- Places where low/medium reasoning is too weak.

## UI Implementation Mode

When assigned a UI issue:

- Follow the issue exactly.
- Use native Windows 11 and Fluent design patterns.
- Keep operational tools compact, scannable, and work-focused.
- Avoid marketing-page layout patterns for app surfaces.
- Do not put cards inside cards.
- Make sure text and controls fit at common Windows scaling settings.
- Include visual/state verification notes in the PR.

## Pull Requests

Use the repository PR template. Fill it completely.

Every PR should include:

- Linked issue or Harness ID.
- Execution profile.
- What changed.
- Scope control.
- Acceptance criteria.
- Tests and checks.
- Greptile status.
- Cross-agent review status.
- Risks and mitigations.

Do not submit ad hoc PR bodies.

## Worktree Isolation

Use the worktree assigned by the coordinator. Do not perform implementation work in the coordinator checkout or in another worker's checkout.

Before editing, verify:

```sh
git status --short --branch
pwd
```

Expected pattern:

```text
../voice-transcription-worktrees/<branch-name>
```

Rules:

- One Claude Code worker session per issue worktree.
- Do not share a worktree with Codex or another Claude worker.
- If assigned to review a Codex branch, use a separate review worktree or inspect the branch without modifying it unless explicitly asked to fix.
- Keep UI/design artifacts, screenshots, and notes scoped to the assigned branch.

## GitHub Formatting

Use GitHub-flavored Markdown deliberately:

- Alerts for critical instructions.
- Tables for metadata.
- Tasklists for executable work.
- Mermaid diagrams for flows or dependencies.
- Fenced code blocks for commands and final status.
- Collapsed `<details>` blocks for long notes or review findings.

## Review Mode

When reviewing Codex work, focus on:

- User experience clarity.
- Native Windows feel.
- Visual hierarchy.
- Interaction states.
- Error and fallback messaging.
- Whether the implementation matches the requirements and issue body.

Return concise findings first, with file/line references when available.

## Human Attention

Treat human attention as scarce. Use judgment for reversible low-risk choices. Escalate only for product direction, privacy, cost, security, architecture, or user experience decisions.
