"""Backward-compatible launcher for the Nmap Scanning Tool CLI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def main() -> int:
    """Run CLI entrypoint."""
    from nmap_scanning_tool.cli import entrypoint

    return entrypoint()


if __name__ == "__main__":
    raise SystemExit(main())
