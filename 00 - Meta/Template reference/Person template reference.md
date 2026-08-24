### Qualities

An article's YALM may have three level of qualities

1 - Stub: These are articles that don't have all required fields met
2 - Incomplete: These are articles that have all (Required) fields but not all of the (Recommended)
3 - Complete: These are articles that have all of the (Recommended) and (Required) fields met, satisfying the basic quality criteria. 

Optional fields do not count for any of these
### Identity

**`type`** — always `person`. (Required).

**`native_name`** — name of this character in its native language. (Recommended)

**`aliases`** — common short names, nicknames, titles, or alternate spellings used in prose. Examples: `Versij`, `KAN`, `Chediji J. Soites`.  (Optional)

**`summary`** — one to two sentence plain-prose description of who this person is and why they matter. Should name the person, their role and their primary significance. (Required)

`known_for:`
  - `item:`
    `notes:`

structured list of wiki links or plain text items representing the person's primary historical significance. Keep from three to five items. (Recommended)

**`era`** — list of era values from the controlled vocabulary in the YAML and Tags file. Use the most specific applicable era. Do not add a war or revolt era unless the person was directly involved in it. Do not add an era the person only lived through as a minor. (Recommended)

**`tags`** — list of subject tags from the controlled vocabulary in the YAML and Tags file. Apply all tags that describe the person's primary domains of activity. (Recommended)

`meta:`
  `stub: true`
  `verified: false`
  `image: null`

---

### Birth and Death

you know the deal. use wiki links, single values. both represent the city / country as they were not their modern day equivalent. 

(Required)

`birth:`
  `year:`
  `city:`
  `state:`
  `country:`

(Optional), all fields become required if at least one of them are filled in

`death:`
  `year:`
  `city:`
  `state:`
  `country:`
  `cause:`

**`death.cause`** — plain text. Use consistent phrasing across files. Examples: `Natural causes`, `Hanging`, `Lung cancer`, `Disappeared`, `Unknown`. 

---

### Family

**`spouse`** — wikilink to the primary consort or partner. Single value. (Optional)

**`children_count`** — integer. Leave blank if unknown; do not write `None`. (Optional)

**`relations`** — list of typed kinship edges to other person articles. This is
the field that makes family structure queryable; `spouse` and `children_count`
are display conveniences and do not replace it. Each entry has three subfields:

- `person` — wikilink to the related person's article. Always link, even where
  the target does not yet exist.
- `relation` — the related person's role **relative to the subject of this
  article**, from the controlled vocabulary below. Record only the closest
  degree that holds: if someone is both a cousin and a brother-in-law, record
  the blood tie.
- `notes` — optional. Use for the legal or contested character of the tie:
  disputed legitimacy, adoption instruments, degrees a source disagrees on.

Record parents, siblings, spouses, and children directly. Record grandparents,
aunts, uncles, cousins, and further degrees only where the person matters to
the subject's article. Do not reconstruct an entire dynasty on every member;
each article records its own edges and the graph assembles itself.

Controlled vocabulary:

```
relation: Father
relation: Mother
relation: Spouse
relation: Son
relation: Daughter
relation: Brother
relation: Sister
relation: Half-brother
relation: Half-sister
relation: Grandfather
relation: Grandmother
relation: Grandson
relation: Granddaughter
relation: Uncle
relation: Aunt
relation: Nephew
relation: Niece
relation: Cousin
relation: Adoptive father
relation: Adoptive mother
relation: Adoptive brother
relation: Adoptive sister
relation: Adoptive son
relation: Adoptive daughter
relation: Ward
relation: Guardian
```

Legitimacy and stillbirth are not relation values. Record the relation and put
the qualification in `notes`: `relation: Son` with `notes: Illegitimate.`, or
`relation: Brother` with `notes: Stillborn.`

(Recommended for members of a named family or dynasty. Optional otherwise.)

---

### Demographics

**`sex`** — `Male` or `Female`. Plain text.  (Required).

**`citizenship`** — legal status in a state. List. Use wikilinks for `type: country` articles. A person can hold multiple citizenships. (Required).

**`nationality`** — cultural or national belonging. Distinct from citizenship: a person born in the Dripstanian Empire may have Susian nationality through cultural identity even before Susia existed as a state. List. Use wikilinks for `type: country` articles. A person can hold multiple citizenships. (Required).

**`ethnicity`** — ancestral and ethnic origin. Plain text. Examples: `West Gaiyanese`, `East Gaiyanese`. (Required).

**`religion`** — wikilink of the religion of this character. `"[[Reformed Armotism]]"`, `"[[Armotist Church of the Confian Synod]]"`. (Recommended)

**`enhanced`** — boolean. Whether the person has undergone cognitive enhancement. Always included. Defaults to `false`. (Required).

---

### Education

(Recommended)

**`education`** — list of degree entries. Each entry has three subfields: 

- `degree` — field of study, not the credential type. Example: `Finance`, `Law`, `Economics`.
- `institution` — wikilink to the institution article.
- `year` — graduation year as a four-digit integer.

---

### Other optional objects

all of these objects are optional, do not remove them if they are not aplicable, only leave them blank. if one field of the object is filled, all of the other respective fields become (Required)

**`written_works`** — list of works authored by this person. Each entry has:

- `title` — wikilink if the work has an article, plain text if not.
- `publication_year` — four-digit year as integer.
- `genre` — plain text. Examples: `Philosophy`, `Political theory`, `Memoir`, `Fiction`.
- `notes` — optional. Use for reception, circumstances of publication, or relationship to other works.

`occupation:`
  - `title:`
    `start_year:`
    `end_year:`

`military_service:`
  - `allegiance:`
    `branch:` 
    `rank:`
    `start_year:`
    `end_year:`
    `conflicts:`
      `-`
    `notes:`

`political_alignment:`
  `-`

`party:`
`parties:`
  `-`

`organizations:`
  `-`

`offices:`
  - `title:
    `employer:`
    `start_year:`
    `end_year:`
    `appointer:`
    `parties:`
      `-`
    `notes:`

`criminal_charges:`
  - `charge:`
    `counts:`
    `charged_year:`
    `plea:`
    `verdict:`
    `verdict_year:`
    `sentence:`
    `served:`
    `in_absentia:`
    `notes:`