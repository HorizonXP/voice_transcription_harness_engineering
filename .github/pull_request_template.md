# Pull Request Summary

<!-- Explain what changed, why it changed, and who benefits. Keep it skimmable. -->

## Linked Issue

<!-- Use Closes #123 when this PR closes a GitHub issue. For pre-issue harness work, link the generated Harness ID or doc. -->

Closes #

## Execution Profile

| Field | Value |
| --- | --- |
| Harness ID |  |
| Implementing Agent |  |
| Model / Effort |  |
| Cross-Reviewer |  |
| Branch |  |

> [!IMPORTANT]
> Keep this PR scoped to the linked issue or harness task. If the work expanded, explain why in **Scope Control**.

## What Changed

| Area | Change |
| --- | --- |
|  |  |

## Scope Control

- [ ] This PR closes or advances exactly one issue/task.
- [ ] Any extra work is listed here with a reason.
- [ ] No unrelated refactors or generated churn were introduced.

## Acceptance Criteria

- [ ] Issue acceptance criteria are satisfied.
- [ ] Scope stayed within the linked issue.
- [ ] Human-readable behavior is documented where needed.
- [ ] Agent-readable artifacts are updated where needed.
- [ ] Issue-prescribed constraints and failure modes were checked.

## Tests And Checks

- [ ] `python3 scripts/harness_plan.py validate --plan generated/harness-plan/plan.json`
- [ ] `python3 -m py_compile scripts/harness_plan.py scripts/github_apply_plan.py scripts/tmux_orchestrator.py`
- [ ] Relevant app or harness tests pass.
- [ ] CI summary artifact is clean or attached failure is understood.

<details>
<summary>Command output or check links</summary>

```text
Paste concise command output or CI links here.
```

</details>

## Reviews

- [ ] Greptile review completed or pending.
- [ ] Greptile findings fixed, replied to with fix commit, and resolved where possible.
- [ ] Cross-agent review completed or explicitly not required.

<details>
<summary>Greptile finding responses</summary>

| Finding | Fix Commit | Response |
| --- | --- | --- |
|  |  |  |

</details>

## CI Failure Handling

If CI failed, start from `artifacts/ci-summary.json` before reading full logs.

| Failed Check | Summary | Fix Commit |
| --- | --- | --- |
|  |  |  |

## Risk

| Risk | Mitigation |
| --- | --- |
|  |  |

## Agent Handoff

```text
HARNESS_STATUS: needs_review
BRANCH:
PR:
SUMMARY:
```
