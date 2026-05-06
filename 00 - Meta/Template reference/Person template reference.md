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

**`known_for`** — structured list of wikilinks or plain text items representing the person's primary historical significance. Keep from three to five items. Examples: `"[[Liberal Revolts]]"`, `"[[Architecture of Freedom]]"`. (Recommended)

---

### Birth and Death

you know the deal. use wki

`birth:`
  `year:`
  `city:`
  `state:`
  `country:`

death:
  year:
  city:
  state:
  country:
  cause:

**`death_cause`** — plain text. Use consistent phrasing across files. Examples: `Natural causes`, `Hanging`, `Lung cancer`, `Disappeared`, `Unknown`.

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

### Written works

**`written_works`** — list of works authored by this person. Each entry has:

- `title` — wikilink if the work has an article, plain text if not.
- `publication_date` — four-digit year as integer.
- `genre` — plain text. Examples: `Philosophy`, `Political theory`, `Memoir`, `Fiction`.
- `notes` — optional. Use for reception, circumstances of publication, or relationship to other works.

Leave the entire block blank for characters with no written output.

---

### Awards and honors

**`awards`** — list of formal honors received. Each entry has:

- `title` — wikilink to the award article if one exists, plain text if not.
- `awarded` — four-digit year as integer.
- `posthumous` — `yes` or `no`.
- `granted_by` — wikilink to the person who granted the award.
- `country` — wikilink to the granting country.
- `notes` — optional context.

---

### Career and politics

**`occupation`** — list of plain text role labels describing what the person is, not where they work. Use broad, consistent categories. Examples: `Philosopher`, `Lawyer`, `Executive`, `Emperor`, `Naval officer`, `Academic`.

**`party`** — list. Wikilink to political party or parties. Use the party at the time of their most significant role if they only held one meaningful affiliation. List multiple if they changed parties in ways that matter to their biography.

**`political_alignment`** — list of plain text ideological descriptors, broader than party affiliation. Examples: `Liberal`, `Pragmatist`, `Orthodox Syndicalism`, `New Syndicalism`.

**`organization`** — list of wikilinks to non-employer organizations the person belongs to, founded, or led. Covers political movements, civic associations, military units, think tanks. Does not include formal offices, which go in `offices`.

---

### Personal life

**`residence`** — wikilink to the city article for the person's primary or last known place of residence. Distinct from birthplace.

**`family`** — wikilink to the family or dynasty article. List if the person belongs to multiple lines by birth and marriage. Examples: `"[[Yatovar family]]"`, `"[[Soites family]]"`.

**`spouse`** — wikilink or plain text. Use `None` if confirmed unmarried. Leave blank if unknown.

**`children`** — list of wikilinks with aliases. Always use wikilinks even for characters without articles yet. Use aliased links when the display name differs from the page title. Example: `"[[Empress Yaneoli|Yaneoli]]"`, `"[[Natesse]]"`.

---

### Offices

**`offices`** — list of formal positions held, in reverse chronological order. Each entry has:

- `title` — plain text job title. Be specific. Example: `CEO`, `President of Susia`, `Governor of Postia`, `Secretary of Justice`.
- `start` / `end` — four-digit year as integer. Use `~` prefix for approximated dates: `~1979`. Leave `end` blank for current positions.
- `appointer` — wikilink to the person or body that appointed them, or to the relevant election article.
- `party` — plain text party name at time of appointment.
- `notes` — optional clarifying context. Use for unusual circumstances, acting roles, or contested appointments.

---

### Criminal record

**`total_sentence`** — plain text summary of the full criminal record for characters with significant legal histories. Written as a single descriptive string. Example: `"29,441 counts of conspiracy to commit murder, treason, and perversion of office — sentenced to death in absentia"`. Leave blank if not applicable.

**`criminal_charges`** — list of individual charges. Each entry has:

- `charge` — plain text description. Example: `Treason`, `Conspiracy to commit murder`.
- `counts` — integer. Leave blank if not applicable or unknown.
- `verdict` — controlled vocabulary: `Convicted`, `Acquitted`, `Tried in absentia`, `Charges dropped`, `Pending`.
- `sentence` — plain text. Examples: `Death`, `15 years`, `Life imprisonment`, `None`.
- `served` — plain text. Examples: `None`, `7 years`, `Full term`.
- `in_absentia` — boolean. Defaults to `false`.
- `notes` — optional context.

Leave both fields blank if the person has no criminal record.

---

### Classification

**`era`** — list of era values from the controlled vocabulary in the YAML and Tags file. Use the most specific applicable era. Do not add a war or revolt era unless the person was directly involved in it. Do not add an era the person only lived through as a minor.

**`tags`** — list of subject tags from the controlled vocabulary in the YAML and Tags file. Apply all tags that describe the person's primary domains of activity.

---

## Legacy fields to remove on sight

These fields exist in older files but are not part of the current schema. Remove them when editing any file that contains them.

- `employer` at the top level — redundant with `offices`.
- `alma_mater` — replaced by `education`.
- `allegiance` — replaced by `organization` and `offices`.
- `birth_place` as a flat list — replaced by split `birth_city`, `birth_state`, `birth_country`.
- `person_name` — replaced by `full_name`.
- `historical_period` — replaced by `era`.