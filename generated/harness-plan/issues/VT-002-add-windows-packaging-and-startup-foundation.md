# Add Windows packaging and startup foundation

> Harness ID: `VT-002`

## Outcome

Establish MSIX-first packaging and startup integration direction.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-001 |
| Labels | `type:foundation`, `area:windows-app`, `agent:codex`, `phase:1`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Add packaging project or documented packaging scaffold.
- [ ] Define startup toggle integration for the selected packaging model.
- [ ] Document signing and local developer constraints.

## Acceptance Criteria

- [ ] Packaging is included from the start or a documented Windows App SDK blocker is recorded.
- [ ] Startup toggle path is documented and testable.
- [ ] CI strategy includes packaging validation expectations.

## Review Plan

- [ ] Codex reviews Windows packaging correctness.
- [ ] Claude reviews settings/startup UX clarity.

## CI Expectations

- [ ] Packaging-related scripts or docs pass harness validation.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-002-add-windows-packaging-and-startup-foundation` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
