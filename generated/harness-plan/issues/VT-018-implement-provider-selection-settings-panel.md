# Implement provider selection settings panel

> Harness ID: `VT-018`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Implement the settings panel that shows saved provider credentials and exactly one active provider.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M3 Provider Integrations |
| Phase | `phase:3` |
| Parallel Group | `provider-settings` |
| Recommended Agent | `agent:claude` |
| Recommended Model | Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs |
| Reasoning Effort | `medium` |
| Agent Command | `claude` |
| Dependencies | `VT-004`, `VT-010`, `VT-011`, `VT-012` |
| Labels | `type:implementation`, `area:ui`, `area:provider`, `agent:claude`, `phase:3`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_018[VT-018]
    VT_004[VT-004] --> VT_018
    VT_010[VT-010] --> VT_018
    VT_011[VT-011] --> VT_018
    VT_012[VT-012] --> VT_018
```

## Scope

- [ ] Show OpenAI and Mistral AI provider rows/cards without nesting cards inside cards.
- [ ] Make saved credential state distinct from active provider state.
- [ ] Allow changing the single active provider.
- [ ] Show clear validation/error state when selected provider lacks credentials.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Show OpenAI and Mistral AI provider rows/cards without nesting cards inside cards.
- [ ] Implement: Make saved credential state distinct from active provider state.
- [ ] Implement: Allow changing the single active provider.
- [ ] Implement: Show clear validation/error state when selected provider lacks credentials.
- [ ] Verify: Exactly one provider can be active at a time.
- [ ] Verify: Saved API keys for inactive providers do not switch the active provider automatically.
- [ ] Verify: User can tell what will be used for the next transcription.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** UI files`
- `docs/**/*.md for UI verification notes`
- `tests/** UI smoke artifacts when available`

## Acceptance Criteria

- [ ] Exactly one provider can be active at a time.
- [ ] Saved API keys for inactive providers do not switch the active provider automatically.
- [ ] User can tell what will be used for the next transcription.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
- Do not bind UI workflow directly to one provider API shape.
- Do not log credentials, raw audio, or full transcripts by default.
- Follow native Windows 11/Fluent patterns; avoid marketing-page composition.
- Text and controls must fit at common Windows desktop scaling settings.

<details>
<summary>Failure modes and escalation rules</summary>

- Acceptance criteria are ambiguous after reading the requirements.
- Required local or Windows-side tool is missing.
- Implementation requires a product/security/architecture decision not already recorded.
- Provider docs or model names conflict with the recorded requirements; verify official docs before coding.
- Visual behavior cannot be verified without a running Windows UI; attach a manual verification checklist.

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

- [ ] Claude reviews UX clarity.
- [ ] Codex reviews state wiring and provider contract fit.

## CI Expectations

- [ ] UI/state tests or manual smoke checklist cover provider switching.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-018-implement-provider-selection-settings-panel` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-018: Implement provider selection settings panel.

Recommended model/effort: Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs / medium.
Primary objective: Implement the settings panel that shows saved provider credentials and exactly one active provider.

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
