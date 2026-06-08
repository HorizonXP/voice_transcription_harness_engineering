# Design settings UI for provider, hotkey, startup, and history controls

> Harness ID: `VT-004`

## Outcome

Create a native Windows 11 settings experience design for provider selection and core preferences.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation-parallel` |
| Recommended Agent | `agent:claude` |
| Dependencies | VT-001, VT-003 |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:1`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Scope

- [ ] Provider selection with exactly one active provider.
- [ ] API key entry affordance per provider.
- [ ] Global hotkey configuration and conflict feedback.
- [ ] Startup toggle.
- [ ] Transcript retention and clear-history controls.

## Acceptance Criteria

- [ ] Settings surface follows Windows 11 design guidance.
- [ ] Provider credentials and active provider state are visually distinct.
- [ ] History retention defaults to 30 days and supports manual clearing.

## Review Plan

- [ ] Claude primary design review.
- [ ] Codex reviews implementation feasibility and settings/state boundaries.

## CI Expectations

- [ ] UI snapshot or design artifact is attached once the app UI exists.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-004-design-settings-ui-for-provider-hotkey-startup-and-history-c` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
