# Implement global push-to-talk hotkey handling

> Harness ID: `VT-005`

## Outcome

Implement configurable global push-to-talk hotkey handling with conflict detection.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `recording` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-001, VT-003 |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Default hotkey is Ctrl+Win+H.
- [ ] Press starts recording and release stops recording.
- [ ] Settings validation rejects detectable conflicts.

## Acceptance Criteria

- [ ] Hotkey lifecycle is testable.
- [ ] Conflict detection failure is shown to the user.
- [ ] The app does not accept a detected conflicting hotkey.

## Review Plan

- [ ] Codex reviews Windows API correctness.
- [ ] Claude reviews user feedback for conflicts.

## CI Expectations

- [ ] Unit or integration tests cover hotkey state transitions where possible.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-005-implement-global-push-to-talk-hotkey-handling` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
