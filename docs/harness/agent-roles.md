# Agent Roles

## Coordinator

The coordinator owns issue assignment, tmux session monitoring, status updates, and escalation. It should not perform feature work unless the work is a harness bug fix or an explicit emergency unblock.

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

## Handoff Contract

Every agent handoff should include:

- Issue URL or generated issue path.
- Branch name.
- Expected files or areas.
- Acceptance criteria.
- Test command.
- Review focus.
- Stop conditions.
