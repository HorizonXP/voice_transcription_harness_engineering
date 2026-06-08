# Agent Roles

## Coordinator

The coordinator owns issue assignment, tmux session monitoring, status updates, and escalation. It should not perform feature work unless the work is a harness bug fix or an explicit emergency unblock.

## Primary Planner

Use Codex with GPT-5.5 extra-high reasoning for requirements decomposition and issue planning.

The primary planner produces the draft harness-plan JSON, including issue sequencing, dependency groups, model/effort recommendations, acceptance criteria, review policy, and CI expectations.

## Critic Planner

Use Claude Code Opus 4.8 extra-high effort as a planning critic before GitHub apply mode.

The critic planner reviews the Codex draft for missing issues, oversized tasks, weak UI/design coverage, unclear acceptance criteria, bad sequencing, insufficient worker instructions, and places where the assigned model or reasoning level is too weak.

The critic should produce structured critique, not directly mutate the plan.

If the critic is blocked because required input, tool access, or the requested model/effort is unavailable, it should return `CRITIQUE_STATUS: blocked`, explain the blocker, and mark the plan unsafe to apply.

## Reconciler

Use Codex with GPT-5.5 extra-high reasoning to reconcile accepted critique into the final harness-plan JSON.

The reconciler should preserve stable issue IDs when possible and explain any ID/title changes in the generated plan notes.

After reconciliation, Claude Code should perform a sign-off pass. If the critic reports `needs_changes` or `blocked`, the coordinator must not apply the plan to GitHub until the unresolved findings are reconciled or explicitly deferred with a documented rationale.

## Codex Worker

Use Codex for:

- Architecture.
- Backend and service logic.
- Windows integration.
- Provider adapters.
- CI and test infrastructure.
- Refactoring.
- Reviewing implementation correctness.

Suggested local invocation:

```sh
codex
```

For non-interactive use, prefer local CLI modes only when available on the machine. Do not use paid API calls.

## Claude Code Worker

Use Claude Code for:

- UI layout.
- Visual polish.
- Interaction design.
- WinUI surface refinement.
- User-facing copy in UI.
- Reviewing design coherence and usability.

Suggested local invocation:

```sh
claude
```

## Reviewer

Reviewer agents inspect a PR from a different perspective than the implementer:

- Codex reviews Claude Code PRs for architecture, correctness, tests, and maintainability.
- Claude Code reviews Codex PRs for usability, visual consistency, interaction polish, and product fit.

## CI Fixer

The CI fixer consumes machine-readable CI summaries and fixes failing checks. It should start from the failure artifact before reading full logs.

## Assignment Policy

Default assignment:

- `agent:codex` for foundations, test infrastructure, provider contracts, Windows APIs, GitHub automation, and review loops.
- `agent:claude` for HUD, settings UI, native visual polish, interaction details, and design-system alignment.
- `agent:either` for documentation, issue templates, small glue scripts, and low-risk cleanup.

## Model And Reasoning Policy

Generated issues must prescribe model and reasoning effort.

- Use GPT-5.5 extra-high reasoning through the local Codex CLI for requirements decomposition and issue planning.
- Use Claude Code Opus 4.8 extra-high effort through the local Claude CLI for planning critique.
- Use GPT-5.5 through the local Codex CLI for Codex workers.
- Use low reasoning only when the issue has narrow scope, clear acceptance criteria, and no architectural/security/API ambiguity.
- Use medium reasoning for foundation, Windows integration, provider, CI, security, review-loop, and test infrastructure work.
- Escalate to high or extra-high only for planning/decomposition, architecture decisions, security-sensitive design, or hard cross-cutting failures.
- Use Claude Code Sonnet with medium effort for most UI/design implementation issues.
- Escalate Claude Code to Opus/high effort only for major visual system decisions or ambiguous UX tradeoffs.

The planner should pay the thinking cost up front. Worker issues should be detailed enough that lower/medium reasoning agents can execute without re-deriving the whole plan.

## Handoff Contract

Every agent handoff should include:

- Issue URL or generated issue path.
- Branch name.
- Expected files or areas.
- Acceptance criteria.
- Test command.
- Review focus.
- Stop conditions.
