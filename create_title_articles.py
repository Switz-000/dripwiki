#!/usr/bin/env python3
"""
create_title_articles.py

Creates the title articles the migration needs, one file per title, in the
titles folder of the country it belongs to. Dry run by default; --write
creates the files. Existing files are never overwritten.

Every field the author has to settle is left blank. Years taken from the
holders rather than from canon carry a comment saying so.
"""
import argparse, os
from pathlib import Path

VAULT = Path(os.environ.get("VAULT_ROOT", "."))
SUSIA, CONFIA = "01 - Susia/09 - Titles", "02 - Confia/09 - Titles"
INCRIA, WORLD = "10 - Dripstanian Incria/Titles", "99 - Rest of the World/Titles"

SUSIAN_STATES = ["Dripia", "Misocévia", "Nessel", "Neutral District", "New Celiolaj",
                 "Orlítia", "Postia", "Sužielaj", "Troli", "Vitrika"]
CONFIAN_STATES = ["Ewenogia", "Gorepalje", "Hašterlan", "Karlotopol'", "Koštanože",
                  "Legrinpija", "Nakotšatija", "North Nijbania", "South Nijbania", "Žošewoš"]

def seats(names, maxh, pattern):
    """pattern names the seat the way canon already writes it, e.g. 'Senator for {}'."""
    return [{"name": pattern.format(n), "for": n, "max_holders": maxh} for n in names]

TITLES = [
    # (folder, name, institution, extras)
    (SUSIA, "Emperor of the Dripstanian Empire", "Dripstanian Empire", {
        "forms": {"male": "Emperor", "female": "Empress"}, "max_holders": 1, "numbered": True,
        "interludes": [
            {"kind": "regency", "name": "Regency council", "start_year": 1738, "end_year": 1740,
             "notes": "The throne passed to [[Empress Veronique]] in 1740."},
            {"kind": "disputed", "name": None, "start_year": 1815, "end_year": 1823,
             "notes": "Civil war. [[Empress Prazde]] and [[Jartes I]] both claimed the throne."},
        ]}),
    (SUSIA, "President of Susia", "Susian Federal Government", {"max_holders": 1, "numbered": True}),
    (SUSIA, "Vice President of Susia", "Susian Federal Government", {"max_holders": 1, "numbered": True}),
    (SUSIA, "Susian Secretary", "Susian Federal Government", {
        "max_holders": 1, "numbered": True,
        "seats": [{"name": "Secretary of Justice", "for": "Justice", "max_holders": 1},
                  {"name": None, "for": None, "max_holders": 1}]}),
    (SUSIA, "Senator", "Susian Senate", {"numbered": False, "seats": seats(SUSIAN_STATES, 5, "Senator for {}")}),
    (SUSIA, "Susian Governor", None, {"numbered": True, "seats": seats(SUSIAN_STATES, 1, "Governor of {}")}),
    (SUSIA, "CEO of the Soites Group", "Soites Group", {"max_holders": 1, "numbered": True}),
    (SUSIA, "Delegate to the Constitutional Convention", None, {"numbered": False}),
    (SUSIA, "Member of the General Government of the Federated Provinces of Galil", None, {"numbered": False}),
    (CONFIA, "Confian President", "Confian National Government", {
        "max_holders": 1, "numbered": True,
        "subtitles": [
            {"name": "President of the Confian Nation", "start_year": None, "end_year": 1958},
            {"name": "Leader of the Confian Nation", "start_year": 1958, "end_year": 1977},
            {"name": "President of the Confian Nation", "start_year": 1978, "end_year": 1996},
            {"name": "President of the Confian Social Republic", "start_year": 2009, "end_year": None},
        ], "subtitles_note": "years taken from the holders, not from canon"}),
    (CONFIA, "Confian Prime Minister", "Confian National Government", {
        "max_holders": 1, "numbered": True,
        "subtitles": [{"name": "President of the Council of Commissars of the United Syndicates of Confia",
                       "start_year": 1978, "end_year": None}],
        "subtitles_note": "years taken from the holders, not from canon"}),
    (CONFIA, "Confian Commissar", "Confian National Government", {
        "max_holders": 1, "numbered": True,
        "seats": [{"name": "Commissar of Education", "for": "Education", "max_holders": 1},
                  {"name": None, "for": None, "max_holders": 1}]}),
    (CONFIA, "Confian State Governor", None, {"numbered": True, "seats": seats(CONFIAN_STATES, 1, "State Governor of {}")}),
    (CONFIA, "North Nijbanian Commissar", "North Nijbania", {
        "max_holders": 1, "numbered": True,
        "seats": [{"name": "Commissar of Health", "for": "Health", "max_holders": 1},
                  {"name": None, "for": None, "max_holders": 1}]}),
    (CONFIA, "Confian Mayor", None, {"numbered": True,
        "seats": [{"name": "Mayor of Imgospalje", "for": "Imgospalje", "max_holders": 1},
                  {"name": None, "for": None, "max_holders": 1}]}),
    (CONFIA, "Member of the National Assembly of Confian Syndicates", "Confian National Government", {"numbered": False}),
    (CONFIA, "First Secretary of the Union of Confian Syndicalists", "Confian Syndicalist Union", {"max_holders": 1, "numbered": True}),
    (CONFIA, "Director of the Central Bank of the Confian Nation", "Central Bank of the Confian Nation", {"max_holders": 1, "numbered": True}),
    (INCRIA, "President of Yar-Firol", None, {"max_holders": 1, "numbered": True}),
    (WORLD, "Emperor of Zaphonia", "Zaphonia", {"max_holders": 1, "numbered": True}),
    (WORLD, "Queen of Zaphonia", "Zaphonia", {"max_holders": 1, "numbered": True}),
]

