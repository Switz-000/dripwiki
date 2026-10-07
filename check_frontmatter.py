#!/usr/bin/env python3
"""
check_frontmatter.py — validate every vault article against 00 - Meta/YAML and Tags.md

Run from the repo root:   python check_frontmatter.py

Exit codes:  0 = no errors        1 = errors found        2 = could not run

Findings are split into two severities:

  ERROR    the file is wrong. Broken links, invalid vocabulary, malformed YAML.
           These fail silently in Obsidian, which is why the checker exists.

  GAP      the file is incomplete. Missing summary, era, tags, required fields.
           Expected on a stub; not a defect.

--errors-only suppresses gaps. Use it in CI, where the question is "did this
change break the schema", not "is the vault finished".

--dates adds a third list, which never changes the exit code:

  DATE     a date in an article body or flags block that is not in a stored
           form: a prose date, an AS year or a Dripstanian month name. The
           rule is in the Dates section of 00 - Meta/Style Guide.md. These
           are matched by pattern, so read each one before acting on it.
"""
import os, re, sys, argparse, collections, datetime, unicodedata

try:
    import yaml
except ImportError:
    print("check_frontmatter: needs pyyaml  ->  pip install pyyaml", file=sys.stderr)
    sys.exit(2)

sys.dont_write_bytecode = True      # keep __pycache__ out of the vault
from vault_dates import parse as parse_date

ROOT   = os.path.dirname(os.path.abspath(__file__))
SKIP   = {".git", ".github", ".githooks", ".obsidian", "00 - Meta"}

TYPES = set("""country state city region geography fez company product person institution
organization law project treaty event war atrocity period rebellion movement ideology
religion concept tradition sport document technology disease species language structure
index meta ethnicity family title""".split())

ERAS = set("""pre-colonial settlement imperial-era early-imperial high-imperial fraternal-war
late-imperial liberal-revolts dissolution republican-era continental-divide continental-war
post-war new-age great-transition global-cold-war techno-federative-era enhancement-era
contemporary aiding-state home-rule secession-war state-of-confia confian-anarchy
united-syndicates paulowic-regime syndicalist-republic social-republic
company-rule general-government united-republics nguan-regime warlord-period bershadi-civil-war
bershadi-partition rally-state keke-era dominion-of-sekyo sekyan-free-state
sekyan-provisional-government state-of-sekyo united-republic-of-sekyo""".split())

TAG_TREE = {
 "politics":  "governance elections dissent monarchy revolution nationalism law diplomacy".split(),
 "economy":   "corporate labor finance industry agriculture energy".split(),
 "society":   "demographics urbanism welfare education immigration race crime".split(),
 "culture":   "tradition arts sport media language firearms".split(),
 "belief":    "religion philosophy ideology".split(),
 "conflict":  "military intelligence".split(),
 "knowledge": "science technology medicine enhancement biology".split(),
 "land":      "geography infrastructure colonial".split(),
}
TAGS = set(TAG_TREE) | {f"{p}/{l}" for p, ls in TAG_TREE.items() for l in ls}

# `tags` is Required in the schema, but 306 articles predate the requirement.
# Until the tagging pass closes that backlog, a missing tags list is reported as
# a gap rather than an error, so CI keeps signalling on real breakage. Flip this
# to True when the backlog is clear.
ENFORCE_TAGS = False

SEX      = {"Male", "Female", "Non-binary"}
RETIRED  = {"spouse": "a relations entry with relation: Spouse",
            "children_count": "a relations entry with relation: Child"}

PERSON_REQ = ["type", "summary", "sex", "ethnicity", "citizenship", "nationality", "enhanced"]
INST_REQ   = ["type", "summary", "nature", "founded", "era", "tags", "meta"]

NUMERIC_HINT = re.compile(r"^\s*([\w]+):[ \t]*\"(\d+)\"[ \t]*$", re.M)
BARE_LINK    = re.compile(r"^\s*(?:-\s+)?[\w]+:[ \t]+\[\[", re.M)
BARE_LIST    = re.compile(r"^\s*-[ \t]+\[\[", re.M)
HALF_LINK    = re.compile(r"\[\[[^\]\n]*\](?!\])")

