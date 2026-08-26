# YAML and Tags

The one file to read before writing frontmatter. Everything the vault enforces
about a YAML header is here: the rules, the base header, the three closed
vocabularies, and what each type adds on top.

If you have written for this vault before and are coming back, read the
**Changelog** at the foot of this file first. The schema has changed since it
was written, and nothing else will tell you that.

To check your work without reading any of this, run `python check_frontmatter.py`
from the repo root.

---

## 1. The five rules that cause silent damage

These are first because breaking them does not produce an error. The file looks
fine in Obsidian, commits without complaint, and is quietly wrong.

### 1.1 Quote every wikilink

```yaml
religion: "[[Sacoitism]]"      # correct
religion: [[Sacoitism]]        # silently broken
```

YAML reads an unquoted `[[` as the start of a nested list, so the second line
does not produce a link. It produces a list containing a list containing a
string, which no link query will ever match.

It gets worse. If anything then parses the file and writes it back — Obsidian's
Properties editor does exactly this — the nested list is re-serialised **without
the brackets**, and the link is gone for good:

```yaml
birth:
  city:
    - - Imgospalje       # this was once city: "[[Imgospalje]]"
```

Five values in the vault had already reached that state before it was noticed.

This applies inside list items too:

```yaml
citizenship:
  - "[[Confia|Confian]]"       # correct
  - [[Confia|Confian]]         # silently broken
```

### 1.2 Years are bare integers

```yaml
founded: 1966       # correct
founded: "1966"     # sorts as text, drops out of timeline queries
```

An approximate year goes in the field as the best single value, with the
approximation recorded in the flags block. Never `~1959`, never `circa 1740`,
never a range.

A year field holds a year and nothing else. `year: Disappeared 1977` belongs in
two fields: `year: 1977` and `cause: Disappeared`.

### 1.3 No quotes around any number

Populations, market caps, death tolls, counts. Same failure as years: a quoted
number is a string and will not compare, sort, or sum.

```yaml
population_1950: 92000       # correct
population_1950: "92000"     # broken
```

### 1.4 `type`, `era` and `tags` are closed vocabularies

A value not listed in this file is not a valid value. If the thing you are
writing has no type that fits, that is a real gap: say so and the vocabulary
gets extended. Do not invent a value in a file — it will not be found by
anything, and nobody will know it exists.

All three vocabularies are lowercase and hyphenated.

### 1.5 Never hand-edit `CHRONOLOGY.md`

It is generated from every article's frontmatter by `generate_chronology.py`,
which runs in CI on every push that touches a `.md` file. Anything you write
there is overwritten on the next push. To change the chronology, fix the dates
in the articles it reads.

---

## 2. The base header

Every article carries this, whatever its type. Type-specific templates in
`00 - Meta/Templates/` add fields on top of it. None of them replace it.

```yaml
---
type:            # required, single value from section 3
summary:         # required, one to two sentences of plain prose
aliases:
  -
era:             # required, from section 4
  -
tags:            # required, from section 5
  -
meta:
  stub: true
  verified: false
  image: null
---
```

**`summary`** is what appears in query results and hover previews, so it has to
carry the article alone. Name the subject, its role, and why it matters. Neutral
register, no wikilinks.

**`aliases`** are other names the subject is known by, so links and search
resolve. Optional, but keep the empty `-` rather than deleting the key.

**`meta.stub`** is true until the article meets Level 3 in section 7. It drives
the "what still needs writing" queries and is only useful if kept honest.

**`meta.verified`** is whether the facts have been checked against the rest of
the vault. Defaults to false.

A list key keeps its empty `-` entry when it has no values. Deleting the key
loses the shape of the header; leaving the dash does not.

---

## 3. `type` — what kind of article this is

Single value. Closed vocabulary.

```
country      state        city         region       geography
fez          company      product      person       institution
organization law          project      treaty       event
war          atrocity     period       rebellion    movement
ideology     religion     concept      tradition    sport
document     technology   disease      species      language
structure    index        meta
```

Notes on the ones that get confused:

- **`region`** is a named area that is not a state and not a city: a
  metropolitan area, a province, a constituent territory.
- **`geography`** is a natural feature: a river, a sea, a continent, a moon.
- **`period`** is a span of a polity's history. The polity itself is a
  `country`, even when it no longer exists. *General Government of Confia* is a
  `country`; *Paulowić regime* is a `period`.
- **`war`** for a whole conflict, **`event`** for a battle, revolt or crisis
  inside one, **`atrocity`** for a massacre or campaign against civilians.
- **`index`** for any list or index file, including generated ones.
- **`meta`** for worldbuilding worksheets that are not articles.

---

## 4. `era` — what historical period the article belongs to

A list. Multiple values allowed. Take the most specific era that applies.

Do not add a war or revolt era unless the subject was directly involved in it —
living through one is not involvement. Do not add an era someone only lived
through as a child.

**These are flat lists.** The indentation below shows which era contains which,
for your reading only. Do not reproduce it in a file — indenting a list item in
YAML makes it a child of the item above and breaks the list. Correct usage:

```yaml
era:
  - late-imperial
  - liberal-revolts
```

### Susia

```
pre-colonial              before Armotist arrival, 1651
settlement                1651–1674, first colonies
imperial-era              1674–1954
    early-imperial        1674–1740, Mantichev through Agamilos
    high-imperial         1740–1837, Veronique through Jartes I
        fraternal-war     1815–1823
    late-imperial         1837–1954, Jartes II through dissolution
        liberal-revolts   1840–1844
        dissolution       1950–1954, Tahuni Accords to the republic
republican-era            1954–2038
    continental-divide    1957–1977, cold war with Confia
        continental-war   1975–1977, hot war
    post-war              1977–2006, reconstruction and boom
    new-age               2006–2038, Amepur war, modernist movement
        great-transition  2036–2038, new constitution convention
global-cold-war           2006–present, Ashgerad cold war
techno-federative-era     2038–present, post great transition
    enhancement-era       2060s–present, cognitive enhancement period
    contemporary          2070s–2090s, present day of the world
```

