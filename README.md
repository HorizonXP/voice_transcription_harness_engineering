# Voice Transcription Harness Engineering

This repository demonstrates harness engineering by coordinating agents to build a Windows 11 voice transcription app incrementally.

The repository starts intentionally small so the harness, task structure, and agent workflow can evolve alongside the application.

## Harness

- Requirements: [docs/requirements.md](docs/requirements.md)
- Harness objective: [docs/harness/objective.md](docs/harness/objective.md)
- Harness architecture: [docs/harness/architecture.md](docs/harness/architecture.md)
- Harness quickstart: [docs/harness/quickstart.md](docs/harness/quickstart.md)
- Generated dry-run plan: [generated/harness-plan/README.md](generated/harness-plan/README.md)

Generate and validate the dry-run plan:

```sh
python3 scripts/harness_plan.py generate --requirements docs/requirements.md --output generated/harness-plan
python3 scripts/harness_plan.py validate --plan generated/harness-plan/plan.json
```
