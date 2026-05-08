from __future__ import annotations

from assay_agent_demo.domain import AcceptedState
from assay_agent_demo.interface import InterfaceCommand, execute_interface_command
from assay_agent_demo.scenarios import BASE_RECEIPTS, REPORT, run_scenario
from assay_agent_demo.spine import ExecutionSpine


def test_adversarial_interface_cannot_mutate_accepted_state() -> None:
    result = run_scenario("adversarial_interface")

    assert tuple(event.policy_result for event in result.events) == (
        "rejected",
        "downgraded",
        "rejected",
    )
    assert result.accepted_state.confirmed_incidents == ()
    assert result.accepted_state.sent_notifications == ()
    assert result.accepted_state.sev_escalations == ()
    assert result.accepted_state.draft_notifications == (
        "draft_notification_created",
    )


def test_invalid_action_is_recorded_but_does_not_mutate_accepted_state() -> None:
    spine = ExecutionSpine(
        report=REPORT,
        receipts=BASE_RECEIPTS,
        accepted_state=AcceptedState(),
    )
    next_spine = execute_interface_command(
        spine,
        InterfaceCommand(action_type="force_execute"),
    )

    assert next_spine is not spine
    assert len(next_spine.events) == 1
    assert next_spine.events[0].policy_result == "rejected"
    assert next_spine.events[0].decision.used_receipt_ids == ("policy_rule_receipt",)
    assert next_spine.events[0].world_delta is None
    assert next_spine.accepted_state == AcceptedState()
