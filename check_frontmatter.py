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
"""
import os, re, sys, argparse, collections

try:
    import yaml
except ImportError:
    print("check_frontmatter: needs pyyaml  ->  pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT   = os.path.dirname(os.path.abspath(__file__))
SKIP   = {".git", ".github", ".githooks", ".obsidian", "00 - Meta"}

TYPES = set("""country state city region geography fez company product person institution
organization law project treaty event war atrocity period rebellion movement ideology
religion concept tradition sport document technology disease species language structure
index meta ethnicity family""".split())

ERAS = set("""pre-colonial settlement imperial-era early-imperial high-imperial fraternal-war
late-imperial liberal-revolts dissolution republican-era continental-divide continental-war
post-war new-age great-transition global-cold-war techno-federative-era enhancement-era
contemporary aiding-state home-rule secession-war state-of-confia confian-anarchy
united-syndicates paulowic-regime syndicalist-republic social-republic""".split())

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

errors, gaps = [], []
def err(p, msg): errors.append((p, msg))
def gap(p, msg): gaps.append((p, msg))

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

def check(path, rel):
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
    a = ap.parse_args()

    n = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP]
        if os.path.relpath(dp, ROOT).split(os.sep)[0] in SKIP: continue
        for f in sorted(fn):
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                check(p, os.path.relpath(p, ROOT)); n += 1

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
