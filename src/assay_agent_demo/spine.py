"""Execution spine: record attempts with policy settlement."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from .domain import AcceptedState, ProposedAction, UserReport
from .policy import PolicyDecision, adjudicate_action
from .receipts import Receipt, stable_hash


@dataclass(frozen=True)
class SpineEvent:
    event_id: str
    sequence: int
    actor: str
    proposed_action: ProposedAction
    attached_receipt_ids: tuple[str, ...]
    policy_result: str
    reason: str
    world_delta: str | None
    decision: PolicyDecision
    accepted_state_hash_after: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "attached_receipt_ids", tuple(self.attached_receipt_ids))

    def to_json(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "sequence": self.sequence,
            "actor": self.actor,
            "proposed_action": self.proposed_action,
            "attached_receipt_ids": self.attached_receipt_ids,
            "policy_result": self.policy_result,
            "reason": self.reason,
            "world_delta": self.world_delta,
            "decision": self.decision,
            "accepted_state_hash_after": self.accepted_state_hash_after,
        }


@dataclass(frozen=True)
class ExecutionSpine:
    report: UserReport
    receipts: tuple[Receipt, ...]
    accepted_state: AcceptedState = AcceptedState()
    events: tuple[SpineEvent, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "receipts",
            tuple(sorted(self.receipts, key=lambda item: item.receipt_id)),
        )
        object.__setattr__(self, "events", tuple(self.events))

    @property
    def receipt_map(self) -> Mapping[str, Receipt]:
        return {item.receipt_id: item for item in self.receipts}

    def next_action_id(self, action_type: str) -> str:
        return f"action_{len(self.events) + 1:03d}_{action_type}"

    def propose(
        self,
        *,
        action_type: str,
        actor: str = "support_agent_interface",
        attached_receipt_ids: tuple[str, ...] = (),
        params: dict[str, Any] | None = None,
    ) -> ExecutionSpine:
        action = ProposedAction(
            action_id=self.next_action_id(action_type),
            action_type=action_type,
            actor=actor,
            attached_receipt_ids=attached_receipt_ids,
            params={} if params is None else params,
        )
        decision = adjudicate_action(action, self.receipt_map, self.accepted_state)
        next_state = self.accepted_state.apply_world_delta(decision.world_delta)
        event = SpineEvent(
            event_id=f"event_{len(self.events) + 1:03d}_{action_type}",
            sequence=len(self.events) + 1,
            actor=actor,
            proposed_action=action,
            attached_receipt_ids=attached_receipt_ids,
            policy_result=decision.outcome.value,
            reason=decision.reason,
            world_delta=decision.world_delta,
            decision=decision,
            accepted_state_hash_after=stable_hash(next_state),
        )
        return replace(
            self,
            accepted_state=next_state,
            events=(*self.events, event),
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "report": self.report,
            "receipt_ids": tuple(item.receipt_id for item in self.receipts),
            "accepted_state": self.accepted_state,
            "events": self.events,
            "accepted_state_hash": stable_hash(self.accepted_state),
        }


__all__ = ["ExecutionSpine", "SpineEvent"]
