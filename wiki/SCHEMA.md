---
title: Wiki Schema (Reading Map)
tags: [meta, schema]
last_updated: 2026-05-02
---

# Wiki Schema — How To Read This Wiki

This file describes **what each folder is for** and **how to navigate the wiki**.
It is the human-facing companion to `AGENTS.md` (which is the operational schema for compile/lint).

> **Looking for the actual synthesis of knowledge?** Start at [Home](Home.md). Each folder below is a layer of evidence underneath that synthesis.

---

## The two layers

| Layer | What lives there | Purpose |
|---|---|---|
| **Synthesis** | [Home](Home.md) + the four checklists in `Checklists/` | Answers the 7 core questions and the 3 lifecycle stages. **Read this first.** |
| **Evidence** | `01–11` topic folders | One article per source. Cited *from* the synthesis layer. **Read this when you want depth on one topic.** |

The wiki is not a flat list of articles — it is a synthesis on top of an evidence base.

---

## The 7 questions the wiki must answer

Every reader should be able to answer these after reading `Home.md`:

1. **How to integrate evals into your app** → `06-Eval-Lifecycle/Integrating-Evals`
2. **How to build an evals dataset** → `02-Building-Evals/build-an-ai-evals-dataset-from-scratch`
3. **How to use synthetic data correctly** → `02-Building-Evals/Generate-Synthetic-Datasets`
4. **How to design evaluators** → `03-LLM-Judges/LLM-as-Judge-Complete-Guide`
5. **How to validate evaluators** → `03-LLM-Judges/Validation-Protocol`
6. **How to evaluate RAG systems** → `08-Applied-Implementation/UC2-The-6-RAG-Evals`
7. **What evals look like in production** → `06-Eval-Lifecycle/behind-the-scenes-of-ai-observability-in-production`

If a future article cannot be tied to one of these seven, it probably belongs in `raw/` as a source, not in `wiki/`.

---

## The 3 lifecycle stages (where evals run)

| Stage | Goal | What runs | Primary articles |
|---|---|---|---|
| **Dev → Optimization** | Test prompts, compare variants, iterate fast | Unit evals + LLM judges on a small dev set | [Unit Evals](01-Foundations/Unit-Evals.md), [LLM as Judge Complete Guide](03-LLM-Judges/LLM-as-Judge-Complete-Guide.md) |
| **Pre-merge → Regression** | New changes don't break existing behaviour | Frozen eval set in CI with must-pass thresholds | [Integrating Evals](06-Eval-Lifecycle/Integrating-Evals.md), [Eval Design Checklist](Checklists/Eval-Design-Checklist.md) |
| **Prod → Monitoring** | Catch failures on real user traffic | Sampled live data, drift alerts, error analysis loop | [behind the scenes of ai observability in production](06-Eval-Lifecycle/behind-the-scenes-of-ai-observability-in-production.md), [Overview](05-Error-Analysis/Overview.md) |

Every article should be tagged in its frontmatter with at least one of `stage: dev | pre-merge | prod` so `Home.md` can route readers correctly. (Tag added on next edit, not retroactively.)

---

## Folder map

| Folder | Owns | Examples |
|---|---|---|
| `01-Foundations` | What evals are; when to use which type | Eval-Types-Overview, Unit-Evals, Human-Evals, Why-Evals-Matter, Eval-Maturity-Ladder |
| `02-Building-Evals` | Datasets — real, synthetic, and the build process | build-an-ai-evals-dataset-from-scratch, Generate-Synthetic-Datasets |
| `03-LLM-Judges` | Designing & validating LLM judges | LLM-as-Judge-Complete-Guide, Validation-Protocol |
| `04-Metrics-and-Scoring` | Choosing the right scoring scheme | Binary-vs-Likert, Mirage-of-Generic-Metrics |
| `05-Error-Analysis` | The highest-ROI iteration loop | Overview, Case-Studies |
| `06-Eval-Lifecycle` | When evals run across dev/pre-merge/prod | Integrating-Evals, EDD-Framework, observability-in-production, Evals-Are-NOT-All-You-Need |
| `07-Agent-Evals` | Multi-step / agentic evaluation | Demystifying-Agent-Evals |
| `08-Applied-Implementation` | The two reference use cases (UC1 classifier, UC2 RAG) | UC1-*, UC2-* |
| `09-Tools-and-Platforms` | MLflow / Databricks / observability tools | mlflow-tracing-genai-observability, evaluate-and-monitor-ai-agents |
| `10-Graph-RAG` | GraphRAG-specific retrieval | graphrag-introduction |
| `11-Community-Detection` | Clustering / graph algorithms | leiden-technique |
| `Checklists/` | Distilled action checklists. **Every checklist must trace back to evidence in 01–11.** | Eval-Design, LLM-Judge-Quality, Error-Analysis, RAG-Eval-Coverage |
| `Diagrams/` | Standalone Mermaid + SVG diagrams reused across articles | Hamel-LLM-Judge-Recreation, RAG-Evals-Framework |

---

## Summary pages — table of contents required

Any **summary or briefing page** (a page that synthesises across multiple topics — `Home.md`, future overview pages, multi-section reference pages) opens with a `## Contents` section listing every `##` and `###` heading in the page, before the first content section. The TOC sits immediately after the page's introductory paragraph and before §1.

Format:

```markdown
## Contents

1. [Section title](#anchor)
2. [Section title](#anchor)
   - [Subsection](#anchor)
   - [Subsection](#anchor)
3. …
```

A reader who lands on the page should see the full shape of the document before scrolling. This rule does not apply to single-topic articles in the topic folders (`01-…`/`11-…`) — those are short enough that a TOC adds friction.

## Article style — the "Hamel-step" convention

Articles answering a "how to" question follow this structure:

```
---
title: …
tags: […]
stage: dev | pre-merge | prod   # which lifecycle stage(s) this serves
last_updated: YYYY-MM-DD
sources: […]
---

# Title

> Pull-quote (optional)

## Step 1: <imperative verb + concrete object>
…
## Step 2: …
…
## Common pitfalls
…
## Sources
- [Article Name](relative/path.md) — what was lifted from it
```

The **Step N** structure is the canonical form for any article in `01–08` that teaches a workflow. Conceptual / reference articles (taxonomies, comparisons) use H2 sections instead of steps.

---

## What this schema rules OUT

To prevent regression to the redundant state we just cleaned up:

- **No two articles in the same folder may answer the same question.** If they do, the older one gets merged into the newer canonical one and deleted, with a `LOG.md` entry.
- **No article without a `sources:` frontmatter list.** An article with no source is a draft and lives in `raw/notes/` until it cites something.
- **No course-TOC dumps in `wiki/`.** Multi-section "course material" pages belong in `raw/notes/` as raw input, not as wiki articles.
- **No sponsor blocks.** `compile.py` strips them; if one slips through, delete on sight.
- **No `[Home](Home.md)` links from inside topic articles.** Home is the entry point, not a destination.

---

## Companions

- `AGENTS.md` — operational rules for the LLM agent (ingestion, naming, lint).
- `wiki/INDEX.md` — machine-readable index used by `compile.py` / `query.py`. Auto-maintained.
- `wiki/LOG.md` — append-only audit trail.
- `wiki/Home.md` — the synthesis (answers the 7 questions + maps the 3 stages).

If `AGENTS.md` and this file ever disagree, `AGENTS.md` wins for tooling behaviour and this file wins for human reading order.
