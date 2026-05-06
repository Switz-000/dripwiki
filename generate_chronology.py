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
from dataclasses import dataclass, field
from typing import Optional

# ── Configuration ────────────────────────────────────────────────────────────

VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "."))
OUTPUT_FILE = VAULT_ROOT / "CHRONOLOGY.md"

# Folders to skip
SKIP_DIRS = {".git", ".obsidian", "_fileClasses", "_templates", "node_modules"}


# ── Event model ──────────────────────────────────────────────────────────────

@dataclass
class RawEvent:
    """
    A single dated happening before consolidation.

    kind        – semantic category used to find mergeable pairs
                  e.g. "office_start", "office_end", "span_start", "span_end"
    year        – calendar year (int)
    label       – final rendered string (filled in after consolidation)
    person_link – wikilink of the note owner, used for role-transition merging
    role        – office / branch title, used to pair start↔end events
    org         – organisation wikilink, ditto
    outcome     – optional project outcome appended on end events
    """
    kind:        str
    year:        int
    label:       str = ""
    person_link: str = ""
    role:        str = ""
    org:         str = ""
    outcome:     str = ""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _wl(value) -> str:
    """Wrap a value in [[ ]] unless it already is one, or return '?' if empty."""
    if not value:
        return "?"
    s = str(value)
    return s if s.startswith("[[") else f"[[{s}]]"


def _valid_year(value) -> Optional[int]:
    """Return value as int if it looks like a year, else None."""
    if not value:
        return None
    s = str(value).lstrip("-")
    return int(value) if s.isdigit() else None


# ── Extraction ────────────────────────────────────────────────────────────────

