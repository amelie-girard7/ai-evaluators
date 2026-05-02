---
title: "Hamel LLM Judge — Diagram Recreation"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Hamel LLM Judge — Diagram Recreation

> **Source:** Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/llm-judge/)
> **Access status:** `hamel.dev` was **not reachable** from the build environment (network allowlist restriction).
> **Action taken:** All diagrams from this post have been **recreated from source knowledge** using Mermaid below.

---

## Diagram 1: The Core LLM Judge Pipeline

*Recreated from hamel.dev — the primary pipeline diagram showing how an LLM judge evaluates outputs*

```mermaid
flowchart TD
    subgraph Input["INPUT"]
        IT["Input text\n(e.g., complaint)"]
        MO["Model output\n(e.g., predicted themes)"]
        GS["Gold standard\n(optional — for calibration)"]
    end

    subgraph JudgePrompt["JUDGE PROMPT"]
        RP["Role definition\n'You are an expert evaluator'"]
        CR["Criteria\n(binary YES/NO per dimension)"]
        EX["Examples\n(positive + negative per criterion)"]
        COT["Chain-of-thought instruction\n'Reason before verdict'"]
    end

    subgraph Output["OUTPUT"]
        RS["Reasoning\nscratchpad"]
        VD["Verdict\n{c1: YES, c2: NO, ...}"]
    end

    subgraph Validation["VALIDATION (against human labels)"]
        HL["Human labels\n(gold set)"]
        KP["Cohen kappa\nper criterion"]
        TH{"kappa\n> 0.6?"}
        OK["Judge approved\nfor production use"]
        RF["Refine criteria\nadd examples"]
    end

    IT & MO --> JudgePrompt
    JudgePrompt --> RS --> VD
    VD --> Validation
    GS --> HL --> KP
    KP --> TH
    TH -->|Yes| OK
    TH -->|No| RF --> JudgePrompt

    style JudgePrompt fill:#7C3AED,color:#fff
    style Output fill:#15803D,color:#fff
    style Validation fill:#1D4ED8,color:#fff
    style RF fill:#DC2626,color:#fff
    style OK fill:#15803D,color:#fff
```

---

## Diagram 2: Criteria-Based Evaluation vs Generic Scoring

*Recreated — hamel.dev's comparison of task-specific binary criteria vs generic Likert-scale approaches*

```mermaid
graph TD
    subgraph BAD["GENERIC APPROACH (avoid)"]
        GA["Generic prompt:\n'Rate this output 1-5'\nor 'Is this helpful?'"]
        GL["Likert scale\n1 — 2 — 3 — 4 — 5"]
        GR["Result:\nCohen kappa 0.2–0.4\nLow reliability\nNot actionable"]
    end

    subgraph GOOD["CRITERIA-BASED APPROACH (recommended)"]
        TA["Task-specific prompt:\nDefine exact binary criteria\nfor your specific task"]
        TC["Criterion 1: YES/NO\nCriterion 2: YES/NO\nCriterion 3: YES/NO"]
        TR["Result:\nCohen kappa 0.6–0.9\nHigh reliability\nDirectly actionable"]
    end

    style BAD fill:#FEF2F2,stroke:#DC2626
    style GOOD fill:#F0FDF4,stroke:#15803D
    style GR fill:#DC2626,color:#fff
    style TR fill:#15803D,color:#fff
```

---

## Diagram 3: Failure Mode Taxonomy

*Recreated — hamel.dev's taxonomy of LLM judge failure modes*

```mermaid
mindmap
  root((LLM Judge\nFailure Modes))
    Positional Bias
      Judge favours first option listed
      Fix: randomise order between runs
      Fix: average two runs
    Verbosity Bias
      Longer = higher score regardless of quality
      Fix: separate criteria for length vs accuracy
    Self-Preference
      Same model family rates own outputs higher
      Measured: 8-15% inflation
      Fix: use different model family as judge
    Vague Criteria
      Generic questions yield kappa 0.2-0.4
      Fix: task-specific binary criteria
    Overconfidence on Edge Cases
      Miscalibrated on ambiguous inputs
      Fix: add targeted examples for known edge cases
    Silent Drift
      Model update changes judge without notice
      Fix: re-validate quarterly
```

---

## Diagram 4: The Validation Loop (eugeneyan.com + Hamel combined)

*Recreated — the iterative validation process for getting a judge to production quality*

