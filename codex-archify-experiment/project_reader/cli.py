from __future__ import annotations

import argparse
import signal
from datetime import datetime, timezone
from pathlib import Path

from .simple import run
from .runner import OpenCode


def main(argv=None):
    parser = argparse.ArgumentParser(description="Free-model reports → one composer → project explanation.")
    parser.add_argument("command", choices=("analyze",))
    parser.add_argument("project", type=Path)
    parser.add_argument("--learning", choices=("off", "samuel"), default="off")
    parser.add_argument("--ref", help="Freeze a Git commit instead of the worktree")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scout-timeout", type=int, default=300)
    parser.add_argument("--composer-timeout", type=int, default=900)
    parser.add_argument("--snapshot-only", action="store_true", help="Inspect eligible input; no model calls")
    args = parser.parse_args(argv)
    if args.scout_timeout <= 0 or args.composer_timeout <= 0:
        parser.error("timeouts must be positive")
    args.output = args.output or Path.cwd() / ".archify-project" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    try:
        runner = OpenCode()
        signal.signal(signal.SIGINT, runner.cancel)
        signal.signal(signal.SIGTERM, runner.cancel)
        return run(args, runner)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"archify-project: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