def extract_raw(fm: dict, title: str) -> list[RawEvent]:
    """
    Parse a note's frontmatter into a flat list of RawEvents.
    Labels are left empty for events that may be consolidated later;
    simple atomic events get their label set immediately.
    """
    raw: list[RawEvent] = []
    link = f"[[{title}]]"
    note_type = fm.get("type", "")

    def atom(year, label: str):
        """Add a simple, non-consolidatable event."""
        y = _valid_year(year)
        if y is not None:
            raw.append(RawEvent(kind="atom", year=y, label=label))

    # ── Universal: written works ──────────────────────────────────────────────
    for work in fm.get("written_works", []) or []:
        if not isinstance(work, dict):
            continue
        wtitle = work.get("title", "Untitled work")
        atom(work.get("publication_date"),
             f"**Publication** — *{wtitle}* by {link}")

    # ── Person ───────────────────────────────────────────────────────────────
    if note_type == "person":

        atom(fm.get("birth_year"),
             f"**Birth** — {link} born in "
             f"{fm.get('birth_city') or '?'}, {_wl(fm.get('birth_state'))}")

        atom(fm.get("death_year"),
             f"**Death** — {link} died in "
             f"{_wl(fm.get('death_state'))} ({fm.get('death_cause') or 'unknown cause'})")

        for edu in fm.get("education", []) or []:
            if not isinstance(edu, dict):
                continue
            atom(edu.get("year"),
                 f"**Graduation** — {link} — {edu.get('degree')} "
                 f"at {_wl(edu.get('institution'))}")

        # Offices — kept as typed events so the consolidator can merge them
        for office in fm.get("offices", []) or []:
            if not isinstance(office, dict):
                continue
            role = office.get("title", "")
            org  = _wl(office.get("organization"))
            ys   = _valid_year(office.get("start"))
            ye   = _valid_year(office.get("end"))
            if ys is not None:
                raw.append(RawEvent(
                    kind="office_start", year=ys,
                    person_link=link, role=role, org=org,
                ))
            if ye is not None:
                raw.append(RawEvent(
                    kind="office_end", year=ye,
                    person_link=link, role=role, org=org,
                ))

        # Military service — same treatment
        for ms in fm.get("military_service", []) or []:
            if not isinstance(ms, dict):
                continue
            branch = _wl(ms.get("branch"))
            role   = ms.get("role", "")
            ys     = _valid_year(ms.get("start"))
            ye     = _valid_year(ms.get("end"))
            if ys is not None:
                raw.append(RawEvent(
                    kind="mil_start", year=ys,
                    person_link=link, role=role, org=branch,
                ))
            if ye is not None:
                raw.append(RawEvent(
                    kind="mil_end", year=ye,
                    person_link=link, role=role, org=branch,
                ))

    # ── Event ────────────────────────────────────────────────────────────────
    elif note_type == "event":
        _add_span(raw, fm, link, prefix="Event", start_key="date_start", end_key="date_end")

    # ── Atrocity ─────────────────────────────────────────────────────────────
    elif note_type == "atrocity":
        _add_span(raw, fm, link, prefix="Atrocity", start_key="date_start", end_key="date_end")

    # ── Project ──────────────────────────────────────────────────────────────
    elif note_type == "project":
        outcome = fm.get("outcome", "")
        organizer = fm.get("organizer")
        ys = _valid_year(fm.get("date_start"))
        ye = _valid_year(fm.get("date_end"))
        start_label = f"**Project begins** — {link}" + (
            f" (organized by {_wl(organizer)})" if organizer else "")
        if ys is not None:
            raw.append(RawEvent(
                kind="span_start", year=ys, label=start_label,
                person_link=link, outcome=outcome,
            ))
        if ye is not None:
            raw.append(RawEvent(
                kind="span_end", year=ye,
                label=f"**Project ends** — {link}" + (f" — {outcome}" if outcome else ""),
                person_link=link,
            ))

    # ── Organization / company / institution ─────────────────────────────────
    elif note_type in ("organization", "company", "institution"):
        founded_by     = fm.get("founded_by")
        founding_place = fm.get("founding_place")
        founded_label  = (
            f"**Founded** — {link}"
            + (f" by {_wl(founded_by)}"     if founded_by     else "")
            + (f" in {_wl(founding_place)}" if founding_place else "")
        )
        atom(fm.get("founded"),   founded_label)
        atom(fm.get("dissolved"), f"**Dissolved** — {link}")

        # Company-specific grants
        if fm.get("yarnojte_granted"):
            atom(fm.get("yarnojte_granted"), f"**Yarnojte granted** — {link}")
        if fm.get("yarnojte_revoked"):
            atom(fm.get("yarnojte_revoked"), f"**Yarnojte revoked** — {link}")

    # ── Location ─────────────────────────────────────────────────────────────
    elif note_type in ("city", "location", "place"):
        atom(fm.get("founded"),     f"**Founded** — {link}")
        atom(fm.get("established"), f"**Established** — {link}")

    # ── Document ─────────────────────────────────────────────────────────────
    elif note_type == "document":
        doc_type = fm.get("document_type")
        atom(fm.get("recorded_year"),
             f"**Document recorded** — {link}"
             + (f" ({doc_type})" if doc_type else ""))

    return raw


def _add_span(
    raw: list[RawEvent],
    fm: dict,
    link: str,
    *,
    prefix: str,
    start_key: str,
    end_key: str,
):
    """
    Add a start/end pair for simple span types (event, atrocity).
    If both dates exist and are the same year the consolidator will collapse
    them; if only start exists it becomes a standalone entry.
    """
    ys = _valid_year(fm.get(start_key))
    ye = _valid_year(fm.get(end_key))
    if ys is not None:
        raw.append(RawEvent(
            kind="span_start", year=ys,
            label=f"**{prefix} begins** — {link}",
            person_link=link,
        ))
    if ye is not None:
        raw.append(RawEvent(
            kind="span_end", year=ye,
            label=f"**{prefix} ends** — {link}",
            person_link=link,
        ))


# ── Consolidation ─────────────────────────────────────────────────────────────

