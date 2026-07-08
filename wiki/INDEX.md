# Wiki Index

_One line per article — used by `query.py` and `compile.py` to route._


## 01-Foundations
- [Eval Maturity Ladder](01-Foundations/Eval-Maturity-Ladder.md) — **Eval Maturity Ladder** — Understanding where your team sits determines what to build next. Most teams underestimate how much value is left at low
- [Eval Types Overview](01-Foundations/Eval-Types-Overview.md) — **Eval Types Overview** — Three fundamentally different types of evaluation exist, each serving a different purpose. The key mistake most teams ma
- [Human Evals](01-Foundations/Human-Evals.md) — **Human Evals** — Human evaluation is the gold standard. It is also expensive and slow. Use it strategically: for building calibration dat
- [Unit Evals](01-Foundations/Unit-Evals.md) — **Unit Evals** — Unit evals are the foundation of any evaluation system. They are deterministic, fast, and free. Most teams underinvest i
- [Why Evals Matter](01-Foundations/Why-Evals-Matter.md) — **Why Evaluations Matter** — > *"Without evals, you are flying blind. With bad evals, you are flying with a broken altimeter."* — Hamel Husain

## 02-Building-Evals
- [Generate Synthetic Datasets](02-Building-Evals/Generate-Synthetic-Datasets.md) — **Generate Synthetic Datasets for AI Evals** — > *"Synthetic data is the missing piece in your evals pipeline. It fills gaps in production data, expands edge cases, an
- [build an ai evals dataset from scratch](02-Building-Evals/build-an-ai-evals-dataset-from-scratch.md) — The content aligns with 02-Building-Evals' focus on dataset creation, providing a step-by-step guide to building eval datasets from scratch.

## 03-LLM-Judges
- [LLM as Judge Complete Guide](03-LLM-Judges/LLM-as-Judge-Complete-Guide.md) — **Using LLM-as-a-Judge: A Complete Guide** — Hamel-style step-by-step canonical for designing LLM judges (PDE → dataset → critique shadowing → harness).
- [Validation Protocol](03-LLM-Judges/Validation-Protocol.md) — **Judge Validation Protocol** — A judge that has not been validated against human labels is not a judge — it is a guess at scale.

## 04-Metrics-and-Scoring
- [Binary vs Likert](04-Metrics-and-Scoring/Binary-vs-Likert.md) — **Binary Evals vs Likert Scales: The Evidence** — Why binary scoring outperforms 5-star ratings for AI evaluation reliability
- [Mirage of Generic Metrics](04-Metrics-and-Scoring/Mirage-of-Generic-Metrics.md) — **The Mirage of Generic AI Metrics** — Why task-specific evaluation beats off-the-shelf benchmarks

## 05-Error-Analysis
- [Case Studies](05-Error-Analysis/Case-Studies.md) — **Error Analysis Case Studies** — Applied to both use cases. Each cluster shows the root cause, a representative example, and the fix.
- [Overview](05-Error-Analysis/Overview.md) — **Error Analysis: The Highest ROI Technique** — > *"Do not trust your dashboard. Read your data."* — Hamel Husain

## 06-Eval-Lifecycle
- [Evals Are NOT All You Need](06-Eval-Lifecycle/Evals-Are-NOT-All-You-Need.md) — **Evals Are NOT All You Need** — > *"Evals are only important in the context of product quality, and product quality is a process."* — Anonymous AI Produ
- [Integrating Evals](06-Eval-Lifecycle/Integrating-Evals.md) — **Integrating Evals Into the AI App Lifecycle** — From development through production: a continuous evaluation strategy
- [behind the scenes of ai observability in production](06-Eval-Lifecycle/behind-the-scenes-of-ai-observability-in-production.md) — The content discusses practical lessons from 6 months of evals in production, aligning with the Eval-Lifecycle's focus on production integra
- [evaluation driven development edd framework](06-Eval-Lifecycle/evaluation-driven-development-edd-framework.md) — The content aligns with 06-Eval-Lifecycle's focus on EDD and integrating evaluations into the AI app development process before launch.

## 07-Agent-Evals
- [Demystifying Agent Evals](07-Agent-Evals/Demystifying-Agent-Evals.md) — **Evaluating Agentic AI Systems** — How evaluation changes when your AI takes multi-step actions

