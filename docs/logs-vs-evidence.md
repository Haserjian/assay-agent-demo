# Logs vs Evidence

## The distinction

Logs tell you what the operator says happened.
Evidence lets another party verify it.

| Property | Logs / Traces | Evidence (Proof Pack) |
|----------|--------------|----------------------|
| **Who controls it** | The operator | Cryptographically bound to signer |
| **Can it be silently changed?** | Yes | No — hash mismatch breaks verification |
| **Can a third party verify it?** | Only if they trust the operator's system | Yes — offline, no vendor access needed |
| **What happens if tampered?** | Nothing visible | Verification fails hard: FAIL + specific error |
| **Requires vendor server?** | Usually | No — air-gap compatible |
| **Format** | Vendor-specific (JSON, spans, dashboards) | 5-file signed pack (JSONL + manifest + signature) |

A system can have 100% observability coverage and 0% evidence coverage. Comprehensive tracing, detailed logging, and full telemetry — with none of it signed, tamper-evident, or independently verifiable.

Observability answers: *"What does the system say happened?"*
Evidence answers: *"What can another party verify happened?"*

## The live proof

This repo contains two proof packs from the same real AI agent call:

**`proof_pack/`** — the original, unmodified evidence.

```
assay verify-pack proof_pack/
# → VERIFICATION PASSED
```

**`tampered_pack/`** — one character changed in the model name.

```
assay verify-pack tampered_pack/
# → VERIFICATION FAILED
# E_MANIFEST_TAMPER: Hash mismatch for receipt_pack.jsonl
```

One changed character. Verification breaks. No server needed.

That is the difference between something you can look at and something you can verify.

## Why it matters

**Incident response.** When an agent causes damage, the first question is "what happened?" Logs are the operator's account. A proof pack is independently checkable evidence. If the operator modified the trace after the incident, logs won't tell you. A proof pack will.

**Vendor trust.** If you're evaluating an AI vendor, "we have observability" means "trust our dashboard." A proof pack means "verify it yourself, offline, without our server."

**Internal governance.** Platform and security teams want to know: did the agent use the approved model? Did it follow the expected workflow? Logs say yes. A proof pack lets you check.

**Auditability.** When a regulator, auditor, or customer asks "prove what happened," traces are testimony. A signed, hash-chained pack with offline verification is evidence.

**Multi-party disputes.** When two parties disagree about what an agent did, the party with independently verifiable evidence has a stronger position than the party with editable logs.

## What this does NOT prove

A proof pack is not a universal truth machine. It has specific limits:

- **Not source honesty.** The signer can emit false receipts. Tamper-evidence means the record wasn't changed after signing. It does not mean the signer was honest when creating it. (Same trust model as HTTPS certificates: they prove identity, not honesty.)
- **Not model correctness.** The pack proves a model call happened with specific parameters. It does not prove the model's output was correct, safe, or appropriate.
- **Not completeness.** Only instrumented calls appear in the pack. Uninstrumented actions are invisible.
- **Not timestamp authority.** Timestamps use the local clock unless externally anchored. They prove ordering, not absolute time.
- **Not regulatory compliance.** A proof pack supports audit review. It is not a certification or legal opinion.

These limits are stated explicitly in every proof pack. Evidence that overclaims is worse than no evidence at all.
