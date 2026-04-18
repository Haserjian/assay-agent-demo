# Hiring AI Evidence Packet For Third-Party Review

**Assay gives hiring-AI vendors a signed technical evidence packet a third-party assessor can verify offline, to support AI Act / NYC AEDT / EEOC documentation.**

Audience: third-party assessor reviewing a hiring-AI vendor's technical evidence packet.

## Workflow

- A hiring-related AI workflow runs and produces an output.
- The run is bound to a specific signer and a pinned `policy_hash`.
- Assay emits a signed proof pack.
- The assessor verifies the pack offline without calling the vendor's server.

## Evidence Included In This Specimen

- `proof_pack/pack_manifest.json`
  - `pack_id`
  - `attestation.run_id`
  - `attestation.policy_hash`
  - `attestation.timestamp_start`
  - `attestation.timestamp_end`
  - `attestation.n_receipts`
  - `attestation.time_authority`
  - `signer_id`
  - `signer_pubkey`
  - per-file SHA-256 hashes
- `proof_pack/receipt_pack.jsonl`
  - timestamp
  - callsite
  - provider / model identifier
  - token and latency metadata
- `proof_pack/verify_report.json`
  - pass / fail result
  - receipt count
  - verifier version
- `proof_pack/verify_transcript.md`
  - human-readable verification summary

## What An Assessor Can Verify Offline In 2 Minutes

1. **Signature validity**: the pack signature verifies against the included public key.
2. **Content integrity**: file hashes in `pack_manifest.json` still match the receipt bundle and verification artifacts.
3. **Policy reference resolves**: the same `policy_hash` appears in the signed attestation and verifier transcript, and the demo reference note shows how that hash resolves for this specimen.

For this specimen, see [DEMO_POLICY_REFERENCE.md](DEMO_POLICY_REFERENCE.md).
In a customer packet, replace the placeholder with the underlying policy artifact or policy registry reference.

## Verify Now

```bash
pip install 'assay-ai>=1.18.0'
assay verify-pack proof_pack/
```

Expected result: `PASS` with a valid signature, `receipt_count = 1`, and no integrity errors.

## Compliance Boundary

This packet is supporting technical evidence, not the full hiring-AI documentation package.
It does **not** by itself cover bias testing, dataset provenance, model evaluation, human-oversight design, or legal analysis of AI Act / NYC AEDT / EEOC obligations.
It is strongest when attached as a verifiable appendix inside a wider assessor or procurement workflow.
