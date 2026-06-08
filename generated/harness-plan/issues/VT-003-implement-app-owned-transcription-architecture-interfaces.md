# Implement app-owned transcription architecture interfaces

> Harness ID: `VT-003`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Create provider, recorder, insertion, history, and settings contracts that reflect ADR 0001.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M1 Native Windows App Foundation |
| Phase | `phase:1` |
| Parallel Group | `foundation` |
| Recommended Agent | `agent:codex` |
| Recommended Model | GPT-5.5 via local Codex CLI, medium reasoning; escalate to high for architecture/security/API uncertainty |
| Reasoning Effort | `medium` |
| Agent Command | `codex` |
| Dependencies | `VT-001` |
| Labels | `type:foundation`, `area:provider`, `agent:codex`, `phase:1`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_003[VT-003]
    VT_001[VT-001] --> VT_003
```

## Scope

- [ ] Define provider abstraction interfaces.
- [ ] Define insertion adapter boundary.
- [ ] Define transcript history data contract.
- [ ] Define secure credential storage boundary.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Define provider abstraction interfaces.
- [ ] Implement: Define insertion adapter boundary.
- [ ] Implement: Define transcript history data contract.
- [ ] Implement: Define secure credential storage boundary.
- [ ] Verify: OpenAI, Mistral AI, and future local providers fit the same provider contract.
- [ ] Verify: Insertion can be replaced later without rewriting providers or recorder logic.
- [ ] Verify: Contracts are covered by unit tests or compile-time checks once app code exists.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `src/** provider files`
- `tests/** provider tests`
- `docs/** provider notes when needed`

## Acceptance Criteria

- [ ] OpenAI, Mistral AI, and future local providers fit the same provider contract.
- [ ] Insertion can be replaced later without rewriting providers or recorder logic.
- [ ] Contracts are covered by unit tests or compile-time checks once app code exists.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
- Do not bind UI workflow directly to one provider API shape.
- Do not log credentials, raw audio, or full transcripts by default.

<details>
<summary>Failure modes and escalation rules</summary>

- Acceptance criteria are ambiguous after reading the requirements.
- Required local or Windows-side tool is missing.
- Implementation requires a product/security/architecture decision not already recorded.
- Provider docs or model names conflict with the recorded requirements; verify official docs before coding.

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

- [ ] Codex reviews architecture boundaries.
- [ ] Claude reviews whether UI-facing contracts support design needs.

## CI Expectations

- [ ] Unit test strategy for contracts is documented or implemented.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-003-implement-app-owned-transcription-architecture-interfaces` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-003: Implement app-owned transcription architecture interfaces.

Recommended model/effort: GPT-5.5 via local Codex CLI, medium reasoning; escalate to high for architecture/security/API uncertainty / medium.
Primary objective: Create provider, recorder, insertion, history, and settings contracts that reflect ADR 0001.

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
