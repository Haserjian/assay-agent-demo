# What This Proves

This demo proves a narrow OAE/Assay pattern in a mundane support-agent workflow.

## Proves

- The interface can propose actions without owning policy.
- Every proposed action is recorded in the execution spine.
- Policy decides whether a proposed action is accepted, rejected, or downgraded.
- Rejected actions do not mutate accepted state.
- Downgraded actions mutate only safer substitute state.
- Policy and missing-evidence receipts explain why stronger actions are blocked.
- Replay hashes are stable across repeated runs.
- No LLM is required to demonstrate the authority boundary.

## Does Not Prove

- production authorization;
- real external tool safety;
- LLM reasoning;
- user identity or permissions;
- external integrations;
- market demand;
- a universal policy engine;
- that every real support workflow can use these exact rules.

## The useful sentence

A product or engineering reader should be able to say:

```text
The agent tried to confirm and notify, but policy rejected confirmation and
downgraded notification because the evidence was insufficient. The trace proves
it.
```
