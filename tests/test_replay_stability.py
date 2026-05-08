from __future__ import annotations

from dataclasses import replace
import json

import pytest

from assay_agent_demo.domain import AcceptedState
from assay_agent_demo.interface import InterfaceCommand, execute_interface_command
from assay_agent_demo.render import render_json
from assay_agent_demo.replay import BOUNDARY_FLAGS, result_from_spine
from assay_agent_demo.scenarios import list_scenarios, run_scenario, scenario_by_id
from assay_agent_demo.spine import ExecutionSpine


def test_replay_hashes_stable_across_repeated_runs() -> None:
    first = run_scenario("happy_but_bounded")
    second = run_scenario("happy_but_bounded")

    assert first.decision_hash == second.decision_hash
    assert first.trace_hash == second.trace_hash
    assert render_json(first) == render_json(second)


def test_json_output_includes_boundary_flags() -> None:
    data = json.loads(render_json(run_scenario("happy_but_bounded")))

    assert data["boundary_flags"] == {
        "external_mutation": "absent",
        "interface_authority": "absent",
        "llm": "absent",
        "policy_owner": "demo_policy_v0",
    }


def test_module_boundary_flags_are_frozen_before_trace_construction() -> None:
    with pytest.raises(TypeError):
        BOUNDARY_FLAGS["llm"] = "present"


def test_replay_boundary_flags_are_frozen_after_hashing() -> None:
    result = run_scenario("happy_but_bounded")
    original_hash = result.trace_hash

    with pytest.raises(TypeError):
        result.trace.boundary_flags["llm"] = "present"

    assert result.trace_hash == original_hash
    assert json.loads(render_json(result))["boundary_flags"]["llm"] == "absent"


def test_trace_hash_commits_to_receipt_contents_not_just_ids() -> None:
    baseline = run_scenario("happy_but_bounded")
    scenario = scenario_by_id("happy_but_bounded")
    mutated_receipts = tuple(
        replace(receipt, body="same id, changed receipt body")
        if receipt.receipt_id == "customer_report_receipt"
        else receipt
        for receipt in scenario.receipts
    )
    mutated_scenario = replace(scenario, receipts=mutated_receipts)

    assert _run_custom_scenario(mutated_scenario).trace_hash != baseline.trace_hash


def test_trace_exposes_receipt_hash_commitments() -> None:
    result = run_scenario("happy_but_bounded")

    commitments = tuple(item["receipt_id"] for item in result.trace.receipt_hashes)
    assert commitments == (
        "customer_report_receipt",
        "missing_repro_receipt",
        "policy_rule_receipt",
    )
    assert all(item["receipt_hash"] for item in result.trace.receipt_hashes)


def test_all_scenarios_are_deterministic() -> None:
    for scenario_id in list_scenarios():
        first = run_scenario(scenario_id)
        second = run_scenario(scenario_id)
        assert first.to_json() == second.to_json()
        assert first.trace_hash == second.trace_hash


def _run_custom_scenario(scenario):
    spine = ExecutionSpine(
        report=scenario.report,
        receipts=scenario.receipts,
        accepted_state=AcceptedState(),
    )
    for proposal in scenario.proposals:
        spine = execute_interface_command(
            spine,
            InterfaceCommand(
                action_type=proposal["action_type"],
                attached_receipt_ids=tuple(proposal.get("attached_receipt_ids", ())),
                params=dict(proposal.get("params", {})),
            ),
        )
    return result_from_spine(scenario, spine)