# ── Dates ─────────────────────────────────────────────────────────────────────
# Fields that hold a date, at any depth. Each takes one of the four stored
# forms: yyyy, mm/yyyy, dd/mm/yyyy, or dd/mm for a date that recurs yearly.
DATE_KEYS = {"year", "founded", "dissolved", "established", "date_start", "date_end",
             "granted", "revoked", "yarnojte_granted", "yarnojte_revoked", "awarded",
             "creation", "in_service_start", "in_service_end"}

def is_date_key(k):
    return isinstance(k, str) and (k in DATE_KEYS or k.endswith("_year"))

GREG_MONTHS = ("January|February|March|April|May|June|July|August|September|"
               "October|November|December")

# The calendar's months, written without accents and in lower case. Canon
# first, then the Susian eighth month, then the two superseded drafts and the
# names the site's clock once used. Whole words only, so the people the
# months are named after (Jartes, Agamilos, Veronique, Mantichev, Olod) and
# the Doremojian League never match.
DRIP_MONTHS = set("""teosary olody vertery boraly mantichevean agamilean veroniquean jartean
lichevy vereny versijean
olodio nikolaio boralio agamilio tichendo petendo chestendo semendo vossendo
lichevio mantichevio doremogio veroniquio vartelio jartio verenio
theosio veronicio""".split())
# Anglicised draft names double as ordinary adjectives (a Mantichevian
# church, the Doremojian League), so they only count beside a day or a year.
DRIP_ADJ = "Mantichevian|Vartelian|Verenian|Boralian|Agamilian|Veroniquian|Olodian|Jartian|Lichevian|Doremojian|Teosian"

def fold(s):
    """Lower case, accents removed."""
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()

ORD = r"(?:st|nd|rd|th)?"
PROSE_DATE = re.compile(
    rf"\b(?:\d{{1,2}}{ORD}\s+(?:of\s+)?(?:{GREG_MONTHS})\b(?:,?\s+(?:of\s+)?\d{{4}}\b)?"
    rf"|(?:{GREG_MONTHS})\s+\d{{1,2}}{ORD},\s*\d{{4}}\b"
    rf"|(?:{GREG_MONTHS}),?\s+(?:of\s+)?\d{{4}}\b)")
AS_YEAR    = re.compile(r"\b\d{1,4}\s?AS\b")           # capitals only: never the word "as"
WORD       = re.compile(r"[^\W\d_]+")
ADJ_DATE   = re.compile(
    rf"\b\d{{1,2}}{ORD}\s+(?:of\s+)?(?:{DRIP_ADJ})\b"
    rf"|\b(?:{DRIP_ADJ})\s*(?:\(\d{{1,2}}\)|\d{{1,2}}{ORD}\b|,?\s+(?:of\s+)?\d{{3,4}}\b)")

# Not scanned for body dates: the calendar's own article is written in its
# dates by design, and the chronology is generated.
DATE_SCAN_SKIP = {"Dripstanian calendar.md", "CHRONOLOGY.md"}

def date_hint(v):
    """What is probably wrong with a value that is not a stored date form."""
    if isinstance(v, (datetime.date, datetime.datetime)):
        return "an ISO date; write dd/mm/yyyy"
    if isinstance(v, float):
        return "not a whole year"
    s = str(v).strip()
    if re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", s):
        return "an ISO date; write dd/mm/yyyy or mm/yyyy"
    if re.search(r"[~?]|\b(circa|around|about|c\.)", s, re.I):
        return "approximate; give the best single value and record the doubt in the flags"
    if AS_YEAR.search(s) or any(fold(w) in DRIP_MONTHS for w in WORD.findall(s)) or re.search(DRIP_ADJ, s):
        return "a Dripstanian date; convert it to Gregorian"
    if re.search(GREG_MONTHS, s):
        return "a prose date; write dd/mm/yyyy or mm/yyyy"
    if re.search(r"\d\s*(?:-|–|—|\bto\b)\s*\d", s) or re.fullmatch(r"\d{3,4}s", s):
        return "a range or decade; a date field holds one date"
    if re.fullmatch(r"\d{1,2}/\d{1,2}(/\d{2,4})?|\d{1,2}/\d{4}", s):
        return "day and month take two digits and must be a real date"
    return "a date field holds a date and nothing else"

