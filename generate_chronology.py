#!/usr/bin/env python3
"""
generate_chronology.py
Walks the vault, extracts dated events from article frontmatter, and writes a
sorted CHRONOLOGY.md to the repo root.

Reads the fields defined by the templates in 00 - Meta/Templates/. A year
written in a field this script does not read will not appear; see the
extract_events() branches for what is read per type.
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ── Configuration ────────────────────────────────────────────────────────────

VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "."))
OUTPUT_FILE = VAULT_ROOT / "CHRONOLOGY.md"
# The same events in a form a program can read, for the site's timeline page.
JSON_FILE = VAULT_ROOT / "chronology.json"

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


# ── Titles ────────────────────────────────────────────────────────────────────
# A title is an article with `type: title`. It owns the display rules: the
# institution, the forms a holder's title takes, the sub-titles that split it
# by place (seats) or by time (periods), and the interludes, which are years
# the title was not held in the normal way.

INTERLUDE_LABELS = {
    "regency":   "Regency",
    "disputed":  "Disputed succession",
    "vacant":    "Vacancy",
    "abolished": "Abolition",
    "other":     "Interlude",
}


def _name(value) -> str:
    """"[[Target|Label]]" or "Target" as the bare target name."""
    if not _has(value):
        return ""
    s = str(value).strip()
    m = re.fullmatch(r"\[\[([^\]]+)\]\]", s)
    if m:
        s = m.group(1).split("|")[0]
    return s.strip()


def title_display(spec: dict, post: dict, sex) -> str:
    """What a holder of this title was called, for this seat and these years.

    A seat's name wins, then the period in force when the term began, then the
    title's own name with the form matching the holder.
    """
    if not spec:
        return _name(post.get("title")) or "?"
    base = spec.get("name", "")

    seat = _name(post.get("seat"))
    if seat:
        for s in spec.get("seats") or []:
            if _name(s.get("for")) == seat:
                return _text(s.get("name")) or f"{base} for {seat}"
        return f"{base} for {seat}"

    # The period a term belongs to is the one it overlaps most. Comparing
    # start years alone breaks on the boundary year, where one period ends and
    # the next begins: a term running 1958 to 1977 belongs to the period that
    # starts in 1958, while a term lasting only 1977 belongs to the one ending
    # then.
    start = _year(post.get("start_year"))
    if start is not None:
        end = _year(post.get("end_year"))
        if end is None:
            end = start
        best, best_overlap = None, None
        for s in spec.get("subtitles") or []:
            a = _year(s.get("start_year"))
            b = _year(s.get("end_year"))
            a = -10**6 if a is None else a
            b = 10**6 if b is None else b
            overlap = min(end, b) - max(start, a)
            if best_overlap is None or overlap > best_overlap:
                best, best_overlap = s, overlap
        if best is not None and best_overlap >= 0:
            return _text(best.get("name")) or base

    forms = spec.get("forms") if isinstance(spec.get("forms"), dict) else {}
    male, female = _text(forms.get("male")), _text(forms.get("female"))
    if female and male and str(sex or "").strip().lower() == "female" and base.startswith(male):
        return female + base[len(male):]
    return base


def load_titles(files) -> dict:
    """name -> the title article's frontmatter, for every `type: title` note."""
    titles = {}
    for path in files:
        fm = parse_frontmatter(path)
        if fm.get("type") == "title":
            fm = dict(fm)
            fm["name"] = path.stem
            titles[path.stem] = fm
    return titles


def interlude_events(titles: dict, paths: dict) -> list[tuple[int, str, str]]:
    """Years a title stood in regency, dispute, vacancy or abolition."""
    events = []
    for name, spec in titles.items():
        link = f"[[{name}]]"
        for i in spec.get("interludes") or []:
            if not isinstance(i, dict):
                continue
            label = INTERLUDE_LABELS.get(str(i.get("kind") or "").strip().lower(), "Interlude")
            what = _text(i.get("name"))
            tail = f" ({what})" if what else ""
            notes = _notes_text(i)
            start, end = _year(i.get("start_year")), _year(i.get("end_year"))
            country = country_of(paths[name]) if name in paths else ""
            if start is not None:
                events.append((start, f"**{label} begins**: {link}{tail}{notes}", country))
            if end is not None:
                events.append((end, f"**{label} ends**: {link}{tail}", country))
    return events


# ── Spans ─────────────────────────────────────────────────────────────────────
# Anything with a start and an end: a term, a war, an institution's life, an
# interlude. The markdown shows these as two events; the site draws them as
# one bar, so they are collected here as well.

COUNTRIES = {
    "01 - Susia": "Susia", "02 - Confia": "Confia", "05 - Ditania": "Ditania",
    "07 - Ariwaro": "Ariwaro", "10 - Dripstanian Incria": "Incria",
    "99 - Rest of the World": "Rest of the world",
}


def country_of(rel: Path) -> str:
    return COUNTRIES.get(rel.parts[0], "")


