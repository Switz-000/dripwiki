#!/usr/bin/env python3
"""
generate_chronology.py
Walks the vault, extracts dated events from article frontmatter, and writes a
sorted CHRONOLOGY.md to the repo root.

Reads the fields defined by the templates in 00 - Meta/Templates/. A year
written in a field this script does not read will not appear; see the
extract_events() branches for what is read per type.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ── Configuration ────────────────────────────────────────────────────────────

VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "."))
OUTPUT_FILE = VAULT_ROOT / "CHRONOLOGY.md"

# Folders to skip. "00 - Meta" holds templates (which carry sample years, e.g.
# the Company Template's yarnojte block) and non-canon session reports, so it
# is excluded for the same reason check_frontmatter.py excludes it.
SKIP_DIRS = {
    ".git", ".github", ".githooks", ".obsidian", "_fileClasses", "_templates",
    "node_modules", "00 - Meta",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _has(value) -> bool:
    """True if the value carries anything. Blank strings and [None] are empty."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set)):
        return any(_has(v) for v in value)
    if isinstance(value, dict):
        return any(_has(v) for v in value.values())
    return True


def _year(value):
    """Return the value as an int year, or None if it is not one.

    Booleans are rejected explicitly: YAML reads `yes`/`true` as True, and
    str(True) is not a year.
    """
    if isinstance(value, bool) or value is None:
        return None
    s = str(value).strip()
    if s.lstrip("-").isdigit():
        return int(s)
    return None


def _wl(value) -> str:
    """Return value as-is if it's already a wikilink string, else wrap it.

    Lists are rendered as a readable series ("A, B and C"). Returns "" for an
    empty value; callers decide whether and how to show a gap.
    """
    if isinstance(value, (list, tuple, set)):
        parts = [_wl(v) for v in value if _has(v)]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        return ", ".join(parts[:-1]) + " and " + parts[-1]
    if not _has(value):
        return ""
    s = str(value).strip()
    if s.startswith("[["):
        return s
    return f"[[{s}]]"


def _text(value) -> str:
    """Plain text, or "" if empty."""
    return str(value).strip() if _has(value) else ""


def _place(d: dict) -> str:
    """'City, State, Country' from whichever of the three are filled in."""
    return ", ".join(p for p in (_wl(d.get(k)) for k in ("city", "state", "country")) if p)


def _series(items: list[str]) -> str:
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _notes_text(d: dict) -> str:
    n = d.get("notes") if isinstance(d, dict) else None
    return f". *{str(n).strip()}*" if _has(n) else ""


def _is_election(appointer) -> bool:
    """True if the appointer wikilink title contains the word 'election'."""
    return _has(appointer) and "election" in str(appointer).lower()