HOLDERS = ("%% Holders below are generated by generate_lists.py from the titles field of\n"
           "person articles. Edit those articles, not this block. %%\n\n"
           "%% holders:start %%\n%% holders:end %%\n")

def link(v): return f'"[[{v}]]"' if v else ""

def frontmatter(name, institution, x):
    L = ["---", "type: title", "summary:", "aliases:", "  -", "era:", "  -", "tags:", "  -",
         f"institution: {link(institution)}".rstrip()]
    if "forms" in x:
        L += ["forms:", f"  male: {x['forms']['male']}", f"  female: {x['forms']['female']}"]
    if "max_holders" in x: L.append(f"max_holders: {x['max_holders']}")
    L.append(f"numbered: {'true' if x.get('numbered') else 'false'}")
    if "subtitles" in x:
        L.append("subtitles:" + (f"   # {x['subtitles_note']}" if x.get("subtitles_note") else ""))
        for s in x["subtitles"]:
            L += [f"  - name: {s['name'] or ''}".rstrip(),
                  f"    start_year: {s['start_year'] or ''}".rstrip(),
                  f"    end_year: {s['end_year'] or ''}".rstrip()]
    if "seats" in x:
        L.append("seats:")
        for s in x["seats"]:
            L += [f"  - name: {s['name'] or ''}".rstrip(),
                  f"    for: {link(s['for'])}".rstrip(),
                  f"    max_holders: {s['max_holders']}"]
    if "interludes" in x:
        L.append("interludes:")
        for i in x["interludes"]:
            L += [f"  - kind: {i['kind']}",
                  f"    name: {i['name'] or ''}".rstrip(),
                  f"    start_year: {i['start_year']}",
                  f"    end_year: {i['end_year']}",
                  f"    notes: {i['notes'] or ''}".rstrip()]
    L += ["meta:", "  stub: true", "  verified: false", "  image: null", "---", "", HOLDERS]
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); a = ap.parse_args()
    made = skipped = 0
    for folder, name, inst, extras in TITLES:
        path = VAULT / folder / f"{name}.md"
        if path.exists():
            print(f"   exists  {path.relative_to(VAULT)}"); skipped += 1; continue
        print(f"   create  {path.relative_to(VAULT)}")
        if a.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(frontmatter(name, inst, extras), encoding="utf-8")
        made += 1
    print(f"\n=== {made} title articles{' created' if a.write else ' would be created'}, {skipped} already there")

main()
