#!/usr/bin/env python3
"""
generate_chronology.py
Walks an Obsidian vault, extracts dated events from frontmatter,
and writes a sorted CHRONOLOGY.md to the repo root.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

# ── Configuration ────────────────────────────────────────────────────────────

VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "."))
OUTPUT_FILE = VAULT_ROOT / "CHRONOLOGY.md"

# Folders to skip
SKIP_DIRS = {".git", ".obsidian", "_fileClasses", "_templates", "node_modules"}

# Maps frontmatter field → (label, use_note_title)
# Each entry is a function that receives the full frontmatter dict and the
# note title, and returns a list of (year, label, note_title) tuples.
# This makes it easy to add new fields without touching the extraction logic.

def extract_events(fm: dict, title: str) -> list[tuple[int, str, str]]:
    events = []
    link = f"[[{title}]]"

    def add(year, label):
        if year and str(year).lstrip("-").isdigit():
            events.append((int(year), label, link))

    note_type = fm.get("type", "")

    # ── Universal ────────────────────────────────────────────────────────────
    # written_works
    for work in fm.get("written_works", []) or []:
        if not isinstance(work, dict):
            continue
        year = work.get("publication_date")
        wtitle = work.get("title", "Untitled work")
        add(year, f"**Publication** — *{wtitle}* by {link}")

    # ── Person ───────────────────────────────────────────────────────────────
    if note_type == "person":
        name = fm.get("native_name") or title

        add(fm.get("birth_year"),
            f"**Birth** — {link} born in "
            f"{fm.get('birth_city') or '?'}, {_wl(fm.get('birth_state'))}")

        add(fm.get("death_year"),
            f"**Death** — {link} died in "
            f"{_wl(fm.get('death_state'))} ({fm.get('death_cause') or 'unknown cause'})")

        for edu in fm.get("education", []) or []:
            if not isinstance(edu, dict):
                continue
            add(edu.get("year"),
                f"**Graduation** — {link} — {edu.get('degree')} at {_wl(edu.get('institution'))}")

        for office in fm.get("offices", []) or []:
            if not isinstance(office, dict):
                continue
            add(office.get("start"),
                f"**Appointment** — {link} becomes {office.get('title')} "
                f"at {_wl(office.get('organization'))}")
            add(office.get("end"),
                f"**End of tenure** — {link} leaves {office.get('title')} "
                f"at {_wl(office.get('organization'))}")

        for ms in fm.get("military_service", []) or []:
            if not isinstance(ms, dict):
                continue
            add(ms.get("start"),
                f"**Enlists** — {link} in {_wl(ms.get('branch'))} "
                f"({ms.get('role', '')})")
            add(ms.get("end"),
                f"**Discharge** — {link} from {_wl(ms.get('branch'))}")

    # ── Event ────────────────────────────────────────────────────────────────
    elif note_type == "event":
        event_name = fm.get("event_name") or title
        add(fm.get("date_start"), f"**Event begins** — {link}")
        add(fm.get("date_end"),   f"**Event ends** — {link}")

    # ── Organization ─────────────────────────────────────────────────────────
    elif note_type in ("organization", "company", "institution"):
        add(fm.get("founded"),   f"**Founded** — {link}")
        add(fm.get("dissolved"), f"**Dissolved** — {link}")

    # ── Location ─────────────────────────────────────────────────────────────
    elif note_type in ("city", "location", "place"):
        add(fm.get("founded"),     f"**Founded** — {link}")
        add(fm.get("established"), f"**Established** — {link}")

    # ── Atrocity ─────────────────────────────────────────────────────────────
    elif note_type == "atrocity":
        add(fm.get("date_start"), f"**Atrocity begins** — {link}")
        add(fm.get("date_end"),   f"**Atrocity ends** — {link}")
        # single-day atrocities may only have date_start
        if not fm.get("date_end") and fm.get("date_start"):
            pass  # already added above

    # ── Company ──────────────────────────────────────────────────────────────
    elif note_type == "company":
        name = fm.get("company_name") or fm.get("native_company_name") or title
        add(fm.get("founded"),
            f"**Founded** — {link}"
            + (f" by {_wl(fm.get('founded_by'))}" if fm.get("founded_by") else "")
            + (f" in {_wl(fm.get('founding_place'))}" if fm.get("founding_place") else ""))
        if fm.get("yarnojte_granted"):
            add(fm.get("yarnojte_granted"), f"**Yarnojte granted** — {link}")
        if fm.get("yarnojte_revoked"):
            add(fm.get("yarnojte_revoked"), f"**Yarnojte revoked** — {link}")

    # ── Document ─────────────────────────────────────────────────────────────
    elif note_type == "document":
        add(fm.get("recorded_year"),
            f"**Document recorded** — {link}"
            + (f" ({fm.get('document_type')})" if fm.get("document_type") else ""))

    # ── Organization ─────────────────────────────────────────────────────────
    elif note_type == "organization":
        add(fm.get("founded"),
            f"**Founded** — {link}"
            + (f" by {_wl(fm.get('founded_by'))}" if fm.get("founded_by") else ""))
        add(fm.get("dissolved"), f"**Dissolved** — {link}")

    # ── Project ──────────────────────────────────────────────────────────────
    elif note_type == "project":
        add(fm.get("date_start"),
            f"**Project begins** — {link}"
            + (f" (organized by {_wl(fm.get('organizer'))})" if fm.get("organizer") else ""))
        add(fm.get("date_end"),
            f"**Project ends** — {link}"
            + (f" — {fm.get('outcome')}" if fm.get("outcome") else ""))

    return events


def _wl(value) -> str:
    """Return value as-is if it's already a wikilink string, else wrap it."""
    if not value:
        return "?"
    s = str(value)
    if s.startswith("[["):
        return s
    return f"[[{s}]]"


# ── Frontmatter parser ────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

def parse_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = FRONTMATTER_RE.match(text)
        if not m:
            return {}
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    by_year: defaultdict[int, list[str]] = defaultdict(list)

    for md_file in VAULT_ROOT.rglob("*.md"):
        # Skip excluded dirs
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        # Skip the output file itself
        if md_file.resolve() == OUTPUT_FILE.resolve():
            continue

        fm = parse_frontmatter(md_file)
        if not fm:
            continue

        title = md_file.stem
        for year, label, _ in extract_events(fm, title):
            by_year[year].append(label)

    if not by_year:
        print("No dated events found.")
        return

    lines = [
        "# Susia — Chronology",
        "",
        "> Auto-generated from vault frontmatter. Do not edit manually.",
        "",
    ]

    for year in sorted(by_year.keys()):
        lines.append(f"## {year}")
        for entry in sorted(by_year[year]):
            lines.append(f"- {entry}")
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(v) for v in by_year.values())
    print(f"✓ CHRONOLOGY.md written — {total} events across {len(by_year)} years.")


if __name__ == "__main__":
    main()
