---
title: "How does the EU AI Act classify AI systems into risk tiers?"
id: 204
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How does the EU AI Act classify AI systems into risk tiers?

**Short answer:** The EU AI Act (Regulation (EU) 2024/1689) sorts systems into four tiers by intended purpose rather than by technology: prohibited practices (Article 5), high-risk systems (Article 6 plus Annex III), limited-risk systems carrying transparency duties (Article 50), and everything else at minimal risk, with a separate obligation track for general-purpose AI models.

## Detail

The classification hinges on **what the system is used for**, not how it was built. The same model can sit in three different tiers across three products: a résumé summarizer used in hiring is high-risk, the same model powering a marketing assistant is minimal-risk, and the same model inferring candidates' emotions in an interview is prohibited.

```text
┌─ Prohibited (Art. 5) ──────── social scoring, untargeted face scraping,
│                               emotion inference at work/school, most
│                               real-time remote biometric ID in public
│                               ──► cannot be placed on the EU market
│
├─ High-risk (Art. 6 + Annex III) ── employment, credit, education access,
│                               essential services, law enforcement, biometrics,
│                               critical infrastructure, plus AI as a safety
│                               component of a regulated product
│                               ──► conformity assessment, risk management,
│                                   data governance, logging, human oversight,
│                                   registration, post-market monitoring
│
├─ Limited-risk (Art. 50) ───── chatbots, emotion/biometric categorisation,
│                               synthetic media ──► disclosure duties
│
└─ Minimal-risk ─────────────── everything else ──► no specific obligations
```

### Your Role Determines Your Obligations

The tier sets _which_ rules apply; your role sets _whose_ they are. **Providers** (who develop and place a system on the market, or rebrand someone else's) carry the heavy compliance burden. **Deployers** (who use a system in a professional capacity) carry a lighter but real set — human oversight, using it per instructions, monitoring, and in some cases a fundamental rights impact assessment.

The trap: a deployer who puts their own name on a high-risk system, or substantially modifies it, or repurposes a non-high-risk system into a high-risk use, **becomes a provider** and inherits the full obligation set. Building a hiring feature on a vendor's API does not keep you a deployer.

### High-Risk Obligations, Concretely

For an Annex III system, the engineering-visible requirements include a risk management system across the lifecycle (Art. 9), data governance with attention to bias in training and test sets (Art. 10), technical documentation (Art. 11 / Annex IV), automatic event logging with traceability (Art. 12), transparency to deployers (Art. 13), meaningful human oversight (Art. 14), and accuracy/robustness/cybersecurity appropriate to purpose (Art. 15) — then conformity assessment, an EU declaration of conformity, CE marking, and registration in the EU database.

There is a **narrow filter in Article 6(3)**: an Annex III system may escape high-risk status if it performs only a narrow procedural task, improves a prior human activity, detects decision patterns without replacing human judgement, or is purely preparatory. Claiming it requires documented assessment and registration — it is not a self-declared exemption, and profiling of natural persons never qualifies.

### General-Purpose AI Models

GPAI models sit on a parallel track: documentation, a copyright policy, and a public summary of training content. Models deemed to carry **systemic risk** take on additional evaluation, adversarial testing, incident reporting, and cybersecurity obligations.

## Example

A triage helper that produces the questions a compliance review must answer — never the verdict:

```python
ANNEX_III_DOMAINS = {
    "biometrics", "critical_infrastructure", "education", "employment",
    "essential_services", "law_enforcement", "migration", "justice",
}
PROHIBITED_PRACTICES = {
    "social_scoring", "emotion_inference_workplace", "emotion_inference_education",
    "untargeted_face_scraping", "realtime_remote_biometric_id_public",
}


def triage_eu_ai_act(use_case: dict) -> dict:
    """Route a use case to a tier. ADVISORY ONLY -- a triage aid, not a legal
    determination. Article 6(3) carve-outs and role analysis need counsel.
    """
    if use_case.get("practice") in PROHIBITED_PRACTICES:
        return {"tier": "prohibited", "action": "Cannot be placed on the EU market. Redesign."}

    if use_case.get("domain") in ANNEX_III_DOMAINS:
        # Art. 6(3) may exclude narrow procedural tasks -- but never when the
        # system profiles natural persons, and never by self-declaration alone.
        narrow = use_case.get("narrow_procedural_task") and not use_case.get("profiles_individuals")
        return {
            "tier": "high_risk_unless_art_6_3",
            "possible_exemption": bool(narrow),
            "action": "Scope conformity assessment (Art. 43) + Annex IV docs; document any 6(3) claim.",
        }

    if use_case.get("interacts_with_humans") or use_case.get("generates_synthetic_media"):
        return {"tier": "limited_risk", "action": "Implement Art. 50 disclosure duties."}

    return {"tier": "minimal_risk", "action": "No specific obligations; revisit if purpose changes."}


print(triage_eu_ai_act({"domain": "employment", "profiles_individuals": True}))
# {'tier': 'high_risk_unless_art_6_3', 'possible_exemption': False,
#  'action': 'Scope conformity assessment (Art. 43) + Annex IV docs; document any 6(3) claim.'}
print(triage_eu_ai_act({"interacts_with_humans": True}))
# {'tier': 'limited_risk', 'action': 'Implement Art. 50 disclosure duties.'}
```

## Interview tips

- Classify by **intended purpose**, not by model or capability. The strongest signal you understand the Act is refusing to answer "is our LLM high-risk?" without asking what it decides and about whom.
- Know the provider/deployer split and how a deployer becomes a provider — rebranding, substantial modification, or repurposing into a high-risk use.
- Treat classification as a launch-timeline input, not a legal footnote. Conformity assessment and registration are schedule items that belong in the roadmap the moment an Annex III use case appears.
- Be careful with dates. Obligations phase in on different timelines by tier, so state which obligation you mean rather than quoting one blanket date.
- Say where your competence ends. This is a regulation with real penalties; engineers scope and document, counsel determines.

## Related Concepts

- [[What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?]] (`#205`): [What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?](../ai-safety-and-governance/what-is-the-nist-ai-risk-management-framework-and-how-do-its-four-functions-structure-ai-governance.md)
- [[What is copyright infringement risk in RAG and fine-tuning datasets?]] (`#183`): [What is copyright infringement risk in RAG and fine-tuning datasets?](../ai-safety-and-governance/what-is-copyright-infringement-risk-in-rag-and-fine-tuning-datasets.md)
- [[What is data lineage tracking for RAG documents and enterprise vector stores?]] (`#185`): [What is data lineage tracking for RAG documents and enterprise vector stores?](../ai-safety-and-governance/what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
