"""Replay trace and hashing for the support-triage demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .domain import ScenarioDefinition
from .policy import POLICY_OWNER
from .receipts import freeze_data, stable_hash
from .spine import ExecutionSpine


BOUNDARY_FLAGS = freeze_data(
    {
        "interface_authority": "absent",
        "policy_owner": POLICY_OWNER,
        "llm": "absent",
        "external_mutation": "absent",
    }
)


@dataclass(frozen=True)
class ReplayTrace:
    trace_id: str
    scenario_id: str
    events: tuple[Any, ...]
    accepted_state: Any
    receipt_hashes: tuple[Any, ...]
    boundary_flags: Mapping[str, str]
    decision_hash: str
    trace_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "events", tuple(self.events))
        object.__setattr__(self, "receipt_hashes", freeze_data(self.receipt_hashes))
        object.__setattr__(self, "boundary_flags", freeze_data(self.boundary_flags))

    def to_json(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "scenario_id": self.scenario_id,
            "events": self.events,
            "accepted_state": self.accepted_state,
            "receipt_hashes": self.receipt_hashes,
            "boundary_flags": self.boundary_flags,
            "decision_hash": self.decision_hash,
            "trace_hash": self.trace_hash,
        }


@dataclass(frozen=True)
class AdjudicationResult:
    scenario_id: str
    report: Any
    receipts: tuple[Any, ...]
    accepted_state: Any
    events: tuple[Any, ...]
    trace: ReplayTrace

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipts", tuple(self.receipts))
        object.__setattr__(self, "events", tuple(self.events))

    @property
    def decision_hash(self) -> str:
        return self.trace.decision_hash

    @property
    def trace_hash(self) -> str:
        return self.trace.trace_hash

    def to_json(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "report": self.report,
            "receipts": self.receipts,
            "events": self.events,
            "accepted_state": self.accepted_state,
            "trace": self.trace,
            "boundary_flags": self.trace.boundary_flags,
        }


DemoRun = AdjudicationResult


def build_trace(
    scenario: ScenarioDefinition,
    spine: ExecutionSpine,
) -> ReplayTrace:
    receipt_hashes = _receipt_commitments(scenario.receipts)
    decision_data = {
        "scenario_id": scenario.scenario_id,
        "accepted_state": spine.accepted_state,
        "events": tuple(
            {
                "action_id": event.proposed_action.action_id,
                "action_type": event.proposed_action.to_json()["action_type"],
                "outcome": event.policy_result,
                "reason": event.reason,
                "used_receipt_ids": event.decision.used_receipt_ids,
                "world_delta": event.world_delta,
            }
            for event in spine.events
        ),
    }
    decision_hash = stable_hash(decision_data)
    trace_data = {
        "scenario_id": scenario.scenario_id,
        "report": scenario.report,
        "receipt_ids": tuple(item.receipt_id for item in scenario.receipts),
        "receipt_hashes": receipt_hashes,
        "events": spine.events,
        "accepted_state": spine.accepted_state,
        "boundary_flags": BOUNDARY_FLAGS,
        "decision_hash": decision_hash,
    }
    trace_hash = stable_hash(trace_data)
    return ReplayTrace(
        trace_id=f"trace_{scenario.scenario_id}",
        scenario_id=scenario.scenario_id,
        events=spine.events,
        accepted_state=spine.accepted_state,
        receipt_hashes=receipt_hashes,
        boundary_flags=dict(BOUNDARY_FLAGS),
        decision_hash=decision_hash,
        trace_hash=trace_hash,
    )


def _receipt_commitments(receipts: tuple[Any, ...]) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "receipt_id": receipt.receipt_id,
            "receipt_hash": stable_hash(receipt),
        }
        for receipt in sorted(receipts, key=lambda item: item.receipt_id)
    )


def result_from_spine(
    scenario: ScenarioDefinition,
    spine: ExecutionSpine,
) -> AdjudicationResult:
    trace = build_trace(scenario, spine)
    return AdjudicationResult(
        scenario_id=scenario.scenario_id,
        report=scenario.report,
        receipts=scenario.receipts,
        accepted_state=spine.accepted_state,
        events=spine.events,
        trace=trace,
    )


__all__ = [
    "BOUNDARY_FLAGS",
    "AdjudicationResult",
    "DemoRun",
    "ReplayTrace",
    "build_trace",
    "result_from_spine",
]
