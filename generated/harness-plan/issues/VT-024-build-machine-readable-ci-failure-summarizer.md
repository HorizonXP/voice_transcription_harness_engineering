# Build machine-readable CI failure summarizer

> Harness ID: `VT-024`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

Create the CI summary artifact generator that agents read before full logs.

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | M4 Polish And Release Readiness |
| Phase | `phase:4` |
| Parallel Group | `ci-foundation` |
| Recommended Agent | `agent:codex` |
| Recommended Model | GPT-5.5 via local Codex CLI, medium reasoning; escalate to high for architecture/security/API uncertainty |
| Reasoning Effort | `medium` |
| Agent Command | `codex` |
| Dependencies | `VT-014` |
| Labels | `type:testing`, `area:ci`, `agent:codex`, `phase:4`, `priority:p0`, `ci:required`, `review:cross-agent` |

## Dependency View

```mermaid
flowchart LR
    VT_024[VT-024]
    VT_014[VT-014] --> VT_024
```

## Scope

- [ ] Emit artifacts/ci-summary.json for failed checks.
- [ ] Include failed check name, summary, likely files, suggested owner, and next command.
- [ ] Keep summaries concise and deterministic.

## Prescribed Implementation Plan

- [ ] Read docs/requirements.md and relevant ADRs before editing.
- [ ] Inspect existing code and tests before choosing an implementation shape.
- [ ] Implement: Emit artifacts/ci-summary.json for failed checks.
- [ ] Implement: Include failed check name, summary, likely files, suggested owner, and next command.
- [ ] Implement: Keep summaries concise and deterministic.
- [ ] Verify: CI uploads ci-summary.json on every run.
- [ ] Verify: Agent repair loop docs point to the artifact first.
- [ ] Verify: A simulated failure can produce a useful summary without noisy logs.
- [ ] Run the issue-specific test command and record the result in the PR.
- [ ] Open a focused PR that closes only this issue unless the issue explicitly says otherwise.

## Expected Files Or Areas

- `.github/workflows/**`
- `scripts/**`
- `docs/harness/ci-strategy.md`

## Acceptance Criteria

- [ ] CI uploads ci-summary.json on every run.
- [ ] Agent repair loop docs point to the artifact first.
- [ ] A simulated failure can produce a useful summary without noisy logs.

## Constraints

- Do not make unrelated refactors.
- Do not introduce paid model API calls for orchestration.
- Preserve user changes and generated harness IDs.
- If a decision is low-risk and reversible, use judgment and document it.
- CI logs must stay segmented and concise; add machine-readable summaries for failures.

<details>
<summary>Failure modes and escalation rules</summary>

- Acceptance criteria are ambiguous after reading the requirements.
- Required local or Windows-side tool is missing.
- Implementation requires a product/security/architecture decision not already recorded.
- CI produces noisy logs or lacks a machine-readable failure artifact.

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

- [ ] Codex reviews failure parsing and artifact shape.
- [ ] Claude reviews human readability of summaries.

## CI Expectations

- [ ] Harness CI validates the summary shape.

## Notes

- None

## Agent Handoff

When assigned, create a branch named `work/vt-024-build-machine-readable-ci-failure-summarizer` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on VT-024: Build machine-readable CI failure summarizer.

Recommended model/effort: GPT-5.5 via local Codex CLI, medium reasoning; escalate to high for architecture/security/API uncertainty / medium.
Primary objective: Create the CI summary artifact generator that agents read before full logs.

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
