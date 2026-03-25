# Your AI Agent Has Logs. It Doesn't Have Evidence.

Every major agent framework ships with tracing. OpenAI, Anthropic, LangGraph — they all produce logs of what happened. Traces, spans, tool calls, handoffs. It looks like observability. It feels like accountability.

It isn't.

Logs are what the system says about itself. If someone modifies a log entry after the fact, you'd never know. If the system omits an action from its trace, the trace just looks shorter. If a vendor's server goes down, your audit trail goes with it.

That's not evidence. That's testimony.

## What evidence actually means

Evidence, in the sense that matters for AI systems, has three properties that logs don't:

**Signed.** Every record is cryptographically signed by the entity that produced it. The signature binds the content to the signer. If the content changes, the signature breaks.

**Tamper-evident.** Records are hash-chained. Change one byte anywhere in the chain and verification fails. Not "we'll flag it in a dashboard" — fails. Hard. Offline. No server call needed.

**Independently verifiable.** Anyone can check the evidence without trusting the system that produced it. No vendor API key. No network access. No "trust us, we logged it." You run one command and get PASS or FAIL.

That distinction — between vendor-asserted traces and independently verifiable evidence — is the gap almost nobody in the AI agent ecosystem has closed.

## How big is the gap?

We scanned 30 popular open-source AI projects for tamper-evident audit trails on model calls.

**None had one.**

These are good projects — well-built, many with real observability infrastructure. But observability and evidence are different things. A project can have comprehensive tracing, detailed logging, and full telemetry coverage, and still have zero *evidence coverage* — because none of those traces are signed, tamper-evident, or independently verifiable.

This isn't a criticism of those projects. It's a description of the ecosystem. The tooling for evidence simply hasn't existed in the same way that the tooling for tracing does.

Today, most agent stacks can tell you what they logged. Very few can prove what happened.

## What evidence looks like in practice

[Assay](https://github.com/Haserjian/assay) is an open-source toolkit that closes this gap. It wraps AI agent workflows and produces a signed, tamper-evident artifact called a *proof pack* — five files you can verify offline with one command.

Here's what happens when you run a real AI agent call through Assay:

```
pip install 'assay-ai>=1.18.0'
assay verify-pack proof_pack/
# → PASS. Evidence intact. Signature valid.
```

Now change one byte — any byte — and verify again:

```
assay verify-pack tampered_pack/
# → FAIL. Hash mismatch detected.
```

That's the whole point. Logs can be silently changed. Evidence fails visibly.

The proof pack explicitly states what it proves and what it doesn't:

- **Proven:** These API calls happened. The evidence hasn't been modified since signing.
- **Not proven:** That the agent's outputs are correct. That every action was recorded. That the signer was honest. That timestamps are externally anchored.

That honesty — the explicit reliance boundary — is part of the design. Evidence that overclaims is worse than no evidence at all.

## Try it yourself

I built a tiny demo that makes this concrete. Clone it, run two commands, and see the difference between logs and evidence for yourself:

**[assay-agent-demo →](https://github.com/Haserjian/assay-agent-demo)**

No API key needed. The repo contains a pre-generated proof pack you can verify right now.

---

*Assay is open-source (Apache 2.0) and available on [PyPI](https://pypi.org/project/assay-ai/). It works with OpenAI, Anthropic, and LangChain. The scanner, signer, and verifier are all offline-capable.*

*Read the full [Logs vs Evidence](docs/logs-vs-evidence.md) breakdown for the detailed comparison.*
