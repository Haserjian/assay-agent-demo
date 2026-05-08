# The Interface Must Not Own Policy

Agent systems often make action cheap and accountability expensive.

The support-triage demo applies the OAE rule to a normal workflow:

```text
The interface operates. The spine records. The adjudicator settles. The replay proves.
```

By OAE, this demo means Open Agent Execution: a pattern where actions are
proposed through an interface, recorded through an execution spine, checked by
policy, and replayed with receipts.

## The rule

An agent interface should make actions possible without becoming the authority
that decides whether those actions are valid.

In this demo, a support/product agent can propose `create_issue`,
`mark_confirmed`, `notify_customer`, and `escalate_sev`. Those proposals are
recorded, but they do not become accepted operational state until policy
settles them.

## The mundane case

A customer reports that an export retry deleted data. The interface tries to
help: it opens an issue, asks for evidence, and tries to notify customers.

Policy accepts the issue and the evidence request. It downgrades notification
to a draft because the incident is not confirmed.

In the overclaim route, the interface tries to confirm the incident and
escalate it as a SEV with only a customer report. Policy records the attempt and
rejects it.

That is the point. The interface can act, but it cannot authorize itself.

## Why this matters

Most agent systems blur interface, tool use, policy, and mutation. That makes
the product feel smooth while making accountability harder to inspect.

This demo separates the layers:

- the interface proposes;
- the spine records every attempt;
- policy accepts, rejects, or downgrades;
- receipts explain why;
- replay reproduces the decision.

The result is not a full production authorization system. It is a small,
deterministic proof that the authority boundary can exist outside a toy domain.
