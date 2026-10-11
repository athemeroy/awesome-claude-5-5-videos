#!/usr/bin/env python3
"""Generate or check the current collection and the frozen research snapshot.

All commands use public files already in the repository. This entry point never
collects live engagement data or extracts media from private source files.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# script, extra arguments, can regenerate from public inputs
# Keep dependencies before the pages/charts that read them.
SNAPSHOT_TASKS = (
    ("generate_cases.py", (), True),
    ("generate_statistics.py", (), True),
    ("refresh_case_engagement.py", ("--date", "2026-09-27", "--require-complete"), False),
    ("generate_domain_style_atlas.py", (), True),
    ("generate_case_thumbnails.py", (), False),
    ("generate_new_case_thumbnails.py", (), False),
    ("check_color_modes.py", (), False),
    ("generate_stat_charts.py", (), True),
    ("generate_intro_charts.py", (), True),
    ("generate_color_charts.py", (), True),
)
COLLECTION_TASKS = (("generate_collection_summary.py", (), True),)


def commands(action: str, scope: str) -> list[list[str]]:
    tasks = ()
    if scope in ("snapshot", "all"):
        tasks += SNAPSHOT_TASKS
    if scope in ("collection", "all"):
        tasks += COLLECTION_TASKS
    result = []
    for script, extra, can_generate in tasks:
        args = [sys.executable, f"scripts/{script}", *extra]
        if (action == "check" or not can_generate) and script != "check_color_modes.py":
            args.append("--check")
        result.append(args)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "check"))
    parser.add_argument(
        "--scope", choices=("collection", "snapshot", "all"), default="collection",
        help="collection (default): source ledgers; snapshot: frozen research; all: both",
    )
    parser.add_argument("--list", action="store_true", help="show commands without running them")
    args = parser.parse_args()
    planned = commands(args.action, args.scope)
    for number, command in enumerate(planned, start=1):
        print(f"[{number}/{len(planned)}] {shlex.join(command)}", flush=True)
        if args.list:
            continue
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            print(f"Stopped: {command[1]} exited with {result.returncode}", file=sys.stderr)
            return result.returncode if result.returncode > 0 else 1
    if not args.list:
        print(f"{args.scope}: {args.action} completed ({len(planned)} commands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
