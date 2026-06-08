# tmux Orchestration

## Session Model

The coordinator uses one tmux session per worker. A worker session is long-lived and can be assigned multiple issues over time.

Recommended session names:

- `harness-coordinator`
- `worker-codex-01`
- `worker-codex-02`
- `worker-claude-01`
- `worker-review-codex-01`
- `worker-review-claude-01`

## Worker Lifecycle

1. Create a tmux session.
2. Start the local agent CLI.
3. Send the assignment prompt.
4. Monitor panes for completion markers or stalled state.
5. Collect branch, commit, PR, and status output.
6. Assign review or fix follow-up.

## Assignment Prompt Shape

Prompts should include:

- Role.
- Issue title and link/path.
- Branch name.
- Objective.
- Acceptance criteria.
- Files likely involved.
- Commands to run.
- Required final response format.

Workers should end with:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```

## Stop Conditions

Stop and escalate only for:

- Missing required credentials or tool permissions.
- Irreversible product/security/architecture choice.
- Repeated CI or review failure after documented attempts.
- Repository state conflict that cannot be safely resolved.

## Script

Use `scripts/tmux_orchestrator.py` to inspect tools and create session skeletons. The script intentionally avoids pretending to be a full autonomous scheduler until the dry-run planning flow is validated.
