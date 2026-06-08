#!/usr/bin/env python3
"""Generate and validate a dry-run GitHub execution plan.

The generator is intentionally deterministic. It reads a requirements document,
emits a structured plan, validates cross references, and renders GitHub-flavored
issue markdown without mutating GitHub.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUIREMENTS = ROOT / "docs" / "requirements.md"
DEFAULT_OUTPUT = ROOT / "generated" / "harness-plan"


LABELS = [
    ("type:foundation", "5319E7", "Foundational work that unlocks later issues."),
    ("type:implementation", "0E8A16", "Product or harness implementation work."),
    ("type:research", "FBCA04", "Research or decision-support work."),
    ("type:testing", "1D76DB", "Testing or validation work."),
    ("type:documentation", "6F42C1", "Documentation work."),
    ("area:windows-app", "0078D4", "Native Windows application area."),
    ("area:provider", "0B7285", "Transcription provider architecture or implementation."),
    ("area:ui", "D93F0B", "User interface and user experience work."),
    ("area:ci", "24292F", "CI, test, or automation work."),
    ("area:harness", "8250DF", "Harness orchestration system work."),
    ("agent:codex", "0969DA", "Recommended for Codex."),
    ("agent:claude", "A855F7", "Recommended for Claude Code."),
    ("agent:either", "BFDADC", "Suitable for either agent."),
    ("phase:0", "D4C5F9", "Harness and repository setup phase."),
    ("phase:1", "BFD4F2", "Application foundation phase."),
    ("phase:2", "ACE5B1", "Core transcription workflow phase."),
    ("phase:3", "FAD8C7", "Provider and settings phase."),
    ("phase:4", "F2CC60", "Polish, packaging, and release-readiness phase."),
    ("priority:p0", "B60205", "Critical path."),
    ("priority:p1", "D1242F", "High priority."),
    ("priority:p2", "FBCA04", "Normal priority."),
    ("status:ready", "0E8A16", "Ready for assignment."),
    ("status:blocked", "B60205", "Blocked and needs attention."),
    ("review:greptile", "5319E7", "Requires Greptile review handling."),
    ("review:cross-agent", "A855F7", "Requires cross-agent review."),
    ("ci:required", "24292F", "CI must pass before merge."),
]


MILESTONES = [
    (
        "M0 Harness Orchestration",
        "Reusable harness artifacts, generation, validation, GitHub workflow, CI, and tmux orchestration.",
    ),
    (
        "M1 Native Windows App Foundation",
        "Windows App SDK/WinUI app shell, packaging, tray, startup, and settings foundation.",
    ),
    (
        "M2 Recording And Insertion Workflow",
        "Push-to-talk capture, HUD, active text insertion, clipboard fallback, and transcript history.",
    ),
    (
        "M3 Provider Integrations",
        "Provider abstraction, secure credentials, OpenAI, Mistral AI, and provider selection.",
    ),
    (
        "M4 Polish And Release Readiness",
        "Design polish, diagnostics, final CI coverage, packaging validation, and release documentation.",
    ),
]


def issue(
    ident: str,
    title: str,
    milestone: str,
    phase: str,
    group: str,
    agent: str,
    labels: list[str],
    deps: list[str],
    outcome: str,
    scope: list[str],
    acceptance: list[str],
    review: list[str],
    ci: list[str],
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": ident,
        "title": title,
        "milestone": milestone,
        "phase": phase,
        "parallel_group": group,
        "agent": agent,
        "labels": labels,
        "dependencies": deps,
        "outcome": outcome,
        "scope": scope,
        "acceptance_criteria": acceptance,
        "review_plan": review,
        "ci_expectations": ci,
        "notes": notes or [],
    }


def build_plan(requirements_path: Path) -> dict[str, Any]:
    requirements_text = requirements_path.read_text(encoding="utf-8")
    if "Voice Transcription App Requirements" not in requirements_text:
        raise ValueError("requirements document does not look like the expected voice transcription requirements")

    labels = [{"name": name, "color": color, "description": description} for name, color, description in LABELS]
    milestones = [{"title": title, "description": description} for title, description in MILESTONES]

    issues = [
        issue(
            "VT-001",
            "Select native Windows app stack and repository structure",
            "M1 Native Windows App Foundation",
            "phase:1",
            "foundation",
            "codex",
            ["type:foundation", "area:windows-app", "agent:codex", "phase:1", "priority:p0", "ci:required", "review:cross-agent"],
            [],
            "Document and scaffold the chosen Windows App SDK/WinUI 3 solution structure without implementing app features.",
            [
                "Create the initial native Windows solution/project structure.",
                "Document Windows-side prerequisites required from WSL2.",
                "Keep the app target Windows 11 only.",
            ],
            [
                "Repository contains a native Windows app skeleton plan or scaffold aligned with Windows App SDK and WinUI 3.",
                "Build prerequisites are documented for Windows 11.",
                "No Electron or browser-wrapper app shell is introduced.",
            ],
            ["Codex implementation review for architecture and build viability.", "Claude review for native app UX implications."],
            ["Harness validation passes.", "Future Windows build command is documented even if not yet runnable from WSL2."],
        ),
        issue(
            "VT-002",
            "Add Windows packaging and startup foundation",
            "M1 Native Windows App Foundation",
            "phase:1",
            "foundation",
            "codex",
            ["type:foundation", "area:windows-app", "agent:codex", "phase:1", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001"],
            "Establish MSIX-first packaging and startup integration direction.",
            [
                "Add packaging project or documented packaging scaffold.",
                "Define startup toggle integration for the selected packaging model.",
                "Document signing and local developer constraints.",
            ],
            [
                "Packaging is included from the start or a documented Windows App SDK blocker is recorded.",
                "Startup toggle path is documented and testable.",
                "CI strategy includes packaging validation expectations.",
            ],
            ["Codex reviews Windows packaging correctness.", "Claude reviews settings/startup UX clarity."],
            ["Packaging-related scripts or docs pass harness validation."],
        ),
        issue(
            "VT-003",
            "Implement app-owned transcription architecture interfaces",
            "M1 Native Windows App Foundation",
            "phase:1",
            "foundation",
            "codex",
            ["type:foundation", "area:provider", "agent:codex", "phase:1", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001"],
            "Create provider, recorder, insertion, history, and settings contracts that reflect ADR 0001.",
            [
                "Define provider abstraction interfaces.",
                "Define insertion adapter boundary.",
                "Define transcript history data contract.",
                "Define secure credential storage boundary.",
            ],
            [
                "OpenAI, Mistral AI, and future local providers fit the same provider contract.",
                "Insertion can be replaced later without rewriting providers or recorder logic.",
                "Contracts are covered by unit tests or compile-time checks once app code exists.",
            ],
            ["Codex reviews architecture boundaries.", "Claude reviews whether UI-facing contracts support design needs."],
            ["Unit test strategy for contracts is documented or implemented."],
        ),
        issue(
            "VT-004",
            "Design settings UI for provider, hotkey, startup, and history controls",
            "M1 Native Windows App Foundation",
            "phase:1",
            "foundation-parallel",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:1", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-001", "VT-003"],
            "Create a native Windows 11 settings experience design for provider selection and core preferences.",
            [
                "Provider selection with exactly one active provider.",
                "API key entry affordance per provider.",
                "Global hotkey configuration and conflict feedback.",
                "Startup toggle.",
                "Transcript retention and clear-history controls.",
            ],
            [
                "Settings surface follows Windows 11 design guidance.",
                "Provider credentials and active provider state are visually distinct.",
                "History retention defaults to 30 days and supports manual clearing.",
            ],
            ["Claude primary design review.", "Codex reviews implementation feasibility and settings/state boundaries."],
            ["UI snapshot or design artifact is attached once the app UI exists."],
        ),
        issue(
            "VT-005",
            "Implement global push-to-talk hotkey handling",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "recording",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001", "VT-003"],
            "Implement configurable global push-to-talk hotkey handling with conflict detection.",
            [
                "Default hotkey is Ctrl+Win+H.",
                "Press starts recording and release stops recording.",
                "Settings validation rejects detectable conflicts.",
            ],
            [
                "Hotkey lifecycle is testable.",
                "Conflict detection failure is shown to the user.",
                "The app does not accept a detected conflicting hotkey.",
            ],
            ["Codex reviews Windows API correctness.", "Claude reviews user feedback for conflicts."],
            ["Unit or integration tests cover hotkey state transitions where possible."],
        ),
        issue(
            "VT-006",
            "Implement microphone recording lifecycle",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "recording",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-005"],
            "Capture audio from the default microphone for push-to-talk transcription.",
            [
                "Start/stop recording follows hotkey state.",
                "Missing microphone permission or device failure produces clear errors.",
                "Audio is not retained by default after transcription completes.",
            ],
            [
                "Recorder exposes audio data in the provider-required format or through a conversion path.",
                "Cancellation and failure are handled.",
                "Audio level information is available for the HUD where feasible.",
            ],
            ["Codex reviews recording lifecycle and cleanup.", "Claude reviews error visibility requirements."],
            ["Recorder tests or documented manual smoke test exists."],
        ),
        issue(
            "VT-007",
            "Design and implement recording HUD",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "recording-parallel",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001", "VT-003"],
            "Create the compact Windows 11 HUD for recording, transcribing, error, and completed states.",
            [
                "HUD is horizontally centered near the lower screen area and inset above the bottom edge.",
                "HUD shows recording state, audio activity, and transcription progress.",
                "HUD dismisses automatically after insertion completes.",
            ],
            [
                "HUD does not steal focus unnecessarily.",
                "All required states are represented.",
                "Text and controls fit across expected desktop scaling conditions.",
            ],
            ["Claude reviews visual and interaction quality.", "Codex reviews state-machine integration."],
            ["UI smoke test or manual verification checklist exists."],
        ),
        issue(
            "VT-008",
            "Implement transcript insertion and clipboard fallback",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "insertion",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-006"],
            "Insert final transcripts into the active text target and fall back to clipboard on failure.",
            [
                "Active text insertion is the default delivery path.",
                "Clipboard fallback runs when insertion fails.",
                "Fallback is visible to the user and history retains the transcript.",
            ],
            [
                "Insertion adapter has a clear success/failure contract.",
                "Clipboard fallback is tested or manually smoke-tested.",
                "Failure does not drop transcript text.",
            ],
            ["Codex reviews Windows insertion behavior.", "Claude reviews fallback notification UX."],
            ["Tests cover insertion success and fallback paths where feasible."],
        ),
        issue(
            "VT-009",
            "Implement persistent transcript history",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "history",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-008"],
            "Persist full transcript text by default with retention and clear-history controls.",
            [
                "Store full transcript text by default.",
                "Default retention is 30 days.",
                "Support manual clearing.",
                "Do not log full transcripts by default.",
            ],
            [
                "History storage is bounded by retention settings.",
                "Clear-history action removes stored transcript text.",
                "History entries include provider and timing metadata.",
            ],
            ["Codex reviews privacy and storage behavior.", "Claude reviews history UI affordances."],
            ["History retention logic has unit coverage."],
        ),
        issue(
            "VT-010",
            "Implement secure credential storage",
            "M3 Provider Integrations",
            "phase:3",
            "providers",
            "codex",
            ["type:implementation", "area:provider", "agent:codex", "phase:3", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-004"],
            "Store provider API keys using Windows-native secure credential storage.",
            [
                "API keys are entered through settings.",
                "Keys are not stored in plain-text app configuration.",
                "Credential failures are surfaced clearly.",
            ],
            [
                "Credential storage uses Windows Credential Manager or equivalent Windows-native secure storage.",
                "Provider adapters can retrieve keys without exposing them in logs.",
                "Deleting a provider credential is supported.",
            ],
            ["Codex reviews security boundary.", "Claude reviews settings clarity around saved credentials."],
            ["Credential storage behavior has tests or documented manual verification."],
        ),
        issue(
            "VT-011",
            "Implement OpenAI transcription provider",
            "M3 Provider Integrations",
            "phase:3",
            "providers-parallel",
            "codex",
            ["type:implementation", "area:provider", "agent:codex", "phase:3", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-006", "VT-010"],
            "Integrate OpenAI transcription through the provider abstraction.",
            [
                "Use the latest best OpenAI transcription direction from official docs.",
                "Support configured API key retrieval.",
                "Normalize provider errors.",
                "Support cancellation where possible.",
            ],
            [
                "OpenAI provider implements the common provider contract.",
                "Provider can be selected as the active provider.",
                "Network and credential failures are user-visible and not logged with secrets.",
            ],
            ["Codex reviews API integration and error normalization.", "Claude reviews user-facing provider error messages."],
            ["Provider contract tests or mocked integration tests exist."],
        ),
        issue(
            "VT-012",
            "Implement Mistral AI transcription provider",
            "M3 Provider Integrations",
            "phase:3",
            "providers-parallel",
            "codex",
            ["type:implementation", "area:provider", "agent:codex", "phase:3", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-006", "VT-010"],
            "Integrate Mistral AI transcription through the provider abstraction.",
            [
                "Use the latest best Mistral transcription direction from official docs.",
                "Support configured API key retrieval.",
                "Normalize provider errors.",
                "Support cancellation where possible.",
            ],
            [
                "Mistral provider implements the common provider contract.",
                "Provider can be selected as the active provider.",
                "Network and credential failures are user-visible and not logged with secrets.",
            ],
            ["Codex reviews API integration and error normalization.", "Claude reviews user-facing provider error messages."],
            ["Provider contract tests or mocked integration tests exist."],
        ),
        issue(
            "VT-013",
            "Implement system tray controls and idle behavior",
            "M1 Native Windows App Foundation",
            "phase:1",
            "foundation-parallel",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:1", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-001"],
            "Run quietly in the system tray with app status and basic actions.",
            [
                "Tray icon indicates app availability.",
                "Tray menu exposes settings and exit.",
                "Idle behavior does not interrupt foreground work.",
            ],
            [
                "Tray integration works with the selected app model.",
                "Settings can be opened from tray.",
                "Exit cleanly releases hotkey and recording resources.",
            ],
            ["Codex reviews tray lifecycle.", "Claude reviews tray menu wording and UX."],
            ["Manual smoke test checklist exists for tray behavior."],
        ),
        issue(
            "VT-014",
            "Add native app CI and test harness",
            "M4 Polish And Release Readiness",
            "phase:4",
            "release",
            "codex",
            ["type:testing", "area:ci", "agent:codex", "phase:4", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001"],
            "Create fast Windows app CI with agent-readable failure summaries.",
            [
                "Define unit, integration, UI smoke, and packaging validation layers.",
                "Keep CI economical and segmented.",
                "Emit concise machine-readable failure summaries.",
            ],
            [
                "CI runs harness validation and app tests appropriate to the current scaffold.",
                "Failure artifact points to failing check, files, and likely owner.",
                "Logs are segmented and not unnecessarily noisy.",
            ],
            ["Codex reviews CI correctness.", "Claude reviews human readability of CI output."],
            ["GitHub Actions workflow passes on the repository."],
        ),
        issue(
            "VT-015",
            "Polish settings, HUD, and transcript history UX",
            "M4 Polish And Release Readiness",
            "phase:4",
            "release",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:4", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-004", "VT-007", "VT-009", "VT-011", "VT-012"],
            "Refine the native Windows 11 user experience across settings, HUD, and history.",
            [
                "Ensure controls are compact, clear, and native-feeling.",
                "Verify provider selection and credential states are understandable.",
                "Verify history deletion and retention controls are easy to find.",
            ],
            [
                "UI fits without overlap at common desktop scaling settings.",
                "User-facing copy is concise and actionable.",
                "Claude and Codex reviews agree the UI is ready for release candidate testing.",
            ],
            ["Claude primary design review.", "Codex reviews implementation integration and accessibility risks."],
            ["UI smoke artifacts or screenshots are attached where possible."],
        ),
    ]

    return {
        "version": 1,
        "source": {
            "requirements_path": str(requirements_path.relative_to(ROOT)),
            "generated_at": "deterministic-dry-run",
        },
        "project": {
            "title": "Voice Transcription Harness Execution",
            "description": "Dependency-aware execution plan for building the native Windows 11 voice transcription app through coordinated agents.",
            "fields": ["Status", "Phase", "Agent", "Parallel Group", "Blocked By", "Review State", "CI State"],
        },
        "labels": labels,
        "milestones": milestones,
        "issues": issues,
    }


def validate_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    label_names = [label["name"] for label in plan["labels"]]
    label_set = set(label_names)
    if len(label_names) != len(label_set):
        errors.append("duplicate label names found")

    milestone_titles = {milestone["title"] for milestone in plan["milestones"]}
    issue_ids = [item["id"] for item in plan["issues"]]
    issue_id_set = set(issue_ids)
    if len(issue_ids) != len(issue_id_set):
        errors.append("duplicate issue ids found")

    for item in plan["issues"]:
        if item["milestone"] not in milestone_titles:
            errors.append(f"{item['id']} references missing milestone {item['milestone']}")
        for label in item["labels"]:
            if label not in label_set:
                errors.append(f"{item['id']} references missing label {label}")
        for dep in item["dependencies"]:
            if dep not in issue_id_set:
                errors.append(f"{item['id']} depends on missing issue {dep}")
            if dep == item["id"]:
                errors.append(f"{item['id']} depends on itself")
        if len(item["acceptance_criteria"]) < 2:
            errors.append(f"{item['id']} needs at least two acceptance criteria")
        if item["agent"] not in {"codex", "claude", "either"}:
            errors.append(f"{item['id']} has invalid agent {item['agent']}")

    return errors


def render_issue_markdown(item: dict[str, Any]) -> str:
    deps = ", ".join(item["dependencies"]) if item["dependencies"] else "None"
    labels = ", ".join(f"`{label}`" for label in item["labels"])
    scope = "\n".join(f"- [ ] {entry}" for entry in item["scope"])
    acceptance = "\n".join(f"- [ ] {entry}" for entry in item["acceptance_criteria"])
    review = "\n".join(f"- [ ] {entry}" for entry in item["review_plan"])
    ci = "\n".join(f"- [ ] {entry}" for entry in item["ci_expectations"])
    notes = "\n".join(f"- {entry}" for entry in item["notes"]) if item["notes"] else "- None"

    return f"""# {item['title']}

