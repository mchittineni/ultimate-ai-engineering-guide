---
title: "How do you architect real-time anomaly detection for rogue agent spends?"
id: 85
category: "LLMOps and Production AI"
difficulty: "Advanced"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you architect real-time anomaly detection for rogue agent spends?

**Short answer:** Real-time anomaly detection for rogue agent spend uses streaming event processors (e.g. Apache Flink, Kafka) to calculate sliding-window token consumption velocities per agent session, triggering automated kill switches when token velocity deviates significantly from historical Z-score baselines.

## Detail

Rogue agents (agents stuck in un-terminated tool loops or recursive API calls) can consume millions of tokens in minutes.

Traditional batch end-of-day billing alerts trigger too late to prevent financial damage.

```
[Agent Stream] ──► [Kafka / Streaming Telemetry] ──► [Sliding Window Velocity (Flink)]
                                                              │
                    ┌─────────────────────────────────────────┴─────────────────────────────────────────┐
                    ▼ (Z-Score > 3.0 or Velocity > 50K tokens/min)                                      ▼ (Normal Velocity)
            [KILL SWITCH TRIGGERED]                                                             Process Normally
      Revoke Session Key & Abort Loop
```

### Detection Algorithms

1. **Sliding Window Token Velocity:** Compute tokens consumed over a 1-minute moving window: $V_{tokens}(t) = \sum_{t-60s}^t T_i$.
2. **Dynamic Z-Score Thresholding:** Calculate standard deviation $\sigma$ and mean $\mu$ of token velocity for the specific agent task type:

$$Z = \frac{V_{tokens}(t) - \mu}{\sigma}$$

If $Z > 3.0$, flag as an anomaly and trigger immediate process termination.

## Example

Python sliding-window anomaly detector concept:

```python
import time
from collections import deque

class TokenAnomalyDetector:
    def __init__(self, window_seconds=60, max_tokens_per_window=20000):
        self.window_seconds = window_seconds
        self.max_tokens = max_tokens_per_window
        self.history = deque() # tuples of (timestamp, token_count)

    def record_and_check(self, tokens: int) -> bool:
        now = time.time()
        self.history.append((now, tokens))
        
        # Evict events outside sliding window
        while self.history and self.history[0][0] < now - self.window_seconds:
            self.history.popleft()
            
        current_window_tokens = sum(t for _, t in self.history)
        if current_window_tokens > self.max_tokens:
            return False # ANOMALY DETECTED: Trigger Kill-Switch
        return True
```

## Interview tips

- Discuss automated remediation actions: revoking session tokens, pausing agent execution, and alerting engineering oncall via PagerDuty.
- Highlight logging full execution stack traces during anomaly events for post-mortem analysis.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
