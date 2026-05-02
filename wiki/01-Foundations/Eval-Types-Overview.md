---
title: Eval Types Overview
tags:
- wiki
last_updated: '2026-05-01'
sources:
- raw/notes/eval-types-overview.md
---

# Eval Types Overview

Three fundamentally different types of evaluation exist, each serving a different purpose. The key mistake most teams make is reaching for the most expensive type (LLM judge) when the cheapest (unit eval) would serve.

---

## Decision tree: which eval type to use?

```mermaid
flowchart TD
    Q1{Is there a known\ncorrect answer?}
    Q1 -->|Yes| A[Unit Eval\nDeterministic check]
    Q1 -->|No| Q2{Is the quality\nnuanced / contextual?}
    Q2 -->|Yes, but scalable| B[LLM-as-Judge\nCriteria-based scoring]
    Q2 -->|High stakes /\nedge case| C[Human Eval\nGold standard]
    B --> D{Validated against\nhuman labels?}
    D -->|No| C
    D -->|Yes, kappa > 0.6| B

    style A fill:#15803D,color:#fff
    style B fill:#1D4ED8,color:#fff
    style C fill:#C2410C,color:#fff
```

---

## Comparison at a glance

| Dimension | Unit Eval | LLM-as-Judge | Human Eval |
|---|---|---|---|
| Speed | Milliseconds | Seconds | Hours–days |
| Cost | Near zero | Low ($0.001–0.01/example) | High |
| Scale | Unlimited | Thousands/day | Hundreds/month |
| Coverage | Known cases only | Generalises to novel cases | Any case |
| Reliability | Perfect (deterministic) | Requires validation (kappa) | Ground truth |
| Actionability | Immediate | Depends on criteria quality | Slow feedback loop |
| Best used for | Regressions, format checks | Quality at scale, nuanced dims | Gold set, calibration |

---

## Using all three together

The correct architecture is not a choice between these three — it is a **layered system** where each type serves a different role:

```mermaid
graph TB
    subgraph Offline["Offline Evaluation"]
        UE[Unit Evals\nRun on every commit] --> LJ[LLM Judge\nRun on dev set daily]
        LJ --> HE[Human Eval\nRun on disagreements weekly]
    end
    subgraph Online["Online Evaluation"]
        Prod[Production traffic] --> Sample[1-2% sampled] --> LJO[LLM Judge\nContinuous]
    end
    HE -->|"Update gold set\nwhen new patterns found"| UE
    LJO -->|"Novel failures feed back\ninto dev eval suite"| LJ

    style Offline fill:#F0F9FF,stroke:#7DD3FC
    style Online fill:#F0FDF4,stroke:#86EFAC
```

---

## Applied to our use cases

### UC1 — Complaint Classifier
- **Unit evals:** 200 complaints with verified theme labels; exact match + taxonomy compliance check
- **LLM judge:** Criteria-based judge for multi-label coverage and theme justification; runs nightly on dev set
- **Human eval:** Domain expert reviews 50 judge disagreements per month; updates gold set

### UC2 — RAG Chatbot
- **Unit evals:** Known query–answer pairs (e.g., "How many complaints 2025-26?" → exact count)
- **LLM judge:** Faithfulness check (are all claims grounded in retrieved context?); relevance check
- **Human eval:** Regulatory staff review 20 sampled responses per week

---

*Next: [Unit Evals](Unit-Evals)*
