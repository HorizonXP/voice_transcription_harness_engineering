#!/usr/bin/env python3
"""Small tmux orchestration helper for harness workers."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class Worker:
    name: str
    command: str
    role: str


WORKERS = [
    Worker("worker-codex-01", "codex", "Codex implementation worker"),
    Worker("worker-codex-review-01", "codex", "Codex reviewer"),
    Worker("worker-claude-01", "claude", "Claude Code UI/design worker"),
    Worker("worker-claude-review-01", "claude", "Claude Code reviewer"),
]


def require_tool(name: str) -> bool:
    return shutil.which(name) is not None


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=True)


def session_exists(name: str) -> bool:
    return run(["tmux", "has-session", "-t", name]).returncode == 0


def start_worker(worker: Worker) -> None:
    if not require_tool(worker.command):
        print(f"SKIP {worker.name}: missing {worker.command}")
        return
    if session_exists(worker.name):
        print(f"EXISTS {worker.name}")
        return
    result = run(["tmux", "new-session", "-d", "-s", worker.name, worker.command])
    if result.returncode == 0:
        print(f"STARTED {worker.name}: {worker.role}")
    else:
        print(f"FAILED {worker.name}: {result.stderr.strip()}")


def status() -> None:
    if not require_tool("tmux"):
        print("tmux not found")
        return
    result = run(["tmux", "list-sessions", "-F", "#{session_name}"])
    sessions = set(result.stdout.splitlines()) if result.returncode == 0 else set()
    for worker in WORKERS:
        state = "running" if worker.name in sessions else "stopped"
        tool_state = "available" if require_tool(worker.command) else "missing"
        print(f"{worker.name}\t{state}\t{worker.command}:{tool_state}\t{worker.role}")


def send_assignment(session: str, issue: str, branch: str, prompt: str) -> None:
    message = f"""You are assigned harness issue {issue}.

Branch: {branch}

{prompt}

End with:
HARNESS_STATUS: complete|blocked|needs_review
BRANCH: {branch}
PR: <url-or-none>
SUMMARY: <one line>
"""
    subprocess.run(["tmux", "send-keys", "-t", session, message, "Enter"], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show worker session status")
    subparsers.add_parser("start", help="Start default worker sessions")

    assign = subparsers.add_parser("assign", help="Send an assignment prompt to a worker session")
    assign.add_argument("--session", required=True)
    assign.add_argument("--issue", required=True)
    assign.add_argument("--branch", required=True)
    assign.add_argument("--prompt", required=True)

    args = parser.parse_args()
    if args.command == "status":
        status()
    elif args.command == "start":
        if not require_tool("tmux"):
            raise SystemExit("tmux not found")
        for worker in WORKERS:
            start_worker(worker)
    elif args.command == "assign":
        send_assignment(args.session, args.issue, args.branch, args.prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