errors, gaps, dates = [], [], []
def err(p, msg): errors.append((p, msg))
def gap(p, msg): gaps.append((p, msg))

def scan_body_dates(rel, body):
    """Dates in the body or flags block that are not in a stored form."""
    for n, line in enumerate(body.splitlines(), 1):
        found = [m.group(0) for m in PROSE_DATE.finditer(line)]
        found += [m.group(0) for m in AS_YEAR.finditer(line)]
        found += [m.group(0) for m in ADJ_DATE.finditer(line)]
        found += [w for w in WORD.findall(line) if fold(w) in DRIP_MONTHS]
        for f in dict.fromkeys(found):
            dates.append((rel, f"body line {n}: {f}"))

def empty(v):
    if v is None: return True
    if isinstance(v, str):  return not v.strip()
    if isinstance(v, list): return all(empty(x) for x in v)
    if isinstance(v, dict): return all(empty(x) for x in v.values())
    return False

def nested_link(v):
    """A wikilink that YAML turned into a list-of-lists, or already stripped to one."""
    return isinstance(v, list) and v and isinstance(v[0], list)

def walk(v, cb):
    if isinstance(v, dict):
        for k, x in v.items(): cb(k, x); walk(x, cb)
    elif isinstance(v, list):
        for x in v: walk(x, cb)

def check(path, rel, body_dates=False):
    raw = open(path, encoding="utf-8", errors="replace").read()

    if "\x00" in raw:
        err(rel, f"contains {raw.count(chr(0))} NUL bytes — file is treated as binary by search and git")

    if not raw.startswith("---"):
        err(rel, "no frontmatter: file does not begin with ---")
        return
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", raw, re.S)
    if not m:
        err(rel, "frontmatter opened with --- but never closed")
        return
    fmtext, body = m.group(1), raw[m.end():]

    if "\t" in fmtext:
        err(rel, "tab character in frontmatter — YAML forbids tabs for indentation")
    for mm in BARE_LINK.finditer(fmtext) :
        err(rel, f"unquoted wikilink: {mm.group(0).strip()}…  — wrap the value in double quotes")
    for mm in BARE_LIST.finditer(fmtext):
        err(rel, f"unquoted wikilink in list item: {mm.group(0).strip()}…  — wrap the value in double quotes")
    for mm in HALF_LINK.finditer(fmtext):
        err(rel, f"malformed wikilink, single closing bracket: {mm.group(0)}")
    for mm in NUMERIC_HINT.finditer(fmtext):
        err(rel, f"quoted number: {mm.group(1)}: \"{mm.group(2)}\" — remove the quotes")

    try:
        fm = yaml.safe_load(fmtext)
    except Exception as e:
        err(rel, f"YAML will not parse: {str(e).splitlines()[0]}")
        return
    if not isinstance(fm, dict):
        err(rel, "frontmatter parses to nothing")
        return

    def cb(k, v):
        if nested_link(v):
            err(rel, f"{k}: became a nested list — an unquoted wikilink that has lost its brackets")
    walk(fm, cb)

    def date_cb(k, v):
        if not is_date_key(k) or isinstance(v, (dict, list)) or empty(v):
            return
        if isinstance(v, bool) or parse_date(v) is None:
            err(rel, f"{k}: {v!s} is not a stored date form ({date_hint(v)})")
    walk(fm, date_cb)

    if body_dates and os.path.basename(rel) not in DATE_SCAN_SKIP:
        scan_body_dates(rel, body)

    for f, repl in RETIRED.items():
        if f in fm: err(rel, f"retired field `{f}` — replace with {repl}")

    t = fm.get("type")
    if empty(t):                     err(rel, "no `type`")
    elif t not in TYPES:             err(rel, f"unknown type `{t}` — not in the vocabulary")

    for key, vocab in (("era", ERAS), ("tags", TAGS)):
        v = fm.get(key, "__absent__")
        if v == "__absent__" or empty(v):
            if key == "tags":
                (err if ENFORCE_TAGS else gap)(rel, "`tags` is empty — required by the schema")
            elif v != "__absent__": gap(rel, f"`{key}` is empty")
            continue
        if isinstance(v, str):
            err(rel, f"`{key}` is a single value, should be a list")
            v = [v]
        if isinstance(v, list):
            for x in v:
                if empty(x): continue
                if not isinstance(x, str) or x not in vocab:
                    err(rel, f"unknown {key} value `{x}`")
                elif key == "tags" and "/" not in x:
                    gap(rel, f"tag `{x}` is a bare parent — refine to a leaf where one fits")

    mv = fm.get("meta")
    if mv is None:
        gap(rel, "no `meta` block")
    elif not isinstance(mv, dict):
        err(rel, "`meta` is not a mapping")
    else:
        for k in ("stub", "verified"):
            if k in mv and not isinstance(mv[k], bool):
                err(rel, f"meta.{k} should be true or false, found {mv[k]!r}")

    if empty(fm.get("summary")): gap(rel, "no `summary`")

    if t == "person":
        s = fm.get("sex")
        if not empty(s) and s not in SEX:
            err(rel, f"sex `{s}` — must be Male, Female or Non-binary")
        if "enhanced" in fm and not isinstance(fm["enhanced"], bool):
            err(rel, f"`enhanced` should be true or false, found {fm['enhanced']!r}")
        miss = [f for f in PERSON_REQ if empty(fm.get(f))]
        if empty(fm.get("birth")): miss.append("birth")
        if miss: gap(rel, "person missing required: " + ", ".join(miss))
    elif t == "institution":
        miss = [f for f in INST_REQ if empty(fm.get(f))]
        if miss: gap(rel, "institution missing required: " + ", ".join(miss))

    words = len(re.findall(r"\w+", body))
    st = mv.get("stub") if isinstance(mv, dict) else None
    if st is False and words < 80:
        err(rel, f"meta.stub is false but the body has {words} words")

