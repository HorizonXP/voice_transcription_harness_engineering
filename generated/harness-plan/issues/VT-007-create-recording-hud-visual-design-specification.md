# Create recording HUD visual design specification

> Harness ID: `VT-007`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Create the visual and interaction specification for the compact Windows 11 HUD before implementation.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `recording-parallel` |
| Recommended Agent | `agent:claude` |
| Recommended Model | Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs |
| Reasoning Effort | `medium` |
| Agent Command | `claude` |
| Dependencies | `VT-001`, `VT-003` |
| Labels | `type:implementation`, `area:ui`, `agent:claude`, `phase:2`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_007[VT-007]
    VT_001[VT-001] --> VT_007
    VT_003[VT-003] --> VT_007
```

## Scope

- [ ] Specify HUD layout, placement, sizing, visual hierarchy, and state variants.
- [ ] Specify how audio activity and transcription progress appear without layout shift.
- [ ] Specify focus and dismissal behavior without implementing the state machine.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Specify HUD layout, placement, sizing, visual hierarchy, and state variants.
- [ ] Implement: Specify how audio activity and transcription progress appear without layout shift.
- [ ] Implement: Specify focus and dismissal behavior without implementing the state machine.
- [ ] Verify: Design spec covers recording, transcribing, fallback, error, and completed states.
- [ ] Verify: Spec follows native Windows 11 visual guidance.
- [ ] Verify: Spec is detailed enough for VT-021 to implement without re-designing the HUD.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** UI files`
- `docs/**/*.md for UI verification notes`
- `tests/** UI smoke artifacts when available`

## Acceptance Criteria

- [ ] Design spec covers recording, transcribing, fallback, error, and completed states.
- [ ] Spec follows native Windows 11 visual guidance.
- [ ] Spec is detailed enough for VT-021 to implement without re-designing the HUD.

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

- [ ] Claude reviews visual and interaction quality.
- [ ] Codex reviews state-machine integration.

## CI Expectations

- [ ] UI smoke test or manual verification checklist exists.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-007-create-recording-hud-visual-design-specification` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-007: Create recording HUD visual design specification.

Recommended model/effort: Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs / medium.
Primary objective: Create the visual and interaction specification for the compact Windows 11 HUD before implementation.

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
