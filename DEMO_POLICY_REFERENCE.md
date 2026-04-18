# Demo Policy Reference

This specimen pack pins the following policy hash:

`4791aaa760a131484e3c971c4f9b171ad1ef2f6fb9c2e4858fdad6d8fc8f6c0f`

For this demo, that hash resolves to the current placeholder policy identifier:

`default-policy-v0`

You can reproduce the hash locally:

```bash
python3 - <<'PY'
import hashlib
print(hashlib.sha256(b"default-policy-v0").hexdigest())
PY
```

Expected output:

```text
4791aaa760a131484e3c971c4f9b171ad1ef2f6fb9c2e4858fdad6d8fc8f6c0f
```

This is a demo-only placeholder, not a full customer policy artifact.
In a real hiring-AI evidence packet, replace this with the actual policy file or registry reference that governs the workflow.
