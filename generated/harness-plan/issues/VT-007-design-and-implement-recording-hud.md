# Design and implement recording HUD

> Harness ID: `VT-007`

## Outcome

Create the compact Windows 11 HUD for recording, transcribing, error, and completed states.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `recording-parallel` |
| Recommended Agent | `agent:claude` |
| Dependencies | VT-001, VT-003 |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:2`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] HUD is horizontally centered near the lower screen area and inset above the bottom edge.
- [ ] HUD shows recording state, audio activity, and transcription progress.
- [ ] HUD dismisses automatically after insertion completes.

## Acceptance Criteria

- [ ] HUD does not steal focus unnecessarily.
- [ ] All required states are represented.
- [ ] Text and controls fit across expected desktop scaling conditions.

## Review Plan

- [ ] Claude reviews visual and interaction quality.
- [ ] Codex reviews state-machine integration.

## CI Expectations

- [ ] UI smoke test or manual verification checklist exists.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-007-design-and-implement-recording-hud` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
