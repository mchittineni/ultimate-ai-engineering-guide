---
title: "What is semantic versioning for prompts and model configurations in production deployments?"
id: 164
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is semantic versioning for prompts and model configurations in production deployments?

**Short answer:** Semantic versioning for prompts applies structured version tags (`MAJOR.MINOR.PATCH`) to prompt templates and model hyperparameter configurations, allowing engineering teams to audit, test, roll back, and correlate prompt changes directly with production telemetry.

## Detail

Un-versioned prompt changes lead to silent quality regressions across production services.

```
Format: vMAJOR.MINOR.PATCH
- MAJOR (v2.0.0): Breaking changes (e.g. changing output schema from Markdown to JSON).
- MINOR (v1.1.0): New features / instructions (e.g. adding new guardrail rules or persona hints).
- PATCH (v1.0.1): Minor typos / wording tweaks (zero change to expected output structure).
```

### Version Configuration Artifact Example

```yaml
prompt_metadata:
  id: "customer_support_intent"
  version: "1.2.0"
  model: "gpt-4o-mini"
  temperature: 0.1
  max_tokens: 500
template: |
  You are an enterprise support agent. Classify user intent into {{ categories }}.
```

## Example

Python prompt registry manager:

```python
class PromptRegistry:
    def __init__(self):
        self.prompts = {}

    def register(self, name: str, version: str, template: str):
        key = f"{name}:{version}"
        self.prompts[key] = template

    def get(self, name: str, version: str) -> str:
        key = f"{name}:{version}"
        if key not in self.prompts:
            raise KeyError(f"Prompt '{key}' not found in registry.")
        return self.prompts[key]

registry = PromptRegistry()
registry.register("support", "1.0.0", "System rule v1...")
print("Loaded Prompt Version:", registry.get("support", "1.0.0"))
```

## Interview tips

- Discuss prompt registries (LangSmith, Phoenix, Humanloop) used to manage prompt deployment pipelines.
- Explain associating prompt version tags with OpenTelemetry span traces.

## Related Concepts

- [[What is prompt priming and how does it set expectations for LLM responses?]] (`#111`): [What is prompt priming and how does it set expectations for LLM responses?](../prompt-engineering/what-is-prompt-priming-and-how-does-it-set-expectations-for-llm-responses.md)
- [[What is an agent system prompt and how does it define tool availability?]] (`#135`): [What is an agent system prompt and how does it define tool availability?](../ai-agents-and-mcp/what-is-an-agent-system-prompt-and-how-does-it-define-tool-availability.md)
- [[How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?]] (`#166`): [How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?](../llmops-and-production-ai/how-do-you-set-up-automated-prompt-regression-pipelines-in-github-actions-ci-cd.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
