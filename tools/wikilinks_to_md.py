"""Convert Obsidian-style [[Folder/Article]] and [[Folder/Article|Alias]] wiki-links
into standard markdown links with relative paths, so the wiki renders correctly
on GitHub-flavored-markdown viewers (Azure DevOps, Databricks, etc.).

Idempotent: running twice is a no-op. Skips fenced code blocks. Reports any
target that does not resolve to an existing wiki/<target>.md file.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"

WIKILINK_RE = re.compile(r"\[\[([^\]\|]+?)(?:\|([^\]]+))?\]\]")
FENCE_RE = re.compile(r"^```")


def basename_display(target: str) -> str:
    """Last path component, stripped of leading ordinal, hyphens-to-spaces."""
    last = target.rstrip("/").split("/")[-1]
    return last.replace("-", " ")


def convert_file(md: Path) -> tuple[int, list[str]]:
    text = md.read_text(encoding="utf-8")
    out_lines: list[str] = []
    in_fence = False
    replaced = 0
    broken: list[str] = []

    for line in text.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        def _sub(m: re.Match[str]) -> str:
            nonlocal replaced
            target = m.group(1).strip()
            alias = (m.group(2) or "").strip()
            target_path = WIKI / f"{target}.md"
            if not target_path.exists():
                broken.append(f"{md.relative_to(REPO)}: [[{target}]] -> wiki/{target}.md (missing)")
                return m.group(0)
            rel = os.path.relpath(target_path, md.parent)
            display = alias or basename_display(target)
            replaced += 1
            return f"[{display}]({rel})"

        out_lines.append(WIKILINK_RE.sub(_sub, line))

    new_text = "".join(out_lines)
    if new_text != text:
        md.write_text(new_text, encoding="utf-8")
    return replaced, broken


def main() -> int:
    total = 0
    all_broken: list[str] = []
    files = sorted(WIKI.rglob("*.md"))
    for md in files:
        n, broken = convert_file(md)
        total += n
        all_broken.extend(broken)
        if n:
            print(f"  {md.relative_to(REPO)}: {n} link(s)")
    print(f"\nconverted {total} wiki-links across {len(files)} file(s)")
    if all_broken:
        print(f"\n{len(all_broken)} broken target(s):")
        for b in all_broken:
            print(f"  - {b}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
