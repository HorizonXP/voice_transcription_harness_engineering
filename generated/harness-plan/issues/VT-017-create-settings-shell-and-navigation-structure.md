# Create settings shell and navigation structure

> Harness ID: `VT-017`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Create the Windows 11 settings shell structure before wiring provider-specific settings.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `settings-ui` |
| Recommended Agent | `agent:claude` |
| Recommended Model | Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs |
| Reasoning Effort | `medium` |
| Agent Command | `claude` |
| Dependencies | `VT-001` |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:1`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_017[VT-017]
    VT_001[VT-001] --> VT_017
```

## Scope

- [ ] Define settings navigation sections.
- [ ] Create shell layout for General, Providers, Hotkey, History, and About/Diagnostics.
- [ ] Use native Windows 11 spacing, typography, and control hierarchy.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Define settings navigation sections.
- [ ] Implement: Create shell layout for General, Providers, Hotkey, History, and About/Diagnostics.
- [ ] Implement: Use native Windows 11 spacing, typography, and control hierarchy.
- [ ] Verify: Settings shell can host later provider, hotkey, startup, and history panels.
- [ ] Verify: Navigation is understandable without explanatory feature-marketing text.
- [ ] Verify: Design is compact and operational, not a landing page.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** settings UI files`
- `docs/** UI notes or screenshots`

## Acceptance Criteria

- [ ] Settings shell can host later provider, hotkey, startup, and history panels.
- [ ] Navigation is understandable without explanatory feature-marketing text.
- [ ] Design is compact and operational, not a landing page.

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

- [ ] Claude reviews visual structure.
- [ ] Codex reviews whether the shell can be wired to settings state.

## CI Expectations

- [ ] UI smoke checklist or screenshots are attached once UI exists.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-017-create-settings-shell-and-navigation-structure` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-017: Create settings shell and navigation structure.

Recommended model/effort: Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs / medium.
Primary objective: Create the Windows 11 settings shell structure before wiring provider-specific settings.

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
