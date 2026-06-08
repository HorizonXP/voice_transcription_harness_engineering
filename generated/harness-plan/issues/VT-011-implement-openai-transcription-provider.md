# Implement OpenAI transcription provider

> Harness ID: `VT-011`

## Outcome

Integrate OpenAI transcription through the provider abstraction.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M3 Provider Integrations |
| Phase | `phase:3` |
| Parallel Group | `providers-parallel` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-003, VT-006, VT-010 |
| Labels | `type:implementation`, `area:provider`, `agent:codex`, `phase:3`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Use the latest best OpenAI transcription direction from official docs.
- [ ] Support configured API key retrieval.
- [ ] Normalize provider errors.
- [ ] Support cancellation where possible.

## Acceptance Criteria

- [ ] OpenAI provider implements the common provider contract.
- [ ] Provider can be selected as the active provider.
- [ ] Network and credential failures are user-visible and not logged with secrets.

## Review Plan

- [ ] Codex reviews API integration and error normalization.
- [ ] Claude reviews user-facing provider error messages.

## CI Expectations

- [ ] Provider contract tests or mocked integration tests exist.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-011-implement-openai-transcription-provider` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
