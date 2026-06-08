# Implement app-owned transcription architecture interfaces

> Harness ID: `VT-003`

## Outcome

Create provider, recorder, insertion, history, and settings contracts that reflect ADR 0001.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-001 |
| Labels | `type:foundation`, `area:provider`, `agent:codex`, `phase:1`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Define provider abstraction interfaces.
- [ ] Define insertion adapter boundary.
- [ ] Define transcript history data contract.
- [ ] Define secure credential storage boundary.

## Acceptance Criteria

- [ ] OpenAI, Mistral AI, and future local providers fit the same provider contract.
- [ ] Insertion can be replaced later without rewriting providers or recorder logic.
- [ ] Contracts are covered by unit tests or compile-time checks once app code exists.

## Review Plan

- [ ] Codex reviews architecture boundaries.
- [ ] Claude reviews whether UI-facing contracts support design needs.

## CI Expectations

- [ ] Unit test strategy for contracts is documented or implemented.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-003-implement-app-owned-transcription-architecture-interfaces` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