# ── Event extraction ──────────────────────────────────────────────────────────

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

    def record(lines, notes: str = "", notes_on: str = "first"):
        """Add one record's lines, attaching its notes to a single line.

        A record's notes describe the record as a whole (an office, an event,
        a company), so they are shown once rather than on every line the
        record produces. They go on the earliest line by default, or on the
        latest with notes_on="last".
        """
        dated = [(y, lbl) for y, lbl in ((_year(y), lbl) for y, lbl in lines) if y is not None]
        if not dated:
            return
        if notes:
            idx = 0
            if notes_on == "last":
                latest = max(y for y, _ in dated)
                idx = max(i for i, (y, _) in enumerate(dated) if y == latest)
            else:
                earliest = min(y for y, _ in dated)
                idx = min(i for i, (y, _) in enumerate(dated) if y == earliest)
            y, lbl = dated[idx]
            dated[idx] = (y, lbl + notes)
        events.extend(dated)

    def entries(key):
        return [e for e in (fm.get(key) or []) if isinstance(e, dict)]

    note_type = fm.get("type", "")

    # ── Universal ────────────────────────────────────────────────────────────
    for work in entries("written_works"):
        wtitle = _text(work.get("title")) or "Untitled work"
        record([(work.get("publication_year"),
                 f"**Publication**: *{wtitle}* by {link}")],
               _notes_text(work))

    # ── Person ───────────────────────────────────────────────────────────────
    if note_type == "person":
        birth = fm.get("birth") if isinstance(fm.get("birth"), dict) else {}
        death = fm.get("death") if isinstance(fm.get("death"), dict) else {}

        place = _place(birth)
        record([(birth.get("year"),
                 f"**Birth**: {link} born" + (f" in {place}" if place else ""))])

        place = _place(death)
        cause = _text(death.get("cause"))
        record([(death.get("year"),
                 f"**Death**: {link} died"
                 + (f" in {place}" if place else "")
                 + (f" ({cause})" if cause else ""))])

        for edu in entries("education"):
            inst = _wl(edu.get("institution"))
            degree = _text(edu.get("degree"))
            record([(edu.get("year"),
                     f"**Graduation**: {link}"
                     + (f" from {inst}" if inst else "")
                     + (f" ({degree})" if degree else ""))],
                   _notes_text(edu))

        for office in entries("offices"):
            appointer = office.get("appointer")
            start     = office.get("start_year")
            org       = _wl(office.get("employer"))
            at_org    = f" at {org}" if org else ""
            title_str = _text(office.get("title")) or "?"
            party     = _wl(office.get("parties"))
            notes     = _notes_text(office)

            lines = []
            if _is_election(appointer) and _year(start) is not None:
                # Election-grouped appointment. The notes go here, on the
                # appointment, so they are not repeated on the end of tenure.
                entry = f"{link}, {title_str}" + (f" ({party})" if party else "") + notes
                by_election.setdefault((_year(start), _wl(appointer)), []).append(entry)
                notes = ""
            else:
                lines.append((start,
                              f"**Appointment**: {link} becomes {title_str}{at_org}"
                              + (f", appointed by {_wl(appointer)}" if _has(appointer) else "")))

            lines.append((office.get("end_year"),
                          f"**End of tenure**: {link} leaves {title_str}{at_org}"))
            record(lines, notes)

        for ms in entries("military_service"):
            branch = _wl(ms.get("branch"))
            rank = _text(ms.get("rank"))
            record([
                (ms.get("start_year"),
                 f"**Enlists**: {link}"
                 + (f" in {branch}" if branch else "")
                 + (f" as {rank}" if rank else "")),
                (ms.get("end_year"),
                 f"**Discharge**: {link}" + (f" from {branch}" if branch else "")),
            ], _notes_text(ms))

        # Criminal charges: one line per person per year, not per count, so a
        # six-charge indictment reads as one indictment.
        charged: defaultdict[int, list[str]] = defaultdict(list)
        verdicts: defaultdict[tuple, list[str]] = defaultdict(list)
        for c in entries("criminal_charges"):
            charge = _text(c.get("charge")) or "?"
            counts = _year(c.get("counts"))
            charge_str = charge + (f" ({counts} counts)" if counts and counts > 1 else "")
            if _year(c.get("charged_year")) is not None:
                charged[_year(c.get("charged_year"))].append(charge_str)
            if _year(c.get("verdict_year")) is not None:
                key = (_year(c.get("verdict_year")),
                       _text(c.get("verdict")) or "?",
                       _text(c.get("sentence")),
                       c.get("in_absentia") is True)
                verdicts[key].append(charge_str)
        for year, charges in charged.items():
            record([(year, f"**Charged**: {link} with {_series(charges)}")])
        for (year, verdict, sentence, absentia), charges in verdicts.items():
            record([(year,
                     f"**Verdict**: {link} found {verdict} of {_series(charges)}"
                     + (" in absentia" if absentia else "")
                     + (f", sentenced to {sentence}" if sentence else ""))])

        for aw in entries("awards"):
            granted_by = _wl(aw.get("granted_by"))
            record([(aw.get("awarded_year"),
                     f"**Award**: {link} receives {_text(aw.get('title')) or '?'}"
                     + (f", granted by {granted_by}" if granted_by else "")
                     + (" (posthumous)" if aw.get("posthumous") is True else ""))],
                   _notes_text(aw))

    # ── Event / War / Rebellion ──────────────────────────────────────────────
    elif note_type in ("event", "war", "rebellion"):
        kind = note_type.capitalize()
        record([(fm.get("date_start"), f"**{kind} begins**: {link}"),
                (fm.get("date_end"),   f"**{kind} ends**: {link}")],
               _notes_text(fm))

    # ── Organization / Institution ───────────────────────────────────────────
    elif note_type in ("organization", "institution"):
        founders = _wl(fm.get("founded_by"))
        record([(fm.get("founded"),
                 f"**Founded**: {link}" + (f" by {founders}" if founders else "")),
                (fm.get("dissolved"), f"**Dissolved**: {link}")],
               _notes_text(fm))

    # ── Location ─────────────────────────────────────────────────────────────
    elif note_type in ("city", "location", "place"):
        record([(fm.get("founded"),     f"**Founded**: {link}"),
                (fm.get("established"), f"**Established**: {link}")],
               _notes_text(fm))

    # ── Atrocity ─────────────────────────────────────────────────────────────
    elif note_type == "atrocity":
        record([(fm.get("date_start"), f"**Atrocity begins**: {link}"),
                (fm.get("date_end"),   f"**Atrocity ends**: {link}")],
               _notes_text(fm))

    # ── Company ──────────────────────────────────────────────────────────────
    elif note_type == "company":
        founders = _wl(fm.get("founded_by"))
        place = _wl(fm.get("founding_place"))
        record([(fm.get("founded"),
                 f"**Founded**: {link}"
                 + (f" by {founders}" if founders else "")
                 + (f" in {place}" if place else "")),
                (fm.get("dissolved"), f"**Dissolved**: {link}")],
               _notes_text(fm))

        # Yarnojte status comes in two shapes. The flat pair is one grant; the
        # list (template key "*yarnojte*", also written "yarnojte_status" in
        # the vault) records each grant separately. Both are read, so a
        # company that fills in both with different years shows both, and the
        # article is where that gets fixed.
        record([(fm.get("yarnojte_granted"), f"**Yarnojte granted**: {link}"),
                (fm.get("yarnojte_revoked"), f"**Yarnojte revoked**: {link}")])
        for key in ("*yarnojte*", "yarnojte_status"):
            for y in entries(key):
                # The notes explain the entry's status, which is set by its
                # latest change, so they go on the latest line.
                record([(y.get("granted"), f"**Yarnojte granted**: {link}"),
                        (y.get("revoked"), f"**Yarnojte revoked**: {link}")],
                       _notes_text(y), notes_on="last")

    # ── Document ─────────────────────────────────────────────────────────────
    elif note_type == "document":
        dtype = _text(fm.get("document_type"))
        record([(fm.get("recorded_year"),
                 f"**Document recorded**: {link}" + (f" ({dtype})" if dtype else ""))],
               _notes_text(fm))

    # ── Project ──────────────────────────────────────────────────────────────
    elif note_type == "project":
        organizer = _wl(fm.get("organizer"))
        outcome = _text(fm.get("outcome"))
        record([(fm.get("date_start"),
                 f"**Project begins**: {link}"
                 + (f" (organized by {organizer})" if organizer else "")),
                (fm.get("date_end"),
                 f"**Project ends**: {link}" + (f". {outcome}" if outcome else ""))],
               _notes_text(fm))

    return events


