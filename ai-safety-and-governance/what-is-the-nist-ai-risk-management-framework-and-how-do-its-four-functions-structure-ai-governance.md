---
title: "What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?"
id: 205
category: "AI Safety and Governance"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?

**Short answer:** The NIST AI Risk Management Framework (AI RMF 1.0) is a voluntary, non-prescriptive framework organized around four functions — **GOVERN, MAP, MEASURE, MANAGE** — where GOVERN is the culture and accountability layer that runs throughout, and MAP/MEASURE/MANAGE form the operating loop of understanding context, assessing risk quantitatively, and then prioritizing and acting.

## Detail

The AI RMF is voluntary and carries no penalties, which leads people to dismiss it. That is a mistake for two reasons: it increasingly appears as a **contractual requirement** in enterprise procurement, and it gives engineering teams a shared vocabulary for AI risk that maps cleanly onto binding regimes like the EU AI Act.

```text
                    ┌──────────────────────────────────────┐
                    │              GOVERN                  │
                    │  accountability, policy, culture     │
                    │  (cross-cutting -- not a phase)      │
                    └──────────────────────────────────────┘
                        │            │             │
                        ▼            ▼             ▼
                   ┌────────┐   ┌─────────┐   ┌────────┐
                   │  MAP   │──►│ MEASURE │──►│ MANAGE │
                   └────────┘   └─────────┘   └────────┘
                        ▲                          │
                        └──────── iterate ─────────┘
```

### The Four Functions

| Function    | The question it answers                        | Engineering artifacts                                                                             |
| ----------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **GOVERN**  | Who is accountable, and what are our policies? | Named owners, model risk policy, review gates, escalation path, third-party model policy          |
| **MAP**     | What is the context, and what could go wrong?  | Intended use and misuse cases, affected populations, dependency inventory, model cards            |
| **MEASURE** | How bad is it, quantitatively?                 | Eval sets, error/hallucination rates by subgroup, red-team results, drift monitoring, uncertainty |
| **MANAGE**  | What do we do about it, in what order?         | Risk register with priorities, mitigations, guardrails, incident response, decommissioning plan   |

GOVERN is drawn wrapping the others deliberately — it is not step one of four. Standing up evals without a named owner who can block a launch produces measurement that changes nothing.

### The Seven Trustworthiness Characteristics

The framework defines what "trustworthy" decomposes into, which is useful precisely because it forces the trade-offs into the open: valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; and fair with harmful bias managed.

These conflict in practice. Explainability can cost accuracy; privacy-enhancing training costs both accuracy and compute; fairness constraints across subgroups can reduce aggregate performance. The framework's position is that you **negotiate and document** these trade-offs rather than pretending a system maximizes all seven.

### Where It Earns Its Keep

The MEASURE function is the one that changes engineering behavior. It insists that "the model seems good" is not a risk assessment: you need an eval set, a metric, a threshold, and measurement disaggregated across the populations the system affects. Most AI incidents trace back to a risk that was mapped in conversation but never measured.

There is also a companion **Generative AI Profile** (NIST AI 600-1) that instantiates the framework for LLM-specific risks — confabulation, dangerous capability uplift, data privacy, harmful bias, information integrity, and supply chain.

## Example

Turning the four functions into a launch gate rather than a document:

```python
from dataclasses import dataclass, field


@dataclass
class AIRiskRecord:
    """One risk, tracked through the RMF functions. The gate is MEASURE:
    a risk that is mapped but unmeasured cannot be knowingly accepted.
    """
    name: str
    mapped_context: str                  # MAP: who is affected, how it fails
    metric: str | None = None            # MEASURE: what number tells us
    measured_value: float | None = None
    threshold: float | None = None
    mitigations: list[str] = field(default_factory=list)  # MANAGE
    owner: str | None = None             # GOVERN: a person, not a team

    def launch_blocking_gaps(self) -> list[str]:
        gaps = []
        if not self.owner:
            gaps.append("GOVERN: no named accountable owner")
        if self.metric is None or self.measured_value is None:
            gaps.append("MEASURE: risk is described but never quantified")
        elif self.threshold is not None and self.measured_value > self.threshold:
            if not self.mitigations:
                gaps.append("MANAGE: over threshold with no mitigation")
        return gaps


risks = [
    AIRiskRecord(
        name="Hallucinated policy citations in support answers",
        mapped_context="Affects all self-serve customers; wrong refund policy quoted as fact",
        metric="ungrounded_claim_rate", measured_value=0.06, threshold=0.02,
        mitigations=["citation-required prompt", "groundedness check on egress"],
        owner="a.patel",
    ),
    AIRiskRecord(
        name="Disparate answer quality across dialects",
        mapped_context="Non-standard English speakers may get lower-quality answers",
        owner="a.patel",  # mapped, owned -- but never measured
    ),
]

for r in risks:
    print(r.name, "->", r.launch_blocking_gaps() or "clear")
# Hallucinated policy citations in support answers -> clear
# Disparate answer quality across dialects -> ['MEASURE: risk is described but never quantified']
```

## Interview tips

- Get GOVERN's role right. It is cross-cutting, not the first of four sequential steps — describing it as a phase is the fastest way to signal you have only skimmed the framework.
- Say it is voluntary **and** explain why it still matters: enterprise contracts increasingly require it, and it maps onto the EU AI Act's binding obligations, so the work is reusable rather than duplicated.
- Anchor on MEASURE. The framework's real contribution to an engineering org is refusing to let a risk be "handled" without a metric, a threshold, and disaggregated results.
- Be honest that the trustworthiness characteristics trade off against each other. Claiming a system maximizes all seven is the answer of someone who has not shipped one.

## Related Concepts

- [[How does the EU AI Act classify AI systems into risk tiers?]] (`#204`): [How does the EU AI Act classify AI systems into risk tiers?](../ai-safety-and-governance/how-does-the-eu-ai-act-classify-ai-systems-into-risk-tiers.md)
- [[What is hallucination and what are its primary causes?]] (`#93`): [What is hallucination and what are its primary causes?](../ai-safety-and-governance/what-is-hallucination-and-what-are-its-primary-causes.md)
- [[What is model inversion and membership inference, and how do you defend against them?]] (`#201`): [What is model inversion and membership inference, and how do you defend against them?](../ai-safety-and-governance/what-is-model-inversion-and-membership-inference-and-how-do-you-defend-against-them.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
