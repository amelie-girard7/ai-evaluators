"""Compile unprocessed sources in raw/ into wiki articles.

For each source:
  1. Ask the model to classify: append-to-existing or create-new.
  2. Either rewrite the target article or create a fresh one.
  3. Update wiki/INDEX.md, append wiki/LOG.md, mark source processed.

Designed for local Ollama (qwen2.5:14b). One source per call. Reads INDEX +
at most 3 candidate articles, never the whole wiki at once.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from _common import (INDEX, RAW, WIKI, append_log, list_articles,
                     list_unprocessed, load_schema_snippet, ollama_chat,
                     read_md, slugify, today, write_md)

CLASSIFY_SYS = """You are the librarian of a wiki on LLM evaluation. Decide whether new source content fits an existing article or warrants a new one. Respond ONLY with JSON: {"action": "append"|"create", "target": "<existing article path or new folder>", "title": "<article title>", "reason": "<one sentence>"}. NEVER target Home.md. Use these folders: 01-Foundations (why evals, maturity, eval types, unit/human evals), 02-Building-Evals (datasets, synthetic data), 03-LLM-Judges (judge design, validation, evaluator design), 04-Metrics-and-Scoring (binary vs likert, generic metrics), 05-Error-Analysis, 06-Eval-Lifecycle (lifecycle, EDD, roadmap, production, observability), 07-Agent-Evals, 08-Applied-Implementation (use cases), 09-Tools-and-Platforms (Databricks, MLflow, tracing tools), 10-Graph-RAG (graph-based retrieval, DRIFT, knowledge graphs). Create a new folder if none fit."""

HOME_SYS = """You are maintaining a wiki on LLM evaluation. Write a Home.md index page that organises all wiki articles around the four phases of the eval lifecycle. Use this exact structure:

## Phase 1: Design (Before You Build)
## Phase 2: Development (Build and Iterate)
## Phase 3: Pre-Production (Before Launch)
## Phase 4: Production (After Launch)

