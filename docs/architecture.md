# Architecture

This demo is intentionally small. Its architecture exists to prove one boundary:
the interface can propose action, but policy decides what becomes accepted
operational state.

## Map

| Concept | File | Role |
|---|---|---|
| chat/interface | `src/assay_agent_demo/interface.py` | creates action proposals without authorizing them |
| execution spine | `src/assay_agent_demo/spine.py` | records every attempted action with its policy settlement |
| policy/adjudication | `src/assay_agent_demo/policy.py` | accepts, rejects, or downgrades proposals |
| receipts | `src/assay_agent_demo/receipts.py` | stores evidence inputs and stable serialization helpers |
| replay | `src/assay_agent_demo/replay.py` | packages events, accepted state, boundary flags, and hashes |
| rendering | `src/assay_agent_demo/render.py` | produces human and JSON output |
| scenarios | `src/assay_agent_demo/scenarios.py` | defines deterministic happy, overclaim, adversarial, and evidence-later routes |
| CLI | `src/assay_agent_demo/cli.py` | runs and replays scenarios |
| examples | `examples/` | public demo entrypoints |

## Data flow

```text
ScenarioDefinition
-> InterfaceCommand
-> ExecutionSpine.propose(...)
-> PolicyDecision
-> SpineEvent
-> AcceptedState
-> ReplayTrace
-> render_human / render_json
```

## Accepted state

Accepted state is explicit:

- `issues_created`
- `confirmed_incidents`
- `draft_notifications`
- `sent_notifications`
- `sev_escalations`
- `evidence_requests`
- `closed_duplicates`

Rejected actions create spine events but do not update accepted state.
Downgraded actions may update safer substitute state, such as
`draft_notification_created` instead of `customer_notification_sent`.

## Boundary flags

Every replay exposes:

```json
{
  "interface_authority": "absent",
  "policy_owner": "demo_policy_v0",
  "llm": "absent",
  "external_mutation": "absent"
}
```

Those flags are not marketing claims. They are constraints of this deterministic
demo.
