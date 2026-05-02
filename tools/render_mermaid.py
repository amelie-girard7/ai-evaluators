"""Pre-render every ```mermaid block in wiki/*.md to SVG via mmdc, replace the
fenced block in the source .md with an image reference. Idempotent: only
re-renders blocks whose source hash has changed.

Output layout:
  wiki/Diagrams/auto/<file-slug>-<index>.png   - rendered diagram
  wiki/Diagrams/auto/<file-slug>-<index>.mmd   - source kept editable

Usage:
  python3 tools/render_mermaid.py            # render + rewrite .md files
  python3 tools/render_mermaid.py --check    # report pending blocks, exit 1 if any

Requires mmdc on PATH (verified: /opt/homebrew/bin/mmdc).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"
AUTO_DIR = WIKI / "Diagrams" / "auto"
MERMAID_RE = re.compile(r"^```mermaid\s*$(.*?)^```\s*$", re.DOTALL | re.MULTILINE)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def short_alt(mermaid_src: str, fallback: str) -> str:
    for line in mermaid_src.splitlines():
        m = re.search(r"\[([^\]\n]{3,60})\]", line)
        if m:
            return re.sub(r"<br/?>", " ", m.group(1)).strip()
    return fallback


def find_blocks(text: str) -> list[tuple[int, int, str]]:
    return [(m.start(), m.end(), m.group(1).strip()) for m in MERMAID_RE.finditer(text)]


def render_one(src: str, out_svg: Path) -> None:
    out_svg.parent.mkdir(parents=True, exist_ok=True)
    mmd_path = out_svg.with_suffix(".mmd")
    mmd_path.write_text(src + "\n", encoding="utf-8")
    result = subprocess.run(
        ["mmdc", "-i", str(mmd_path), "-o", str(out_svg), "-b", "white", "-w", "1600", "-q"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"mmdc failed for {out_svg.name}:\n{result.stderr}")


def process(md: Path, write: bool, errors: list[str]) -> tuple[int, int]:
    text = md.read_text(encoding="utf-8")
    blocks = find_blocks(text)
    if not blocks:
        return 0, 0

    file_slug = slugify(md.stem)
    rendered = 0
    new_text_parts: list[str] = []
    cursor = 0

    for idx, (start, end, src) in enumerate(blocks, start=1):
        new_text_parts.append(text[cursor:start])
        h = hashlib.sha1(src.encode("utf-8")).hexdigest()[:8]
        svg_name = f"{file_slug}-{idx}-{h}.png"
        svg_path = AUTO_DIR / svg_name
        rel = os.path.relpath(svg_path, md.parent)
        alt = short_alt(src, f"Diagram {idx}")
        replacement = f"![{alt}]({rel})"

        if write:
            if not svg_path.exists():
                try:
                    render_one(src, svg_path)
                    rendered += 1
                    print(f"  rendered {svg_path.relative_to(REPO)}")
                except RuntimeError as e:
                    errors.append(f"{md.relative_to(REPO)} block {idx}: {e}")
                    new_text_parts.append(text[start:end])
                    cursor = end
                    continue
            new_text_parts.append(replacement)
        cursor = end

    if write:
        new_text_parts.append(text[cursor:])
        new_text = "".join(new_text_parts)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
    return len(blocks), rendered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, do not modify files")
    args = ap.parse_args()

    files = sorted(WIKI.rglob("*.md"))
    total_blocks = 0
    total_rendered = 0
    files_with_blocks: list[Path] = []
    errors: list[str] = []

    for md in files:
        if AUTO_DIR in md.parents:
            continue
        n, r = process(md, write=not args.check, errors=errors)
        total_blocks += n
        total_rendered += r
        if n:
            files_with_blocks.append(md)

    if args.check:
        if files_with_blocks:
            print(f"{total_blocks} unrendered Mermaid block(s) across {len(files_with_blocks)} file(s):")
            for f in files_with_blocks:
                print(f"  - {f.relative_to(REPO)}")
            return 1
        print("OK — no unrendered Mermaid blocks")
        return 0

    print(f"\nrendered {total_rendered} new SVG(s); rewrote {len(files_with_blocks)} file(s) "
          f"(total {total_blocks} block reference(s))")
    if errors:
        print(f"\n{len(errors)} block(s) failed to render — fenced source kept in place:")
        for e in errors:
            print(f"  - {e.splitlines()[0]}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
