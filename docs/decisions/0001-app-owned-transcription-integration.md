# ADR 0001: App-Owned Transcription Integration

## Status

Accepted

## Context

Windows 11 includes built-in voice typing, but the project does not currently assume a public extension point that allows a third-party app to replace or augment Windows' built-in transcription provider.

The product still needs to work across Windows applications, feel native, and let users choose between transcription providers such as OpenAI, Mistral AI, and future local models.

## Decision

Build the product as a native Windows 11 app that owns the transcription workflow end to end:

- The app registers and handles the global push-to-talk hotkey.
- The app captures microphone audio.
- The app shows its own recording/transcription HUD.
- The app routes audio through an internal provider abstraction.
- OpenAI, Mistral AI, and future local models are app-level providers, not Windows subsystem providers.
- Windows sees one installed app, not separate OpenAI or Mistral integrations.
- The app inserts the resulting transcript into the active text target by default.

The first implementation should not attempt to plug OpenAI, Mistral AI, or any other provider directly into Windows voice typing, Text Services Framework, or an IME.

## Consequences

- The app can ship incrementally without depending on deep Windows text-service integration.
- Provider switching remains under the app's settings and credential model.
- Recording, provider selection, transcript history, HUD behavior, and insertion behavior stay testable as app-owned components.
- The insertion mechanism must be abstracted so a future Text Services Framework or IME-based integration can be evaluated without rewriting the recording or provider layers.
- Windows voice typing remains separate from this app.

## Future Considerations

A later research track may evaluate deeper Windows text input integration through Text Services Framework or a custom IME. That work should be treated as a separate architectural decision because it changes packaging, signing, security, and implementation complexity.
