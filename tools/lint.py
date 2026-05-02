"""Wiki health check. No LLM call."""
from __future__ import annotations

import datetime as dt
import re
from collections import defaultdict
from pathlib import Path

from _common import INDEX, LOG, RAW, WIKI, list_articles, read_md

LINK_RE = re.compile(r"\[\[([^\]\|]+?)(?:\|[^\]]+)?\]\]")


def main() -> int:
    issues: list[str] = []

    articles = list_articles()
    article_set = {p.relative_to(WIKI).with_suffix("").as_posix() for p in articles}

    inbound: dict[str, set[str]] = defaultdict(set)
    for p in articles:
        body = p.read_text(encoding="utf-8", errors="ignore")
        for m in LINK_RE.finditer(body):
            inbound[m.group(1).strip()].add(p.relative_to(WIKI).with_suffix("").as_posix())

    for art in article_set:
        if not inbound.get(art):
            issues.append(f"orphan article (no inbound links): wiki/{art}.md")

    if INDEX.exists():
        index_text = INDEX.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(index_text):
            target = m.group(1).strip()
            if target not in article_set:
                issues.append(f"INDEX points at missing article: {target}")

    today = dt.date.today()
    for sub in ("papers", "web", "notes"):
        d = RAW / sub
        if not d.exists():
            continue
        for src in d.glob("*.md"):
            fm, _ = read_md(src)
            ingested = fm.get("ingested_at")
            if fm.get("processed") in (False, None) and ingested:
                try:
                    age = (today - dt.date.fromisoformat(str(ingested))).days
                    if age > 7:
                        issues.append(f"stale unprocessed source ({age}d): {src.relative_to(RAW.parent)}")
                except ValueError:
                    pass

    log_text = LOG.read_text(encoding="utf-8") if LOG.exists() else ""
    for sub in ("papers", "web", "notes"):
        d = RAW / sub
        if not d.exists():
            continue
        for src in d.glob("*.md"):
            fm, _ = read_md(src)
            if fm.get("processed") is True:
                rel = src.relative_to(RAW.parent).as_posix()
                if rel not in log_text:
                    issues.append(f"processed but no LOG entry: {rel}")

    # Stale article: last_updated > 90d old AND a referenced source is newer.
    repo_root = RAW.parent
    for p in articles:
        fm, _ = read_md(p)
        last_updated = fm.get("last_updated")
        sources = fm.get("sources") or []
        if not last_updated or not sources:
            continue
        try:
            lu = dt.date.fromisoformat(str(last_updated))
        except ValueError:
            continue
        if (today - lu).days <= 90:
            continue
        for src_rel in sources:
            src_path = repo_root / str(src_rel)
            if not src_path.exists():
                continue
            src_mtime = dt.date.fromtimestamp(src_path.stat().st_mtime)
            if src_mtime > lu:
                issues.append(
                    f"stale article ({(today - lu).days}d) with newer source: "
                    f"wiki/{p.relative_to(WIKI).as_posix()} (source {src_rel} modified {src_mtime})"
                )
                break

    if not issues:
        print("OK — wiki is clean")
        return 0
    print(f"{len(issues)} issue(s):")
    for i in issues:
        print(f"  - {i}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
