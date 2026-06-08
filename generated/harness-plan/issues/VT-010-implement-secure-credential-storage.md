# Implement secure credential storage

> Harness ID: `VT-010`

## Outcome

Store provider API keys using Windows-native secure credential storage.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M3 Provider Integrations |
| Phase | `phase:3` |
| Parallel Group | `providers` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-003, VT-004 |
| Labels | `type:implementation`, `area:provider`, `agent:codex`, `phase:3`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] API keys are entered through settings.
- [ ] Keys are not stored in plain-text app configuration.
- [ ] Credential failures are surfaced clearly.

## Acceptance Criteria

- [ ] Credential storage uses Windows Credential Manager or equivalent Windows-native secure storage.
- [ ] Provider adapters can retrieve keys without exposing them in logs.
- [ ] Deleting a provider credential is supported.

## Review Plan

- [ ] Codex reviews security boundary.
- [ ] Claude reviews settings clarity around saved credentials.

## CI Expectations

- [ ] Credential storage behavior has tests or documented manual verification.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-010-implement-secure-credential-storage` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
