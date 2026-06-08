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
    model: str | None = None,
    reasoning: str | None = None,
    expected_files: list[str] | None = None,
    implementation_steps: list[str] | None = None,
    constraints: list[str] | None = None,
    failure_modes: list[str] | None = None,
) -> dict[str, Any]:
    model = model or default_model(agent, labels)
    reasoning = reasoning or default_reasoning(labels, agent)

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
        "execution": {
            "model": model,
            "reasoning_effort": reasoning,
            "agent_command": "codex" if agent == "codex" else "claude" if agent == "claude" else "codex or claude",
            "context_budget": "medium",
            "expected_files": expected_files or infer_expected_files(labels),
            "implementation_steps": implementation_steps or default_steps(scope, acceptance),
            "constraints": constraints or default_constraints(labels),
            "failure_modes": failure_modes or default_failure_modes(labels),
        },
    }


def default_model(agent: str, labels: list[str]) -> str:
    if agent == "claude":
        return "Claude Code Sonnet, medium effort; use Opus/high only for visual system decisions or ambiguous UX tradeoffs"
    if "type:foundation" in labels or "area:ci" in labels or "area:provider" in labels:
        return "GPT-5.5 via local Codex CLI, medium reasoning; escalate to high for architecture/security/API uncertainty"
    return "GPT-5.5 via local Codex CLI, low-to-medium reasoning"


def default_reasoning(labels: list[str], agent: str) -> str:
    if agent == "claude":
        return "medium"
    if "priority:p0" in labels or "type:foundation" in labels or "area:ci" in labels:
        return "medium"
    return "low"


def infer_expected_files(labels: list[str]) -> list[str]:
    if "area:ui" in labels:
        return ["src/** UI files", "docs/**/*.md for UI verification notes", "tests/** UI smoke artifacts when available"]
    if "area:provider" in labels:
        return ["src/** provider files", "tests/** provider tests", "docs/** provider notes when needed"]
    if "area:ci" in labels:
        return [".github/workflows/**", "scripts/**", "docs/harness/ci-strategy.md"]
    if "area:harness" in labels:
        return ["docs/harness/**", "scripts/**", "generated/harness-plan/**"]
    return ["src/**", "tests/**", "docs/** when implementation choices need explanation"]


def default_steps(scope: list[str], acceptance: list[str]) -> list[str]:
    return [
        "Read docs/requirements.md and relevant ADRs before editing.",
        "Inspect existing code and tests before choosing an implementation shape.",
        *[f"Implement: {item}" for item in scope],
        *[f"Verify: {item}" for item in acceptance],
        "Run the issue-specific test command and record the result in the PR.",
        "Open a focused PR that closes only this issue unless the issue explicitly says otherwise.",
    ]


def default_constraints(labels: list[str]) -> list[str]:
    constraints = [
        "Do not make unrelated refactors.",
        "Do not introduce paid model API calls for orchestration.",
        "Preserve user changes and generated harness IDs.",
        "If a decision is low-risk and reversible, use judgment and document it.",
    ]
    if "area:windows-app" in labels:
        constraints.append("Keep the implementation native Windows 11; do not introduce Electron or a browser-wrapper shell.")
    if "area:provider" in labels:
        constraints.append("Do not bind UI workflow directly to one provider API shape.")
        constraints.append("Do not log credentials, raw audio, or full transcripts by default.")
    if "area:ui" in labels:
        constraints.append("Follow native Windows 11/Fluent patterns; avoid marketing-page composition.")
        constraints.append("Text and controls must fit at common Windows desktop scaling settings.")
    if "area:ci" in labels:
        constraints.append("CI logs must stay segmented and concise; add machine-readable summaries for failures.")
    return constraints


