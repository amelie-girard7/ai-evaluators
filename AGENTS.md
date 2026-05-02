# AGENTS.md — LLM Wiki Schema

This file is the operational contract for any LLM agent that maintains the wiki, whether local (Ollama) or hosted. Read it in full before processing any source.

## Goal

Maintain `wiki/` as a coherent, interlinked second brain on **LLM and agentic AI evaluation**. The wiki is the durable artifact; raw sources in `raw/` are inputs, not the deliverable.

## Layout

- `raw/` — append-only source materials. Never edited after ingestion except to flip `processed: false` → `true` in frontmatter.
  - `raw/papers/` — research papers (PDF → Markdown).
  - `raw/web/` — web articles **clipped via the Obsidian Web Clipper** (`.md` + sibling folder of local images). No raw HTML, no on-demand fetches; this guarantees offline reads, vision-capable image references, and immunity to link rot.
  - `raw/notes/` — your own freeform notes.
  - `raw/INBOX.md` — queue of links/items not yet ingested.
- `wiki/` — LLM-generated articles. Editable by both human and agent.
  - `wiki/INDEX.md` — one line per article: `- [[Folder/Article]] — one-sentence summary`. The agent MUST read this before deciding where new content goes.
  - `wiki/LOG.md` — append-only audit trail. Format: `YYYY-MM-DD HH:MM | <action> | <source path> | <article(s) affected>`.
  - `wiki/<NN-Topic>/` — topic folders.
  - `wiki/Diagrams/`, `wiki/Checklists/` — special-purpose folders.
- `outputs/` — query answers and synthesis reports. Never read back by the compile step.

## Ingestion rule

Every file under `raw/` is processed exactly once. A source is "processed" when:
1. Its frontmatter `processed:` field is set to `true`.
2. A line was appended to `wiki/LOG.md` describing what changed.
3. Either an existing article was updated OR a new article was created, with the source path added to that article's frontmatter `sources:` list.

If a source cannot be processed (corrupt, off-topic, unreadable), set `processed: skipped` and log the reason.

### Per source-type handling

The compile step is identical, but the *reading strategy* differs by source type:

- **`raw/papers/` (research papers)** — read abstract, intro, method, results/limitations; skim related work. Extract: claim, evidence, dataset, metric, sample size, caveat. Cite figures/tables explicitly when they carry the argument. Long papers may legitimately spawn 2–3 articles (one per distinct contribution).
- **`raw/web/` (Obsidian Web Clipper output)** — treat the `.md` as the canonical text; treat the sibling image folder as figures the agent may *reference by relative path* in wiki articles (vision-capable models can read them, others should still cite them). Strip clipper boilerplate (cookie banners, nav, related-posts) before merging into the wiki. Web posts are usually opinionated — quote the author's strongest claim verbatim and attribute it.
- **`raw/notes/` (personal notes, including video/podcast transcripts)** — already curated; do not re-summarise heavily. Lift quotable lines, pair them with the timestamp or section header, and merge.
- **Repos / code dumps** — not currently ingested. If one is added later, place at `raw/code/<repo>/` and treat the README + the top-level entrypoint as the primary source; everything else is reference, not summarised.

## Compile rule

For each unprocessed source:
1. Read `wiki/INDEX.md` in full.
2. Decide: does this content fit an existing article (append) or warrant a new one (create)? Prefer append unless the topic is genuinely new.
3. If append: read the target article, write the merged version preserving existing structure and citations.
4. If create: place under the most relevant `<NN-Topic>/` folder; use the next available filename.
5. Update `wiki/INDEX.md` (add or update the line).
6. Insert backlinks (`[[Folder/Article]]`) from related articles where natural.
7. Append to `wiki/LOG.md`.
8. Set `processed: true` on the source frontmatter.

## Article conventions

- Markdown only. One topic per file.
- Frontmatter (YAML):
  ```yaml
  ---
  title: <human title>
  tags: [eval, rag, judge, ...]
  last_updated: YYYY-MM-DD
  sources:
    - raw/papers/<file>.md
    - raw/web/<file>.md
  ---
  ```