def consolidate(raw: list[RawEvent]) -> list[tuple[int, str]]:
    """
    Convert raw events into final (year, label) pairs, applying two passes:

    Pass 1 — Span collapse:
        If a span_start and span_end share the same link AND the same year,
        drop both and emit a single "**X** — [[link]]" entry (no begins/ends).

    Pass 2 — Office/military role transitions:
        If person P leaves role A at org O and starts role B at org Q in the
        same year, merge into one entry:
            "**X** leaves <role A> at <org O> and becomes <role B> at <org Q>"
        If the same-year end has no matching start, fall back to:
            "**X** leaves <role A> at <org O>"  (and vice-versa for lone starts)
    """
    results: list[tuple[int, str]] = []

    # ── Pass 1: span collapse ─────────────────────────────────────────────────
    # Group span_start / span_end by (year, person_link)
    span_starts: dict[tuple[int, str], RawEvent] = {}
    span_ends:   dict[tuple[int, str], RawEvent] = {}
    remaining: list[RawEvent] = []

    for ev in raw:
        if ev.kind == "span_start":
            span_starts[(ev.year, ev.person_link)] = ev
        elif ev.kind == "span_end":
            span_ends[(ev.year, ev.person_link)] = ev
        else:
            remaining.append(ev)

    # Collapse same-year pairs
    collapsed_links: set[tuple[int, str]] = set()
    for key, start_ev in span_starts.items():
        if key in span_ends:
            # Same year: strip "begins"/"ends" and emit a clean entry
            clean_label = re.sub(
                r"\*\*(Event|Atrocity|Project) (begins|ends)\*\*",
                lambda m: f"**{m.group(1)}**",
                start_ev.label,
            )
            results.append((start_ev.year, clean_label))
            collapsed_links.add(key)
        else:
            remaining.append(start_ev)

    for key, end_ev in span_ends.items():
        if key not in collapsed_links:
            remaining.append(end_ev)

    # ── Pass 2: office/military role transitions ──────────────────────────────
    # Index ends and starts by (year, person_link)
    office_ends:   defaultdict[tuple[int, str], list[RawEvent]] = defaultdict(list)
    office_starts: defaultdict[tuple[int, str], list[RawEvent]] = defaultdict(list)
    final_pass: list[RawEvent] = []

    for ev in remaining:
        if ev.kind == "office_end":
            office_ends[(ev.year, ev.person_link)].append(ev)
        elif ev.kind == "office_start":
            office_starts[(ev.year, ev.person_link)].append(ev)
        elif ev.kind == "mil_end":
            office_ends[(ev.year, ev.person_link)].append(ev)
        elif ev.kind == "mil_start":
            office_starts[(ev.year, ev.person_link)].append(ev)
        else:
            final_pass.append(ev)

    all_keys = set(office_ends) | set(office_starts)

    for key in all_keys:
        year, person = key
        ends   = office_ends.get(key, [])
        starts = office_starts.get(key, [])

        # Pair them off greedily (one end → one start, extras fall through)
        paired = min(len(ends), len(starts))
        for i in range(paired):
            e, s = ends[i], starts[i]
            label = (
                f"**Transition** — {person} leaves {e.role} at {e.org} "
                f"and becomes {s.role} at {s.org}"
            )
            results.append((year, label))

        # Unmatched ends
        for e in ends[paired:]:
            results.append((year,
                f"**End of tenure** — {person} leaves {e.role} at {e.org}"))

        # Unmatched starts
        for s in starts[paired:]:
            results.append((year,
                f"**Appointment** — {person} becomes {s.role} at {s.org}"))

    # ── Flush atoms and any residual labelled events ──────────────────────────
    for ev in final_pass:
        results.append((ev.year, ev.label))

    return results


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
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        if md_file.resolve() == OUTPUT_FILE.resolve():
            continue

        fm = parse_frontmatter(md_file)
        if not fm:
            continue

        title  = md_file.stem
        raw    = extract_raw(fm, title)
        events = consolidate(raw)

        for year, label in events:
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
