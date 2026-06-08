# Greptile Review Loop

## Purpose

Greptile is an automated PR reviewer. The harness treats Greptile findings as first-class review work.

## Flow

1. Open a PR.
2. Wait for Greptile review to appear.
3. Collect review comments and inline threads.
4. Assign findings to the original implementer unless the fix is better suited to a reviewer or CI fixer.
5. Push a fix commit.
6. Reply to each Greptile thread with:
   - Fix commit SHA.
   - What changed.
   - Why the finding is resolved.
   - Test command or CI check covering the fix.
7. Resolve the thread when permissions and GitHub API support allow it.

## GitHub Commands

Use GitHub CLI first:

```sh
gh pr view <number> --json reviews,comments,reviewDecision,statusCheckRollup
gh api graphql -f query=@query.graphql
```

Inline review thread resolution may require GraphQL API calls and repository permissions. If resolution fails, leave a clear reply and mark the issue/PR with `review:needs-human`.

## Agent Instructions

Agents fixing Greptile findings should begin from the review comments, not from a speculative reread of the whole codebase. Full-code inspection is appropriate only when the finding points to a broader design issue.
