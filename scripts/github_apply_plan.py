#!/usr/bin/env python3
"""Apply a generated harness plan to GitHub.

Dry-run is the default. Use --apply to mutate GitHub.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], apply: bool) -> None:
    printable = " ".join(command)
    if not apply:
        print(f"DRY-RUN: {printable}")
        return
    subprocess.run(command, check=True)


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"required tool not found: {name}")


def upsert_labels(plan: dict[str, Any], apply: bool) -> None:
    for label in plan["labels"]:
        name = label["name"]
        color = label["color"]
        description = label["description"]
        run(["gh", "label", "create", name, "--color", color, "--description", description, "--force"], apply)


def upsert_milestones(plan: dict[str, Any], apply: bool) -> None:
    existing: dict[str, int] = {}
    if apply:
        result = subprocess.run(
            ["gh", "api", "repos/:owner/:repo/milestones?state=all"],
            check=True,
            text=True,
            capture_output=True,
        )
        existing = {item["title"]: item["number"] for item in json.loads(result.stdout)}

    for milestone in plan["milestones"]:
        title = milestone["title"]
        description = milestone["description"]
        payload = json.dumps({"title": title, "description": description})
        if title in existing:
            endpoint = f"repos/:owner/:repo/milestones/{existing[title]}"
            run(["gh", "api", endpoint, "--method", "PATCH", "--input", "-"], apply=False)
            if apply:
                subprocess.run(["gh", "api", endpoint, "--method", "PATCH", "--input", "-"], input=payload.encode("utf-8"), check=True)
            continue

        run(["gh", "api", "repos/:owner/:repo/milestones", "--method", "POST", "--input", "-"], apply=False)
        if apply:
            subprocess.run(
                ["gh", "api", "repos/:owner/:repo/milestones", "--method", "POST", "--input", "-"],
                input=payload.encode("utf-8"),
                check=True,
            )


def existing_harness_issue_numbers() -> dict[str, str]:
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "all", "--limit", "200", "--json", "number,body"],
        check=True,
        text=True,
        capture_output=True,
    )
    issues = json.loads(result.stdout)
    mapping: dict[str, str] = {}
    for issue in issues:
        body = issue.get("body") or ""
        marker = "Harness ID: `"
        if marker not in body:
            continue
        ident = body.split(marker, 1)[1].split("`", 1)[0]
        mapping[ident] = str(issue["number"])
    return mapping


def issue_body_path(output_dir: Path, issue: dict[str, Any]) -> Path:
    matches = sorted((output_dir / "issues").glob(f"{issue['id']}-*.md"))
    if not matches:
        raise FileNotFoundError(f"missing rendered issue body for {issue['id']}")
    return matches[0]


def upsert_issues(plan: dict[str, Any], output_dir: Path, apply: bool) -> None:
    existing = existing_harness_issue_numbers() if apply else {}
    for issue in plan["issues"]:
        body_path = issue_body_path(output_dir, issue)
        labels = ",".join(issue["labels"])
        if issue["id"] in existing:
            number = existing[issue["id"]]
            run(["gh", "issue", "edit", number, "--title", issue["title"], "--body-file", str(body_path), "--add-label", labels], apply)
        else:
            command = [
                "gh",
                "issue",
                "create",
                "--title",
                issue["title"],
                "--body-file",
                str(body_path),
                "--label",
                labels,
                "--milestone",
                issue["milestone"],
            ]
            run(command, apply)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", default=str(ROOT / "generated" / "harness-plan" / "plan.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "generated" / "harness-plan"))
    parser.add_argument("--apply", action="store_true", help="Mutate GitHub. Omit for dry-run.")
    parser.add_argument("--skip-milestones", action="store_true", help="Do not create milestones.")
    args = parser.parse_args()

    require_tool("gh")
    plan_path = Path(args.plan).resolve()
    output_dir = Path(args.output_dir).resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    if not args.apply:
        print("Dry-run mode. No GitHub resources will be changed.")

    upsert_labels(plan, args.apply)
    if not args.skip_milestones:
        upsert_milestones(plan, args.apply)
    upsert_issues(plan, output_dir, args.apply)

    if not args.apply:
        print("Review the dry-run commands. Re-run with --apply to mutate GitHub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
