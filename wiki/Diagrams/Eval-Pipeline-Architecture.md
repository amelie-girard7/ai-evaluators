---
title: "Diagram: Eval Pipeline Architecture"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Diagram: Eval Pipeline Architecture

*Full end-to-end evaluation pipeline for the complaint classification system (UC1).*
*The standalone SVG version of this diagram is also available in the course materials.*

---

```mermaid
flowchart TD
    subgraph Ingestion["DATA INGESTION"]
        RC["Raw Complaints\n50k+ per year"]
        PP["Pre-processing\nClean, deduplicate"]
        SS["Sampling\nStratified / random"]
        HL["Human Labeling\nGold set 200-500"]
        RC --> PP --> SS --> HL
    end

    subgraph LLMSystem["LLM SYSTEM"]
        PT["Prompt Template\nTaxonomy + few-shot"]
        LM["LLM Classifier\nClaude / GPT / Gemini"]
        SO["Structured Output\nThemes + confidence"]
        PI["Prompt Iteration\nVersion controlled"]
        PT --> LM --> SO --> PI
    end

    subgraph EvalLayer["EVALUATION LAYER"]
        UE["Unit Evals\nKnown inputs → exact labels"]
        LJ["LLM Judge\nCriteria-based binary scoring"]
        HE["Human Evals\nSpot checks on disagreements"]
        MD["Metrics Dashboard\nAccuracy, Precision, Recall, F1\nConfusion matrix, Cohen kappa, Cost"]
        EA["Error Analysis\nCluster failures → find systematic patterns"]
        RG["Regression Guard CI/CD\nRun on every prompt change"]
        EDD["Eval-Driven Development\nFix evals first, improve model second"]
        UE & LJ & HE --> MD --> EA --> RG --> EDD
    end

    subgraph Observability["OBSERVABILITY"]
        LOG["Logging\nAll inputs + outputs"]
        TRC["Tracing\nToken use, latency, cost"]
        DD["Drift Detection\nScore drop alerts"]
        OE["Online Evals\nSample prod traffic"]
        LOG --> TRC --> DD --> OE
    end

    subgraph Action["ACTION"]
        ALT["Alert\nThreshold breach"]
        RB["Rollback\nPrior prompt version"]
        RL["Re-label\nExpand gold set"]
        DP["Deploy\nNew version"]
        ALT --> RB & RL --> DP
    end

    SS --> PT
    PI --> LM
    HL --> LJ
    SO --> EvalLayer
    EvalLayer --> Observability
    Observability --> Action
    Action -->|"Feedback loop"| PI
```

---

## Design principles encoded in this diagram

| Principle | Source | Where in diagram |
|---|---|---|
| Start with unit evals before LLM judges | Hamel Husain | UE → LJ ordering |
| Binary scoring over Likert | Decodingai.com | LLM Judge criteria |
| Error analysis is highest ROI | Hamel Husain (YouTube) | EA as central hub |
| Eval-driven development | Decodingai.com | EDD feedback loop |
| LLM judges need validation | eugeneyan.com | Human Evals → calibration |
| Online evals close the loop | Anthropic | Observability layer |
| Avoid generic metrics | Decodingai.com | Metrics Dashboard specificity |
| Evals alone not enough | O'Reilly / Reganti | Observability + Action layers |

---

*Next diagram: [LLM Judge Setup](LLM-Judge-Setup)*
