# Implement persistent transcript history

> Harness ID: `VT-009`

## Outcome

Persist full transcript text by default with retention and clear-history controls.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `history` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-003, VT-008 |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Store full transcript text by default.
- [ ] Default retention is 30 days.
- [ ] Support manual clearing.
- [ ] Do not log full transcripts by default.

## Acceptance Criteria

- [ ] History storage is bounded by retention settings.
- [ ] Clear-history action removes stored transcript text.
- [ ] History entries include provider and timing metadata.

## Review Plan

- [ ] Codex reviews privacy and storage behavior.
- [ ] Claude reviews history UI affordances.

## CI Expectations

- [ ] History retention logic has unit coverage.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-009-implement-persistent-transcript-history` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
