"""Deterministic support-agent OAE proof demo."""

from .domain import (
    AcceptedState,
    ActionType,
    PolicyOutcome,
    ProposedAction,
    ScenarioDefinition,
    UserReport,
)
from .policy import POLICY_OWNER, PolicyDecision, adjudicate_action
from .receipts import Receipt, ReceiptType, stable_hash, to_canonical_json
from .render import render_human, render_json
from .replay import AdjudicationResult, DemoRun, ReplayTrace
from .scenarios import list_scenarios, run_scenario, scenario_by_id
from .spine import ExecutionSpine, SpineEvent

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
