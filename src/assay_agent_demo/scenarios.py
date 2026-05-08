"""Deterministic support-triage scenarios."""

from __future__ import annotations

from .domain import ActionType, AcceptedState, ScenarioDefinition, UserReport
from .interface import InterfaceCommand, execute_interface_command
from .receipts import Receipt, ReceiptType
from .replay import AdjudicationResult, result_from_spine
from .spine import ExecutionSpine


REPORT = UserReport(
    report_id="report_export_retry_deleted_data",
    summary=(
        "Customer says the export job deleted data after retrying. "
        "They want support to confirm it as a SEV and notify all affected "
        "customers."
    ),
)


BASE_RECEIPTS = (
    Receipt(
        receipt_id="customer_report_receipt",
        receipt_type=ReceiptType.CUSTOMER_REPORT,
        claim="customer reported export retry deleted data",
        body=REPORT.summary,
        source="customer_ticket",
    ),
    Receipt(
        receipt_id="missing_repro_receipt",
        receipt_type=ReceiptType.MISSING_REPRO,
        claim="no internal reproduction exists yet",
        body="Support has not reproduced the deletion.",
        source="support_triage",
    ),
    Receipt(
        receipt_id="policy_rule_receipt",
        receipt_type=ReceiptType.POLICY_RULE,
        claim="confirmation and notification require stronger evidence",
        body="demo_policy_v0",
        source="policy_registry",
    ),
)


LOG_RECEIPT = Receipt(
    receipt_id="log_excerpt_receipt",
    receipt_type=ReceiptType.LOG_EXCERPT,
    claim="export retry produced deletion-like errors in service logs",
    body="2026-05-07 retry worker emitted delete-after-retry warning.",
    source="service_logs",
)


SCENARIOS: dict[str, ScenarioDefinition] = {
    "happy_but_bounded": ScenarioDefinition(
        scenario_id="happy_but_bounded",
        report=REPORT,
        receipts=BASE_RECEIPTS,
        description=(
            "The interface opens an issue, asks for evidence, and tries to "
            "notify customers before confirmation. Policy downgrades the "
            "notification to a draft."
        ),
        proposals=(
            {
                "action_type": ActionType.CREATE_ISSUE.value,
                "attached_receipt_ids": ("customer_report_receipt",),
            },
            {"action_type": ActionType.REQUEST_MORE_EVIDENCE.value},
            {"action_type": ActionType.NOTIFY_CUSTOMER.value},
        ),
    ),
    "overclaim_rejected": ScenarioDefinition(
        scenario_id="overclaim_rejected",
        report=REPORT,
        receipts=BASE_RECEIPTS,
        description=(
            "The interface tries to confirm and escalate with only a customer "
            "report. Policy records the attempt and refuses authority."
        ),
        proposals=(
            {
                "action_type": ActionType.CREATE_ISSUE.value,
                "attached_receipt_ids": ("customer_report_receipt",),
            },
            {
                "action_type": ActionType.MARK_CONFIRMED.value,
                "attached_receipt_ids": ("customer_report_receipt",),
            },
            {"action_type": ActionType.ESCALATE_SEV.value},
            {"action_type": ActionType.NOTIFY_CUSTOMER.value},
        ),
    ),
    "adversarial_interface": ScenarioDefinition(
        scenario_id="adversarial_interface",
        report=REPORT,
        receipts=BASE_RECEIPTS,
        description=(
            "The interface skips issue creation and attempts consequential "
            "state changes without enough receipts."
        ),
        proposals=(
            {"action_type": ActionType.MARK_CONFIRMED.value},
            {"action_type": ActionType.NOTIFY_CUSTOMER.value},
            {"action_type": ActionType.ESCALATE_SEV.value},
        ),
    ),
    "evidence_arrives_later": ScenarioDefinition(
        scenario_id="evidence_arrives_later",
        report=REPORT,
        receipts=(*BASE_RECEIPTS, LOG_RECEIPT),
        description=(
            "The same interface confidence becomes acceptable only after log "
            "evidence arrives."
        ),
        proposals=(
            {
                "action_type": ActionType.CREATE_ISSUE.value,
                "attached_receipt_ids": ("customer_report_receipt",),
            },
            {
                "action_type": ActionType.MARK_CONFIRMED.value,
                "attached_receipt_ids": ("log_excerpt_receipt",),
            },
            {"action_type": ActionType.NOTIFY_CUSTOMER.value},
        ),
    ),
}


def list_scenarios() -> tuple[str, ...]:
    return tuple(sorted(SCENARIOS))


def scenario_by_id(scenario_id: str) -> ScenarioDefinition:
    try:
        return SCENARIOS[scenario_id]
    except KeyError as exc:
        raise KeyError(f"unknown scenario: {scenario_id}") from exc


def run_scenario(scenario_id: str) -> AdjudicationResult:
    scenario = scenario_by_id(scenario_id)
    spine = ExecutionSpine(
        report=scenario.report,
        receipts=scenario.receipts,
        accepted_state=AcceptedState(),
    )
    for proposal in scenario.proposals:
        command = InterfaceCommand(
            action_type=proposal["action_type"],
            attached_receipt_ids=tuple(proposal.get("attached_receipt_ids", ())),
            params=dict(proposal.get("params", {})),
        )
        spine = execute_interface_command(spine, command)
    return result_from_spine(scenario, spine)


__all__ = [
    "BASE_RECEIPTS",
    "LOG_RECEIPT",
    "REPORT",
    "SCENARIOS",
    "list_scenarios",
    "run_scenario",
    "scenario_by_id",
]
