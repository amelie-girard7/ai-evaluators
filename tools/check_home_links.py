"""Verify every [[wiki-link]] in wiki/Home.md still resolves.

Extracts each [[Folder/Article]] target from Home.md (ignoring any |alias),
checks that wiki/<target>.md exists, and reports broken links. For each broken
target, greps the wiki for a likely renamed file as a correction hint. Does NOT
edit Home.md — the user actions findings.

Run via launchd or directly: python3 tools/check_home_links.py
"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = REPO / "wiki" / "Home.md"
WIKI = REPO / "wiki"
LINK_RE = re.compile(r"\[\[([^\]\|]+?)(?:\|[^\]]+)?\]\]")


def main() -> int:
    print(f"# Home.md link check — {dt.datetime.now().isoformat(timespec='seconds')}")
    if not HOME.exists():
        print(f"FATAL: {HOME} does not exist")
        return 2

    targets = sorted({m.group(1).strip() for m in LINK_RE.finditer(HOME.read_text())})
    print(f"found {len(targets)} unique [[…]] targets in Home.md\n")

    broken: list[tuple[str, list[str]]] = []
    for t in targets:
        candidate = WIKI / f"{t}.md"
        if candidate.exists():
            continue
        stem = Path(t).name
        try:
            hits = subprocess.run(
                ["find", str(WIKI), "-type", "f", "-iname", f"*{stem}*.md"],
                capture_output=True, text=True, check=False, timeout=10,
            ).stdout.strip().splitlines()
        except Exception:
            hits = []
        broken.append((t, hits))

    if not broken:
        print("OK — every link resolves.")
        return 0

    print(f"{len(broken)} broken link(s):\n")
    for target, hits in broken:
        print(f"  - [[{target}]]")
        if hits:
            print("    possible matches:")
            for h in hits:
                print(f"      {Path(h).relative_to(REPO)}")
        else:
            print("    no similar file found in wiki/")
        print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
