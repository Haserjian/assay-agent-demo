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

**[What this proves and what it doesn't →](WHAT_THIS_PROVES.md)**

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

## Read more

- **[Logs vs Evidence →](docs/logs-vs-evidence.md)** — the core distinction in detail
- **[Your AI Agent Has Logs. It Doesn't Have Evidence. →](THESIS.md)** — the full argument
- **[What this proves and what it doesn't →](WHAT_THIS_PROVES.md)** — explicit limits

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
