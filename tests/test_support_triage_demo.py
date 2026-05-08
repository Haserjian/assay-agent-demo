from __future__ import annotations

from pathlib import Path

from assay_agent_demo.render import render_human
from assay_agent_demo.scenarios import list_scenarios, run_scenario


def test_happy_scenario_produces_expected_sequence() -> None:
    result = run_scenario("happy_but_bounded")

    assert tuple(event.policy_result for event in result.events) == (
        "accepted",
        "accepted",
        "downgraded",
    )
    assert tuple(event.world_delta for event in result.events) == (
        "issue_created",
        "evidence_requested",
        "draft_notification_created",
    )
    assert result.accepted_state.issues_created == ("issue_created",)
    assert result.accepted_state.evidence_requests == ("evidence_requested",)
    assert result.accepted_state.draft_notifications == (
        "draft_notification_created",
    )
    assert result.accepted_state.sent_notifications == ()


def test_all_required_scenarios_exist() -> None:
    assert set(list_scenarios()) >= {
        "happy_but_bounded",
        "overclaim_rejected",
        "adversarial_interface",
        "evidence_arrives_later",
    }


def test_human_transcript_contains_policy_and_replay_language() -> None:
    rendered = render_human(run_scenario("overclaim_rejected"))

    assert "The interface proposed" in rendered
    assert "Policy accepted" in rendered
    assert "Policy rejected" in rendered
    assert "Replay hash" in rendered
    assert "receipts: missing_repro_receipt, policy_rule_receipt" in rendered


def test_public_transcript_hashes_match_current_scenarios() -> None:
    transcript = Path("docs/demo-transcript.md").read_text(encoding="utf-8")

    for scenario_id in list_scenarios():
        assert run_scenario(scenario_id).trace_hash in transcript
