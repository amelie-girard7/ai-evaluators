"""Shared helpers for the wiki tools."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WIKI = ROOT / "wiki"
OUTPUTS = ROOT / "outputs"
INDEX = WIKI / "INDEX.md"
LOG = WIKI / "LOG.md"

MODEL = "qwen3:14b"  # dense, ~9GB resident, fits comfortably on 24GB Macs
NUM_CTX = 16384

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s[:max_len] or "untitled"


def now_iso() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def today() -> str:
    return dt.date.today().isoformat()


def read_md(path: Path) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body). Empty dict if no frontmatter."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def write_md(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    fm_yaml = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    path.write_text(f"---\n{fm_yaml}\n---\n{body}", encoding="utf-8")


def append_log(line: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{now_iso()} | {line}\n")


def ollama_chat(system: str, user: str, model: str = MODEL, temperature: float = 0.2) -> str:
    import ollama
    resp = ollama.chat(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        options={"num_ctx": NUM_CTX, "temperature": temperature},
    )
    return resp["message"]["content"]


def load_schema_snippet() -> str:
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        return ""
    return agents.read_text(encoding="utf-8")


def list_unprocessed() -> list[Path]:
    out: list[Path] = []
    for sub in ("papers", "web", "notes"):
        d = RAW / sub
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            fm, _ = read_md(p)
            if fm.get("processed") in (False, None):
                out.append(p)
    return out


def list_articles() -> list[Path]:
    return [p for p in WIKI.rglob("*.md")
            if p.name not in {"INDEX.md", "LOG.md"}]
