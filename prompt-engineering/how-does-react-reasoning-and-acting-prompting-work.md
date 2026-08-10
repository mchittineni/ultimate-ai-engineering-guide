---
title: "How does ReAct (Reasoning and Acting) prompting work?"
id: 3
category: "Prompt Engineering"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does ReAct (Reasoning and Acting) prompting work?

**Short answer:** ReAct (Reasoning + Acting) is a prompting technique that combines Chain-of-Thought reasoning with external action/tool execution in an interleaved loop (**Thought → Action → Observation → Thought**), allowing LLMs to solve complex tasks dynamically.

## Detail

Standard Chain-of-Thought (CoT) prompting encourages the model to generate internal reasoning steps before outputting a final answer. However, CoT is limited by the model's static parameter memory and cannot inspect real-world databases, call APIs, or handle dynamic environment changes.

ReAct bridges reasoning and execution by structuring prompt generation into discrete steps:

1. **Thought:** The model analyzes the current context, sub-goal, and what information is missing.
2. **Action:** The model emits a structured command or tool call (e.g., `Search[query]`, `ExecuteSQL[query]`, `Calculator[expression]`).
3. **Observation:** The external system runs the tool and appends the result back into the conversation context as an `Observation`.
4. **Repeat:** The model reads the new observation and generates the next `Thought`, continuing until it reaches a final `Thought` and outputs `Finish[answer]`.

````text
User Query
    │
    ▼
┌───────┐
│Thought│ ──► "I need to check stock price of Apple."
└───────┘
    │
    ▼
┌───────┐
│Action │ ──► GetStockPrice("AAPL")
└───────┘
    │
    ▼
┌───────────┐
│Observation│ ──► "$224.50" (Result returned by API)
└───────────┘
    │
    ▼
┌───────┐
│Thought│ ──► "Now I have the price. I can return the final answer."
└───────┘
    │
    ▼
  Finish
```text

### Why ReAct is central to AI Engineering

- **Explainability:** Human developers can inspect the model's reasoning trajectory step-by-step.
- **Error Recovery:** If an action returns an error or empty result, the subsequent `Thought` step allows the LLM to modify its search query or try an alternative tool.
- **Groundedness:** Reduces hallucinations by grounding answers in retrieved observations rather than parametric memory.

## Example

Prompt template structure for a ReAct agent:

```text
You operate in a loop of Thought, Action, Observation, Thought.
Available Tools:
- Search[query]: Searches the internet for information.
- Calculator[expression]: Evaluates a mathematical expression.

Format your response strictly as follows:
Thought: <reasoning about what to do>
Action: <ToolName[argument]>

When you have the final answer, format it as:
Thought: I know the final answer.
Final Answer: <your response>

User Question: What is the age of the current President of France multiplied by 2?

Thought: First I need to find out who the current President of France is and their age.
Action: Search[current President of France age]
Observation: Emmanuel Macron is 46 years old.

Thought: I found Emmanuel Macron's age (46). Now I need to multiply it by 2.
Action: Calculator[46 * 2]
Observation: 92

Thought: I have calculated the final result.
Final Answer: The age of the current President of France multiplied by 2 is 92.
```text

## Interview tips

- Contrast ReAct with pure zero-shot tool calling (Function Calling API): ReAct explicitly surfaces reasoning tokens prior to tool execution, improving tool argument selection accuracy.
- Discuss common failure modes: infinite loops (model repeatedly trying broken tools), context window overflow from long observation outputs, and high API costs.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
````
