# Voice Transcription App Requirements

## Purpose

Build a native Windows 11 voice transcription application using a harness-engineering workflow, where coordinated agents can incrementally design, implement, test, and refine the product.

The application should let a user trigger voice transcription from anywhere in Windows, see clear recording/transcription feedback, and receive transcribed text through a pluggable transcription backend.

## Product Goals

- Feel like a true native Windows 11 application.
- Support global hotkey driven transcription from any active application.
- Default to push-to-talk transcription.
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
- Windows keyboard shortcuts: https://support.microsoft.com/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec

## Core User Experience

### Idle State

- The app can run in the background.
- A system tray icon indicates the app is installed and available.
- The user can open settings or exit the app from the tray icon.
- The app can optionally start automatically when Windows starts.

### Triggering Transcription

- The user can hold a global hotkey to record and release it to stop recording.
- Push-to-talk is the default interaction model.
- The default hotkey is `Ctrl+Win+H`.
- The default hotkey uses the user's requested `Ctrl+Win` modifier chord plus `H` as the trigger key. A modifier-only chord is not sufficient for reliable push-to-talk behavior.
- The hotkey must be configurable in settings.
- The app must validate hotkey conflicts when the user configures the hotkey.
- The app must not accept a hotkey that conflicts with another registered hotkey when that conflict can be detected.
- Toggle recording may be added as an optional mode later.

### Recording HUD

- When transcription is active, a compact HUD appears.
- The HUD should be horizontally centered.
- The HUD should sit in the lower part of the screen, roughly around the bottom 10% area, but inset above the physical bottom edge.
- The HUD should feel like a native Windows 11 surface.
- The HUD should show recording state, audio activity, and transcription progress.
- The HUD should support a clear stop/cancel affordance.
- The HUD should avoid stealing focus unnecessarily from the application the user is dictating into.
- The HUD should handle loading, recording, transcribing, error, and completed states.
- The HUD should dismiss automatically after transcription completes and the resulting text is inserted.

### Transcription Result

- The app records audio and sends it to a configured transcription provider.
- The app should support real-time or near-real-time transcription where the selected provider supports it.
- The app should insert final transcribed text into the active text field by default.
- If active text insertion fails, the app should copy the transcript to the clipboard, keep it in transcript history, and make the fallback visible to the user.
- HUD display may be available as a secondary behavior.
- The app should preserve enough metadata for debugging, such as provider name, duration, and error state, without exposing sensitive audio content unnecessarily.

## Functional Requirements

### Must Have

- Native Windows 11 application shell.
- System tray icon with app status and basic actions.
- Configurable global hotkey.
- Audio recording from the default microphone.
- Recording/transcription HUD.
- OpenAI transcription provider integration.
- Mistral AI transcription provider integration.
- Provider abstraction that allows additional cloud or local providers.
- Settings UI for hotkey, provider configuration, microphone selection if feasible, and startup behavior.
- API key entry in settings for each provider.
- Secure API key storage using Windows-appropriate credential storage.
- Persistent transcript history.
- Full transcript text stored in transcript history by default.
- Clear error handling for missing microphone permissions, unavailable provider credentials, network failures, and provider failures.

### Should Have

- Automatic startup toggle.
- Provider selection UI.
- API key or credential configuration flow.
- Audio level visualization during recording.
- Partial transcription display for providers that support streaming.
- Secure handling of credentials using Windows-appropriate storage.
- Logging that helps diagnose failures without recording sensitive transcript/audio content by default.

### Could Have

- Local transcription provider integration.
- Multiple language support.
- Custom vocabulary or prompt/context support.
- Toggle recording mode in addition to push-to-talk.
- Per-provider advanced settings.
- Export transcript history.
- Clipboard-only mode for workflows where active text insertion is not desirable.

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

The initial cloud providers are:

- OpenAI using the current best available transcription model for the chosen OpenAI transcription path. As of June 8, 2026, prefer `gpt-4o-transcribe` for the Transcription API and `gpt-4o-transcribe-latest` where a latest alias is supported by the Realtime transcription API.
- Mistral AI using the current best available transcription model for the chosen Mistral transcription path. As of June 8, 2026, prefer `voxtral-mini-latest` for `audio/transcriptions`.

Provider model choices should use stable provider aliases such as `latest` where the provider supports them and where product behavior does not require a pinned snapshot. If a provider deprecates or replaces a model, agents should update the provider adapter and documentation based on official provider docs.

References:

- OpenAI speech to text: https://platform.openai.com/docs/guides/speech-to-text
- OpenAI realtime transcription: https://platform.openai.com/docs/guides/realtime-transcription
- Mistral audio transcription: https://docs.mistral.ai/capabilities/audio/

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
- Store provider API keys outside plain-text app configuration, using Windows Credential Manager or an equivalent Windows-native secure credential mechanism.
- Because transcript history stores full transcript text by default, the app must provide a clear way to delete transcript history.
- Persistent transcript history should default to a bounded retention window of 30 days, with settings for shorter retention, longer retention, and manual clearing.
- Do not log raw audio, full transcripts, or credentials by default.
- Provide clear errors when credentials or microphone access are missing.
- Prefer explicit user control before sending audio to external services.

## Packaging and Distribution Requirements

- The app should be buildable on Windows 11 with current Microsoft tooling.
- Packaging should be part of the application from the start.
- The initial packaging target should be MSIX unless a Windows App SDK constraint forces a different documented choice.
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

## Resolved Product Decisions

- Initial transcription providers: OpenAI and Mistral AI.
- Initial OpenAI model direction: latest best OpenAI transcription model, currently `gpt-4o-transcribe` for Transcription API and `gpt-4o-transcribe-latest` where the Realtime transcription API supports that alias.
- Initial Mistral AI model direction: latest best Mistral transcription model, currently `voxtral-mini-latest` for `audio/transcriptions`.
- Default interaction model: push-to-talk.
- Default hotkey: `Ctrl+Win+H`.
- Default transcript delivery: insert into the active text field.
- Fallback transcript delivery: copy to clipboard, retain in transcript history, and notify the user.
- Packaging: include MSIX packaging from the start.
- Credential entry: allow users to paste provider API keys into the app settings UI.
- Credential storage: keep API keys in Windows-native secure credential storage, not plain-text settings.
- Transcript history: include persistent full-text transcript history in v1.
- Transcript retention: default to 30 days, with user controls for retention and manual clearing.
- HUD placement: horizontally centered near the lower portion of the screen, inset above the bottom edge.
- HUD dismissal: automatic after transcription completes and text insertion finishes.
- Hotkey conflicts: flag conflicts during configuration and do not accept conflicting hotkeys where detection is possible.

## Open Decisions

- Should provider selection default to OpenAI, Mistral AI, or whichever provider has valid credentials configured first?