def default_failure_modes(labels: list[str]) -> list[str]:
    failures = [
        "Acceptance criteria are ambiguous after reading the requirements.",
        "Required local or Windows-side tool is missing.",
        "Implementation requires a product/security/architecture decision not already recorded.",
    ]
    if "area:provider" in labels:
        failures.append("Provider docs or model names conflict with the recorded requirements; verify official docs before coding.")
    if "area:ui" in labels:
        failures.append("Visual behavior cannot be verified without a running Windows UI; attach a manual verification checklist.")
    if "area:ci" in labels:
        failures.append("CI produces noisy logs or lacks a machine-readable failure artifact.")
    return failures


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
            "Create recording HUD visual design specification",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "recording-parallel",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-001", "VT-003"],
            "Create the visual and interaction specification for the compact Windows 11 HUD before implementation.",
            [
                "Specify HUD layout, placement, sizing, visual hierarchy, and state variants.",
                "Specify how audio activity and transcription progress appear without layout shift.",
                "Specify focus and dismissal behavior without implementing the state machine.",
            ],
            [
                "Design spec covers recording, transcribing, fallback, error, and completed states.",
                "Spec follows native Windows 11 visual guidance.",
                "Spec is detailed enough for VT-021 to implement without re-designing the HUD.",
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
            "Wire transcript history into completed transcription workflow",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "history",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-008", "VT-022"],
            "Ensure completed and fallback transcripts are written to history through the storage engine.",
            [
                "Write successful active-insertion transcripts to history.",
                "Write clipboard-fallback transcripts to history.",
                "Include provider, duration, timestamp, and delivery outcome metadata.",
                "Do not duplicate entries on retry or UI refresh.",
            ],
            [
                "Every completed transcript path records exactly one history entry.",
                "Fallback path preserves transcript text even when insertion fails.",
                "History writes use the VT-022 storage engine instead of ad hoc persistence.",
            ],
            ["Codex reviews workflow and persistence integration.", "Claude reviews user-visible fallback/history behavior."],
            ["Workflow tests cover active insertion and clipboard fallback history writes."],
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
            ["VT-018", "VT-019", "VT-021", "VT-023", "VT-011", "VT-012"],
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
        issue(
            "VT-016",
            "Research current provider APIs and pin adapter defaults",
            "M3 Provider Integrations",
            "phase:3",
            "providers-research",
            "codex",
            ["type:research", "area:provider", "agent:codex", "phase:3", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003"],
            "Verify current OpenAI and Mistral transcription docs immediately before provider implementation and record adapter defaults.",
            [
                "Check official OpenAI transcription and realtime transcription docs.",
                "Check official Mistral audio transcription docs.",
                "Record selected endpoint, model alias, audio format, and streaming support for each provider.",
                "Add source links and date checked to provider documentation.",
            ],
            [
                "Provider implementation tickets have current model/API facts available.",
                "No provider adapter relies on stale remembered API details.",
                "Docs explain whether each provider supports batch, streaming, cancellation, and error normalization.",
            ],
            ["Codex reviews source accuracy and API implications.", "Claude reviews user-facing provider wording implications."],
            ["Harness validation passes.", "Provider documentation includes official source links."],
            expected_files=["docs/providers/**", "docs/harness/** if workflow guidance changes"],
            implementation_steps=[
                "Use official provider docs only; do not rely on memory for model names or endpoints.",
                "Create provider research notes with endpoint, model, audio format, auth, streaming, cancellation, and known errors.",
                "Update generated issue notes or provider docs if the requirements need a non-product correction.",
                "Run harness validation.",
            ],
        ),
        issue(
            "VT-017",
            "Create settings shell and navigation structure",
            "M1 Native Windows App Foundation",
            "phase:1",
            "settings-ui",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:1", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-001"],
            "Create the Windows 11 settings shell structure before wiring provider-specific settings.",
            [
                "Define settings navigation sections.",
                "Create shell layout for General, Providers, Hotkey, History, and About/Diagnostics.",
                "Use native Windows 11 spacing, typography, and control hierarchy.",
            ],
            [
                "Settings shell can host later provider, hotkey, startup, and history panels.",
                "Navigation is understandable without explanatory feature-marketing text.",
                "Design is compact and operational, not a landing page.",
            ],
            ["Claude reviews visual structure.", "Codex reviews whether the shell can be wired to settings state."],
            ["UI smoke checklist or screenshots are attached once UI exists."],
            expected_files=["src/** settings UI files", "docs/** UI notes or screenshots"],
        ),
        issue(
            "VT-018",
            "Implement provider selection settings panel",
            "M3 Provider Integrations",
            "phase:3",
            "provider-settings",
            "claude",
            ["type:implementation", "area:ui", "area:provider", "agent:claude", "phase:3", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-004", "VT-010", "VT-011", "VT-012"],
            "Implement the settings panel that shows saved provider credentials and exactly one active provider.",
            [
                "Show OpenAI and Mistral AI provider rows/cards without nesting cards inside cards.",
                "Make saved credential state distinct from active provider state.",
                "Allow changing the single active provider.",
                "Show clear validation/error state when selected provider lacks credentials.",
            ],
            [
                "Exactly one provider can be active at a time.",
                "Saved API keys for inactive providers do not switch the active provider automatically.",
                "User can tell what will be used for the next transcription.",
            ],
            ["Claude reviews UX clarity.", "Codex reviews state wiring and provider contract fit."],
            ["UI/state tests or manual smoke checklist cover provider switching."],
        ),
        issue(
            "VT-019",
            "Implement hotkey settings panel and conflict feedback",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "hotkey-settings",
            "claude",
            ["type:implementation", "area:ui", "area:windows-app", "agent:claude", "phase:2", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-004", "VT-005"],
            "Create the settings UI for recording the global hotkey and displaying conflict feedback.",
            [
                "Default visible hotkey is Ctrl+Win+H.",
                "Hotkey capture UI handles press/release clearly.",
                "Conflict errors prevent saving and explain the problem.",
                "User can cancel without changing the current hotkey.",
            ],
            [
                "Conflict state is visible and actionable.",
                "The UI does not accept a detected conflicting hotkey.",
                "The hotkey capture interaction is keyboard-accessible.",
            ],
            ["Claude reviews interaction design.", "Codex reviews integration with hotkey validation service."],
            ["UI/state tests or manual smoke checklist cover valid, invalid, and cancel paths."],
        ),
        issue(
            "VT-020",
            "Define HUD state machine before visual implementation",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "hud-design",
            "codex",
            ["type:foundation", "area:ui", "area:windows-app", "agent:codex", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-006", "VT-008"],
            "Define the HUD state machine so visual implementation does not invent workflow behavior.",
            [
                "Define idle, preparing, recording, transcribing, inserting, fallback, error, and completed states.",
                "Define transitions, cancellation behavior, and auto-dismiss triggers.",
                "Define data each state exposes to the UI.",
            ],
            [
                "HUD implementation can follow the state machine without product guesswork.",
                "Auto-dismiss happens only after insertion or fallback notification is complete.",
                "Error states preserve transcript text when available.",
            ],
            ["Codex reviews state-machine completeness.", "Claude reviews whether states support clear UI."],
            ["State-machine tests or documentation examples exist."],
        ),
        issue(
            "VT-021",
            "Implement HUD visual surface from state machine",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "hud-implementation",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:2", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-007", "VT-020"],
            "Implement the HUD visual surface using the prescribed state machine.",
            [
                "Render all HUD states from VT-020.",
                "Position centered near the lower screen and inset above the bottom edge.",
                "Show audio activity without layout shift.",
                "Keep the foreground application focus behavior intact.",
            ],
            [
                "HUD renders every state without text overlap.",
                "HUD does not behave like a modal dialog.",
                "HUD is visually consistent with Windows 11 surfaces.",
            ],
            ["Claude reviews visual polish.", "Codex reviews state binding and focus behavior."],
            ["UI smoke checklist or screenshot artifacts cover all states."],
        ),
        issue(
            "VT-022",
            "Implement transcript history storage and retention engine",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "history-engine",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:2", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-003"],
            "Implement full-text transcript history storage with 30-day retention and manual clearing, independent of UI polish.",
            [
                "Persist full transcript text and metadata.",
                "Apply default 30-day retention.",
                "Expose clear-history operation.",
                "Keep raw audio out of history by default.",
            ],
            [
                "Retention engine can delete expired history entries.",
                "Manual clearing removes full transcript text.",
                "History writes do not log full transcript text by default.",
            ],
            ["Codex reviews privacy and persistence behavior.", "Claude reviews history state needed by UI."],
            ["Unit tests cover save, query, retention cleanup, and clear-history behavior."],
        ),
        issue(
            "VT-023",
            "Implement transcript history UI",
            "M2 Recording And Insertion Workflow",
            "phase:2",
            "history-ui",
            "claude",
            ["type:implementation", "area:ui", "agent:claude", "phase:2", "priority:p2", "ci:required", "review:cross-agent"],
            ["VT-017", "VT-022"],
            "Implement the transcript history view and retention controls.",
            [
                "Show recent transcript entries with provider and timestamp metadata.",
                "Support manual clear-history action.",
                "Expose retention setting with 30-day default.",
                "Avoid showing raw audio or credentials.",
            ],
            [
                "History UI is scannable and compact.",
                "Clear-history action is explicit and hard to trigger accidentally.",
                "Retention control is understandable without long explanatory text.",
            ],
            ["Claude reviews UI clarity.", "Codex reviews privacy and state integration."],
            ["UI/state tests or manual smoke checklist cover history display and clearing."],
        ),
        issue(
            "VT-024",
            "Build machine-readable CI failure summarizer",
            "M4 Polish And Release Readiness",
            "phase:4",
            "ci-foundation",
            "codex",
            ["type:testing", "area:ci", "agent:codex", "phase:4", "priority:p0", "ci:required", "review:cross-agent"],
            ["VT-014"],
            "Create the CI summary artifact generator that agents read before full logs.",
            [
                "Emit artifacts/ci-summary.json for failed checks.",
                "Include failed check name, summary, likely files, suggested owner, and next command.",
                "Keep summaries concise and deterministic.",
            ],
            [
                "CI uploads ci-summary.json on every run.",
                "Agent repair loop docs point to the artifact first.",
                "A simulated failure can produce a useful summary without noisy logs.",
            ],
            ["Codex reviews failure parsing and artifact shape.", "Claude reviews human readability of summaries."],
            ["Harness CI validates the summary shape."],
        ),
        issue(
            "VT-025",
            "Implement Greptile review collection and reply workflow",
            "M4 Polish And Release Readiness",
            "phase:4",
            "review-automation",
            "codex",
            ["type:implementation", "area:harness", "agent:codex", "phase:4", "priority:p1", "ci:required", "review:cross-agent", "review:greptile"],
            ["VT-014"],
            "Add scripts or documented commands to collect Greptile findings and prepare fix replies.",
            [
                "Fetch PR reviews/comments with gh and GraphQL where needed.",
                "Extract Greptile findings into a machine-readable file.",
                "Generate reply text that references fix commit SHA and test command.",
                "Document when thread resolution requires human permissions.",
            ],
            [
                "Greptile findings can be handed to a fixer agent without manually reading the whole PR.",
                "Reply format includes exact fix commit and explanation.",
                "Permission failures leave actionable status instead of silent failure.",
            ],
            ["Codex reviews GitHub API correctness.", "Claude reviews review-status readability."],
            ["Harness validation passes and dry-run output explains required gh commands."],
        ),
        issue(
            "VT-026",
            "Add Windows app smoke test strategy and checklist",
            "M4 Polish And Release Readiness",
            "phase:4",
            "testing-strategy",
            "codex",
            ["type:testing", "area:ci", "area:windows-app", "agent:codex", "phase:4", "priority:p1", "ci:required", "review:cross-agent"],
            ["VT-001", "VT-014"],
            "Define a practical Windows 11 smoke test strategy that is fast enough for CI and useful for release confidence.",
            [
                "Document unit, integration, UI, packaging, and manual smoke layers.",
                "Define which checks run on every PR versus release candidate.",
                "Define expected artifacts for UI and packaging checks.",
            ],
            [
                "Testing strategy avoids hours-long CI runs.",
                "Failures point to likely file/test owner.",
                "Windows-specific checks are separated from fast harness checks.",
            ],
            ["Codex reviews test architecture.", "Claude reviews UI verification coverage."],
            ["Docs and CI expectations are consistent."],
        ),
        issue(
            "VT-027",
            "Create first-run diagnostics and logging policy",
            "M4 Polish And Release Readiness",
            "phase:4",
            "diagnostics",
            "codex",
            ["type:implementation", "area:windows-app", "agent:codex", "phase:4", "priority:p2", "ci:required", "review:cross-agent"],
            ["VT-003", "VT-010", "VT-014"],
            "Define and implement diagnostics that help fix failures without logging sensitive content.",
            [
                "Log provider name, operation state, duration, and normalized error codes.",
                "Do not log credentials, raw audio, or full transcripts by default.",
                "Expose enough diagnostics for CI and user support.",
            ],
            [
                "Diagnostics help identify microphone, credential, network, provider, insertion, and history failures.",
                "Sensitive content is excluded by default.",
                "Logs are structured enough for agent consumption.",
            ],
            ["Codex reviews security and observability.", "Claude reviews user-facing diagnostics copy."],
            ["Tests or manual checks verify sensitive values are not logged."],
        ),
    ]
    issues = topological_order(issues)

    return {
        "version": 1,
        "source": {
            "requirements_path": str(requirements_path.relative_to(ROOT)),
            "generated_at": "deterministic-dry-run",
        },
        "planner": {
            "mode": "deterministic_sample",
            "intended_production_planner": "GPT-5.5 extra-high reasoning via local Codex CLI/subscription",
            "note": "This sample plan is a regression fixture and demo output. Production decomposition should be performed by a high-reasoning planner, then validated and rendered by this harness.",
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


def topological_order(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {item["id"]: item for item in issues}
    visited: set[str] = set()
    ordered: list[dict[str, Any]] = []

    def visit(item: dict[str, Any]) -> None:
        if item["id"] in visited:
            return
        for dep in item["dependencies"]:
            if dep in by_id:
                visit(by_id[dep])
        visited.add(item["id"])
        ordered.append(item)

    for item in issues:
        visit(item)
    return ordered


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
        execution = item.get("execution", {})
        for field in ["model", "reasoning_effort", "agent_command", "implementation_steps", "constraints", "failure_modes"]:
            if not execution.get(field):
                errors.append(f"{item['id']} missing execution.{field}")

    errors.extend(validate_dependency_cycles(plan["issues"]))
    return errors


def validate_dependency_cycles(issues: list[dict[str, Any]]) -> list[str]:
    by_id = {item["id"]: item for item in issues}
    visiting: set[str] = set()
    visited: set[str] = set()
    errors: list[str] = []

    def visit(ident: str, path: list[str]) -> None:
        if ident in visited:
            return
        if ident in visiting:
            cycle = " -> ".join([*path, ident])
            errors.append(f"dependency cycle detected: {cycle}")
            return
        visiting.add(ident)
        for dep in by_id.get(ident, {}).get("dependencies", []):
            if dep in by_id:
                visit(dep, [*path, ident])
        visiting.remove(ident)
        visited.add(ident)

    for item in issues:
        visit(item["id"], [])
    return errors


def render_issue_markdown(item: dict[str, Any]) -> str:
    deps = ", ".join(item["dependencies"]) if item["dependencies"] else "None"
    labels = ", ".join(f"`{label}`" for label in item["labels"])
    scope = "\n".join(f"- [ ] {entry}" for entry in item["scope"])
    acceptance = "\n".join(f"- [ ] {entry}" for entry in item["acceptance_criteria"])
    review = "\n".join(f"- [ ] {entry}" for entry in item["review_plan"])
    ci = "\n".join(f"- [ ] {entry}" for entry in item["ci_expectations"])
    notes = "\n".join(f"- {entry}" for entry in item["notes"]) if item["notes"] else "- None"
    execution = item["execution"]
    steps = "\n".join(f"- [ ] {entry}" for entry in execution["implementation_steps"])
    constraints = "\n".join(f"- {entry}" for entry in execution["constraints"])
    failures = "\n".join(f"- {entry}" for entry in execution["failure_modes"])
    expected_files = "\n".join(f"- `{entry}`" for entry in execution["expected_files"])
    dep_text = ", ".join(f"`{dep}`" for dep in item["dependencies"]) if item["dependencies"] else "`None`"
    mermaid_deps = render_issue_mermaid(item)

    return f"""# {item['title']}

> Harness ID: `{item['id']}`

> [!IMPORTANT]
> This issue is designed for a lower/medium-effort worker. Do not re-plan the product.
> Execute the prescribed scope, keep the PR focused, and escalate only for material product,
> security, architecture, CI, or UX decisions.

## Outcome

{item['outcome']}

## Work Metadata

| Field | Value |
| --- | --- |
| Milestone | {item['milestone']} |
| Phase | `{item['phase']}` |
| Parallel Group | `{item['parallel_group']}` |
| Recommended Agent | `agent:{item['agent']}` |
| Recommended Model | {execution['model']} |
| Reasoning Effort | `{execution['reasoning_effort']}` |
| Agent Command | `{execution['agent_command']}` |
| Dependencies | {dep_text} |
| Labels | {labels} |

## Dependency View

```mermaid
{mermaid_deps}
```

## Scope

{scope}

## Prescribed Implementation Plan

{steps}

## Expected Files Or Areas

{expected_files}

## Acceptance Criteria

{acceptance}

## Constraints

{constraints}

<details>
<summary>Failure modes and escalation rules</summary>

{failures}

If one of these occurs, stop and report:

```text
HARNESS_STATUS: blocked
BLOCKER: <specific blocker>
NEEDED_DECISION: <yes|no>
```

</details>

## Review Plan

{review}

## CI Expectations

{ci}

## Notes

{notes}

## Agent Handoff

When assigned, create a branch named `work/{item['id'].lower()}-{slug(item['title'])}` and open a PR that links this issue.

Use this worker prompt:

```text
You are working on {item['id']}: {item['title']}.

Recommended model/effort: {execution['model']} / {execution['reasoning_effort']}.
Primary objective: {item['outcome']}

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
"""


def render_issue_mermaid(item: dict[str, Any]) -> str:
    lines = ["flowchart LR"]
    current = item["id"].replace("-", "_")
    lines.append(f"    {current}[{item['id']}]")
    for dep in item["dependencies"]:
        dep_node = dep.replace("-", "_")
        lines.append(f"    {dep_node}[{dep}] --> {current}")
    if not item["dependencies"]:
        lines.append(f"    Start([Ready]) --> {current}")
    return "\n".join(lines)


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
    for stale_issue in issues_dir.glob("*.md"):
        stale_issue.unlink()

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
        "> [!TIP]",
        "> Each generated issue includes a recommended model, reasoning effort, dependency diagram,",
        "> implementation checklist, constraints, failure modes, and worker prompt. The intent is",
        "> to pay planning cost up front so lower/medium-effort workers can execute safely.",
        "",
        "> [!IMPORTANT]",
        "> This generated plan is a deterministic sample and regression fixture. The intended",
        "> production workflow uses GPT-5.5 extra-high reasoning through the local Codex CLI",
        "> to perform decomposition, then uses this harness to validate, render, and apply it.",
        "",
        "## Dependency Map",
        "",
        "```mermaid",
        render_plan_mermaid(plan),
        "```",
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
            effort = item["execution"]["reasoning_effort"]
            lines.append(f"| {item['id']} | {item['title']} | `{item['agent']}` / `{effort}` | {deps} | `{item['parallel_group']}` |")
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


def render_plan_mermaid(plan: dict[str, Any]) -> str:
    lines = ["flowchart LR"]
    for item in plan["issues"]:
        node = item["id"].replace("-", "_")
        title = item["title"].replace('"', "'")
        lines.append(f'    {node}["{item["id"]}<br/>{title}"]')
    for item in plan["issues"]:
        current = item["id"].replace("-", "_")
        for dep in item["dependencies"]:
            lines.append(f"    {dep.replace('-', '_')} --> {current}")
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
