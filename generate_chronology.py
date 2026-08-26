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


# ── Helpers ───────────────────────────────────────────────────────────────────

def _wl(value) -> str:
    """Return value as-is if it's already a wikilink string, else wrap it.

    Lists are rendered as a readable series rather than stringified, which
    previously produced output like [[['[[A]]', '[[B]]']]] for multi-value
    fields such as founded_by.
    """
    if not value:
        return "?"
    if isinstance(value, (list, tuple, set)):
        parts = [_wl(v) for v in value if v]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0]
        return ", ".join(parts[:-1]) + " and " + parts[-1]
    s = str(value).strip()
    if s.startswith("[["):
        return s
    return f"[[{s}]]"


def _notes(d: dict) -> str:
    """Return an inline notes tail if the dict has a non-empty 'notes' field."""
    n = d.get("notes", "")
    if not n:
        return ""
    return f" — *{str(n).strip()}*"


def _is_election(appointer: str) -> bool:
    """True if the appointer wikilink title contains the word 'election'."""
    return bool(appointer) and "election" in appointer.lower()


# ── Event extraction ──────────────────────────────────────────────────────────

# ElectionEntry: groups offices under a shared election header.
# Stored as: by_election[(year, election_link)] = list of formatted strings
ElectionEntries = dict  # type alias for clarity

