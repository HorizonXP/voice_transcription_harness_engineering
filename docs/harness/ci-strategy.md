# CI Strategy

## Goals

CI should be fast, economical, reliable, and easy for both humans and agents to read.

The harness CI starts by validating repository artifacts. Application CI should be expanded when the native Windows app skeleton exists.

## Current Harness Checks

- Validate generated harness plan JSON.
- Validate generated issue markdown exists for every issue.
- Validate GitHub labels are unique.
- Validate dependencies reference existing issues.
- Validate Python scripts compile.

## Future Windows App Checks

Based on current Microsoft guidance for Windows App SDK and WinUI 3 testing, use:

- Unit tests for non-UI logic where code does not depend on `Microsoft.UI.Xaml`.
- WinUI Unit Test App or equivalent Windows App SDK-compatible test project for XAML-dependent behavior.
- Targeted smoke tests on `windows-latest` or a pinned Windows runner.
- Packaging validation for MSIX once the app skeleton exists.
- UI automation only for high-value flows because Windows UI automation can be slower and more brittle than unit-level checks.

References:

- Microsoft WinUI 3 testing: https://learn.microsoft.com/windows/apps/winui/winui3/testing/
- GitHub hosted runners: https://docs.github.com/actions/reference/github-hosted-runners-reference

## Machine-Readable Failure Summary

CI should produce `artifacts/ci-summary.json` with this shape:

```json
{
  "status": "failed",
  "failed_checks": [
    {
      "name": "validate-harness-plan",
      "summary": "Issue VT-001 depends on missing issue VT-000.",
      "files": ["generated/harness-plan/plan.json"],
      "suggested_owner": "agent:codex"
    }
  ]
}
```

Agents should read the summary artifact first, then inspect detailed logs only when necessary.
