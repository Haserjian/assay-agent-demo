"""Pure domain objects for the support-triage OAE demo."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from .receipts import DemoEnum, Receipt, freeze_data


class ActionType(DemoEnum):
    CREATE_ISSUE = "create_issue"
    MARK_CONFIRMED = "mark_confirmed"
    NOTIFY_CUSTOMER = "notify_customer"
    ESCALATE_SEV = "escalate_sev"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"
    CLOSE_AS_DUPLICATE = "close_as_duplicate"


class PolicyOutcome(DemoEnum):
    ACCEPTED = "accepted"
    DOWNGRADED = "downgraded"
    REJECTED = "rejected"
    REQUIRES_MORE_EVIDENCE = "requires_more_evidence"


@dataclass(frozen=True)
class UserReport:
    report_id: str
    summary: str
    customer_id: str = "customer_acme"

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id must be non-empty")
        if not self.summary:
            raise ValueError("summary must be non-empty")

    def to_json(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "summary": self.summary,
            "customer_id": self.customer_id,
        }


@dataclass(frozen=True)
class ProposedAction:
    action_id: str
    action_type: ActionType | str
    actor: str
    attached_receipt_ids: tuple[str, ...] = ()
    params: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.action_id:
            raise ValueError("action_id must be non-empty")
        if not self.actor:
            raise ValueError("actor must be non-empty")
        object.__setattr__(self, "attached_receipt_ids", tuple(self.attached_receipt_ids))
        object.__setattr__(self, "params", freeze_data(self.params))

    def to_json(self) -> dict[str, Any]:
        action_type = (
            self.action_type.value
            if isinstance(self.action_type, ActionType)
            else self.action_type
        )
        return {
            "action_id": self.action_id,
            "action_type": action_type,
            "actor": self.actor,
            "attached_receipt_ids": self.attached_receipt_ids,
            "params": self.params,
        }


@dataclass(frozen=True)
class AcceptedState:
    issues_created: tuple[str, ...] = ()
    confirmed_incidents: tuple[str, ...] = ()
    draft_notifications: tuple[str, ...] = ()
    sent_notifications: tuple[str, ...] = ()
    sev_escalations: tuple[str, ...] = ()
    evidence_requests: tuple[str, ...] = ()
    closed_duplicates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "issues_created",
            "confirmed_incidents",
            "draft_notifications",
            "sent_notifications",
            "sev_escalations",
            "evidence_requests",
            "closed_duplicates",
        ):
            object.__setattr__(self, name, tuple(getattr(self, name)))

    def apply_world_delta(self, world_delta: str | None) -> AcceptedState:
        if world_delta is None:
            return self
        if world_delta == "issue_created":
            return replace(self, issues_created=(*self.issues_created, world_delta))
        if world_delta == "incident_confirmed":
            return replace(
                self,
                confirmed_incidents=(*self.confirmed_incidents, world_delta),
            )
        if world_delta == "draft_notification_created":
            return replace(
                self,
                draft_notifications=(*self.draft_notifications, world_delta),
            )
        if world_delta == "customer_notification_sent":
            return replace(
                self,
                sent_notifications=(*self.sent_notifications, world_delta),
            )
        if world_delta == "sev_escalated":
            return replace(
                self,
                sev_escalations=(*self.sev_escalations, world_delta),
            )
        if world_delta == "evidence_requested":
            return replace(
                self,
                evidence_requests=(*self.evidence_requests, world_delta),
            )
        if world_delta == "duplicate_closed":
            return replace(
                self,
                closed_duplicates=(*self.closed_duplicates, world_delta),
            )
        raise ValueError(f"unknown world delta: {world_delta}")

    def to_json(self) -> dict[str, Any]:
        return {
            "issues_created": self.issues_created,
            "confirmed_incidents": self.confirmed_incidents,
            "draft_notifications": self.draft_notifications,
            "sent_notifications": self.sent_notifications,
            "sev_escalations": self.sev_escalations,
            "evidence_requests": self.evidence_requests,
            "closed_duplicates": self.closed_duplicates,
        }


@dataclass(frozen=True)
class ScenarioDefinition:
    scenario_id: str
    report: UserReport
    receipts: tuple[Receipt, ...]
    proposals: tuple[dict[str, Any], ...]
    description: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipts", tuple(self.receipts))
        object.__setattr__(self, "proposals", tuple(freeze_data(self.proposals)))

    def to_json(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "report": self.report,
            "receipts": self.receipts,
            "proposals": self.proposals,
            "description": self.description,
        }


__all__ = [
    "AcceptedState",
    "ActionType",
    "PolicyOutcome",
    "ProposedAction",
    "ScenarioDefinition",
    "UserReport",
]
