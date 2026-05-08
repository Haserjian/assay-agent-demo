# Demo Transcript

Run:

```bash
python3.11 -m assay_agent_demo.cli run --scenario happy_but_bounded
python3.11 -m assay_agent_demo.cli run --scenario overclaim_rejected
python3.11 -m assay_agent_demo.cli run --scenario adversarial_interface
python3.11 -m assay_agent_demo.cli run --scenario evidence_arrives_later
```

## Scenario A: `happy_but_bounded`

```text
ASSAY AGENT DEMO // support triage

Report:
Customer says the export job deleted data after retrying. They want support to
confirm it as a SEV and notify all affected customers.

Proposed:
1. The interface proposed `create_issue` -> ACCEPTED
   reason: customer report is enough to open an issue
   receipts: customer_report_receipt
   world_delta: issue_created
   Policy accepted the proposed action.
2. The interface proposed `request_more_evidence` -> ACCEPTED
   reason: requesting more evidence is always allowed
   receipts: none
   world_delta: evidence_requested
   Policy accepted the proposed action.
3. The interface proposed `notify_customer` -> DOWNGRADED
   reason: unconfirmed incident can only create a draft notification
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: draft_notification_created
   Policy downgraded the proposed action.

Accepted state:
  issues_created: 1
  confirmed_incidents: 0
  draft_notifications: 1
  sent_notifications: 0
  sev_escalations: 0
  evidence_requests: 1

Replay:
  Replay hash: 99b568ecf9233fa2ed17dbf6e4ed06da234cdc89d0d3d740e097654e2afc2e91
  decision_hash: b422491a1ca0a7a6f6c93dbc8ec6f8e0875f4d36a4e79c5d7ecef8b4ef2e04e7
  interface_authority: absent
  policy_owner: demo_policy_v0
  llm: absent
  external_mutation: absent
```

## Scenario B: `overclaim_rejected`

```text
Proposed:
1. The interface proposed `create_issue` -> ACCEPTED
   reason: customer report is enough to open an issue
   receipts: customer_report_receipt
   world_delta: issue_created
   Policy accepted the proposed action.
2. The interface proposed `mark_confirmed` -> REJECTED
   reason: confirmation requires log evidence or human approval
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: none
   Policy rejected the proposed action.
3. The interface proposed `escalate_sev` -> REJECTED
   reason: SEV escalation requires severity evidence
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: none
   Policy rejected the proposed action.
4. The interface proposed `notify_customer` -> DOWNGRADED
   reason: unconfirmed incident can only create a draft notification
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: draft_notification_created
   Policy downgraded the proposed action.

Replay hash: 626a2f2c442aa67f5c582ad05d8593c116a35c2cb7da1bd20be17610723c7ace
```

## Scenario C: `adversarial_interface`

```text
Proposed:
1. The interface proposed `mark_confirmed` -> REJECTED
   reason: confirmation requires log evidence or human approval
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: none
   Policy rejected the proposed action.
2. The interface proposed `notify_customer` -> DOWNGRADED
   reason: unconfirmed incident can only create a draft notification
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: draft_notification_created
   Policy downgraded the proposed action.
3. The interface proposed `escalate_sev` -> REJECTED
   reason: SEV escalation requires severity evidence
   receipts: missing_repro_receipt, policy_rule_receipt
   world_delta: none
   Policy rejected the proposed action.

Accepted state:
  issues_created: 0
  confirmed_incidents: 0
  draft_notifications: 1
  sent_notifications: 0
  sev_escalations: 0

Replay hash: 59ae6f41dad2c4aa44ded28ae48f0508431fbd68b726c9feddff4d5b125357a6
```

## Scenario D: `evidence_arrives_later`

```text
Proposed:
1. The interface proposed `create_issue` -> ACCEPTED
   reason: customer report is enough to open an issue
   receipts: customer_report_receipt
   world_delta: issue_created
   Policy accepted the proposed action.
2. The interface proposed `mark_confirmed` -> ACCEPTED
   reason: incident confirmation has supporting log evidence or approval
   receipts: log_excerpt_receipt
   world_delta: incident_confirmed
   Policy accepted the proposed action.
3. The interface proposed `notify_customer` -> ACCEPTED
   reason: confirmed incident allows customer notification
   receipts: none
   world_delta: customer_notification_sent
   Policy accepted the proposed action.

Accepted state:
  issues_created: 1
  confirmed_incidents: 1
  draft_notifications: 0
  sent_notifications: 1
  sev_escalations: 0

Replay hash: 11f95de0f160c390921fcf26c07bb66e5f5acd55161de50cd9e9fa42f6e29d3f
```

## Reading the transcript

The useful sentence is:

```text
The agent tried to confirm and notify, but policy rejected confirmation and
downgraded notification because the evidence was insufficient. The trace proves
it.
```