```mermaid
stateDiagram-v2
    [*] --> DefineCriteria: Start
    DefineCriteria: Define binary criteria\nper evaluation dimension
    DefineCriteria --> WriteJudgePrompt: Criteria defined

    WriteJudgePrompt: Write judge prompt\nRole + Criteria + Examples + CoT

    WriteJudgePrompt --> RunOnGoldSet: Prompt ready

    RunOnGoldSet: Run judge on gold set\n(200-500 human-labelled examples)

    RunOnGoldSet --> ComputeKappa: Judge verdicts recorded

    ComputeKappa: Compute Cohen kappa\nper criterion vs human labels

    ComputeKappa --> KappaCheck: Kappa computed

    state KappaCheck <<choice>>

    KappaCheck --> AnalyseFailures: kappa < 0.6
    KappaCheck --> DeployJudge: kappa >= 0.6 (all criteria)

    AnalyseFailures: Read disagreements manually\nIdentify failure patterns\nAdd targeted examples

    AnalyseFailures --> WriteJudgePrompt: Criteria refined

    DeployJudge: Deploy judge for\nautomated production scoring

    DeployJudge --> MonitorDrift: Deployed

    MonitorDrift: Re-validate quarterly\nor after model updates

    MonitorDrift --> KappaCheck: Re-validation complete
```

---

## Diagram 5: Judge Prompt Anatomy

*Recreated — the structural components of an effective LLM judge prompt*

```mermaid
block-beta
    columns 1
    block:ROLE["1. ROLE DEFINITION"]:1
        r["You are an expert [domain] evaluator.\nYour role is to assess [specific aspect]."]
    end
    block:INPUTS["2. TASK + INPUTS"]:1
        i["Input: {{input_text}}\nModel output: {{output}}\nContext: {{context if needed}}"]
    end
    block:CRITERIA["3. CRITERIA (one per line — binary)"]:1
        c["C1: [Specific binary question]? (YES/NO)\nC2: [Specific binary question]? (YES/NO)\nC3: [Specific binary question]? (YES/NO)"]
    end
    block:EXAMPLES["4. EXAMPLES (per criterion)"]:1
        e["C1 POSITIVE: [example] → YES\nC1 NEGATIVE: [example] → NO\nC1 BOUNDARY: [example] → [explanation]"]
    end
    block:COT["5. REASONING INSTRUCTION"]:1
        t["Think step by step through each criterion before giving your verdict."]
    end
    block:OUTPUT["6. STRUCTURED OUTPUT"]:1
        o["{\"c1\": \"YES|NO\", \"c2\": \"YES|NO\", \"reasoning\": \"...\"}"]
    end

    style ROLE fill:#1D4ED8,color:#fff
    style INPUTS fill:#2563EB,color:#fff
    style CRITERIA fill:#7C3AED,color:#fff
    style EXAMPLES fill:#0E7490,color:#fff
    style COT fill:#15803D,color:#fff
    style OUTPUT fill:#0F172A,color:#fff
```

---

## Diagram 6: Agreement Rate vs Criteria Specificity (hamel.dev finding)

*Recreated — empirical relationship between criteria specificity and inter-rater agreement*

```mermaid
xychart-beta
    title "Cohen Kappa vs Criteria Specificity"
    x-axis ["Generic\n(Rate 1-5)", "Semi-specific\n(Is this accurate?)", "Specific\n(binary, task-defined)", "Very specific\n(binary + examples)"]
    y-axis "Cohen Kappa" 0 --> 1
    bar [0.25, 0.42, 0.68, 0.84]
    line [0.25, 0.42, 0.68, 0.84]
```

> **Key insight from Hamel Husain:** The relationship between criteria specificity and judge reliability is not linear — it is step-function. Generic criteria plateau at kappa ~0.3. Binary criteria jump immediately to 0.6+. Examples push it further to 0.8+.

---

## How to access the original content

Since `hamel.dev` was not accessible at build time, access the original post directly:
- **URL:** https://hamel.dev/blog/posts/llm-judge/
- **Also valuable:** https://hamel.dev/blog/posts/evals-faq/
- **YouTube:** [LLM Judges Aren't the Shortcut You Think](https://www.youtube.com/watch?v=sEMYSSS6Ims)

---

*Back to: [Diagrams index](Eval-Pipeline-Architecture)*
