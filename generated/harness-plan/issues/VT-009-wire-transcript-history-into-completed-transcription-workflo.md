# Wire transcript history into completed transcription workflow

> Harness ID: `VT-009`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Ensure completed and fallback transcripts are written to history through the storage engine.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `history` |
| Recommended Agent | `agent:codex` |
| Recommended Model | GPT-5.5 via local Codex CLI, low-to-medium reasoning |
| Reasoning Effort | `low` |
| Agent Command | `codex` |
| Dependencies | `VT-003`, `VT-008`, `VT-022` |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_009[VT-009]
    VT_003[VT-003] --> VT_009
    VT_008[VT-008] --> VT_009
    VT_022[VT-022] --> VT_009
```

## Scope

- [ ] Write successful active-insertion transcripts to history.
- [ ] Write clipboard-fallback transcripts to history.
- [ ] Include provider, duration, timestamp, and delivery outcome metadata.
- [ ] Do not duplicate entries on retry or UI refresh.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Write successful active-insertion transcripts to history.
- [ ] Implement: Write clipboard-fallback transcripts to history.
- [ ] Implement: Include provider, duration, timestamp, and delivery outcome metadata.
- [ ] Implement: Do not duplicate entries on retry or UI refresh.
- [ ] Verify: Every completed transcript path records exactly one history entry.
- [ ] Verify: Fallback path preserves transcript text even when insertion fails.
- [ ] Verify: History writes use the VT-022 storage engine instead of ad hoc persistence.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/**`
- `tests/**`
- `docs/** when implementation choices need explanation`

## Acceptance Criteria

- [ ] Every completed transcript path records exactly one history entry.
- [ ] Fallback path preserves transcript text even when insertion fails.
- [ ] History writes use the VT-022 storage engine instead of ad hoc persistence.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
- Keep the implementation native Windows 11; do not introduce Electron or a browser-wrapper shell.

<details>
<summary>Failure modes and escalation rules</summary>

- Acceptance criteria are ambiguous after reading the requirements.
- Required local or Windows-side tool is missing.
- Implementation requires a product/security/architecture decision not already recorded.

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

- [ ] Codex reviews workflow and persistence integration.
- [ ] Claude reviews user-visible fallback/history behavior.

## CI Expectations

- [ ] Workflow tests cover active insertion and clipboard fallback history writes.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-009-wire-transcript-history-into-completed-transcription-workflo` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-009: Wire transcript history into completed transcription workflow.

Recommended model/effort: GPT-5.5 via local Codex CLI, low-to-medium reasoning / low.
Primary objective: Ensure completed and fallback transcripts are written to history through the storage engine.

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
