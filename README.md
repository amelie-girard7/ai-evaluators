# LLMKnowledgeBase

A personal "second brain" — a local-first, LLM-compiled wiki built on Karpathy's pattern: **raw sources → schema → LLM-authored wiki**, with no vector DB and no embeddings. The current topic area is **LLM and agentic AI evaluation**; future topics live as additional folders inside `wiki/`.

## How it works

1. **Drop a source into `raw/`.**
   - Research papers: PDF → Markdown into `raw/papers/`.
   - Web articles: clip via the **Obsidian Web Clipper** into `raw/web/`. The clipper saves images locally next to the `.md`, so the wiki has no external URLs and no link rot, and a vision-capable model can read the figures.
   - Personal notes: free-form Markdown into `raw/notes/`.
2. **Run the compiler.** `tools/compile.py` reads each unprocessed source, consults `wiki/INDEX.md`, and either appends to an existing article or creates a new one — one source per LLM call, against local Ollama (`qwen3:14b`).
3. **Query the wiki.** `tools/query.py "your question"` reads the index, pulls the relevant articles, and writes the answer to `outputs/`.
4. **Lint periodically.** `tools/lint.py` flags orphans, broken links, stale articles, and unprocessed sources.

The agent contract — file layout, frontmatter, ingestion rules, conflict handling — lives in [`AGENTS.md`](AGENTS.md). Read it before editing anything in `wiki/`.

## Layout

```
LLMKnowledgeBase/
├── AGENTS.md      # schema and rules for the wiki agent
├── raw/           # sources (committed; append-only)
├── wiki/          # LLM-authored articles (committed)
├── outputs/       # query answers (gitignored)
└── tools/         # ingest, compile, query, lint (Ollama)
```

## Setup

```bash
pip install -r requirements.txt
# install Ollama from https://ollama.com, then:
ollama pull qwen3:14b
```

## Why this design

- **Local-first.** No cloud LLM costs; the wiki survives offline.
- **No RAG.** The schema keeps the index small enough for a 14B model to navigate by reading `wiki/INDEX.md` directly.
- **Durable artefacts.** `wiki/` is the deliverable; `raw/` is just substrate. Web content is captured at clip time, never re-fetched.
