"""Convert a PDF or HTML file to a markdown source under raw/.

Usage:
  python tools/ingest.py <path-to-pdf-or-html> [--kind papers|web|notes] [--url URL]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from _common import RAW, slugify, today, write_md


def pdf_to_md(pdf: Path) -> tuple[str, str]:
    try:
        import pymupdf4llm
        body = pymupdf4llm.to_markdown(str(pdf))
    except Exception:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        body = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    return pdf.stem, body


def html_to_md(html: Path) -> tuple[str, str]:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
    soup = BeautifulSoup(html.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    title = (soup.title.string.strip() if soup.title and soup.title.string else html.stem)
    body = md(str(soup), heading_style="ATX")
    return title, body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--kind", choices=("papers", "web", "notes"), default=None)
    ap.add_argument("--url", default=None)
    args = ap.parse_args()

    src = Path(args.path).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"not found: {src}")

    if src.suffix.lower() == ".pdf":
        title, body = pdf_to_md(src)
        kind = args.kind or "papers"
    elif src.suffix.lower() in (".html", ".htm"):
        title, body = html_to_md(src)
        kind = args.kind or "web"
    elif src.suffix.lower() == ".md":
        title, body = src.stem, src.read_text(encoding="utf-8")
        kind = args.kind or "notes"
    else:
        raise SystemExit(f"unsupported extension: {src.suffix}")

    out_dir = RAW / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slugify(title)}.md"

    fm = {
        "title": title,
        "source_path": str(src),
        "source_url": args.url,
        "ingested_at": today(),
        "processed": False,
    }
    write_md(out_path, fm, body)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