> Harness ID: `{item['id']}`

## Outcome

{item['outcome']}

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | {item['milestone']} |
| Phase | `{item['phase']}` |
| Parallel Group | `{item['parallel_group']}` |
| Recommended Agent | `agent:{item['agent']}` |
| Dependencies | {deps} |
| Labels | {labels} |

## Scope

{scope}

## Acceptance Criteria

{acceptance}

## Review Plan

{review}

## CI Expectations

{ci}

## Notes

{notes}

## Agent Handoff

When assigned, create a branch named `work/{item['id'].lower()}-{slug(item['title'])}` and open a PR that links this issue.

Final worker response should include:

```text
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: <branch>
PR: <url-or-none>
SUMMARY: <one line>
```
"""


def slug(value: str) -> str:
    result = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            result.append(char)
            previous_dash = False
        elif not previous_dash:
            result.append("-")
            previous_dash = True
    return "".join(result).strip("-")[:60]


def write_plan(plan: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    issues_dir = output_dir / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    for item in plan["issues"]:
        path = issues_dir / f"{item['id']}-{slug(item['title'])}.md"
        path.write_text(render_issue_markdown(item), encoding="utf-8")

    summary = render_summary(plan)
    (output_dir / "README.md").write_text(summary, encoding="utf-8")


def render_summary(plan: dict[str, Any]) -> str:
    by_phase: dict[str, list[dict[str, Any]]] = {}
    for item in plan["issues"]:
        by_phase.setdefault(item["phase"], []).append(item)

    lines = [
        "# Generated Harness Plan",
        "",
        f"Source: `{plan['source']['requirements_path']}`",
        "",
        "This is a dry-run plan. It has not created GitHub issues or projects.",
        "",
        "## Issues By Phase",
        "",
    ]

    for phase in sorted(by_phase):
        lines.append(f"### {phase}")
        lines.append("")
        lines.append("| ID | Title | Agent | Dependencies | Parallel Group |")
        lines.append("| --- | --- | --- | --- | --- |")
        for item in by_phase[phase]:
            deps = ", ".join(item["dependencies"]) if item["dependencies"] else "None"
            lines.append(f"| {item['id']} | {item['title']} | `{item['agent']}` | {deps} | `{item['parallel_group']}` |")
        lines.append("")

    lines.extend(
        [
            "## Apply",
            "",
            "Review `plan.json` and issue markdown first. To apply later:",
            "",
            "```sh",
            "python3 scripts/github_apply_plan.py --plan generated/harness-plan/plan.json --apply",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def command_generate(args: argparse.Namespace) -> int:
    requirements = Path(args.requirements).resolve()
    output = Path(args.output).resolve()
    plan = build_plan(requirements)
    errors = validate_plan(plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    write_plan(plan, output)
    print(f"Generated {len(plan['issues'])} issues into {output}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    plan_path = Path(args.plan).resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    errors = validate_plan(plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        write_ci_summary("failed", errors)
        return 1
    write_ci_summary("passed", [])
    print(f"Validated {len(plan['issues'])} issues from {plan_path}")
    return 0


def write_ci_summary(status: str, errors: list[str]) -> None:
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    failed_checks = [
        {
            "name": "validate-harness-plan",
            "summary": error,
            "files": ["generated/harness-plan/plan.json"],
            "suggested_owner": "agent:codex",
        }
        for error in errors
    ]
    payload = {"status": status, "failed_checks": failed_checks}
    (artifacts / "ci-summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate a dry-run plan")
    generate.add_argument("--requirements", default=str(DEFAULT_REQUIREMENTS))
    generate.add_argument("--output", default=str(DEFAULT_OUTPUT))
    generate.set_defaults(func=command_generate)

    validate = subparsers.add_parser("validate", help="Validate a generated plan")
    validate.add_argument("--plan", default=str(DEFAULT_OUTPUT / "plan.json"))
    validate.set_defaults(func=command_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
