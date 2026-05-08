from __future__ import annotations

from assay_agent_demo.domain import ActionType
from assay_agent_demo.scenarios import run_scenario


def test_overclaim_route_rejects_confirmation_and_sev() -> None:
    result = run_scenario("overclaim_rejected")
    decisions = {
        event.proposed_action.to_json()["action_type"]: event.decision
        for event in result.events
    }

    assert decisions[ActionType.MARK_CONFIRMED.value].outcome == "rejected"
    assert decisions[ActionType.MARK_CONFIRMED.value].reason == (
        "confirmation requires log evidence or human approval"
    )
    assert decisions[ActionType.MARK_CONFIRMED.value].used_receipt_ids == (
        "missing_repro_receipt",
        "policy_rule_receipt",
    )
    assert decisions[ActionType.ESCALATE_SEV.value].outcome == "rejected"
    assert decisions[ActionType.ESCALATE_SEV.value].used_receipt_ids == (
        "missing_repro_receipt",
        "policy_rule_receipt",
    )
    assert result.accepted_state.confirmed_incidents == ()
    assert result.accepted_state.sev_escalations == ()


def test_notify_customer_is_downgraded_without_confirmed_incident() -> None:
    result = run_scenario("happy_but_bounded")
    notify = result.events[-1]

    assert notify.proposed_action.to_json()["action_type"] == "notify_customer"
    assert notify.policy_result == "downgraded"
    assert notify.decision.used_receipt_ids == (
        "missing_repro_receipt",
        "policy_rule_receipt",
    )
    assert notify.world_delta == "draft_notification_created"
    assert result.accepted_state.sent_notifications == ()


def test_evidence_arriving_later_changes_policy_outcome() -> None:
    result = run_scenario("evidence_arrives_later")

    assert tuple(event.policy_result for event in result.events) == (
        "accepted",
        "accepted",
        "accepted",
    )
    assert result.events[1].decision.used_receipt_ids == ("log_excerpt_receipt",)
    assert result.accepted_state.confirmed_incidents == ("incident_confirmed",)
    assert result.accepted_state.sent_notifications == (
        "customer_notification_sent",
    )
