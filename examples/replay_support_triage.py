"""Replay all deterministic support-triage scenarios as canonical JSON."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from assay_agent_demo.receipts import to_canonical_json
from assay_agent_demo.scenarios import list_scenarios, run_scenario


def replay_all() -> dict[str, object]:
    return {
        "artifact_id": "assay_agent_demo_support_triage_replay_v0",
        "scenarios": {
            scenario_id: run_scenario(scenario_id)
            for scenario_id in list_scenarios()
        },
    }


def main() -> int:
    print(to_canonical_json(replay_all()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
