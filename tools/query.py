"""Answer a question against the wiki and save to outputs/.

Usage:
  python tools/query.py "what is an LLM-as-judge"
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _common import (INDEX, OUTPUTS, WIKI, now_iso, ollama_chat, slugify,
                     today)

PICK_SYS = """You are a librarian. Given a question and an INDEX of wiki articles, return JSON: {"articles": ["<path1>", "<path2>", "<path3>"]} naming up to 3 most relevant articles. Use the exact paths from the INDEX. JSON only."""

ANSWER_SYS = """Answer the user's question using ONLY the provided wiki articles. Cite each claim inline like (wiki/Folder/Article.md). If the wiki is silent on a point, say so. Do not invent facts."""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="+")
    args = ap.parse_args()
    question = " ".join(args.question)

    index_text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""

    pick_user = f"QUESTION: {question}\n\nINDEX:\n```\n{index_text}\n```\n\nJSON only."
    raw = ollama_chat(PICK_SYS, pick_user)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    picks = json.loads(m.group(0))["articles"] if m else []

    blobs = []
    for p in picks:
        path = (WIKI.parent / p.strip()) if p.strip().startswith("wiki/") else (WIKI / p.strip())
        if not path.suffix:
            path = path.with_suffix(".md")
        if path.exists():
            blobs.append(f"--- {path.relative_to(WIKI.parent)} ---\n{path.read_text(encoding='utf-8')}")
    if not blobs:
        for p in WIKI.rglob("*.md"):
            if p.name in {"INDEX.md", "LOG.md"}:
                continue
            blobs.append(f"--- {p.relative_to(WIKI.parent)} ---\n{p.read_text(encoding='utf-8')[:1500]}")
            if len(blobs) >= 3:
                break

    answer_user = f"QUESTION: {question}\n\nWIKI ARTICLES:\n{chr(10).join(blobs)}"
    answer = ollama_chat(ANSWER_SYS, answer_user, temperature=0.1)

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    out = OUTPUTS / f"{today()}-{slugify(question, 50)}.md"
    out.write_text(
        f"# {question}\n\n_Answered {now_iso()}_\n\n{answer}\n\n## Sources consulted\n"
        + "\n".join(f"- {p}" for p in picks),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print()
    print(answer)


if __name__ == "__main__":
    main()
