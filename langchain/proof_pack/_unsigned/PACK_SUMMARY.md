# Proof Pack Summary

**Pack ID:** `pack_20260331T003634_8cf4105f`
**Run ID:** `trace_20260331T003626_d72d69ae`
**Signed by:** `assay-local`

## Verdicts

| Check | Result |
|-------|--------|
| Integrity | **PASS** |
| Claims | **NONE** |

## What Happened

- **2 receipts** recorded: 2 model_call
- **Providers:** anthropic
- **Models:** claude-sonnet-4-20250514
- **Time window:** 2026-03-31T00:36:31.150931+00:00 to 2026-03-31T00:36:34.527183+00:00

## Integrity Check

All file hashes match. The Ed25519 signature is valid.
This evidence has not been tampered with since creation.

## Claim Checks

No claims were declared for this pack.

## What This Proves

- The recorded evidence is authentic (signed, hash-verified)

## What This Does NOT Prove

- That every action was recorded (only recorded actions are in the pack)
- That model outputs are correct or safe
- That receipts were honestly created (tamper-evidence, not source attestation)
- That timestamps are externally anchored (local clock was used)
- That the signer key was not compromised

## Verify Independently

```bash
python3 -m pip install assay-ai && assay verify-pack .assay_pack_staging_ekl1h1f1
```
