# Voice Transcription App Requirements

## Purpose

Build a native Windows 11 voice transcription application using a harness-engineering workflow, where coordinated agents can incrementally design, implement, test, and refine the product.

The application should let a user trigger voice transcription from anywhere in Windows, see clear recording/transcription feedback, and receive transcribed text through a pluggable transcription backend.

## Product Goals

- Feel like a true native Windows 11 application.
- Support global hotkey driven transcription from any active application.
- Provide a visible, low-friction recording/transcription HUD.
- Run quietly in the system tray when idle.
- Support configurable startup behavior.
- Use a provider abstraction so cloud transcription services and future local models can share the same app workflow.
- Optimize for Windows 11 only; do not spend effort on older Windows versions or cross-platform compatibility.

## Target Platform

- Operating system: Windows 11.
- Development host may include WSL2 Ubuntu, but the application target is native Windows 11.
- Build and packaging flows may require Windows-side tooling outside WSL2.
- Backward compatibility with Windows 10 or older platforms is not required.

## Native Windows Direction

The default implementation direction should be:

- Windows App SDK for modern Windows desktop application infrastructure.
- WinUI 3 for native Windows UI.
- Fluent / Windows 11 design guidance for visual and interaction patterns.
- Windows-native APIs for system tray integration, global hotkeys, startup tasks, audio capture, and app packaging where appropriate.

Avoid choosing web-wrapper frameworks only because the agent is running inside WSL2. If Windows tooling, Visual Studio, Windows SDK, MSIX packaging, or PowerShell commands are required, the harness should surface those requirements rather than compromise the target.

References:

- Windows App SDK: https://learn.microsoft.com/windows/apps/windows-app-sdk/
- WinUI 3: https://learn.microsoft.com/windows/apps/winui/winui3/
- Design and code Windows apps: https://learn.microsoft.com/windows/apps/design/

## Core User Experience

### Idle State

- The app can run in the background.
- A system tray icon indicates the app is installed and available.
- The user can open settings or exit the app from the tray icon.
- The app can optionally start automatically when Windows starts.

### Triggering Transcription

- The user can start and stop transcription with a global hotkey.
- The default hotkey should be chosen to avoid common Windows and application shortcuts.
- The hotkey must be configurable in settings.
- The app should validate hotkey conflicts where practical.
- The app should make clear whether the hotkey starts/stops recording, toggles dictation, or performs a push-to-talk action.

### Recording HUD

- When transcription is active, a compact HUD appears.
- The HUD should feel like a native Windows 11 surface.
- The HUD should show recording state, audio activity, and transcription progress.
- The HUD should support a clear stop/cancel affordance.
- The HUD should avoid stealing focus unnecessarily from the application the user is dictating into.
- The HUD should handle loading, recording, transcribing, error, and completed states.

### Transcription Result

- The app records audio and sends it to a configured transcription provider.
- The app should support real-time or near-real-time transcription where the selected provider supports it.
- The app should define how transcribed text is delivered:
  - copy to clipboard,
  - insert into the active text field,
  - display for manual copy,
  - or another explicit behavior chosen during design.
- The app should preserve enough metadata for debugging, such as provider name, duration, and error state, without exposing sensitive audio content unnecessarily.

## Functional Requirements

### Must Have

- Native Windows 11 application shell.
- System tray icon with app status and basic actions.
- Configurable global hotkey.
- Audio recording from the default microphone.
- Recording/transcription HUD.
- At least one external transcription provider integration.
- Provider abstraction that allows additional cloud or local providers.
- Settings UI for hotkey, provider configuration, microphone selection if feasible, and startup behavior.
- Clear error handling for missing microphone permissions, unavailable provider credentials, network failures, and provider failures.

### Should Have

- Automatic startup toggle.
- Provider selection UI.
- API key or credential configuration flow.
- Audio level visualization during recording.
- Partial transcription display for providers that support streaming.
- Final transcript history for the current session.
- Secure handling of credentials using Windows-appropriate storage.
- Logging that helps diagnose failures without recording sensitive transcript/audio content by default.

### Could Have

- Local transcription provider integration.
- Multiple language support.
- Custom vocabulary or prompt/context support.
- Push-to-talk mode in addition to toggle mode.
- Per-provider advanced settings.
- Export transcript history.
- Optional automatic insertion into the foreground application.

## Non-Goals

- Cross-platform support.
- Windows 10 support.
- Browser-based application shell.
- Long-term audio archive by default.
- Full meeting recorder features.
- Speaker diarization as an initial requirement.
- Translation as an initial requirement.

## Provider Architecture Requirements

The transcription subsystem should be provider-based.

Each provider should expose a common contract for:

- Provider identity and capability description.
- Required configuration values.
- Credential validation where supported.
- Audio format requirements.
- Batch transcription.
- Streaming transcription if supported.
- Cancellation.
- Error normalization.

The app should not bind core UI workflow directly to one provider's API shape. A local model provider should be possible later without rewriting the HUD, hotkey handling, recording lifecycle, or settings shell.

## Privacy and Security Requirements

- Make it visible when audio is being recorded.
- Do not record silently.
- Avoid storing audio by default after transcription completes.
- Store credentials securely using Windows-appropriate facilities.
- Do not log raw audio, full transcripts, or credentials by default.
- Provide clear errors when credentials or microphone access are missing.
- Prefer explicit user control before sending audio to external services.

## Packaging and Distribution Requirements

- The app should be buildable on Windows 11 with current Microsoft tooling.
- Packaging should be compatible with normal Windows 11 installation expectations.
- Startup integration should work through an appropriate Windows mechanism for the chosen packaging model.
- The repository should document any Windows-side setup needed because agents may be operating from WSL2.

## Harness Engineering Requirements

This repository should support coordinated agent work by maintaining:

- Clear requirements and open questions.
- Incremental task decomposition.
- Git commits representing coherent changes.
- Documentation of build and test commands.
- Testable boundaries for provider logic, hotkey handling, recording lifecycle, and settings.
- A bias toward small, reviewable implementation steps.

## Open Decisions

- Which first transcription provider should be implemented?
- Should the default interaction be toggle recording or push-to-talk?
- What should happen to the final transcript by default: clipboard, active text insertion, HUD display, or a combination?
- Should the initial app be packaged as MSIX from the start, or should packaging come after the first working prototype?
- Which credential storage mechanism should be used for the first provider?
- Should transcript history exist in v1, and if so, should it persist across restarts?
- How should the HUD be positioned and dismissed?
- What is the expected behavior when the configured global hotkey conflicts with another app?
