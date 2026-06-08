# Add native app CI and test harness

> Harness ID: `VT-014`

## Outcome

Create fast Windows app CI with agent-readable failure summaries.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M4 Polish And Release Readiness |
| Phase | `phase:4` |
| Parallel Group | `release` |
| Recommended Agent | `agent:codex` |
| Dependencies | VT-001 |
| Labels | `type:testing`, `area:ci`, `agent:codex`, `phase:4`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Define unit, integration, UI smoke, and packaging validation layers.
- [ ] Keep CI economical and segmented.
- [ ] Emit concise machine-readable failure summaries.

## Acceptance Criteria

- [ ] CI runs harness validation and app tests appropriate to the current scaffold.
- [ ] Failure artifact points to failing check, files, and likely owner.
- [ ] Logs are segmented and not unnecessarily noisy.

## Review Plan

- [ ] Codex reviews CI correctness.
- [ ] Claude reviews human readability of CI output.

## CI Expectations

- [ ] GitHub Actions workflow passes on the repository.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-014-add-native-app-ci-and-test-harness` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
