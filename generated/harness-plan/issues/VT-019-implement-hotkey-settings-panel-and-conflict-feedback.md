# Implement hotkey settings panel and conflict feedback

> Harness ID: `VT-019`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Create the settings UI for recording the global hotkey and displaying conflict feedback.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `hotkey-settings` |
| Recommended Agent | `agent:claude` |
| Recommended Model | Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs |
| Reasoning Effort | `medium` |
| Agent Command | `claude` |
| Dependencies | `VT-004`, `VT-005` |
| Labels | `type:implementation`, `area:ui`, `area:windows-app`, `agent:claude`, `phase:2`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_019[VT-019]
    VT_004[VT-004] --> VT_019
    VT_005[VT-005] --> VT_019
```

## Scope

- [ ] Default visible hotkey is Ctrl+Win+H.
- [ ] Hotkey capture UI handles press/release clearly.
- [ ] Conflict errors prevent saving and explain the problem.
- [ ] User can cancel without changing the current hotkey.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Default visible hotkey is Ctrl+Win+H.
- [ ] Implement: Hotkey capture UI handles press/release clearly.
- [ ] Implement: Conflict errors prevent saving and explain the problem.
- [ ] Implement: User can cancel without changing the current hotkey.
- [ ] Verify: Conflict state is visible and actionable.
- [ ] Verify: The UI does not accept a detected conflicting hotkey.
- [ ] Verify: The hotkey capture interaction is keyboard-accessible.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** UI files`
- `docs/**/*.md for UI verification notes`
- `tests/** UI smoke artifacts when available`

## Acceptance Criteria

- [ ] Conflict state is visible and actionable.
- [ ] The UI does not accept a detected conflicting hotkey.
- [ ] The hotkey capture interaction is keyboard-accessible.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
- Keep the implementation native Windows 11; do not introduce Electron or a browser-wrapper shell.
- Follow native Windows 11/Fluent patterns; avoid marketing-page composition.
- Text and controls must fit at common Windows desktop scaling settings.

<details>
<summary>Failure modes and escalation rules</summary>

- Acceptance criteria are ambiguous after reading the requirements.
- Required local or Windows-side tool is missing.
- Implementation requires a product/security/architecture decision not already recorded.
- Visual behavior cannot be verified without a running Windows UI; attach a manual verification checklist.

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

- [ ] Claude reviews interaction design.
- [ ] Codex reviews integration with hotkey validation service.

## CI Expectations

- [ ] UI/state tests or manual smoke checklist cover valid, invalid, and cancel paths.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-019-implement-hotkey-settings-panel-and-conflict-feedback` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-019: Implement hotkey settings panel and conflict feedback.

Recommended model/effort: Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs / medium.
Primary objective: Create the settings UI for recording the global hotkey and displaying conflict feedback.

Read:
- docs/requirements.md
- docs/decisions/0001-app-owned-transcription-integration.md
- This issue body

Do only this issue's scope. Make the smallest coherent change. Run the listed CI/test expectations.
Open a PR that closes this issue and include test output plus Greptile/cross-agent review status.
```

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
