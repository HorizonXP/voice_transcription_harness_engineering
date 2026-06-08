# Polish settings, HUD, and transcript history UX

> Harness ID: `VT-015`

## Outcome

Refine the native Windows 11 user experience across settings, HUD, and history.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M4 Polish And Release Readiness |
| Phase | `phase:4` |
| Parallel Group | `release` |
| Recommended Agent | `agent:claude` |
| Dependencies | VT-004, VT-007, VT-009, VT-011, VT-012 |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:4`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Ensure controls are compact, clear, and native-feeling.
- [ ] Verify provider selection and credential states are understandable.
- [ ] Verify history deletion and retention controls are easy to find.

## Acceptance Criteria

- [ ] UI fits without overlap at common desktop scaling settings.
- [ ] User-facing copy is concise and actionable.
- [ ] Claude and Codex reviews agree the UI is ready for release candidate testing.

## Review Plan

- [ ] Claude primary design review.
- [ ] Codex reviews implementation integration and accessibility risks.

## CI Expectations

- [ ] UI smoke artifacts or screenshots are attached where possible.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-015-polish-settings-hud-and-transcript-history-ux` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
