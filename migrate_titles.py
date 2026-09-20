#!/usr/bin/env python3
"""
migrate_titles.py

One-off pass that turns the `offices` field of person articles into the new
`titles` and `roles` fields. Dry run by default: it prints what it would do
and writes nothing. Pass --write to apply.

Mapping decisions are in TITLES, ROLES and FIXES below, all settled with the
author on 20 September 2026. Anything not listed is reported and left alone.
"""
import argparse, os, re, sys, io
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

VAULT = Path(os.environ.get("VAULT_ROOT", "."))
SKIP = {".git", ".github", ".githooks", ".obsidian", "_fileClasses", "_templates", "node_modules", "00 - Meta"}
AS_EPOCH = 1950            # vault year = AS_EPOCH - AS, from the family-chart reconciliations

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096
yaml.indent(mapping=2, sequence=4, offset=2)

# (title, employer) -> (title article, seat or None). Employer None matches any.
TITLES = {
    ("Emperor of the Dripstanian Empire", None): ("Emperor of the Dripstanian Empire", None),
    ("Empress of the Dripstanian Empire", None): ("Emperor of the Dripstanian Empire", None),
    ("President of Susia", None):                ("President of Susia", None),
    ("Vice President of Susia", None):           ("Vice President of Susia", None),
    ("Senator for Postia", None):                ("Senator", "Postia"),
    ("Governor of Postia", None):                ("Susian Governor", "Postia"),
    ("Secretary of Justice", None):              ("Susian Secretary", "Justice"),
    ("State Governor of North Nijbania", None):  ("Confian State Governor", "North Nijbania"),
    ("Commissar of Education", None):            ("Confian Commissar", "Education"),
    ("Commissar of Health", None):               ("North Nijbanian Commissar", "Health"),
    ("Mayor of Imgospalje", None):               ("Confian Mayor", "Imgospalje"),
    ("President of the Confian Nation", None):       ("Confian President", None),
    ("Leader of the Confian Nation", None):          ("Confian President", None),
    ("President of the Confian Social Republic", None): ("Confian President", None),
    ("President of the Republic", None):             ("Confian President", None),
    ("President of the Council of Commissars of the United Syndicates of Confia", None):
                                                     ("Confian Prime Minister", None),
    ("First Secretary of the Union of Confian Syndicalists", None):
        ("First Secretary of the Union of Confian Syndicalists", None),
    ("Director of the Central Bank of the Confian Nation", None):
        ("Director of the Central Bank of the Confian Nation", None),
    ("Member of the National Assembly of Confian Syndicates", None):
        ("Member of the National Assembly of Confian Syndicates", None),
    ("Member of the General Government of the Federated Provinces of Galil", None):
        ("Member of the General Government of the Federated Provinces of Galil", None),
    ("Delegate, Constitutional Convention", None): ("Delegate to the Constitutional Convention", None),
    ("President of Yar-Firol", None):              ("President of Yar-Firol", None),
    ("CEO", "Soites Group"):                       ("CEO of the Soites Group", None),
    ("Emperor of Zaphonia", None):                 ("Emperor of Zaphonia", None),   # shape settled later
    ("Queen of Zaphonia", None):                   ("Queen of Zaphonia", None),     # shape settled later
}

# (title, employer) that become plain jobs. Employer None matches any.
ROLES = {
    ("Engineer", None),
    ("Journalist", None),
    ("Independent contractor", None),
    ("Philosophical Advisor", None),
    ("Board Member", None),
    ("Regional Operations Manager, Central-East", None),
    ("President", "Žošewoš Machinery"),
}

# Per-person corrections, applied after the mapping.
#   drop:  (title, start_year) entries to remove
#   set:   (title, start_year) -> {field: value}
#   add:   whole new title entries
FIXES = {
    "Empress Prazde": {
        # The bare "Empress" entry Martín ruled on lives in `occupation`, not
        # `offices`, so this pass leaves it alone. See the report's notes.
        "set":  {("Queen of Zaphonia", None): {"start_year": 1793, "end_year": 1825,
                 "notes": "157 AS to 125 AS in the family chart."}},
    },
    "Empress Veronique": {
        "add": [{"title": DQ("[[Emperor of the Dripstanian Empire]]"), "start_year": 1740, "end_year": 1787,
                 "appointer": None, "parties": [None],
                 "notes": "Reign ends at 163 AS in the family chart. Took the throne after the regency council."}],
    },
    "Ňotrič Apaj": {
        "set": {("Independent contractor", 1985): {"end_year": 2042}},  # ran until his death
    },
    "Nisa Peskilonna": {
        "set": {("President of the Republic", None): {"start_year": 2014, "end_year": 2018}},
        "add": [{"title": DQ("[[Confian President]]"), "start_year": 2019, "end_year": 2023,
                 "appointer": None, "parties": [None], "notes": None}],
    },
}

