"""Checkout-time package shim for `python -m assay_agent_demo.cli`.

The implementation lives under `src/assay_agent_demo`. This lightweight shim
lets the demo run from a fresh checkout without requiring an editable install.
"""

from __future__ import annotations

from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "assay_agent_demo"
if _SRC_PACKAGE.is_dir():
    __path__.append(str(_SRC_PACKAGE))  # type: ignore[name-defined]

from .domain import (  # noqa: E402
    AcceptedState,
    ActionType,
    PolicyOutcome,
    ProposedAction,
    ScenarioDefinition,
    UserReport,
)
from .policy import POLICY_OWNER, PolicyDecision, adjudicate_action  # noqa: E402
from .receipts import Receipt, ReceiptType, stable_hash, to_canonical_json  # noqa: E402
from .render import render_human, render_json  # noqa: E402
from .replay import AdjudicationResult, DemoRun, ReplayTrace  # noqa: E402
from .scenarios import list_scenarios, run_scenario, scenario_by_id  # noqa: E402
from .spine import ExecutionSpine, SpineEvent  # noqa: E402

__all__ = [
    "AcceptedState",
    "ActionType",
    "AdjudicationResult",
    "DemoRun",
    "ExecutionSpine",
    "POLICY_OWNER",
    "PolicyDecision",
    "PolicyOutcome",
    "ProposedAction",
    "Receipt",
    "ReceiptType",
    "ReplayTrace",
    "ScenarioDefinition",
    "SpineEvent",
    "UserReport",
    "adjudicate_action",
    "list_scenarios",
    "render_human",
    "render_json",
    "run_scenario",
    "scenario_by_id",
    "stable_hash",
    "to_canonical_json",
]
