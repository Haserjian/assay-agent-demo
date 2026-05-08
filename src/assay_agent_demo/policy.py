"""Deterministic policy/adjudication layer for support triage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .domain import AcceptedState, ActionType, PolicyOutcome, ProposedAction
from .receipts import Receipt, ReceiptType


POLICY_OWNER = "demo_policy_v0"


@dataclass(frozen=True)
class PolicyDecision:
    decision_id: str
    action_id: str
    action_type: str
    outcome: PolicyOutcome | str
    reason: str
    used_receipt_ids: tuple[str, ...] = ()
    resulting_action_type: str | None = None
    world_delta: str | None = None

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision_id must be non-empty")
        object.__setattr__(self, "outcome", PolicyOutcome(self.outcome))
        object.__setattr__(self, "used_receipt_ids", tuple(self.used_receipt_ids))

    def to_json(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "action_id": self.action_id,
            "action_type": self.action_type,
            "outcome": self.outcome,
            "reason": self.reason,
            "used_receipt_ids": self.used_receipt_ids,
            "resulting_action_type": self.resulting_action_type,
            "world_delta": self.world_delta,
        }


def adjudicate_action(
    action: ProposedAction,
    receipts: Mapping[str, Receipt],
    state: AcceptedState,
) -> PolicyDecision:
    action_type = action.to_json()["action_type"]
    all_receipts = tuple(sorted(receipts.values(), key=lambda item: item.receipt_id))
    try:
        enum_type = ActionType(action_type)
    except ValueError:
        return _decision(
            action,
            outcome=PolicyOutcome.REJECTED,
            reason=f"unknown action type: {action_type}",
            used_receipts=_policy_basis(all_receipts, ReceiptType.POLICY_RULE),
        )

    attached = tuple(
        receipt
        for receipt_id in action.attached_receipt_ids
        if (receipt := receipts.get(receipt_id)) is not None
    )

    if enum_type is ActionType.CREATE_ISSUE:
        receipt = _first(attached, ReceiptType.CUSTOMER_REPORT)
        if receipt is None:
            return _decision(
                action,
                outcome=PolicyOutcome.REJECTED,
                reason="creating an issue requires a customer report receipt",
                used_receipts=_policy_basis(all_receipts, ReceiptType.POLICY_RULE),
            )
        return _decision(
            action,
            outcome=PolicyOutcome.ACCEPTED,
            reason="customer report is enough to open an issue",
            used_receipts=(receipt.receipt_id,),
            world_delta="issue_created",
        )

    if enum_type is ActionType.MARK_CONFIRMED:
        receipt = _first(attached, ReceiptType.LOG_EXCERPT, ReceiptType.APPROVAL)
        if receipt is None:
            return _decision(
                action,
                outcome=PolicyOutcome.REJECTED,
                reason="confirmation requires log evidence or human approval",
                used_receipts=_policy_basis(
                    all_receipts,
                    ReceiptType.MISSING_REPRO,
                    ReceiptType.POLICY_RULE,
                ),
            )
        return _decision(
            action,
            outcome=PolicyOutcome.ACCEPTED,
            reason="incident confirmation has supporting log evidence or approval",
            used_receipts=(receipt.receipt_id,),
            world_delta="incident_confirmed",
        )

    if enum_type is ActionType.NOTIFY_CUSTOMER:
        if state.confirmed_incidents:
            return _decision(
                action,
                outcome=PolicyOutcome.ACCEPTED,
                reason="confirmed incident allows customer notification",
                world_delta="customer_notification_sent",
            )
        return _decision(
            action,
            outcome=PolicyOutcome.DOWNGRADED,
            reason="unconfirmed incident can only create a draft notification",
            used_receipts=_policy_basis(
                all_receipts,
                ReceiptType.MISSING_REPRO,
                ReceiptType.POLICY_RULE,
            ),
            resulting_action_type="draft_notification",
            world_delta="draft_notification_created",
        )

    if enum_type is ActionType.ESCALATE_SEV:
        receipt = _first(attached, ReceiptType.SEVERITY_EVIDENCE)
        if receipt is None:
            return _decision(
                action,
                outcome=PolicyOutcome.REJECTED,
                reason="SEV escalation requires severity evidence",
                used_receipts=_policy_basis(
                    all_receipts,
                    ReceiptType.MISSING_REPRO,
                    ReceiptType.POLICY_RULE,
                ),
            )
        return _decision(
            action,
            outcome=PolicyOutcome.ACCEPTED,
            reason="severity evidence supports escalation",
            used_receipts=(receipt.receipt_id,),
            world_delta="sev_escalated",
        )

    if enum_type is ActionType.REQUEST_MORE_EVIDENCE:
        return _decision(
            action,
            outcome=PolicyOutcome.ACCEPTED,
            reason="requesting more evidence is always allowed",
            world_delta="evidence_requested",
        )

    if enum_type is ActionType.CLOSE_AS_DUPLICATE:
        receipt = _first(attached, ReceiptType.DUPLICATE_ISSUE)
        if receipt is None:
            return _decision(
                action,
                outcome=PolicyOutcome.REJECTED,
                reason="closing as duplicate requires duplicate issue evidence",
                used_receipts=_policy_basis(all_receipts, ReceiptType.POLICY_RULE),
            )
        return _decision(
            action,
            outcome=PolicyOutcome.ACCEPTED,
            reason="duplicate issue receipt supports closing as duplicate",
            used_receipts=(receipt.receipt_id,),
            world_delta="duplicate_closed",
        )

    raise AssertionError(f"unhandled action type: {enum_type}")


def _decision(
    action: ProposedAction,
    *,
    outcome: PolicyOutcome,
    reason: str,
    used_receipts: tuple[str, ...] = (),
    resulting_action_type: str | None = None,
    world_delta: str | None = None,
) -> PolicyDecision:
    return PolicyDecision(
        decision_id=f"decision_{action.action_id}",
        action_id=action.action_id,
        action_type=action.to_json()["action_type"],
        outcome=outcome,
        reason=reason,
        used_receipt_ids=used_receipts,
        resulting_action_type=resulting_action_type,
        world_delta=world_delta,
    )


def _first(
    receipts: tuple[Receipt, ...],
    *receipt_types: ReceiptType,
) -> Receipt | None:
    for receipt in receipts:
        if receipt.receipt_type in receipt_types:
            return receipt
    return None


def _policy_basis(
    receipts: tuple[Receipt, ...],
    *receipt_types: ReceiptType,
) -> tuple[str, ...]:
    allowed = set(receipt_types)
    return tuple(
        receipt.receipt_id
        for receipt in receipts
        if receipt.receipt_type in allowed
    )


__all__ = ["POLICY_OWNER", "PolicyDecision", "adjudicate_action"]
