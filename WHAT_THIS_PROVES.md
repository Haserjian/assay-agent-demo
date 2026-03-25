# What This Proof Pack Proves (and What It Doesn't)

## What happened

An AI agent made one call to `claude-sonnet-4-20250514`, asking it to explain the three laws of thermodynamics. That call was recorded as a signed receipt.

## What is proven

- **This API call happened.** The receipt records the model, token count, latency, and callsite.
- **The evidence has not been modified since creation.** The Ed25519 signature is valid. The hash chain is intact.
- **The pack was created by a specific signer** at a specific time.

## What is NOT proven

- That the agent's output is correct or safe
- That every action was recorded (only instrumented calls appear)
- That the receipts were honestly created (tamper-evidence is not source honesty)
- That timestamps are externally anchored (local clock was used)

## How to verify

```
pip install assay-ai
assay verify-pack proof_pack/
```

**PASS** means: the evidence is intact and authentic to the signer.
**FAIL** means: something was modified after signing. Do not trust this pack.

## What's in each file

| File | Contents |
|------|----------|
| `receipt_pack.jsonl` | One receipt per line. Each receipt records one agent action. |
| `verify_report.json` | Machine-readable verification result (PASS/FAIL + details). |
| `verify_transcript.md` | Human-readable verification summary. |
| `pack_manifest.json` | Signed envelope. Contains hashes of all files + Ed25519 signature. |
| `pack_signature.sig` | Detached signature for air-gap verification. |

## How is this different from logs?

Logs are what the system says about itself. You trust the system.

A proof pack is signed, hash-chained, and offline-verifiable. If one byte changes, verification fails. No server needed. No vendor trust required.

If someone modifies a trace in your observability tool, you'd never know.
If someone modifies a proof pack, `assay verify-pack` fails.

## FAQ

**"How is this different from OpenTelemetry / LangSmith / Langfuse?"**
Those are observability tools. They show you what happened. They don't sign it, hash-chain it, or let you verify it offline without trusting the vendor.

**"Can I fake the receipts?"**
The signer can emit false receipts. Assay provides tamper-evidence, not source attestation. The pack proves the evidence wasn't modified after signing. It does not prove the signer was honest. This is the same trust model as HTTPS certificates: they prove identity, not honesty.

**"Why offline verification?"**
Evidence that requires the vendor's server to verify is not independent evidence. Offline verification means you can check the evidence in an air-gapped environment with zero network access.