def main():
    ap = argparse.ArgumentParser(description="Validate vault frontmatter.")
    ap.add_argument("--errors-only", action="store_true", help="suppress incompleteness gaps")
    ap.add_argument("--dates", action="store_true",
                    help="also list dates in article bodies that are not in a stored form")
    a = ap.parse_args()

    n = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP]
        if os.path.relpath(dp, ROOT).split(os.sep)[0] in SKIP: continue
        for f in sorted(fn):
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                check(p, os.path.relpath(p, ROOT), a.dates); n += 1

    def show(items, label):
        by = collections.defaultdict(list)
        for p, msg in items: by[p].append(msg)
        for p in sorted(by):
            print(f"\n  {p}")
            for msg in by[p]: print(f"      {label} {msg}")

    if errors:
        print(f"\n{'='*72}\nERRORS — {len(errors)} in {len({p for p,_ in errors})} files")
        show(errors, "✗")
    if gaps and not a.errors_only:
        print(f"\n{'='*72}\nGAPS — {len(gaps)} in {len({p for p,_ in gaps})} files (incomplete, not wrong)")
        show(gaps, "·")

    if a.dates and dates:
        print(f"\n{'='*72}\nDATES — {len(dates)} in {len({p for p,_ in dates})} files "
              f"(not in a stored form; matched by pattern, so check each)")
        show(dates, "!")

    print(f"\n{'='*72}")
    print(f"{n} articles checked — {len(errors)} errors, {len(gaps)} gaps")
    if not ENFORCE_TAGS:
        pending = sum(1 for _, m in gaps if m.startswith("`tags` is empty"))
        if pending:
            print(f"note: {pending} articles have no tags. Required by the schema, "
                  f"not yet enforced (see ENFORCE_TAGS).")
    if not errors: print("no schema errors")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