def plain(v):
    """A string with any wikilinks reduced to their bare names."""
    if v is None: return None
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("|")[0], str(v)).strip()
    return s or None

def lookup(table, title, employer):
    for key in ((title, employer), (title, None)):
        if key in table if isinstance(table, set) else key in table:
            return key
    return None

def convert(entry):
    """One offices entry -> ('title'|'role'|None, new entry)."""
    title = plain(entry.get("title"))
    employer = plain(entry.get("employer"))
    if not title:
        return None, None
    key = lookup(TITLES, title, employer)
    if key:
        article, seat = TITLES[key]
        out = {"_from": title, "title": DQ(f"[[{article}]]")}
        if seat: out["seat"] = DQ(f"[[{seat}]]")
        for f in ("start_year", "end_year", "appointer", "parties", "notes"):
            if f in entry: out[f] = entry[f]
        return "title", out
    key = lookup(ROLES, title, employer)
    if key:
        out = {"_from": title, "role": title, "employer": DQ(f"[[{employer}]]") if employer else None}
        for f in ("start_year", "end_year", "notes"):
            if f in entry: out[f] = entry[f]
        return "role", out
    return None, None

TITLE_WORDS = ("king", "queen", "emperor", "empress", "prince", "princess", "duke", "duchess",
               "count", "countess", "baron", "baroness", "consort", "heir", "lord", "lady")

def looks_like_title(name):
    n = (plain(name) or "").lower()
    return any(w in n.split() or n.startswith(w + " ") or f" {w} " in n or n.endswith(" " + w)
               for w in TITLE_WORDS)

def restates(occ_title, title_names):
    """True when an occupation entry just repeats a title the person holds."""
    o = (plain(occ_title) or "").lower().strip()
    if not o: return False
    for n in title_names:
        n = n.lower().strip()
        if o == n or n.startswith(o + " ") or o.startswith(n + " "):
            return True
    return False

EMPTY_BLOCKS = [
    "titles:", "  - title:", "    seat:", "    start_year:", "    end_year:",
    "    appointer:", "    parties:", "      -", "    notes:", "",
    "roles:", "  - role:", "    employer:", "    start_year:", "    end_year:", "    notes:",
]

def rename_offices_header(front):
    return re.sub(r"^# ── OFFICES ─+$",
                  lambda mm: "# ── TITLES AND ROLES " + "─" * max(1, len(mm.group(0)) - 22),
                  front, flags=re.M)

