# Polish settings, HUD, and transcript history UX

> Harness ID: `VT-015`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Refine the native Windows 11 user experience across settings, HUD, and history.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M4 Polish And Release Readiness |
| Phase | `phase:4` |
| Parallel Group | `release` |
| Recommended Agent | `agent:claude` |
| Recommended Model | Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs |
| Reasoning Effort | `medium` |
| Agent Command | `claude` |
| Dependencies | `VT-018`, `VT-019`, `VT-021`, `VT-023`, `VT-011`, `VT-012` |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:4`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_015[VT-015]
    VT_018[VT-018] --> VT_015
    VT_019[VT-019] --> VT_015
    VT_021[VT-021] --> VT_015
    VT_023[VT-023] --> VT_015
    VT_011[VT-011] --> VT_015
    VT_012[VT-012] --> VT_015
```

## Scope

- [ ] Ensure controls are compact, clear, and native-feeling.
- [ ] Verify provider selection and credential states are understandable.
- [ ] Verify history deletion and retention controls are easy to find.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Ensure controls are compact, clear, and native-feeling.
- [ ] Implement: Verify provider selection and credential states are understandable.
- [ ] Implement: Verify history deletion and retention controls are easy to find.
- [ ] Verify: UI fits without overlap at common desktop scaling settings.
- [ ] Verify: User-facing copy is concise and actionable.
- [ ] Verify: Claude and Codex reviews agree the UI is ready for release candidate testing.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** UI files`
- `docs/**/*.md for UI verification notes`
- `tests/** UI smoke artifacts when available`

## Acceptance Criteria

- [ ] UI fits without overlap at common desktop scaling settings.
- [ ] User-facing copy is concise and actionable.
- [ ] Claude and Codex reviews agree the UI is ready for release candidate testing.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
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

- [ ] Claude primary design review.
- [ ] Codex reviews implementation integration and accessibility risks.

## CI Expectations

- [ ] UI smoke artifacts or screenshots are attached where possible.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-015-polish-settings-hud-and-transcript-history-ux` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-015: Polish settings, HUD, and transcript history UX.

Recommended model/effort: Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs / medium.
Primary objective: Refine the native Windows 11 user experience across settings, HUD, and history.

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
