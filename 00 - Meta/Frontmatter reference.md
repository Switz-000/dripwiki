# Frontmatter reference

The base header every article carries, whatever its type, and the quality
scale that applies to all of them. Type-specific templates in
`00 - Meta/Templates/` add fields on top of this header. None of them
replace it.

Read this file alongside the template for the type being written. Where a
type has a companion reference in `00 - Meta/Template reference/`, that file
governs its type-specific fields and this one governs the base.

---

## The base header

```
---
type:            # required, single value from the closed vocabulary
summary:         # required, one to two sentences of plain prose
aliases:
  -
era:             # required, from the closed vocabulary
  -
tags:            # required, from the closed vocabulary
  -
meta:
  stub: true
  verified: false
  image: null
---
```

**`type`** — what kind of article this is. Single value, from the list in
`YAML and Tags.md`. A type not in that list is not a valid type; extend the
vocabulary rather than inventing a value in a file.

**`summary`** — one to two sentences identifying the subject and why it
matters. Plain prose, neutral register, no wikilinks. This is what appears
in query results and hover previews, so it carries the article on its own.

**`aliases`** — other names the subject is known by, used so that links and
search resolve. Optional. Leave the empty list entry rather than deleting
the key.

**`era`** — historical periods the subject primarily belongs to, from the
vocabulary in `YAML and Tags.md`. Multiple values. Use the most specific
applicable era. Do not add a war or revolt era unless the subject was
directly involved.

**`tags`** — subject areas, from the vocabulary in `YAML and Tags.md`.
Multiple values. Apply all that describe the subject's primary domains.

**`meta.stub`** — whether the article is incomplete. True until the article
meets Level 3 below. This field drives the "what still needs writing"
queries, so it is only useful if it is kept honest.

**`meta.verified`** — whether the article's facts have been checked against
the rest of the vault. Defaults to false.

**`meta.image`** — path to the article's lead image, or null.

---

## Quality scale

Applies to every type. The Required and Recommended tiers for a given type
are defined in that type's companion reference; where none exists, the base
header's required fields are the Required tier.

1. **Stub** — missing one or more Required fields.
2. **Incomplete** — all Required fields present, some Recommended missing.
3. **Complete** — all Required and Recommended fields present.

Optional fields never affect quality level.

A field that does not apply to the subject is left blank and does not count
against the article. `dissolved` on an extant institution, `death` on a
living person, and `state` on a birth predating the state layer are all
blank by correctness, not by omission. Where a blank is a genuine gap in
what the vault knows, record it in the flags block.

---

## Value formatting

Wikilinks are always quoted: `religion: "[[Sacoitism]]"`. Unquoted, YAML
reads `[[` as the start of a nested list, and the value becomes a list of
lists that no link query will ever resolve.

Years are bare integers, never quoted: `founded: 1966`. An approximate year
goes in the field as the best single value, with the approximation recorded
in the flags block rather than in the field.

Booleans are bare `true` or `false`, not quoted and not capitalised.

Era and tag values are lowercase and hyphenated.

A list key keeps its empty entry when it has no values. Deleting the key
loses the shape of the header; leaving `  -` under it does not.

---

## Retired fields

Remove these on sight when editing any file.

- `spouse` — record as a `relations` entry with `relation: Spouse`.
- `children_count` — record as a single `relations` entry with `person`
  blank, `relation: Child`, and the number in `notes`.