## 08-Applied-Implementation
- [References](08-Applied-Implementation/References.md) — **References** — All 11 source references with access status, key contribution, and mapping to wiki sections.
- [UC1 Complaint Classification Overview](08-Applied-Implementation/UC1-Complaint-Classification-Overview.md) — **UC1: Complaint Theme Classification — Overview** — > **System:** LLM classifier assigning business themes to 100,000+ formal property client feedback per year
- [UC1 Deidentified Examples](08-Applied-Implementation/UC1-Deidentified-Examples.md) — **Deidentified Complaint Examples** — > **Privacy notice:** All identifying information (agency names, agent names, property addresses, individual names) has 
- [UC1 Eval Design Step by Step](08-Applied-Implementation/UC1-Eval-Design-Step-by-Step.md) — **UC1: Eval Design — Step by Step** — The 8-step process for building a production-grade eval suite for complaint theme classification.
- [UC2 RAG Chatbot Overview](08-Applied-Implementation/UC2-RAG-Chatbot-Overview.md) — **UC2: RAG Chatbot — Overview** — > **System:** Conversational chatbot allowing regulatory staff to query complaint data without writing SQL
- [UC2 The 6 RAG Evals](08-Applied-Implementation/UC2-The-6-RAG-Evals.md) — **The 6 RAG Evals** — > *"There are only 6 RAG evals."* — Jason Liu, [jxnl.co](https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/)

## 09-Tools-and-Platforms
- [building mlflow evaluation datasets](09-Tools-and-Platforms/building-mlflow-evaluation-datasets.md) — The content aligns with the 09-Tools-and-Platforms folder's focus on MLflow-specific evaluation implementation details.
- [tutorial evaluate and improve a genai application](09-Tools-and-Platforms/tutorial-evaluate-and-improve-a-genai-application.md) — The content aligns with 09-Tools-and-Platforms' focus on MLflow-specific evaluation implementation, demonstrating practical application of e
- [evaluate and monitor ai agents](09-Tools-and-Platforms/evaluate-and-monitor-ai-agents.md) — The content discusses MLflow's evaluation and monitoring capabilities for AI agents, aligning with the 09-Tools-and-Platforms folder's focus
- [mlflow tracing genai observability](09-Tools-and-Platforms/mlflow-tracing-genai-observability.md) — The content fits under 09-Tools-and-Platforms as it discusses MLflow's tracing feature for GenAI observability, aligning with the folder's f

## 10-Graph-RAG
- [graphrag introduction](10-Graph-RAG/graphrag-introduction.md) — The content introduces GraphRAG as a significant advancement in LLM capabilities using knowledge graphs, aligning with the 10-Graph-RAG fold

## 11-Community-Detection
- [leiden technique](11-Community-Detection/leiden-technique.md) — The content introduces a novel community detection algorithm (Leiden) not covered by existing folders, requiring a new category for network

## Checklists
- [Error Analysis Checklist](Checklists/Error-Analysis-Checklist.md) — **Checklist: Error Analysis Session** — Run this before starting any error analysis session. The structure prevents the two most common mistakes: jumping to aut
- [Eval Design Checklist](Checklists/Eval-Design-Checklist.md) — **Checklist: Eval Design (Before Building Any LLM System)** — Use this before writing the first line of code or the first prompt. The discipline of defining "good" in advance is what
- [LLM Judge Quality Checklist](Checklists/LLM-Judge-Quality-Checklist.md) — **Checklist: LLM Judge Quality** — Before deploying an LLM judge for automated scoring, verify all items below. An unvalidated judge is not a judge — it is
- [RAG Eval Coverage Checklist](Checklists/RAG-Eval-Coverage-Checklist.md) — **Checklist: RAG Eval Coverage** — All 6 RAG evals must be covered before a RAG system is production-ready. Skip any and you have a blind spot that will pr

## Diagrams
- [Error Analysis Workflow](Diagrams/Error-Analysis-Workflow.md) — **Diagram: Error Analysis Workflow** — *The 5-step error analysis loop — the highest ROI technique in AI engineering.*
- [Eval Pipeline Architecture](Diagrams/Eval-Pipeline-Architecture.md) — **Diagram: Eval Pipeline Architecture** — *Full end-to-end evaluation pipeline for the complaint classification system (UC1).*
- [Hamel LLM Judge Recreation](Diagrams/Hamel-LLM-Judge-Recreation.md) — **Hamel LLM Judge — Diagram Recreation** — > **Source:** Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/llm-judge/)
- [RAG Evals Framework](Diagrams/RAG-Evals-Framework.md) — **Diagram: RAG Evals Framework** — *The 6 RAG evals mapped to the complaints chatbot pipeline.*
