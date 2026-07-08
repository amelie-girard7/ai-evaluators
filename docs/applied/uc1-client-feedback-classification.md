# UC1: Client Feedback Classification - Overview

> **System:** LLM classifier assigning business themes to 100,000+ formal property client feedback per year
> **Domain:** Professional services - client interactions, service quality, billing practices

---

## The business problem

An organisation receives over 100,000+ formal client feedback per year about service delivery and related matters. Manually reading and categorising each item is not scalable. An LLM-powered classifier must assign one or more themes from a controlled taxonomy to each item, enabling analytics, workload routing, and trend reporting.

---

## System architecture

![Raw client feedback\n100k+/year](../assets/diagrams/uc1-complaint-classification-overview-1-3a956034.png)
---

## Deidentified examples

See: [Deidentified Examples](deidentified-examples)

---

## The multi-label challenge

Both illustrative examples share the same 5 themes. The most common failure mode for this system is **single-label output on multi-theme client feedback**. The classifier must:

1. Recognise that a feedback item can justify multiple themes simultaneously
2. Apply all applicable themes, not just the most prominent one
3. Not apply themes that are not supported by the feedback text

---

## Quick reference

| Page | Content |
|---|---|
| [Deidentified Examples](deidentified-examples) | Two anonymised feedback examples with correct theme labels |
| [Eval Design Step by Step](eval-design-step-by-step) | 8-step process from gold set to CI/CD |