def spans_of(fm: dict, name: str, rel: Path, titles: dict) -> list[dict]:
    country = country_of(rel)
    kind = str(fm.get("type") or "")
    out = []

    def add(lane, label, start, end, **extra):
        a, b = _year(start), _year(end)
        if a is None and b is None:
            return
        out.append({"lane": lane, "label": label, "start": a, "end": b,
                    "country": country, **{k: v for k, v in extra.items() if v}})

    if kind == "person":
        for post in (fm.get("titles") or []):
            if not isinstance(post, dict) or not _has(post.get("title")):
                continue
            title_name = _name(post.get("title"))
            spec = titles.get(title_name, {})
            add("titles", name, post.get("start_year"), post.get("end_year"),
                title=title_name, display=title_display(spec, post, fm.get("sex")),
                seat=_name(post.get("seat")), holder=name)
    elif kind in ("organization", "institution", "company"):
        add("institutions", name, fm.get("founded"), fm.get("dissolved"))
    elif kind in ("event", "war", "rebellion", "atrocity", "project"):
        add("events", name, fm.get("date_start"), fm.get("date_end"))
    return out


def interlude_spans(titles: dict, paths: dict) -> list[dict]:
    out = []
    for name, spec in titles.items():
        for i in spec.get("interludes") or []:
            if not isinstance(i, dict):
                continue
            label = INTERLUDE_LABELS.get(str(i.get("kind") or "").strip().lower(), "Interlude")
            a, b = _year(i.get("start_year")), _year(i.get("end_year"))
            if a is None and b is None:
                continue
            out.append({"lane": "titles", "label": _text(i.get("name")) or label,
                        "start": a, "end": b, "title": name,
                        "interlude": str(i.get("kind") or "other").strip().lower(),
                        "country": country_of(paths[name])})
    return out


# ── Event extraction ──────────────────────────────────────────────────────────

def extract_events(
    fm: dict,
    title: str,
    by_election: dict,
    titles: dict | None = None,
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

        # Titles only. A role is a job, not an office, so it produces no event.
        for office in entries("titles"):
            spec      = (titles or {}).get(_name(office.get("title")), {})
            appointer = office.get("appointer")
            start     = office.get("start_year")
            title_str = title_display(spec, office, fm.get("sex"))
            org       = _wl(spec.get("institution"))
            # "Emperor of the Dripstanian Empire at [[Dripstanian Empire]]"
            # says it twice, so the institution is dropped when the title
            # already names it
            at_org    = f" at {org}" if org and _name(org).lower() not in title_str.lower() else ""
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
    records: list[dict] = []          # the same events, for chronology.json

    files = [
        f for f in sorted(VAULT_ROOT.rglob("*.md"))
        if not any(part in SKIP_DIRS for part in f.relative_to(VAULT_ROOT).parts)
        and f.resolve() != OUTPUT_FILE.resolve()
    ]
    titles = load_titles(files)
    paths = {f.stem: f.relative_to(VAULT_ROOT) for f in files}
    spans: list[dict] = []

    def note(year: int, label: str, source: str, source_type: str, election: str = "",
             country: str = ""):
        by_year[year].append(label)
        m = re.match(r"\*\*(.+?)\*\*: (.*)", label, re.S)
        records.append({
            "year": year,
            "kind": m.group(1) if m else "",
            "text": m.group(2) if m else label,
            "source": source,
            "source_type": source_type,
            **({"country": country} if country else {}),
            **({"election": election} if election else {}),
        })

    for md_file in files:
        fm = parse_frontmatter(md_file)
        if not fm:
            continue

        title = md_file.stem
        rel = md_file.relative_to(VAULT_ROOT)
        for year, label in extract_events(fm, title, by_election, titles):
            note(year, label, title, str(fm.get("type") or ""), country=country_of(rel))
        spans.extend(spans_of(fm, title, rel, titles))

    for year, label, country in interlude_events(titles, paths):
        note(year, label, "", "title", country=country)
    spans.extend(interlude_spans(titles, paths))

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

    # The election blocks carry their own records, added here so the JSON
    # holds every event the markdown does.
    for (year, election_link), people in by_election.items():
        for entry in people:
            records.append({"year": year, "kind": "Appointment", "text": entry,
                            "source": "", "source_type": "person", "election": election_link})
    records.sort(key=lambda r: (r["year"], r["kind"], r["text"]))
    spans.sort(key=lambda s: (s["start"] if s["start"] is not None else 10**6,
                              s["end"] if s["end"] is not None else 10**6, s["label"]))
    with open(JSON_FILE, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"events": records, "spans": spans}, f, ensure_ascii=False, indent=1)
        f.write("\n")

    total_regular  = sum(len(v) for v in by_year.values())
    total_election = sum(len(v) for v in by_election.values())
    total          = total_regular + total_election
    # ASCII only: a Windows console on a legacy code page cannot encode
    # typographic characters and would raise after the file was written.
    print(
        f"CHRONOLOGY.md written: {total} events across {len(by_year)} years "
        f"({len(by_election)} election block(s)); "
        f"chronology.json: {len(records)} events, {len(spans)} spans."
    )


if __name__ == "__main__":
    main()
