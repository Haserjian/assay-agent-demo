"""Human and JSON rendering for the support-triage demo."""

from __future__ import annotations

from .receipts import to_canonical_json
from .replay import AdjudicationResult


def render_json(result: AdjudicationResult) -> str:
    return to_canonical_json(result)


def render_human(result: AdjudicationResult) -> str:
    lines = [
        "ASSAY AGENT DEMO // support triage",
        "",
        "Report:",
        result.report.summary,
        "",
        "Proposed:",
    ]
    for index, event in enumerate(result.events, start=1):
        action_type = event.proposed_action.to_json()["action_type"]
        outcome = event.policy_result.upper()
        lines.extend(
            [
                f"{index}. The interface proposed `{action_type}` -> {outcome}",
                f"   reason: {event.reason}",
                "   receipts: "
                + (
                    ", ".join(event.decision.used_receipt_ids)
                    if event.decision.used_receipt_ids
                    else "none"
                ),
                f"   world_delta: {event.world_delta or 'none'}",
            ]
        )
        if event.policy_result == "accepted":
            lines.append("   Policy accepted the proposed action.")
        elif event.policy_result == "downgraded":
            lines.append("   Policy downgraded the proposed action.")
        elif event.policy_result == "rejected":
            lines.append("   Policy rejected the proposed action.")
        else:
            lines.append("   Policy requested more evidence.")
    lines.extend(
        [
            "",
            "Accepted state:",
            f"  issues_created: {len(result.accepted_state.issues_created)}",
            f"  confirmed_incidents: {len(result.accepted_state.confirmed_incidents)}",
            f"  draft_notifications: {len(result.accepted_state.draft_notifications)}",
            f"  sent_notifications: {len(result.accepted_state.sent_notifications)}",
            f"  sev_escalations: {len(result.accepted_state.sev_escalations)}",
            f"  evidence_requests: {len(result.accepted_state.evidence_requests)}",
            "",
            "Replay:",
            f"  Replay hash: {result.trace_hash}",
            f"  decision_hash: {result.decision_hash}",
            "  interface_authority: absent",
            "  policy_owner: demo_policy_v0",
            "  llm: absent",
            "  external_mutation: absent",
        ]
    )
    return "\n".join(lines)


__all__ = ["render_human", "render_json"]
