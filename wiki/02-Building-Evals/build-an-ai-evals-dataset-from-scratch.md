---
title: Build an AI Evals Dataset from Scratch
tags: [evals, dataset, error-analysis, ai-evals, observability]
last_updated: 2026-05-01
sources: ["raw/web/No Evals Dataset? Here's How to Build One from Scratch.md"]
---

# Build an AI Evals Dataset from Scratch

A step-by-step guide to creating a high-quality evaluation dataset using real-world data and error analysis. This article is part of the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**, designed for busy engineers and product teams.

---

## Why You Need a Dataset

Most AI teams skip building datasets and jump straight to evaluation criteria or dashboards. This leads to:

- **Irrelevant metrics** that waste resources on low-probability defects
- **Unrealistic expectations** that the technology can't meet
- **Missed failure modes** that users actually care about

The solution is **error analysis** — a flywheel process that starts with 20–50 real traces and iteratively grows your dataset and evaluators.

---

## Step 1: Collect Production Traces

The highest-value source for your dataset is **real production traces**. These include:

- User input
- System prompt
- Model output
- Tool calls
- Retrieved documents
- Metadata (timestamp, user ID, channel)

### Tools for Logging
Use observability/LLMOps platforms like [LLMOps tools](../04-Metrics-and-Scoring/Mirage-of-Generic-Metrics.md) to log and search traces. Aim for 50–100 traces initially.

### Sampling Strategies
If you have large datasets, use advanced sampling:
- Outlier detection (extreme response lengths, latency)
- User feedback signals (negative feedback, escalations)
- Stratified sampling (group by user type, query category)
- Embedding clustering (identify edge cases)

---

## Step 2: Manual Labeling

Label your dataset with **domain experts** to define what "good" looks like. Focus on:

1. **Input**: User query or request
2. **Output**: Final agent response
3. **Context**: Retrieved documents, conversation history
4. **Trace Spans**: Tool calls, model outputs

### Example Dataset Entry
```json
{
  "input": "Where is my order #123?",
  "output": "Order #123 is being shipped and will arrive by Friday.",
  "context": {"user_id": "12345", "channel": "web"},
  "trace_spans": [
    {"tool_call": "order_lookup", "response": "Found 3 orders with similar numbers"}
  ]
}
```

---

## Step 3: Fix Errors and Grow the Dataset

Use **error analysis** to identify failure modes and create regression tests:

1. **Cluster errors** by type (e.g., ambiguous response, missing data)
2. **Prioritize fixes** based on severity and frequency
3. **Automate regression tests** for high-impact errors

---

## Step 4: Build and Align an LLM Judge

Create **LLM judges** that align with human expertise using **Critique Shadowing**:

1. **Train judges** on labeled data from domain experts
2. **Validate judges** by comparing scores to human labels
3. **Iterate** based on error analysis and feedback

### Example Judge Prompt
> *You are a customer service director. Rate the response on a scale of 1–5 for clarity and helpfulness. Provide a brief explanation.*

---

## Step 5: Systematic Error Analysis

Use error analysis to:
- **Cluster failures** into categories
- **Prioritize fixes** based on business impact
- **Refine evaluators** to catch real-world issues

### Error Analysis Flywheel
![Collect Traces](../Diagrams/auto/build-an-ai-evals-dataset-from-scratch-1-461cb91e.svg)
---

## Step 6: Transition to Specialized Evaluators

As understanding deepens, move from **generic evaluators** to **specialized ones**:

- **Domain-specific metrics** (e.g., "accuracy in medical diagnosis")
- **Task-specific rubrics** (e.g., "completeness of legal document summary")
- **LLM judges** trained on domain expertise

---

## Next Steps

- [LLM-as-Judge: Complete Guide](../03-LLM-Judges/LLM-as-Judge-Complete-Guide.md) — Learn Critique Shadowing
- [Generate Synthetic Datasets](Generate-Synthetic-Datasets.md) — Fill gaps with synthetic data
- [Error Analysis: The Highest ROI Technique](../05-Error-Analysis/Overview.md) — Deep dive into error clustering

---
