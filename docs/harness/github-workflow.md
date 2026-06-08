# GitHub Workflow

## Issues

Issues are the unit of assignable work. Each generated issue should be small enough for one agent to complete in a focused branch and pull request.

Issue bodies should include:

- Stable harness metadata.
- Outcome.
- Context.
- Scope.
- Acceptance criteria.
- Dependencies.
- Parallelization group.
- Recommended agent role.
- Review plan.
- CI expectations.
- Human notes when relevant.

## Pull Requests

Pull requests should close exactly one issue by default. Larger PRs need an explicit reason.

PRs should include:

- Linked issue.
- Summary.
- Files changed.
- Acceptance criteria checklist.
- Tests run.
- CI artifact links when available.
- Greptile review status.
- Cross-agent review status.
- Known risks.

## Labels

The generated label set uses prefixes so humans can scan quickly:

- `type:*` for work type.
- `area:*` for product or harness area.
- `agent:*` for recommended primary agent.
- `phase:*` for sequencing.
- `priority:*` for urgency.
- `status:*` for workflow status.
- `review:*` for review state.
- `ci:*` for CI state.

Labels should be created idempotently by `scripts/github_apply_plan.py`.

## Milestones

Milestones group sequenced work. For this repository, milestone names should remain human-readable and not overfit to one implementation language.

## Projects

The GitHub Project should expose:

- Status.
- Phase.
- Agent.
- Parallel group.
- Blocked by.
- Review state.
- CI state.

GitHub Projects apply mode may require extra permissions. The harness should detect permission failures and provide exact next steps rather than partially hiding the failure.

## Status Flow

Recommended status flow:

1. `Backlog`
2. `Ready`
3. `Assigned`
4. `In Progress`
5. `PR Open`
6. `CI Fix Needed`
7. `Greptile Fix Needed`
8. `Cross Review`
9. `Ready To Merge`
10. `Done`

Blocked work should use `Blocked` plus a comment explaining the blocker and owner.
