# Create first-run diagnostics and logging policy

> Harness ID: `VT-027`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Define and implement diagnostics that help fix failures without logging sensitive content.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M4 Polish And Release Readiness |
| Phase | `phase:4` |
| Parallel Group | `diagnostics` |
| Recommended Agent | `agent:codex` |
| Recommended Model | GPT-5.5 via local Codex CLI, low-to-medium reasoning |
| Reasoning Effort | `low` |
| Agent Command | `codex` |
| Dependencies | `VT-003`, `VT-010`, `VT-014` |
| Labels | `type:implementation`, `area:windows-app`, `agent:codex`, `phase:4`, `priority:p2`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_027[VT-027]
    VT_003[VT-003] --> VT_027
    VT_010[VT-010] --> VT_027
    VT_014[VT-014] --> VT_027
```

## Scope

- [ ] Log provider name, operation state, duration, and normalized error codes.
- [ ] Do not log credentials, raw audio, or full transcripts by default.
- [ ] Expose enough diagnostics for CI and user support.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Log provider name, operation state, duration, and normalized error codes.
- [ ] Implement: Do not log credentials, raw audio, or full transcripts by default.
- [ ] Implement: Expose enough diagnostics for CI and user support.
- [ ] Verify: Diagnostics help identify microphone, credential, network, provider, insertion, and history failures.
- [ ] Verify: Sensitive content is excluded by default.
- [ ] Verify: Logs are structured enough for agent consumption.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/**`
- `tests/**`
- `docs/** when implementation choices need explanation`

## Acceptance Criteria

- [ ] Diagnostics help identify microphone, credential, network, provider, insertion, and history failures.
- [ ] Sensitive content is excluded by default.
- [ ] Logs are structured enough for agent consumption.

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

- [ ] Codex reviews security and observability.
- [ ] Claude reviews user-facing diagnostics copy.

## CI Expectations

- [ ] Tests or manual checks verify sensitive values are not logged.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-027-create-first-run-diagnostics-and-logging-policy` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-027: Create first-run diagnostics and logging policy.

Recommended model/effort: GPT-5.5 via local Codex CLI, low-to-medium reasoning / low.
Primary objective: Define and implement diagnostics that help fix failures without logging sensitive content.

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