def extract_events(
    fm: dict,
    title: str,
    by_election: dict,
) -> list[tuple[int, str]]:
    """
    Returns a list of (year, label) tuples for regular (non-election) events.
    Election-appointed offices are written directly into by_election instead.
    """
    events: list[tuple[int, str]] = []
    link = f"[[{title}]]"

    def add(year, label):
        if year and str(year).lstrip("-").isdigit():
            events.append((int(year), label))

    note_type = fm.get("type", "")

    # ── Universal ────────────────────────────────────────────────────────────
    for work in fm.get("written_works", []) or []:
        if not isinstance(work, dict):
            continue
        year = work.get("publication_year")
        wtitle = work.get("title", "Untitled work")
        add(year, f"**Publication** — *{wtitle}* by {link}{_notes(work)}")

    # ── Person ───────────────────────────────────────────────────────────────
    if note_type == "person":
        birth = fm.get("birth") or {}
        death = fm.get("death") or {}
        add(birth.get("year"),
            f"**Birth** — {link} born in "
            f"{birth.get('city') or '?'}, {_wl(birth.get('state'))}")

        add(death.get("year"),
            f"**Death** — {link} died in "
            f"{_wl(death.get('state'))} ({death.get('cause') or 'unknown cause'})")

        for edu in fm.get("education", []) or []:
            if not isinstance(edu, dict):
                continue
            add(edu.get("year"),
                f"**Graduation** — {link} — {edu.get('degree')} "
                f"at {_wl(edu.get('institution'))}{_notes(edu)}")

        for office in fm.get("offices", []) or []:
            if not isinstance(office, dict):
                continue

            appointer = office.get("appointer", "")
            start     = office.get("start_year")
            end       = office.get("end_year")
            org       = _wl(office.get("employer"))
            title_str = office.get("title", "?")
            party     = _wl(office.get("parties")) if office.get("parties") else None
            note_tail = _notes(office)

            if _is_election(str(appointer)):
                # ── Election-grouped appointment ──────────────────────────
                election_link = _wl(appointer)
                if start and str(start).lstrip("-").isdigit():
                    key = (int(start), election_link)
                    entry = f"{link} — {title_str}"
                    if party:
                        entry += f" — {party}"
                    entry += note_tail
                    by_election.setdefault(key, []).append(entry)
            else:
                # ── Regular appointment ───────────────────────────────────
                appt_label = (
                    f"**Appointment** — {link} becomes {title_str} at {org}"
                    + (f", appointed by {_wl(appointer)}" if appointer else "")
                    + note_tail
                )
                add(start, appt_label)

            # End of tenure is always a regular line
            if end:
                add(end,
                    f"**End of tenure** — {link} leaves {title_str} "
                    f"at {org}{note_tail}")

        for ms in fm.get("military_service", []) or []:
            if not isinstance(ms, dict):
                continue
            add(ms.get("start_year"),
                f"**Enlists** — {link} in {_wl(ms.get('branch'))} "
                f"({ms.get('role', '')}){_notes(ms)}")
            add(ms.get("end_year"),
                f"**Discharge** — {link} from {_wl(ms.get('branch'))}{_notes(ms)}")

    # ── Event ────────────────────────────────────────────────────────────────
    elif note_type == "event":
        add(fm.get("date_start"), f"**Event begins** — {link}{_notes(fm)}")
        add(fm.get("date_end"),   f"**Event ends** — {link}{_notes(fm)}")

    # ── Organization / Company / Institution ─────────────────────────────────
    elif note_type in ("organization", "institution"):
        add(fm.get("founded"),
            f"**Founded** — {link}"
            + (f" by {_wl(fm.get('founded_by'))}" if fm.get("founded_by") else "")
            + _notes(fm))
        add(fm.get("dissolved"), f"**Dissolved** — {link}{_notes(fm)}")

    # ── Location ─────────────────────────────────────────────────────────────
    elif note_type in ("city", "location", "place"):
        add(fm.get("founded"),     f"**Founded** — {link}{_notes(fm)}")
        add(fm.get("established"), f"**Established** — {link}{_notes(fm)}")

    # ── Atrocity ─────────────────────────────────────────────────────────────
    elif note_type == "atrocity":
        add(fm.get("date_start"), f"**Atrocity begins** — {link}{_notes(fm)}")
        add(fm.get("date_end"),   f"**Atrocity ends** — {link}{_notes(fm)}")

    # ── Company ──────────────────────────────────────────────────────────────
    elif note_type == "company":
        add(fm.get("founded"),
            f"**Founded** — {link}"
            + (f" by {_wl(fm.get('founded_by'))}" if fm.get("founded_by") else "")
            + (f" in {_wl(fm.get('founding_place'))}" if fm.get("founding_place") else "")
            + _notes(fm))
        if fm.get("yarnojte_granted"):
            add(fm.get("yarnojte_granted"), f"**Yarnojte granted** — {link}{_notes(fm)}")
        if fm.get("yarnojte_revoked"):
            add(fm.get("yarnojte_revoked"), f"**Yarnojte revoked** — {link}{_notes(fm)}")
        add(fm.get("dissolved"), f"**Dissolved** — {link}{_notes(fm)}")

    # ── Document ─────────────────────────────────────────────────────────────
    elif note_type == "document":
        add(fm.get("recorded_year"),
            f"**Document recorded** — {link}"
            + (f" ({fm.get('document_type')})" if fm.get("document_type") else "")
            + _notes(fm))

    # ── Project ──────────────────────────────────────────────────────────────
    elif note_type == "project":
        add(fm.get("date_start"),
            f"**Project begins** — {link}"
            + (f" (organized by {_wl(fm.get('organizer'))})" if fm.get("organizer") else "")
            + _notes(fm))
        add(fm.get("date_end"),
            f"**Project ends** — {link}"
            + (f" — {fm.get('outcome')}" if fm.get("outcome") else "")
            + _notes(fm))

    return events


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
    # by_election[(year, "[[Election Note]]")] = [formatted person lines]
    by_election: dict[tuple[int, str], list[str]] = {}

    for md_file in VAULT_ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        if md_file.resolve() == OUTPUT_FILE.resolve():
            continue

        fm = parse_frontmatter(md_file)
        if not fm:
            continue

        title = md_file.stem
        for year, label in extract_events(fm, title, by_election):
            by_year[year].append(label)

    if not by_year and not by_election:
        print("No dated events found.")
        return

    # Merge election years into by_year so we sort everything together
    for (year, _election_link) in by_election:
        # Ensure the year key exists even if it has no regular events
        by_year[year]  # defaultdict creates it

    lines = [
        # Frontmatter. This file is a vault article like any other and must
        # carry the base header from 00 - Meta/Frontmatter reference.md, or it
        # drops out of every type query on each regeneration.
        "---",
        "type: index",
        "summary: Chronological index of every dated event recorded in vault frontmatter.",
        "aliases:",
        "  -",
        "era:",
        "  -",
        "tags:",
        "  - history",
        "meta:",
        "  stub: false",
        "  verified: false",
        "  image: null",
        "---",
        "",
        "# Susia — Chronology",
        "",
        "> Auto-generated from vault frontmatter. Do not edit manually.",
        "",
    ]

    for year in sorted(by_year.keys()):
        lines.append(f"## {year}")

        # ── Election blocks first ─────────────────────────────────────────
        election_keys = sorted(
            [k for k in by_election if k[0] == year],
            key=lambda k: k[1],  # alphabetical by election link
        )
        for key in election_keys:
            _yr, election_link = key
            lines.append(f"### {election_link}")
            for entry in sorted(by_election[key]):
                lines.append(f"- {entry}")
            lines.append("")

        # ── Regular events ────────────────────────────────────────────────
        for entry in sorted(by_year[year]):
            lines.append(f"- {entry}")
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    total_regular  = sum(len(v) for v in by_year.values())
    total_election = sum(len(v) for v in by_election.values())
    total          = total_regular + total_election
    print(
        f"✓ CHRONOLOGY.md written — {total} events across {len(by_year)} years "
        f"({len(by_election)} election block(s))."
    )


if __name__ == "__main__":
    main()