Under each phase, list the relevant wiki articles as [[Folder/Article|Title]] links with a one-sentence description of what each covers. Include a short intro paragraph before the phases. Output ONLY the full markdown including YAML frontmatter (title, tags, last_updated)."""

MERGE_SYS = """You are maintaining a wiki on LLM evaluation. Merge new source content into the existing article. Preserve existing structure, citations, and headers. Add a 'sources' frontmatter entry. Use Mermaid for diagrams. Wiki-links use [[Folder/Article]] form. Ignore and do not reproduce any sponsored sections, advertisements, or promotional content for specific tools. Output ONLY the full merged markdown article including frontmatter."""

CREATE_SYS = """You are maintaining a wiki on LLM evaluation. Create a new wiki article from the source content. Use H2 headers, frontmatter (title, tags, last_updated, sources), Mermaid for diagrams, and [[Folder/Article]] wiki-links to related topics. Ignore and do not reproduce any sponsored sections, advertisements, or promotional content for specific tools. Output ONLY the full markdown article including frontmatter."""


def _strip_sponsored(body: str) -> str:
    # Lead-in line: "*...sponsor/opik...* ↓"
    body = re.sub(r"\*[^*\n]*(?:sponsor|opik)[^*\n]*\*\s*↓?\n?", "", body, flags=re.IGNORECASE)
    # Dedicated sponsor section: "## ... (Sponsored)" heading through next "---" or end
    body = re.sub(r"##[^\n]*\(Sponsored\)[^\n]*\n.*?(?=\n---|\Z)", "", body, flags=re.DOTALL | re.IGNORECASE)
    # Closing thanks + banner: "*Thanks again to [Opik]..." through next heading or end
    body = re.sub(r"\*Thanks again to \[Opik\].*?(?=\n##|\Z)", "", body, flags=re.DOTALL | re.IGNORECASE)
    return body


def _index_lines() -> str:
    return INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""


def _candidate_articles(target_hint: str, k: int = 3) -> list[Path]:
    """Cheap lexical match: rank articles by token overlap with the hint."""
    hint = set(re.findall(r"[a-z]{4,}", target_hint.lower()))
    arts = list_articles()
    scored = []
    for p in arts:
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        score = sum(1 for tok in hint if tok in text)
        scored.append((score, p))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in scored[:k]]


def _classify(source_body: str, source_title: str) -> dict:
    user = (
        f"INDEX.md:\n```\n{_index_lines()}\n```\n\n"
        f"NEW SOURCE TITLE: {source_title}\n\n"
        f"NEW SOURCE EXCERPT (first 2000 chars):\n{source_body[:2000]}\n\n"
        "Decide append vs create. JSON only."
    )
    raw = ollama_chat(CLASSIFY_SYS, user)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(m.group(0)) if m else {"action": "create", "target": "wiki/", "title": source_title, "reason": "fallback"}


def _update_index(article_path: Path, summary: str) -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    rel = article_path.relative_to(WIKI).with_suffix("")
    line = f"- [[{rel}]] — {summary}"
    if not INDEX.exists():
        INDEX.write_text("# Wiki Index\n\n", encoding="utf-8")
    text = INDEX.read_text(encoding="utf-8")

    # If the entry already exists, just update it in place.
    pattern = re.compile(rf"^- \[\[{re.escape(str(rel))}\]\].*$", re.MULTILINE)
    if pattern.search(text):
        INDEX.write_text(pattern.sub(line, text), encoding="utf-8")
        return

    # Otherwise insert under the correct `## <folder>` heading, creating it
    # if missing. The folder is the first path component (e.g. "06-Eval-Lifecycle").
    section = rel.parts[0] if len(rel.parts) > 1 else "Misc"
    heading_re = re.compile(rf"^## {re.escape(section)}\s*$", re.MULTILINE)
    m = heading_re.search(text)
    if m:
        # Find the end of this section: next "## " or EOF.
        next_heading = re.search(r"^## ", text[m.end():], re.MULTILINE)
        if next_heading:
            insert_at = m.end() + next_heading.start()
            new_text = text[:insert_at].rstrip() + "\n" + line + "\n\n" + text[insert_at:]
        else:
            new_text = text.rstrip() + "\n" + line + "\n"
    else:
        # Append a new section. Keep sections in lexicographic order so numeric
        # folder prefixes (01, 02, …) sort naturally.
        sections = sorted(set(re.findall(r"^## (.+)$", text, re.MULTILINE)) | {section})
        idx = sections.index(section)
        if idx == len(sections) - 1:
            new_text = text.rstrip() + f"\n\n## {section}\n{line}\n"
        else:
            after = sections[idx + 1]
            after_match = re.search(rf"^## {re.escape(after)}\s*$", text, re.MULTILINE)
            insert_at = after_match.start()
            new_text = text[:insert_at].rstrip() + f"\n\n## {section}\n{line}\n\n" + text[insert_at:]
    INDEX.write_text(new_text, encoding="utf-8")


def _build_home() -> None:
    articles = list_articles()
    article_list = "\n".join(
        f"- {p.relative_to(WIKI).with_suffix('')} — {p.stem.replace('-', ' ')}"
        for p in sorted(articles)
        if p.name not in {"Home.md", "INDEX.md", "LOG.md"}
    )
    index = _index_lines()
    user = (
        f"WIKI INDEX:\n```\n{index}\n```\n\n"
        f"ALL ARTICLES:\n{article_list}\n\n"
        f"Write the Home.md index page. last_updated: {today()}."
    )
    home = WIKI / "Home.md"
    home.write_text(ollama_chat(HOME_SYS, user).strip() + "\n", encoding="utf-8")
    print("built: wiki/Home.md")


def _process_one(source_path: Path) -> None:
    fm, body = read_md(source_path)
    body = _strip_sponsored(body)
    title = fm.get("title", source_path.stem)
    decision = _classify(body, title)

    # Never let qwen append to Home.md — it is built separately by _build_home()
    if "home" in decision.get("target", "").lower():
        decision["action"] = "create"
        decision["target"] = "Misc"

    candidates = _candidate_articles(decision.get("target", "") + " " + title, k=3)
    cand_blob = "\n\n---\n\n".join(
        f"PATH: {p.relative_to(WIKI)}\n{p.read_text(encoding='utf-8', errors='ignore')[:3000]}"
        for p in candidates
    )

    rel_source = source_path.relative_to(RAW.parent)
    if decision["action"] == "append" and candidates:
        target = candidates[0]
        user = (
            f"EXISTING ARTICLE ({target.relative_to(WIKI)}):\n```\n{target.read_text(encoding='utf-8')}\n```\n\n"
            f"NEW SOURCE ({rel_source}):\n```\n{body[:8000]}\n```\n\n"
            f"Merge. Add '{rel_source}' to sources frontmatter. Output the full updated article."
        )
        merged = ollama_chat(MERGE_SYS, user)
        target.write_text(merged.strip() + "\n", encoding="utf-8")
        article = target
        action = "append"
    else:
        target_dir = WIKI / (decision.get("target", "Misc") or "Misc")
        if target_dir.is_file() or target_dir.suffix:
            target_dir = WIKI / "Misc"
        target_dir.mkdir(parents=True, exist_ok=True)
        article_title = decision.get("title") or title
        article = target_dir / f"{slugify(article_title)}.md"
        user = (
            f"NEAREST EXISTING ARTICLES (for backlinks):\n{cand_blob}\n\n"
            f"NEW SOURCE ({rel_source}), title '{article_title}':\n```\n{body[:8000]}\n```\n\n"
            f"Write the new article. Frontmatter must include sources: ['{rel_source}'] and last_updated: {today()}."
        )
        article.write_text(ollama_chat(CREATE_SYS, user).strip() + "\n", encoding="utf-8")
        action = "create"

    summary = decision.get("reason", title)[:140]
    _update_index(article, summary)
    fm["processed"] = True
    fm.setdefault("processed_at", today())
    write_md(source_path, fm, body)
    append_log(f"{action} | {rel_source} | {article.relative_to(WIKI.parent)}")
    print(f"{action}: {article.relative_to(WIKI.parent)}")


def _unload_model() -> None:
    import subprocess
    subprocess.run(["ollama", "stop", "qwen3:14b"], check=False)


def main() -> None:
    sources = list_unprocessed()
    if not sources:
        print("nothing to process")
    try:
        for s in sources:
            try:
                _process_one(s)
            except Exception as e:
                print(f"FAILED {s}: {e}")
                append_log(f"error | {s.relative_to(RAW.parent)} | {e!r}")
        _build_home()
    finally:
        _unload_model()


if __name__ == "__main__":
    main()