### Confia

```
pre-colonial              before Racpalian colonization, 1780
settlement                1786–1811, first colonies
imperial-era              1786–1950
    early-imperial        1674–1740, Mantichev through Agamilos
    high-imperial         1740–1837, Veronique through Jartes I
        fraternal-war     1815–1823
    late-imperial         1837–1954, Jartes II through dissolution
        aiding-state      1845–1922
        home-rule         1922–1937, rule from St. Mantichev City
        secession-war     1937–1950
        state-of-confia   1950–1953
        confian-anarchy   1954–1956
united-syndicates         1956–2008, Proclamation to the 2008 constitution
    paulowic-regime       1956–1977, Presidential Empowerment Amendment to
                          the Bayonet Revolution
        continental-war   1975–1977, hot war
    syndicalist-republic  1977–2008
social-republic           2009–present
```

> **The Confian dates are under review and are known to disagree with
> themselves.** `imperial-era` is dated 1786–1950 while its own children run
> 1674–1954; `pre-colonial` ends 1780 while `settlement` begins 1786; there are
> gaps at 1953/1954 and 2008/2009; and `paulowic-regime` starts 1956 here while
> the *Paulowić regime* article dates it from 1958. The **slugs** are correct
> and safe to use. Treat the **dates** as provisional until this note is
> removed.

---

## 5. `tags` — what subject area the article belongs to

A list. Multiple values allowed. Apply all that describe the subject's primary
domains of activity, not every topic it touches.

```
politics      military      economy       corporate     law
journalism    intelligence  philosophy    religion      culture
sport         science       technology    medicine      geography
diplomacy     colonial      labor         media         education
infrastructure finance      energy        agriculture   crime
immigration   race          history
```

---

## 6. What each type adds

Twelve types have a template in `00 - Meta/Templates/`. Read it alongside this
file; where a companion reference exists in `00 - Meta/Template reference/`,
that file governs the type-specific fields and this one governs the base.

| Type | Template | Companion reference |
| --- | --- | --- |
| `person` | Person Template | Person template reference |
| `institution` | Institution Template | Institution template reference |
| `country` | Country Template | — |
| `state` | State Template | — |
| `city` | City Template | — |
| `company` | Company Template | — |
| `organization` | Political Party Template | — |
| `project` | Project Template | — |
| `event` | Rebellion Template | — |
| `atrocity` | Atrocity Template | — |
| `ideology` | Ideology Template | — |
| `document` | Interview Template | — |

The remaining types have no template yet. Use the base header from section 2
and add fields as the article needs them. Templates get written as each type
gets carved properly, rather than in advance.

Two fields worth stating explicitly because they are easy to get wrong:

- **`sex`** on a person is `Male`, `Female` or `Non-binary`. Capitalised.
  Closed vocabulary.
- **`relations`** replaces the old `spouse` and `children_count`. See the
  person template reference for the relation vocabulary and how to record an
  unnamed group of children.

---

## 7. Quality scale

Applies to every type. A type's Required and Recommended tiers are defined in
its companion reference; where none exists, the base header's required fields
are the Required tier.

1. **Stub** — missing one or more Required fields.
2. **Incomplete** — all Required present, some Recommended missing.
3. **Complete** — all Required and Recommended present.

Optional fields never affect the level.

A field that does not apply is left blank and does not count against the
article. `dissolved` on an extant institution, `death` on a living person, and
`state` on a birth predating the state layer are blank by correctness, not by
omission. Where a blank is a genuine gap in what the vault knows, record it in
the flags block.

An article can be long and still be a stub. A 1,600-word biography with no
`summary` is missing a Required field and is Level 1.

---

## 8. Checking your work

```
python check_frontmatter.py
```

Run from the repo root. It reads every article outside `00 - Meta/` and reports
anything that breaks this file. No arguments, no setup beyond `pip install pyyaml`.

Do not rely on reading this document to stay correct. Run the checker.

---

## 9. Retired fields

Remove these on sight when editing any file.

| Field | Retired | Replaced by |
| --- | --- | --- |
| `spouse` | 2026-08-26 | a `relations` entry with `relation: Spouse` |
| `children_count` | 2026-08-26 | a `relations` entry with `person` blank, `relation: Child`, and the number in `notes` |

---

## 10. Changelog

Newest first. If you have not written for the vault since a date below, the
entries above it are what changed under you.

**2026-08-26**
- Added eight types: `atrocity`, `region`, `geography`, `species`, `disease`,
  `product`, `language`, `period`. The vocabulary had stopped at Susia's
  political core; `Biology/`, `Languages/`, `Technology/` and `Planet/` had no
  legal type.
- `sex` widened from two values to three: `Non-binary` added.
- Retired `spouse` and `children_count` in favour of `relations`.
- Era slugs `united_syndicates` and `paulowic_regime` normalised to hyphens,
  matching every other slug.
- Base header formalised and made mandatory for every type.
- Rules added for quoting wikilinks and for unquoted numeric values. Both had
  been unwritten conventions, and both had been broken in dozens of files.
- Confian era dates flagged as internally inconsistent, pending review.
- This file renamed from `YALM and Tags.md` and restructured: rules first,
  vocabularies second, changelog added.