- Use H2 (`##`) for major sections.
- Mermaid for diagrams (Obsidian renders it natively).
- Wiki-style links: `[[Folder/Article]]` (Obsidian-compatible).
- Inline citations: cite the source path, e.g. `(see raw/papers/anthropic-2024-judges.md)`.

### Naming conventions

- **Topic folders**: `wiki/<NN>-<Topic-Title-Case>/` — two-digit prefix establishes reading order; gaps allowed (e.g. 01, 02, 05) so insertions don't renumber siblings.
- **Article filenames**: `Title-Case-Hyphenated.md`. No spaces, no underscores, no dates, no version suffixes. The filename *is* the wiki-link target — keep it stable. Renames require updating every inbound `[[...]]` link.
- **Source filenames in `raw/`**: kebab-case slugs (`hamel-llm-judge.md`, `anthropic-demystifying-evals.md`). Web Clipper's default title-based filenames are acceptable as long as they remain unique.
- **Image folders for clipped pages**: same slug as the `.md`, sibling location.
- **Outputs**: `outputs/YYYY-MM-DD-<query-slug>.md`.

### Backlink rule

When an article mentions a concept that has its own article, replace the first mention with a `[[Folder/Article]]` link. Do not link every mention — once per article is enough. After creating a new article, scan the 3 most-related existing articles and insert a link from each (this is what creates the bidirectional graph).

## Conflict resolution

If a new source contradicts an existing claim, do NOT silently overwrite. Add a `## Contradictions` section that quotes both sources and flags the disagreement. The human resolves it later.

## Query routing — `outputs/` vs inline

Not every question needs a file written. Decide by *durability*:

- **Inline answer (no file written)** — quick lookups, definitional questions, "where is X documented", anything the user is likely to read once and discard. The agent answers in chat and stops.
- **Write to `outputs/YYYY-MM-DD-<slug>.md`** — synthesis across ≥2 articles, comparisons, decision memos, anything the user said "write up" or "draft", and any answer the user might want to cite later. The file must list, in frontmatter, the `articles:` consulted and the original `query:`.
- **Never** write a query answer back into `wiki/`. The wiki is sourced from `raw/`, not from prior queries — that path leads to a feedback loop where the model cites itself.

If unsure, ask the user once: "inline or written up?"

## Linting rules (run `tools/lint.py` weekly)

Flag (do not auto-fix):
- Articles with no inbound backlinks (orphans).
- `INDEX.md` entries pointing at missing files.
- Sources in `raw/` with `processed: false` older than 7 days.
- Sources in `raw/` with no entry in `LOG.md` even though `processed: true` (audit gap).
- Articles with `last_updated` older than 90 days where `sources` references a file modified more recently.

## Local-model concession (when running on Ollama 8–14B)

Frontier long-context models can hold the whole INDEX + several articles in context. Local 14B models cannot. So:
- Process ONE source per LLM call.
- Read INDEX + at most the 3 most likely target articles, not the whole `wiki/`.
- Use temperature 0.2 and `num_ctx` ≥ 16384.
- If the merged article would exceed ~3000 tokens, split it into a parent + child article rather than letting it sprawl.

## Hard rules (do not violate)

1. Never delete from `raw/`. Mark, don't remove.
2. Never edit `wiki/LOG.md` history; only append.
3. Never invent source citations. Every claim in `wiki/` must trace to a file in `raw/` (or be marked `# unsourced` for the human to verify).
4. Never embed binaries in the repo; link to them.

## Schema co-evolution

This file is not frozen. As the wiki grows, ingestion and naming rules will reveal weaknesses — a source type the schema didn't anticipate, a linting check that produces false positives, a folder convention that collapses under a new topic. When that happens:

1. Propose the schema change in chat first; do not edit `AGENTS.md` silently mid-task.
2. Once accepted, update `AGENTS.md` in its own commit (separate from any content changes that motivated it), with a one-line rationale.
3. If the change invalidates existing articles (e.g. a renamed folder convention), open a follow-up task to migrate them — do not leave the wiki in two regimes.

The schema serves the wiki, not the other way around. Karpathy's framing: the schema and the corpus co-evolve — expect 3–5 schema revisions in the first hundred sources, then it stabilises.
