# Harness Architecture

## Purpose

The harness turns a requirements document into an execution plan that coordinated agents can carry out through GitHub and tmux.

The harness does not build the application directly. It creates the substrate for building the application incrementally: issues, labels, milestones, project metadata, role assignments, review expectations, CI expectations, and orchestration instructions.

## Operating Model

The harness has two modes:

- `dry-run`: generate plan files under `generated/harness-plan/` without mutating GitHub.
- `apply`: create or update GitHub labels, milestones, issues, and project metadata from a generated plan. This must be explicitly requested.

Dry-run is the default because the plan should be inspectable before GitHub is changed.

## Planner Model

The checked-in dry-run plan is a deterministic sample and regression fixture. It proves the renderer, validator, templates, and GitHub apply path.

The intended production workflow is different:

1. Run a high-capability planner against the requirements document.
2. Use GPT-5.5 extra-high reasoning through the local Codex CLI/subscription for decomposition.
3. Start a separate tmux session running Claude Code Opus 4.8 extra-high effort as a planning critic.
4. Ask Claude to critique the decomposition for missing work, unclear issues, bad sequencing, weak UI/design coverage, insufficient worker instructions, and places where low/medium-effort workers may fail.
5. Feed Claude's critique back to the Codex planner for reconciliation.
6. Produce the same structured harness-plan JSON shape.
7. Validate the plan with `scripts/harness_plan.py validate`.
8. Render and inspect the issue markdown.
9. Apply to GitHub only after explicit human approval.

Do not use paid API calls for this planning stage. Use the local Codex CLI/subscription available on the machine. If the CLI cannot provide the requested model or reasoning level, stop and document the tool limitation instead of silently downgrading the planner.

The Claude critique stage should also use the local Claude Code subscription/CLI. If Opus 4.8 or extra-high effort is unavailable locally, the planner should stop and report the limitation rather than silently falling back to a weaker critique.

## Planning Review Loop

The production planning loop has three roles:

- Primary planner: Codex, GPT-5.5, extra-high reasoning.
- Critic planner: Claude Code, Opus 4.8, extra-high effort.
- Reconciler: Codex, GPT-5.5, extra-high reasoning.

The critic should not rewrite the plan directly. It should produce structured critique:

- Missing issues.
- Oversized issues.
- Dependency or sequencing problems.
- UI/UX gaps.
- Review/CI gaps.
- Places where the worker model or reasoning effort is too low.
- Ambiguous acceptance criteria.
- Human decisions that should not be asked because they are low-risk.

The reconciler turns accepted critique into the final plan JSON, preserving stable IDs where possible.

## Pipeline

1. Read a requirements document.
2. Create a structured work breakdown.
3. Assign milestones, dependency groups, labels, and recommended agent roles.
4. Render issue bodies and project metadata.
5. Validate the plan for missing dependencies, duplicate identifiers, unclear acceptance criteria, and invalid labels.
6. Optionally apply the plan to GitHub.
7. Use tmux orchestration to assign issues to Codex and Claude Code workers.
8. Move work through implementation, PR, CI, Greptile review, cross-agent review, fixes, and ready-to-merge.

## Repository Artifacts

- `docs/harness/objective.md`: full objective and non-goals.
- `docs/harness/architecture.md`: harness design.
- `docs/harness/github-workflow.md`: issue, PR, label, milestone, and project conventions.
- `docs/harness/agent-roles.md`: role definitions and assignment guidance.
- `docs/harness/tmux-orchestration.md`: local worker session model.
- `docs/harness/greptile-review-loop.md`: automated review handling protocol.
- `docs/harness/ci-strategy.md`: fast CI and agent-readable failure summary strategy.
- `schemas/harness-plan.schema.json`: machine-readable generated-plan contract.
- `scripts/harness_plan.py`: generate and validate a dry-run plan.
- `scripts/github_apply_plan.py`: explicit GitHub apply mode.
- `scripts/tmux_orchestrator.py`: tmux worker session helper.
- `generated/harness-plan/`: generated dry-run plan outputs.

## Idempotency

Every generated issue has a stable `id`. Apply mode must tag GitHub-created resources with stable identifiers in issue bodies and labels so reruns can update instead of duplicating. Generated issue bodies include a `Harness ID` line for this purpose.

## Human Attention Rule

Agents should use judgment for reversible low-risk choices. Add open decisions only when a choice materially affects architecture, orchestration, GitHub workflow, CI, review policy, security, cost, or live-demo clarity.