def empty_block_rewrite(path, write):
    """A person (or the template) whose offices block is blank: swap it for
    blank titles and roles blocks, so every article carries the new shape."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if not m: return False
    lines = m.group(1).split("\n")
    span = block_span(lines, "offices")
    if not span: return False
    a, b = span
    if write:
        lines[a:b] = EMPTY_BLOCKS
        front = rename_offices_header("\n".join(l.rstrip() for l in lines))
        path.write_text("---\n" + front + "\n---\n" + text[m.end():], encoding="utf-8")
    return True

def block_span(lines, key):
    """Line range of a top-level `key:` block, body included, comments and
    blank lines that belong to the next section excluded."""
    for i, l in enumerate(lines):
        if l.startswith(key + ":"):
            j = i + 1
            while j < len(lines):
                if lines[j].startswith((" ", "\t")):
                    j += 1; continue
                break
            return i, j
    return None

def dump_block(key, items):
    buf = io.StringIO(); yaml.dump({key: items}, buf)
    return buf.getvalue().rstrip("\n").split("\n")

def person_files():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for f in sorted(files):
            if f.endswith(".md"):
                yield Path(root) / f

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply the changes")
    args = ap.parse_args()

    report, unmapped, titles_seen, nobility_seen, empty = [], [], {}, [], []
    changed = 0
    for path in person_files():
        text = path.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
        if not m: continue
        try:
            data = yaml.load(m.group(1))
        except Exception as e:
            report.append(f"!! {path.name}: unreadable frontmatter ({e})")
            continue
        if not data: continue
        entries = [e for e in (data.get("offices") or []) if isinstance(e, dict) and plain(e.get("title"))]
        # a person with no offices is still processed when FIXES adds one
        if not entries and path.stem not in FIXES:
            if empty_block_rewrite(path, args.write):
                empty.append(str(path.relative_to(VAULT)))
            continue

        titles, roles, lines = [], [], []
        for e in entries:
            kind, out = convert(e)
            if kind is None:
                unmapped.append(f"{path.name}: {plain(e.get('title'))} at {plain(e.get('employer'))}")
                continue
            (titles if kind == "title" else roles).append(out)
            lines.append((kind, plain(e.get("title")), out))

        fix = FIXES.get(path.stem, {})
        # fixes match on the ORIGINAL title, and optionally the start year
        for t, y in fix.get("drop", []):
            before = len(titles)
            titles = [x for x in titles if not (x.get("_from") == t and (y is None or x.get("start_year") == y))]
            if len(titles) != before: lines.append(("drop", t, None))
        for (t, y), fields in fix.get("set", {}).items():
            for x in titles + roles:
                if x.get("_from") == t and (y is None or x.get("start_year") == y):
                    x.update(fields); lines.append(("set", t, fields)); break
            else:
                report.append(f"   !! fix for {t} in {path.stem} matched nothing")
        for extra in fix.get("add", []):
            titles.append(extra); lines.append(("add", plain(extra["title"]), extra))

        # Occupations that just repeat a title go; occupations that repeat a
        # role stay, and so do titles that only ever existed as occupations.
        held = [plain(x.get("_from")) for x in titles] + [plain(x.get("title")) for x in titles]
        held = [h for h in held if h]
        occ = data.get("occupation")
        kept_occ, nobility = None, []
        if isinstance(occ, list):
            kept_occ = []
            for o in occ:
                name = o.get("title") if isinstance(o, dict) else o
                if name and restates(name, held):
                    lines.append(("occ", plain(name), None))
                elif name and looks_like_title(name) and not restates(name, held):
                    nobility.append(plain(name)); kept_occ.append(o)
                else:
                    kept_occ.append(o)

        for x in titles:
            a = plain(x["title"]); titles_seen.setdefault(a, set())
            if x.get("seat"): titles_seen[a].add(plain(x["seat"]))

        report.append(f"\n{path.relative_to(VAULT)}")
        for kind, name, out in lines:
            if kind == "title":
                seat = f" seat {plain(out['seat'])}" if out.get("seat") else ""
                report.append(f"   title  {name:55.55} -> [[{plain(out['title'])}]]{seat}  {out.get('start_year')}-{out.get('end_year')}")
            elif kind == "role":
                report.append(f"   role   {name:55.55} -> {plain(out.get('employer'))}  {out.get('start_year')}-{out.get('end_year')}")
            elif kind == "drop":
                report.append(f"   DROP   {name:55.55} duplicate")
            elif kind == "set":
                report.append(f"   FIX    {name:55.55} {out}")
            elif kind == "add":
                report.append(f"   ADD    {name:55.55} {out.get('start_year')}-{out.get('end_year')}")
            elif kind == "occ":
                report.append(f"   OCC    {name:55.55} removed, the title says it")
        changed += 1

        for x in titles + roles:
            x.pop("_from", None)

        for n in nobility:
            nobility_seen.append(f"{path.stem}: {n}")

        if args.write:
            # Only the two blocks are rewritten. Everything else in the
            # frontmatter, comments and blank lines included, is left byte for
            # byte as the author wrote it.
            lines = m.group(1).split("\n")

            if kept_occ is not None and len(kept_occ) != len(data.get("occupation") or []):
                span = block_span(lines, "occupation")
                if span:
                    a, b = span
                    # an emptied block keeps the template's blank entry, the
                    # way the rest of the vault leaves unused fields
                    lines[a:b] = dump_block("occupation", kept_occ) if kept_occ else \
                        ["occupation:", "  - title:", "    start_year:", "    end_year:"]

            new = []
            if titles: new += dump_block("titles", titles)
            if roles: new += dump_block("roles", roles)
            span = block_span(lines, "offices")
            if span:
                a, b = span
                lines[a:b] = new
            else:
                lines += [""] + new

            front = "\n".join(l.rstrip() for l in lines)
            front = re.sub(r"^# ── OFFICES ─+$", lambda mm: "# ── TITLES AND ROLES " + "─" * max(1, len(mm.group(0)) - 22),
                           front, flags=re.M)
            path.write_text("---\n" + front + "\n---\n" + text[m.end():], encoding="utf-8")

    print("\n".join(report))
    tpl = VAULT / "00 - Meta" / "Templates" / "Person Template.md"
    if tpl.exists() and empty_block_rewrite(tpl, args.write):
        empty.append(str(tpl.relative_to(VAULT)))

    print(f"\n=== {changed} person articles rewritten, {len(empty)} blank offices blocks swapped, "
          f"{'written' if args.write else 'dry run'}")
    if unmapped:
        print(f"\n=== {len(unmapped)} entries with no mapping:")
        for u in unmapped: print("   " + u)
    if nobility_seen:
        print(f"\n=== {len(nobility_seen)} title-like occupations with no office entry (left alone, "
              f"they may deserve titles of their own):")
        for n in nobility_seen: print("   " + n)
    print(f"\n=== {len(titles_seen)} title articles to create:")
    for t in sorted(titles_seen):
        seats = ", ".join(sorted(titles_seen[t]))
        print(f"   {t}" + (f"   seats: {seats}" if seats else ""))

main()
