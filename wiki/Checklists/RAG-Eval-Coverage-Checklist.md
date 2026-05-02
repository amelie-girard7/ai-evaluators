---
title: "Checklist: RAG Eval Coverage"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Checklist: RAG Eval Coverage

All 6 RAG evals must be covered before a RAG system is production-ready. Skip any and you have a blind spot that will produce production failures.

---

## Retrieval evals

- [ ] **Context Precision measured** — what fraction of retrieved chunks are relevant?
  - Target: > 85%
  - Test: manually label top-k results for a sample of 50 queries
- [ ] **Context Recall measured** — what fraction of all relevant records are retrieved?
  - Target: > 90%
  - Test: compare retrieved set to full database query for same parameters

## Generation evals

- [ ] **Answer Faithfulness measured** — are all claims grounded in retrieved context?
  - Target: 100% (zero tolerance for unsupported claims)
  - Test: LLM judge checks each claim against retrieved context chunks
- [ ] **Answer Relevance measured** — does the answer address what was asked?
  - Target: > 0.85 cosine similarity (re-generated questions vs original)
  - Test: LLM generates questions from the answer; compare to original query
- [ ] **Answer Correctness measured** — does the answer match ground truth?
  - Target: Exact match for counts; > 0.9 F1 for descriptions
  - Test: Compare to pre-computed ground truth from database
- [ ] **Answer Completeness measured** — are all question dimensions covered?
  - Target: 1.0 for multi-part questions
  - Test: Parse question for required dimensions; check each in answer

## UC2-specific checks

- [ ] Geography normalisation validated — Western Sydney maps to consistent postcode list
- [ ] Date range convention documented — FY vs calendar year handled explicitly
- [ ] Citation requirement in system prompt — every claim must cite source
- [ ] Multi-part answer template in prompt — structured response for AND queries
- [ ] Numeric answer accuracy validated against database queries
