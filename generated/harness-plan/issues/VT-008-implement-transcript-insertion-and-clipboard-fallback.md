# Implement transcript insertion and clipboard fallback

> Harness ID: `VT-008`

## Outcome

Insert final transcripts into the active text target and fall back to clipboard on failure.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `insertion` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-003, VT-006 |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Active text insertion is the default delivery path.
- [ ] Clipboard fallback runs when insertion fails.
- [ ] Fallback is visible to the user and history retains the transcript.

## Acceptance Criteria

- [ ] Insertion adapter has a clear success/failure contract.
- [ ] Clipboard fallback is tested or manually smoke-tested.
- [ ] Failure does not drop transcript text.

## Review Plan

- [ ] Codex reviews Windows insertion behavior.
- [ ] Claude reviews fallback notification UX.

## CI Expectations

- [ ] Tests cover insertion success and fallback paths where feasible.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-008-implement-transcript-insertion-and-clipboard-fallback` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
