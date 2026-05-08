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
  Replay hash: fb06eee5f96be3ad6e4b0537c904a33281c7239deb949aa7bb8ad7ff40b0dd71
  decision_hash: a6b73e443694721a578d757f4c47a5be4d7b38e099a1db17e2205475985fbfcb
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

Replay hash: 807dba449ab808e51877a7aabcca1108f1efc53e11b030c6100b316bc0e7f671
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

Replay hash: e76007002065b5c538b6a296c146054797f17ab1355dea50f8a513c404c30fee
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

Replay hash: 8a9da8712a636a1a44ab6613966419aa0cf8eb9fd7f7e6467312058fc7980553
```

## Reading the transcript

The useful sentence is:

```text
The agent tried to confirm and notify, but policy rejected confirmation and
downgraded notification because the evidence was insufficient. The trace proves
it.
```
