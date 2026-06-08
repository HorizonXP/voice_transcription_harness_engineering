# Implement microphone recording lifecycle

> Harness ID: `VT-006`

## Outcome

Capture audio from the default microphone for push-to-talk transcription.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `recording` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-003, VT-005 |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Start/stop recording follows hotkey state.
- [ ] Missing microphone permission or device failure produces clear errors.
- [ ] Audio is not retained by default after transcription completes.

## Acceptance Criteria

- [ ] Recorder exposes audio data in the provider-required format or through a conversion path.
- [ ] Cancellation and failure are handled.
- [ ] Audio level information is available for the HUD where feasible.

## Review Plan

- [ ] Codex reviews recording lifecycle and cleanup.
- [ ] Claude reviews error visibility requirements.

## CI Expectations

- [ ] Recorder tests or documented manual smoke test exists.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-006-implement-microphone-recording-lifecycle` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
