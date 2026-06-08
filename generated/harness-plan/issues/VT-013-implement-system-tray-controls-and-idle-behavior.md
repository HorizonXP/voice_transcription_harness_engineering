# Implement system tray controls and idle behavior

> Harness ID: `VT-013`

## Outcome

Run quietly in the system tray with app status and basic actions.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation-parallel` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-001 |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:1`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Tray icon indicates app availability.
- [ ] Tray menu exposes settings and exit.
- [ ] Idle behavior does not interrupt foreground work.

## Acceptance Criteria

- [ ] Tray integration works with the selected app model.
- [ ] Settings can be opened from tray.
- [ ] Exit cleanly releases hotkey and recording resources.

## Review Plan

- [ ] Codex reviews tray lifecycle.
- [ ] Claude reviews tray menu wording and UX.

## CI Expectations

- [ ] Manual smoke test checklist exists for tray behavior.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-013-implement-system-tray-controls-and-idle-behavior` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
