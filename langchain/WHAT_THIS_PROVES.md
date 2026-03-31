# What This Proof Pack Proves (and What It Doesn't)

## What happened

A LangChain agent answered a two-part temperature conversion question.
It made three LLM calls:
1. Initial reasoning — deciding which tools to use and in what order
2. Tool invocation — calling `convert_celsius_to_fahrenheit` and `convert_fahrenheit_to_celsius`
3. Final synthesis — combining tool results into a natural-language answer

Each LLM call produced a signed receipt via `AssayCallbackHandler`.

## What is proven

- **These LLM calls happened.** Each receipt records the model, provider, token count,
  latency, and a hash of the prompt and response.
- **The evidence has not been modified since creation.** The Ed25519 signature is valid.
  The hash chain is intact.
- **The multi-step reasoning chain is receipted.** Not just the final answer — every
  step where the model was called is in the pack.

## What is NOT proven

- That the agent's reasoning was correct or safe
- That every LangChain event was captured (only LLM calls via `AssayCallbackHandler`
  are receipted; tool executions are plain Python)
- That the receipts were honestly created (tamper-evidence is not source honesty)
- That the signing key was held by an authorized signer — at T0, any holder of a valid
  key could produce this pack; signer authority requires a higher trust tier

## How to verify

```
pip install 'assay-ai>=1.20.0'
assay verify-pack proof_pack/
```

**PASS** means: the evidence is structurally intact and authentic to the signer.
**FAIL** means: something was modified after signing. Do not trust this pack.

## How to generate your own

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
assay run -- python agent.py
assay verify-pack proof_pack_*/
assay explain proof_pack_*/
```

## Why this matters

Logs record what an AI system reported. Receipts record what was sent and received,
in a form a third party can verify without accessing your servers.

A multi-step agent run with tool use is the pattern most companies are building.
This proof pack shows what that pattern looks like when it's evidenced, not just logged.
