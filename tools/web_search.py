"""Search DuckDuckGo and ingest top N results as markdown into raw/web/.

Usage:
  python tools/web_search.py "rag eval gold dataset" --n 5
"""
from __future__ import annotations

import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md

from _common import RAW, slugify, today, write_md

UA = "Mozilla/5.0 (Macintosh; Apple Silicon Mac OS X 14_0) AppleWebKit/605.1.15"


def search(query: str, n: int) -> list[tuple[str, str]]:
    from ddgs import DDGS
    with DDGS() as d:
        return [(r["title"], r["href"]) for r in d.text(query, max_results=n)]


def fetch_md(url: str) -> tuple[str, str]:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "nav", "footer", "aside"]):
        t.decompose()
    title = (soup.title.string.strip() if soup.title and soup.title.string else url)
    body = html_to_md(str(soup.body or soup), heading_style="ATX")
    return title, body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("--n", type=int, default=5)
    args = ap.parse_args()
    q = " ".join(args.query)

    out_dir = RAW / "web"
    out_dir.mkdir(parents=True, exist_ok=True)

    for title, url in search(q, args.n):
        try:
            t, body = fetch_md(url)
        except Exception as e:
            print(f"skip {url}: {e}")
            continue
        out = out_dir / f"{today()}-{slugify(t or title)}.md"
        write_md(out, {
            "title": t or title,
            "source_url": url,
            "ingested_at": today(),
            "search_query": q,
            "processed": False,
        }, body)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
