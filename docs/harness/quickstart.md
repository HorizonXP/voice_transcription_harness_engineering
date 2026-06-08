# Harness Quickstart

## Current GitHub State

As of the last local check:

- Repository: `HorizonXP/voice_transcription_harness_engineering`
- Visibility: public
- Default branch: `main`
- Branch protection: not enabled
- GitHub Projects: none found

Before using the harness for real implementation work, protect `main` and use pull requests.

## Recommended GitHub Setup

### 1. Protect `main`

Recommended branch protection policy:

- Require pull request before merging.
- Require at least one approval.
- Require conversation resolution before merge.
- Require status checks to pass.
- Require `Harness CI / Validate harness artifacts`.
- Do not allow force pushes.
- Do not allow deletions.
- Keep admin bypass available during the live demo only if needed.

GitHub UI path:

```text
Settings -> Branches -> Add branch protection rule -> Branch name pattern: main
```

The repository currently has `Harness CI`, but the exact required check name only appears after GitHub Actions has run at least once on a PR or push.

### 2. Enable Greptile

Install or enable Greptile for the repository before relying on the automated review loop.

The harness expects Greptile to review every pull request. The orchestrator should wait for Greptile findings before moving a PR to ready-to-merge.

### 3. Create a GitHub Project

Create a project for the generated plan. Suggested title:

```text
Voice Transcription Harness Execution
```

Use the project design in [GitHub Project Blueprint](github-project-blueprint.md).

The current apply script creates labels, milestones, and issues. GitHub Project field automation is documented as part of the harness but should be added after the issue apply path is validated.

## Generate The Dry-Run Plan

From the repository root:

```sh
python3 scripts/harness_plan.py generate --requirements docs/requirements.md --output generated/harness-plan
python3 scripts/harness_plan.py validate --plan generated/harness-plan/plan.json
```

Review:

- `generated/harness-plan/README.md`
- `generated/harness-plan/plan.json`
- `generated/harness-plan/issues/*.md`

The checked-in plan is a deterministic sample. The intended production planning loop is:

1. Codex GPT-5.5 extra-high produces the draft decomposition.
2. Claude Code Opus 4.8 extra-high critiques the plan.
3. Codex GPT-5.5 extra-high reconciles the critique.
4. The harness validates, renders, and applies the final plan only after approval.

## Start tmux Sessions

Check local tool availability:

```sh
python3 scripts/tmux_orchestrator.py status
```

Start planner and worker sessions:

```sh
python3 scripts/tmux_orchestrator.py start
```

Attach to a planner session:

```sh
tmux attach -t planner-codex-extra-high
tmux attach -t planner-claude-opus-critic
```

Attach to worker sessions:

```sh
tmux attach -t worker-codex-01
tmux attach -t worker-claude-01
```

## Apply The Plan To GitHub

Always dry-run first:

```sh
python3 scripts/github_apply_plan.py \
  --plan generated/harness-plan/plan.json \
  --output-dir generated/harness-plan
```

Apply only after reviewing the printed operations:

```sh
python3 scripts/github_apply_plan.py \
  --plan generated/harness-plan/plan.json \
  --output-dir generated/harness-plan \
  --apply
```

The apply script is intended to create or update:

- Labels
- Milestones
- Issues

Project automation should be layered in after the issue workflow is proven.

## PR Workflow From Now On

Use pull requests for repository changes.

Recommended branch naming:

```text
work/<harness-id>-short-title
docs/<short-title>
harness/<short-title>
```

Minimum PR requirements:

- Linked issue or clear harness task.
- Passing Harness CI.
- Greptile review handled.
- Cross-agent review handled when applicable.
- No unresolved review threads.

## First Real Run

Recommended first real sequence:

1. Enable branch protection for `main`.
2. Enable Greptile.
3. Open and merge this quickstart PR.
4. Run Harness CI once so the required check name is available.
5. Create the GitHub Project.
6. Run the production planning loop with Codex planner and Claude critic.
7. Review the reconciled generated plan.
8. Apply labels, milestones, and issues.
9. Assign the first ready issue through tmux.
