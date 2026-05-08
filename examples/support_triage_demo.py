"""Run the deterministic support-triage demo in human-readable form."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from assay_agent_demo.render import render_human
from assay_agent_demo.scenarios import run_scenario


def main() -> int:
    print(render_human(run_scenario("happy_but_bounded")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
