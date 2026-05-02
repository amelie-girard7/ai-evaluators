---
title: References
tags:
- wiki
last_updated: '2026-05-01'
sources:
- raw/notes/references.md
---

# References

All 11 source references with access status, key contribution, and mapping to wiki sections.

---

## Access status key

| Status | Meaning |
|---|---|
| BLOCKED | Site not reachable from build environment; content from training knowledge |
| ACCESSIBLE | Site reached; content used directly |

---

## Reference list

### 1. Hamel Husain — LLM Judge
- **URL:** https://hamel.dev/blog/posts/llm-judge/
- **Access:** BLOCKED
- **Diagrams recreated:** See [Diagrams/Hamel-LLM-Judge-Recreation](../Diagrams/Hamel-LLM-Judge-Recreation)
- **Key contribution:** Criteria-based judge design; binary scoring; failure modes; validation against human labels
- **Wiki sections:** [LLM-as-Judge](../03-LLM-Judges/LLM-as-Judge-Complete-Guide), [Judge Design](../03-LLM-Judges/LLM-as-Judge-Complete-Guide), [Error Analysis](../06-Error-Analysis/Overview)

---

### 2. Decodingai.com — Integrating AI Evals into Your AI App
- **URL:** https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app
- **Access:** BLOCKED
- **Key contribution:** Four-phase eval lifecycle: design → development → pre-production → production
- **Wiki sections:** [Integrating Evals](../06-Eval-Lifecycle/Integrating-Evals)

---

### 3. Anthropic — Demystifying Evals for AI Agents
- **URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- **Access:** ACCESSIBLE (content too large; summarised from training knowledge)
- **Key contribution:** Unit evals, trajectory evals, final-state evals for agentic systems
- **Wiki sections:** [Agent Evals](../09-Agent-Evals/Demystifying-Agent-Evals)

---

### 4. Jason Liu (jxnl.co) — There Are Only 6 RAG Evals
- **URL:** https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/
- **Access:** BLOCKED
- **Key contribution:** The definitive framework: context precision, recall, faithfulness, relevance, correctness, completeness
- **Wiki sections:** [The 6 RAG Evals](../04-Use-Case-02-RAG-Chatbot/The-6-RAG-Evals), [RAG Evals Framework diagram](../Diagrams/RAG-Evals-Framework)

---

### 5. Decodingai.com — Evaluation-Driven Development
- **URL:** https://www.decodingai.com/p/stop-launching-ai-apps-without-this
- **Access:** BLOCKED
- **Key contribution:** Write evals before building; eval-driven development as a discipline
- **Wiki sections:** [Eval Design Step by Step](../03-Use-Case-01-Complaint-Classification/Eval-Design-Step-by-Step)

---

### 6. Decodingai.com — The 5-Star Lie (Binary vs Likert)
- **URL:** https://www.decodingai.com/p/the-5-star-lie-you-are-doing-ai-evals
- **Access:** BLOCKED
- **Key contribution:** Binary evals yield kappa 0.6–0.9; Likert scales yield kappa 0.2–0.4
- **Wiki sections:** [Binary vs Likert](../04-Metrics-and-Scoring/Binary-vs-Likert)

---

### 7. Decodingai.com — The Mirage of Generic AI Metrics
- **URL:** https://www.decodingai.com/p/the-mirage-of-generic-ai-metrics
- **Access:** BLOCKED
- **Key contribution:** Generic metrics (BLEU, ROUGE) do not predict success on actual task; always validate metrics against human judgments on your specific data
- **Wiki sections:** [Mirage of Generic Metrics](../04-Metrics-and-Scoring/Mirage-of-Generic-Metrics)

---

### 8. Error Analysis — Highest ROI Technique
- **Key contribution:** Error clustering, root cause analysis, prioritisation by business impact
- **Wiki sections:** [Error Analysis Overview](../06-Error-Analysis/Overview), [5-Step Framework](../06-Error-Analysis/5-Step-Framework)

---

### 9. Hamel Husain — Error Analysis (YouTube)
- **URL:** https://www.youtube.com/watch?v=e2i6JbU2R-s
- **Access:** BLOCKED
- **Key contribution:** Practical walkthrough of error analysis; the discipline of reading data manually
- **Wiki sections:** [Error Analysis](../06-Error-Analysis/Overview)

---

### 10. Eugene Yan — Evaluating the Effectiveness of LLM Evaluators
- **URL:** https://eugeneyan.com/writing/llm-evaluators/
- **Access:** BLOCKED
- **Key contribution:** Empirical study of judge reliability; positional bias, self-preference, verbosity bias measured; validation protocol
- **Wiki sections:** [Validation Protocol](../03-LLM-Judges/Validation-Protocol), [Failure Modes](../03-LLM-Judges/LLM-as-Judge-Complete-Guide)

---

### 11. Hamel Husain — LLM Judges Aren't the Shortcut You Think (YouTube)
- **URL:** https://www.youtube.com/watch?v=sEMYSSS6Ims
- **Access:** BLOCKED
- **Key contribution:** Practical judge design; common pitfalls; calibration walkthrough
- **Wiki sections:** [Judge Design](../03-LLM-Judges/LLM-as-Judge-Complete-Guide), [LLM-as-Judge](../03-LLM-Judges/LLM-as-Judge-Complete-Guide)

---

## Additional references (academic)

- Reganti, A. N., & Badam, K. (2025). *Evals Are NOT All You Need.* O'Reilly. https://www.oreilly.com/radar/evals-are-not-all-you-need/
- Habib, R. (2024). *Why Your AI Product Needs Evals with Hamel Husain.* Humanloop Blog. https://humanloop.com/blog/why-your-product-needs-evals
- Lenny's Podcast. *Why AI evals are the hottest new skill for product builders | Hamel Husain & Shreya Shankar.* YouTube. https://www.youtube.com/watch?v=BsWxPI9UM4c

---

*See also: [Blocked Resources Notice](Blocked-Resources-Notice)*
