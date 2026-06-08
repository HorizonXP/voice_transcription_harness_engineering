# Generated Harness Plan

Source: `docs/requirements.md`

This is a dry-run plan. It has not created GitHub issues or projects.

## Issues By Phase

### phase:1

| ID | Title | Agent | Dependencies | Parallel Group |
| --- | --- | --- | --- | --- |
| VT-001 | Select native Windows app stack and repository structure | `codex` | None | `foundation` |
| VT-002 | Add Windows packaging and startup foundation | `codex` | VT-001 | `foundation` |
| VT-003 | Implement app-owned transcription architecture interfaces | `codex` | VT-001 | `foundation` |
| VT-004 | Design settings UI for provider, hotkey, startup, and history controls | `claude` | VT-001, VT-003 | `foundation-parallel` |
| VT-013 | Implement system tray controls and idle behavior | `codex` | VT-001 | `foundation-parallel` |

### phase:2

| ID | Title | Agent | Dependencies | Parallel Group |
| --- | --- | --- | --- | --- |
| VT-005 | Implement global push-to-talk hotkey handling | `codex` | VT-001, VT-003 | `recording` |
| VT-006 | Implement microphone recording lifecycle | `codex` | VT-003, VT-005 | `recording` |
| VT-007 | Design and implement recording HUD | `claude` | VT-001, VT-003 | `recording-parallel` |
| VT-008 | Implement transcript insertion and clipboard fallback | `codex` | VT-003, VT-006 | `insertion` |
| VT-009 | Implement persistent transcript history | `codex` | VT-003, VT-008 | `history` |

### phase:3

| ID | Title | Agent | Dependencies | Parallel Group |
| --- | --- | --- | --- | --- |
| VT-010 | Implement secure credential storage | `codex` | VT-003, VT-004 | `providers` |
| VT-011 | Implement OpenAI transcription provider | `codex` | VT-003, VT-006, VT-010 | `providers-parallel` |
| VT-012 | Implement Mistral AI transcription provider | `codex` | VT-003, VT-006, VT-010 | `providers-parallel` |

### phase:4

| ID | Title | Agent | Dependencies | Parallel Group |
| --- | --- | --- | --- | --- |
| VT-014 | Add native app CI and test harness | `codex` | VT-001 | `release` |
| VT-015 | Polish settings, HUD, and transcript history UX | `claude` | VT-004, VT-007, VT-009, VT-011, VT-012 | `release` |

## Apply

Review `plan.json` and issue markdown first. To apply later:

```sh
python3 scripts/github_apply_plan.py --plan generated/harness-plan/plan.json --apply
```
