# Checklist: Eval Design (Before Building Any LLM System)

Use this before writing the first line of code or the first prompt. The discipline of defining "good" in advance is what separates evaluation-driven development from vibe-checking.

---

## Pre-build checklist

- [ ] **Task definition written in plain language** — what must the system do, for whom, and how will we know it succeeded?
- [ ] **Success criteria defined per output dimension** — not "is this good?" but specific measurable properties
- [ ] **Gold set collection plan** — who labels, how many examples (target 200–500), how are disagreements resolved?
- [ ] **Target metrics defined with thresholds** — e.g., F1 > 0.85 per theme, kappa > 0.6
- [ ] **Taxonomy or output schema documented** — written definitions for every valid output category
- [ ] **LLM judge criteria drafted** — binary YES/NO per dimension, with examples
- [ ] **Human reviewer identified and briefed** — domain expert who understands the task
- [ ] **CI/CD gate criteria established** — which metrics trigger a merge block?
- [ ] **Eval suite written before first prompt** — the evals are the specification

---

## UC1 — Client Feedback Classifier specific

- [ ] All 8+ taxonomy themes have written definitions
- [ ] Each theme has inclusion and exclusion criteria
- [ ] Boundary cases between adjacent themes documented
- [ ] Multi-label output explicitly allowed in prompt design
- [ ] At least 2 positive and 2 negative examples prepared per theme

## UC2 — RAG Chatbot specific

- [ ] All 6 RAG evals planned: precision, recall, faithfulness, relevance, correctness, completeness
- [ ] Ground-truth query–answer pairs built from actual database queries
- [ ] Geography normalisation strategy decided before indexing
- [ ] Date format convention (FY vs calendar year) documented in system prompt
- [ ] Citation requirement specified in system prompt design

---

*Related: [LLM Judge Quality Checklist](llm-judge-quality-checklist)*
