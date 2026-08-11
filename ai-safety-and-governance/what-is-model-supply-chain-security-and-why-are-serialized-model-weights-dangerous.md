---
title: "What is model supply chain security and why are serialized model weights dangerous?"
id: 203
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# What is model supply chain security and why are serialized model weights dangerous?

**Short answer:** Model supply chain security covers everything you inherit when you download a model — weights, tokenizer, config, and custom code — and the acute risk is that legacy PyTorch checkpoint files are Python object serializations that execute arbitrary code on load, which is why safetensors, hash pinning, and provenance verification are the baseline controls.

## Detail

Downloading a model feels like downloading data. It is closer to installing a dependency: you are running someone else's code with your service account's permissions.

```text
What you think you fetched          What you actually fetched
────────────────────────            ─────────────────────────
A tensor of weights          ──►    A serialized object graph that runs
                                    code during deserialization
A tokenizer                  ──►    Config that may reference remote code
A model repo                 ──►    Optional custom modules, executed when
                                    trust_remote_code=True
```

### Why the Legacy Checkpoint Format Executes Code

The classic `.bin` / `.pt` checkpoint is produced by Python's object serialization protocol. That format is not a passive data container — it encodes *instructions for reconstructing objects*, including a hook that names a callable to invoke during loading. A crafted checkpoint can therefore run a command the instant you call `torch.load`, before a single inference happens. There is no "safe parse" of the format, because execution is the format's designed behavior.

This is why **safetensors** exists. It stores only tensor data plus a JSON header of shapes and dtypes, with no mechanism to express executable objects. Loading is a bounded parse, and the format is zero-copy, so the safe option is usually also the faster one.

### The Three Distinct Risks

| Risk | Vector | Control |
| --- | --- | --- |
| **Code execution on load** | Legacy serialized checkpoints | Require safetensors; refuse legacy formats from untrusted sources |
| **Remote code execution by design** | `trust_remote_code=True` runs repo-authored Python | Default off; vendor and review the code if genuinely required |
| **Model substitution / tampering** | Typosquatted repo, compromised account, MITM | Pin exact revision hashes, verify checksums, mirror internally |

`trust_remote_code=True` deserves separate emphasis because it is not an exploit — it is a documented feature that runs arbitrary repository code, and it appears throughout tutorials and Stack Overflow answers as a fix for load errors. Enabling it to make an error go away is the single most common way this risk enters a codebase.

### Baseline Controls

1. **Prefer safetensors, and enforce it.** Make it a CI check on model artifacts, not a convention.
2. **Pin the exact revision.** A branch or tag name resolves to whatever the publisher pushed most recently; a commit hash does not move.
3. **Mirror models internally.** Scan and approve once, then serve from your own registry, so production never fetches from the public internet at deploy time.
4. **Load in a sandbox with least privilege.** No cloud credentials, no outbound network, on the process that deserializes an untrusted artifact.
5. **Record provenance in the model registry** — source, revision, checksum, scan date, approver — so you can answer "where did this artifact come from" during an incident.

## Example

A pre-load gate that refuses artifacts failing supply chain policy:

```python
import hashlib
from pathlib import Path

UNSAFE_SUFFIXES = {".bin", ".pt", ".pth", ".ckpt"}  # object-serialization formats


class ModelPolicyError(Exception):
    """Raised when a model artifact fails supply chain policy."""


def verify_model_artifact(path: Path, expected_sha256: str, allow_legacy: bool = False) -> dict:
    """Gate a model file before anything deserializes it.

    Order matters: check the format BEFORE hashing. A matching hash proves the
    bytes are the ones you approved -- it says nothing about whether loading
    those bytes executes code. Both checks are required, and neither implies
    the other.
    """
    if path.suffix in UNSAFE_SUFFIXES and not allow_legacy:
        raise ModelPolicyError(
            f"{path.name}: legacy checkpoint format executes code on load. "
            "Convert to .safetensors or set allow_legacy for a vetted internal artifact."
        )

    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    actual = digest.hexdigest()

    if actual != expected_sha256:
        raise ModelPolicyError(f"{path.name}: checksum mismatch (got {actual[:16]}...)")

    return {"artifact": path.name, "sha256": actual, "format_ok": True}


# Loading is then pinned by revision, never by a mutable branch name:
#   AutoModel.from_pretrained(
#       "org/model",
#       revision="9f2c1b7e...",     # exact commit, not "main"
#       use_safetensors=True,
#       trust_remote_code=False,    # never flip this to silence a load error
#   )
```

## Interview tips

- Say clearly that loading a legacy checkpoint is **code execution, not parsing**. Candidates who describe it as "a risky file format" have not understood that execution is what the format is for.
- Know that safetensors is fast as well as safe — the security argument does not require a performance sacrifice, which is what makes it an easy mandate.
- Flag `trust_remote_code=True` as a review-blocking change. It is a feature, widely copy-pasted, and it grants a third-party repository arbitrary execution in your process.
- Pin revisions, not tags. "We use the official repo" is not an answer when the threat is a compromised or updated publisher account.
- Connect it to [[What is training data poisoning and how do backdoor triggers survive fine-tuning?]]: even a perfectly safe file format cannot tell you whether the weights inside carry a backdoor. Format safety and behavioral integrity are different problems.

## Related Concepts

- [[What is training data poisoning and how do backdoor triggers survive fine-tuning?]] (`#202`): [What is training data poisoning and how do backdoor triggers survive fine-tuning?](../ai-safety-and-governance/what-is-training-data-poisoning-and-how-do-backdoor-triggers-survive-fine-tuning.md)
- [[What is data lineage tracking for RAG documents and enterprise vector stores?]] (`#185`): [What is data lineage tracking for RAG documents and enterprise vector stores?](../ai-safety-and-governance/what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)
- [[How do sandbox execution environments secure Code Interpreter tools?]] (`#140`): [How do sandbox execution environments secure Code Interpreter tools?](../ai-agents-and-mcp/how-do-sandbox-execution-environments-secure-code-interpreter-tools.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
