---
title: "Diagram: RAG Evals Framework"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Diagram: RAG Evals Framework

*The 6 RAG evals mapped to the complaints chatbot pipeline.*

---

```mermaid
flowchart LR
    Q["User Query\n'Complaints Western Sydney\n2025-2026?'"]

    subgraph Retrieval["RETRIEVAL STAGE"]
        EMB["Embed query"]
        VS["Vector search\nComplaint DB"]
        MF["Metadata filter\nRegion + Date"]
        CK["Top-k chunks\nComplaint records"]
        EMB --> VS --> MF --> CK
    end

    subgraph Generation["GENERATION STAGE"]
        ASM["Context assembly\nQuery + chunks"]
        LLM["LLM synthesis"]
        ANS["Answer\n'147 complaints\nfrom W. Sydney'"]
        ASM --> LLM --> ANS
    end

    subgraph RetEvals["RETRIEVAL EVALS"]
        E1["1. Context Precision\nRelevant retrieved / Total retrieved\nTarget: > 85%"]
        E2["2. Context Recall\nRelevant retrieved / Total relevant in DB\nTarget: > 90%"]
    end

    subgraph GenEvals["GENERATION EVALS"]
        E3["3. Faithfulness\nSupported claims / Total claims\nTarget: 100% | CRITICAL"]
        E4["4. Relevance\nAnswer addresses the question asked\nTarget: > 0.85 cosine sim"]
        E5["5. Correctness\nMatches ground-truth answer\nTarget: exact match | CRITICAL"]
        E6["6. Completeness\nCovered aspects / Required aspects\nTarget: 1.0 for multi-part"]
    end

    Q --> Retrieval
    CK --> Generation
    CK -.->|"Eval"| E1 & E2
    ANS -.->|"Eval"| E3 & E4 & E5 & E6

    style E3 fill:#DC2626,color:#fff
    style E5 fill:#DC2626,color:#fff
    style E1 fill:#7C3AED,color:#fff
    style E2 fill:#0891B2,color:#fff
    style E4 fill:#EA580C,color:#fff
    style E6 fill:#B45309,color:#fff
```

---

## Fix decision tree: when an eval fails

```mermaid
flowchart TD
    F["An eval is failing"] --> Q1{Which eval?}

    Q1 --> CP["Context Precision failing"]
    Q1 --> CR["Context Recall failing"]
    Q1 --> FA["Faithfulness failing"]
    Q1 --> RE["Relevance failing"]
    Q1 --> CO["Correctness failing"]
    Q1 --> CM["Completeness failing"]

    CP --> FCP["Fix retrieval:\nImprove chunking\nAdd metadata pre-filters\nReduce top-k noise"]
    CR --> FCR["Fix retrieval:\nRe-index DB\nIncrease top-k\nImprove embeddings\nAdd keyword fallback"]
    FA --> FFA["Fix generation:\nAdd citation requirement to prompt\nConstrained generation\nAdd faithfulness gate"]
    RE --> FRE["Fix generation:\nStrengthen query scope in prompt\nFew-shot examples of focused answers"]
    CO --> Q2{Is it a retrieval\nor generation failure?}
    Q2 -->|"Recall low"| FCR
    Q2 -->|"Retrieval OK"| FCO["Fix generation:\nStructured output\nDate normalisation\nGeography normalisation"]
    CM --> FCM["Fix generation:\nStructured multi-part template\nExplicit schema in prompt"]

    style FA fill:#DC2626,color:#fff
    style CO fill:#DC2626,color:#fff
    style FFA fill:#15803D,color:#fff
    style FCO fill:#15803D,color:#fff
```

---

*Source: Jason Liu (jxnl.co) — There Are Only 6 RAG Evals | Anthropic — Demystifying Evals for AI Agents*

*Next diagram: [Error Analysis Workflow](Error-Analysis-Workflow)*
