---
title: "Diagram: Error Analysis Workflow"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Diagram: Error Analysis Workflow

*The 5-step error analysis loop — the highest ROI technique in AI engineering.*

---

```mermaid
flowchart TD
    START(["New failures\naccumulate"]) --> S1

    S1["Step 1: Collect failures\nAll outputs below eval threshold\nTarget: 50-200 cases\nStratify by theme, date, source"]

    S1 --> S2["Step 2: Read the data\nManually read 20-50 cases\nBefore ANY automation\nForm hypotheses about root causes\n'Do not trust your dashboard'"]

    S2 --> S3["Step 3: Cluster by root cause\nGroup by WHY, not by symptom\nCommon root causes:\n- Prompt ambiguity\n- Taxonomy gap\n- Multi-label blind spot\n- Retrieval failure\n- Training data gap"]

    S3 --> S4["Step 4: Prioritise\nScore = Frequency × Severity × Fixability\nFix highest-impact cluster first\nNOT the easiest one"]

    S4 --> S5["Step 5: Hypothesise and test fix\nPropose targeted fix\nTest on failing cluster ONLY\nVerify no regression on others"]

    S5 --> D1{Did fix\nwork?}

    D1 -->|"Yes — cluster improved\nno regression"| DEPLOY["Deploy fix\nAdd cases to gold set\nDocument root cause\nMonitor for recurrence"]
    D1 -->|"No — cluster unchanged\nor regressed"| S2

    DEPLOY --> MONITOR["Monitor production\n1-2% sampling\nAlert on drift"] --> START

    style S1 fill:#1D4ED8,color:#fff
    style S2 fill:#7C3AED,color:#fff
    style S3 fill:#C2410C,color:#fff
    style S4 fill:#15803D,color:#fff
    style S5 fill:#0E7490,color:#fff
    style DEPLOY fill:#0F172A,color:#fff
    style MONITOR fill:#374151,color:#fff
```

---

## Root cause taxonomy for both use cases

```mermaid
mindmap
  root((Root Cause\nCategories))
    Prompt-caused
      Multi-label blind spot UC1
      Incomplete answer UC2
      Indirect language missed UC1
    Retrieval-caused
      Geography not normalised UC2
      Date range ambiguity UC2
      Index incomplete UC2
    Taxonomy-caused
      Theme boundary overlap UC1
      Novel complaint type UC1
      Confidentiality not in scope UC1
    Model-caused
      Hallucinated calculation UC2
      Overconfident on edge case UC1
    Data-caused
      Gold set too narrow UC1
      Test set not stratified UC2
```

---

## Prioritisation scorecard

| Cluster | Freq (1-3) | Severity (1-3) | Fixable (1-3) | Score | Fix |
|---|---|---|---|---|---|
| Multi-label gap (UC1) | 3 | 3 | 3 | **9** | Prompt: allow list output |
| Hallucinated % (UC2) | 3 | 3 | 3 | **9** | Prompt: citation required |
| Underquoting/Advertising boundary (UC1) | 2 | 2 | 3 | **12→6** | Add boundary examples |
| Geography not normalised (UC2) | 2 | 3 | 2 | **12→8** | Engineering: normalise index |
| Indirect honesty language (UC1) | 2 | 3 | 3 | **18→7** | Add few-shot examples |

---

*Source: Hamel Husain — Error Analysis (YouTube) | Highest ROI Technique article*

*Back to: [Diagrams index](Eval-Pipeline-Architecture)*
