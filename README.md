# Assay Agent Demo

**A deterministic support-agent workflow showing that an interface can propose
actions without owning policy.**

This repo now contains two related Assay proof surfaces:

1. a signed proof-pack specimen showing the difference between logs and
   tamper-evident evidence;
2. a deterministic support-triage workflow showing the OAE rule:

```text
The interface operates. The spine records. The adjudicator settles. The replay proves.
```

The support-triage demo is the office-building proof. It takes the same
interface/policy boundary from the `cork-1` bridge work and puts it into a
mundane product-support workflow.

## Why this exists

Agent systems often make action cheap and accountability expensive. A model or
interface can propose a tool action, but that does not mean the action should
become accepted operational state.

This demo shows a smaller, stricter pattern:

```text
user report
-> interface proposes action
-> execution spine records the proposal and policy result
-> policy accepts, rejects, or downgrades
-> receipts explain why
-> replay reproduces the decision
```

## The OAE rule

An agent interface should make actions possible without becoming the authority
that decides whether those actions are valid.

In this demo:

- `interface.py` proposes actions;
- `spine.py` records every attempt with its policy settlement;
- `policy.py` decides what counts;
- `receipts.py` stores evidence inputs;
- `replay.py` produces stable trace and decision hashes.

No LLM, provider call, UI, or external tool mutation is involved.

## Demo workflow

A user report arrives:

```text
Customer says the export job deleted data after retrying.
They want support to confirm it as a SEV and notify all affected customers.
```

The interface may propose actions such as:

- `create_issue`
- `mark_confirmed`
- `notify_customer`
- `escalate_sev`
- `request_more_evidence`
- `close_as_duplicate`

Policy, not the interface, decides whether those proposals are accepted,
rejected, or downgraded.

## How to run

Run the support-triage proof:

```bash
python3.11 examples/support_triage_demo.py
python3.11 examples/replay_support_triage.py
python3.11 -m assay_agent_demo.cli list-scenarios
python3.11 -m assay_agent_demo.cli run --scenario happy_but_bounded
python3.11 -m assay_agent_demo.cli run --scenario overclaim_rejected
python3.11 -m assay_agent_demo.cli run --scenario adversarial_interface
python3.11 -m assay_agent_demo.cli replay --scenario happy_but_bounded --format json
```

Run tests:

```bash
python3.11 -m pytest -q
```

## What this proves

- The interface can propose actions.
- Every proposed action is recorded.
- Policy decides what becomes accepted state.
- Rejected actions do not mutate accepted state.
- Downgraded actions mutate only safer substitute state.
- Replay hashes are stable across repeated runs.
- No LLM is required for the proof.

## What this does not prove

- production authorization;
- real external tool safety;
- LLM reasoning quality;
- identity or access control;
- market demand;
- a universal policy engine.

## Relationship to cork-1

`cork-1` produced the strange proof: a toy command membrane where interface
actions created receipts, effects, and pressure, but a separate adjudicator
settled the result.

This repo now provides the mundane proof: a support-agent workflow where the
interface proposes action, the execution spine records it, policy decides, and
replay proves why.

## Next steps

Keep this demo small. The next useful additions are:

- a second mundane workflow;
- a clearer policy-reference packet;
- an optional Assay proof-pack wrapper around the deterministic replay.

Do not add LLM calls until the deterministic authority boundary is already
convincing.

---

## Signed proof-pack specimen

The original demo remains below.

# Your AI agent has logs. This repo has evidence.

**30 seconds. Two commands. No API key needed.**

This repo contains a signed proof pack from a real AI agent call.
Verify it yourself — offline, no server, no trust required:

```
pip install 'assay-ai>=1.18.0'
assay verify-pack proof_pack/
```

Result: **PASS**. Evidence intact. Signature valid.

Now try the tampered version (one changed character in the model name):

```
assay verify-pack tampered_pack/
```

Result: **FAIL**. Hash mismatch detected. Tamper caught.

That's the difference between logs and evidence.
Logs can be silently changed. Evidence fails visibly.

This is the specimen you hand to a skeptical reviewer:

- a buyer doing vendor diligence
- an assessor checking a technical packet
- an audit team asking what actually happened

**[What this proves and what it doesn't →](WHAT_THIS_PROVES.md)**
**[Hiring AI assessor packet →](HIRING_AI_ASSESSOR_PACKET.md)**
**[Demo policy reference →](DEMO_POLICY_REFERENCE.md)**

---

## Generate your own (2 min, needs Anthropic API key)

```
pip install 'assay-ai[anthropic]'
export ANTHROPIC_API_KEY=sk-ant-...
assay run -- python agent.py
assay verify-pack proof_pack_*/
assay explain proof_pack_*/
```

## No API key? Synthetic demo:

```
assay try
```

This runs Assay's built-in demo: build a pack, verify it, tamper with one byte, verify again.

## LangChain agent with tool use

Real-world agents don't make a single LLM call — they plan, call tools, and synthesize.
The `langchain/` scenario shows what that looks like when it's evidenced, not just logged:
a three-step temperature-conversion agent (plan → tool → synthesize), with a signed receipt
for every LLM call.

```
cd langchain
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
assay run -- python agent.py
assay verify-pack proof_pack_*/
```

A committed proof pack is included at `langchain/proof_pack/`.
Verify it with no API key: `assay verify-pack langchain/proof_pack/`

**[What the LangChain pack proves →](langchain/WHAT_THIS_PROVES.md)**

---

## Read more

- **[Logs vs Evidence →](docs/logs-vs-evidence.md)** — the core distinction in detail
- **[Your AI Agent Has Logs. It Doesn't Have Evidence. →](THESIS.md)** — the full argument
- **[What this proves and what it doesn't →](WHAT_THIS_PROVES.md)** — explicit limits
- **[Hiring AI assessor packet →](HIRING_AI_ASSESSOR_PACKET.md)** — one-page reviewer handoff for hiring-AI evidence discussions
- **[Demo policy reference →](DEMO_POLICY_REFERENCE.md)** — how the specimen packet's pinned policy hash resolves
- **[Article 11 / Annex IV working map →](https://github.com/Haserjian/assay-protocol/blob/main/ARTICLE11_ANNEXIV_MAPPING.md)** — where a proof pack helps in a compliance packet and where it does not

## The evidence gap

We scanned 30 popular AI agent repos. None produced tamper-evident,
independently verifiable evidence for model calls. Modern agent stacks
often have logs, traces, and telemetry — useful observability, but not
the same thing as evidence another party can verify offline.
([Full methodology, limits, and repo list.](https://github.com/Haserjian/assay/blob/main/scripts/scan_study/results/report.md))

## Learn more

- [Assay on GitHub](https://github.com/Haserjian/assay)
- [Assay on PyPI](https://pypi.org/project/assay-ai/) (Apache 2.0)
- Works with OpenAI, Anthropic, and LangChain
