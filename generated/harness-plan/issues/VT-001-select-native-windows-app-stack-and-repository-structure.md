# Select native Windows app stack and repository structure

> Harness ID: `VT-001`

## Outcome

Document and scaffold the chosen Windows App SDK/WinUI 3 solution structure without implementing app features.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation` |
| Recommended Agent | `agent:codex` |
| Dependencies | None |
| Labels | `type:foundation`, `area:windows-app`, `agent:codex`, `phase:1`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Create the initial native Windows solution/project structure.
- [ ] Document Windows-side prerequisites required from WSL2.
- [ ] Keep the app target Windows 11 only.

## Acceptance Criteria

- [ ] Repository contains a native Windows app skeleton plan or scaffold aligned with Windows App SDK and WinUI 3.
- [ ] Build prerequisites are documented for Windows 11.
- [ ] No Electron or browser-wrapper app shell is introduced.

## Review Plan

- [ ] Codex implementation review for architecture and build viability.
- [ ] Claude review for native app UX implications.

## CI Expectations

- [ ] Harness validation passes.
- [ ] Future Windows build command is documented even if not yet runnable from WSL2.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-001-select-native-windows-app-stack-and-repository-structure` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
