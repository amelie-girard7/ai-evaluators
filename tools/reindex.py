"""Rebuild wiki/INDEX.md from the current article set.

Walks wiki/, extracts each article's first H1 (or filename if absent) and the
first non-empty paragraph as the summary, writes one line per article.
Deterministic, no LLM call.

Usage: python tools/reindex.py
"""
from __future__ import annotations

import re

from _common import INDEX, WIKI, list_articles, read_md

H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def first_summary(body: str, max_len: int = 140) -> str:
    for para in re.split(r"\n\s*\n", body):
        para = para.strip()
        if not para or para.startswith("#") or para.startswith("|") or para.startswith("```"):
            continue
        para = re.sub(r"\s+", " ", para)
        para = re.sub(r"[*_`\[\]]", "", para)
        return para[:max_len].rstrip() + ("…" if len(para) > max_len else "")
    return ""


def main() -> None:
    lines = ["# Wiki Index", "", "_One line per article — used by `query.py` and `compile.py` to route._", ""]
    grouped: dict[str, list[str]] = {}
    for p in sorted(list_articles()):
        rel = p.relative_to(WIKI).with_suffix("").as_posix()
        _, body = read_md(p)
        h1 = H1_RE.search(body)
        title = h1.group(1).strip() if h1 else p.stem.replace("-", " ")
        summary = first_summary(body)
        folder = rel.split("/")[0] if "/" in rel else "_root"
        line = f"- [[{rel}]] — **{title}** — {summary}" if summary else f"- [[{rel}]] — **{title}**"
        grouped.setdefault(folder, []).append(line)

    for folder in sorted(grouped):
        label = folder if folder != "_root" else "Top-level"
        lines.append(f"## {label}")
        lines.extend(grouped[folder])
        lines.append("")

    INDEX.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    total = sum(len(v) for v in grouped.values())
    print(f"wrote {INDEX} with {total} entries across {len(grouped)} folders")


if __name__ == "__main__":
    main()
