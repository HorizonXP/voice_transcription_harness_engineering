# Implement transcript history storage and retention engine

> Harness ID: `VT-022`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Implement full-text transcript history storage with 30-day retention and manual clearing, independent of UI polish.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M2 Recording And Insertion Workflow |
| Phase | `phase:2` |
| Parallel Group | `history-engine` |
| Recommended Agent | `agent:codex` |
| Recommended Model | GPT-5.5 via local Codex CLI, low-to-medium reasoning |
| Reasoning Effort | `low` |
| Agent Command | `codex` |
| Dependencies | `VT-003` |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:2`, `priority:p1`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_022[VT-022]
    VT_003[VT-003] --> VT_022
```

## Scope

- [ ] Persist full transcript text and metadata.
- [ ] Apply default 30-day retention.
- [ ] Expose clear-history operation.
- [ ] Keep raw audio out of history by default.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Persist full transcript text and metadata.
- [ ] Implement: Apply default 30-day retention.
- [ ] Implement: Expose clear-history operation.
- [ ] Implement: Keep raw audio out of history by default.
- [ ] Verify: Retention engine can delete expired history entries.
- [ ] Verify: Manual clearing removes full transcript text.
- [ ] Verify: History writes do not log full transcript text by default.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/**`
- `tests/**`
- `docs/** when implementation choices need explanation`

## Acceptance Criteria

- [ ] Retention engine can delete expired history entries.
- [ ] Manual clearing removes full transcript text.
- [ ] History writes do not log full transcript text by default.

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

- [ ] Codex reviews privacy and persistence behavior.
- [ ] Claude reviews history state needed by UI.

## CI Expectations

- [ ] Unit tests cover save, query, retention cleanup, and clear-history behavior.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-022-implement-transcript-history-storage-and-retention-engine` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-022: Implement transcript history storage and retention engine.

Recommended model/effort: GPT-5.5 via local Codex CLI, low-to-medium reasoning / low.
Primary objective: Implement full-text transcript history storage with 30-day retention and manual clearing, independent of UI polish.

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
