# Harness Engineering Objective

## Goal Name

Build the reusable multi-agent GitHub/tmux orchestration harness.

## Objective

Design and implement a reusable harness-engineering orchestration system for this repository that can turn a requirements document into a sequenced, dependency-aware GitHub execution plan for multiple AI coding agents.

The goal is not to build the Windows voice transcription app yet. The goal is also not to immediately create all GitHub Issues and Projects as a one-off manual act. Instead, build the repository artifacts, scripts, schemas, templates, and documented workflow that can take `docs/requirements.md` as input, produce a high-quality issue/project/PR plan, and later apply that plan to GitHub when explicitly run in apply mode.

The harness should be reusable for future requirements documents. A later feature, module, or product requirement should be feedable into the same system and produce a similarly structured execution plan.

The system should coordinate multiple AI coding agents, including Codex and Claude Code, using GitHub Issues, GitHub Pull Requests, GitHub Projects, GitHub Actions CI, Greptile PR review, and tmux as the primary control surfaces.

## Requirements-To-Workflow Pipeline

The pipeline should support these stages:

1. Parse and analyze a requirements document.
2. Produce a structured decomposition into epics, milestones, issues, dependencies, parallelization groups, agent-role recommendations, review expectations, and acceptance criteria.
3. Render beautifully formatted, human-readable and agent-readable GitHub Issue bodies, PR templates, labels, milestones, and project metadata.
4. Validate the generated plan for missing dependencies, oversized issues, unclear acceptance criteria, duplicate labels, impossible sequencing, and excessive human-decision points.
5. Support a dry-run mode that writes the generated plan to repository artifacts without mutating GitHub.
6. Support a later explicit apply mode that creates or updates GitHub Issues, labels, milestones, and Projects through GitHub CLI/API-backed commands.
7. Support repeatable and idempotent execution so rerunning the harness does not create uncontrolled duplicate issues or project state.

## GitHub Surface

GitHub Issues and Pull Requests should be beautifully formatted, well-designed, human-readable, and agent-readable. They should give humans confidence that the work is clear, bounded, reviewed, tested, and progressing appropriately.

Use GitHub-flavored Markdown, checklists, tables, linked dependencies, labels, milestones, status fields, acceptance criteria, risk sections, implementation notes, review instructions, and agent handoff metadata where useful.

The GitHub surface should be stream-friendly and operationally useful. Issues, labels, project fields, milestones, PRs, reviews, CI checks, artifacts, and status updates should make it obvious what is being built, who or what is working on it, what is blocked, what can run in parallel, what passed review, and what is ready to merge.

## Agent Orchestration

The orchestration layer should include scripts and documentation for running a long-lived coordinating agent that monitors tmux sessions, assigns work to Codex and Claude Code worker sessions, tracks progress, collects results, and moves work through issue, branch, pull request, review, CI, fix, and ready-to-merge states.

The tmux orchestration should support interactive agent sessions and may also support local non-interactive Codex/Claude CLI prompt runs where useful. Do not use paid API calls for agent orchestration. Use the locally installed Codex and Claude Code CLIs/subscriptions available on this machine, or detect and document missing tools clearly.

When non-interactive agent runs are used, define the prompt shape, expected output format, model/thinking-effort guidance, timeouts, retry behavior, and review checkpoints instead of treating them as one-shot black boxes.

The harness should support role-aware assignment:

- Codex should be favored for architecture, backend logic, Windows integration, CI, testing, review, and refactoring tasks.
- Claude Code should be favored for UI, visual design, interaction polish, UX structure, and design-sensitive implementation tasks.
- The system should support cross-review workflows where Codex reviews Claude Code work and Claude Code reviews Codex work.

## Greptile Review Loop

The system should integrate Greptile as an automated pull request reviewer.

For each PR, the orchestrator should wait for Greptile's review, collect all findings, assign the original coding agent or a follow-up agent to fix them, push a fix commit, reply to each Greptile inline review thread with the exact fix commit and explanation, and resolve the relevant review threads when possible.

## CI And Repair Loop

The system should include CI and testing infrastructure as a first-class harness concern.

CI should be fast, economical, reliable, and structured for both human and AI consumption. Logs should be concise and segmented. Failures should produce machine-readable summaries, artifacts, and direct pointers to likely failing files/tests so an agent can repair CI failures without searching through noisy logs.

The harness should research and document an appropriate testing strategy for the native Windows 11 app stack, including unit, integration, UI, packaging, and smoke-test layers where appropriate. This goal may produce CI workflows, test reporting conventions, and failure-summary tooling, but it should not implement the actual application features yet.

## Deliverables

- `docs/harness/` architecture and operating docs.
- Worker role definitions for Codex, Claude Code, coordinator, reviewer, and CI fixer.
- Requirements decomposition schema.
- Generated dry-run issue/project plan for `docs/requirements.md`.
- GitHub Issue and PR templates.
- Label, milestone, status, and project-field conventions.
- GitHub setup/apply script with dry-run default.
- tmux orchestration scripts.
- Local Codex/Claude CLI invocation guidance where useful.
- Greptile review handling workflow.
- CI strategy and initial GitHub Actions harness.
- Machine-readable CI failure summary format.
- Demo workflow showing one planned issue moving through assignment, PR, review, CI, fix, and ready-to-merge states.

## Non-Goals

- Do not build the Windows transcription app implementation yet.
- Do not manually create the full GitHub issue backlog as an unreproducible one-off.
- Do not call paid model APIs for orchestration.
- Do not assume Claude Code, Codex CLI, Greptile, or GitHub Projects permissions are available without detection and clear failure handling.
- Do not make the harness depend on a single requirements document format so tightly that it cannot be reused.

## Operating Rule

Use judgment for low-risk implementation details. Ask the user only for decisions that materially affect architecture, orchestration model, GitHub workflow, CI strategy, review policy, security, cost, or live-demo clarity.