# ── Frontmatter parser ────────────────────────────────────────────────────────

# Same pattern as check_frontmatter.py: tolerates CRLF and requires the
# closing --- to be a line of its own.
FRONTMATTER_RE = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.DOTALL)


def parse_frontmatter(path: Path) -> dict:
    """Return the frontmatter as a dict, or {} if there is none.

    A file whose frontmatter will not parse is reported on stderr rather than
    skipped in silence, since its events would otherwise vanish from the
    chronology with no trace.
    """
    try:
        # utf-8-sig strips a byte-order mark, which would otherwise hide the
        # opening --- from the pattern.
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        first = str(e).splitlines()[0] if str(e) else type(e).__name__
        print(f"warning: skipped {path}, frontmatter will not parse: {first}", file=sys.stderr)
        return {}
    return fm if isinstance(fm, dict) else {}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    by_year: defaultdict[int, list[str]] = defaultdict(list)
    # by_election[(year, "[[Election Note]]")] = [formatted person lines]
    by_election: dict[tuple[int, str], list[str]] = {}

    for md_file in sorted(VAULT_ROOT.rglob("*.md")):
        rel = md_file.relative_to(VAULT_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
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

    # Ensure every election year has a heading even with no regular events
    for (year, _election_link) in by_election:
        by_year[year]  # defaultdict creates it

    lines = [
        # Frontmatter. This file is a vault article like any other and must
        # carry the base header from 00 - Meta/YAML and Tags.md, or it
        # drops out of every type query on each regeneration.
        "---",
        "type: index",
        "summary: Chronological index of every dated event recorded in vault frontmatter.",
        "aliases:",
        "  -",
        "era:",
        "  -",
        "tags:",
        "  - politics",
        "meta:",
        "  stub: false",
        "  verified: false",
        "  image: null",
        "---",
        "",
        "# Chronology",
        "",
        "> Auto-generated from vault frontmatter. Do not edit manually.",
        "",
    ]

    for year in sorted(by_year.keys()):
        lines.append(f"## {year}")
        lines.append("")

        # Regular events come first, directly under the year. Election blocks
        # follow as ### subsections; placed before, the regular events would
        # sit inside the last election's section.
        for entry in sorted(by_year[year]):
            lines.append(f"- {entry}")
        if by_year[year]:
            lines.append("")

        election_keys = sorted(
            [k for k in by_election if k[0] == year],
            key=lambda k: k[1],  # alphabetical by election link
        )
        for key in election_keys:
            _yr, election_link = key
            lines.append(f"### {election_link}")
            lines.append("")
            for entry in sorted(by_election[key]):
                lines.append(f"- {entry}")
            lines.append("")

    # newline="\n" keeps LF on Windows too, matching .gitattributes.
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    total_regular  = sum(len(v) for v in by_year.values())
    total_election = sum(len(v) for v in by_election.values())
    total          = total_regular + total_election
    # ASCII only: a Windows console on a legacy code page cannot encode
    # typographic characters and would raise after the file was written.
    print(
        f"CHRONOLOGY.md written: {total} events across {len(by_year)} years "
        f"({len(by_election)} election block(s))."
    )


if __name__ == "__main__":
    main()
