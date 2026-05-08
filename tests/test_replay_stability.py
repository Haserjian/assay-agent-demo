from __future__ import annotations

import json

import pytest

from assay_agent_demo.render import render_json
from assay_agent_demo.scenarios import list_scenarios, run_scenario


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


def test_replay_boundary_flags_are_frozen_after_hashing() -> None:
    result = run_scenario("happy_but_bounded")
    original_hash = result.trace_hash

    with pytest.raises(TypeError):
        result.trace.boundary_flags["llm"] = "present"

    assert result.trace_hash == original_hash
    assert json.loads(render_json(result))["boundary_flags"]["llm"] == "absent"


def test_all_scenarios_are_deterministic() -> None:
    for scenario_id in list_scenarios():
        first = run_scenario(scenario_id)
        second = run_scenario(scenario_id)
        assert first.to_json() == second.to_json()
        assert first.trace_hash == second.trace_hash
