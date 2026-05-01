# Vault writing guidelines

A reference document for writing articles in the Susia vault. All editorial 
decisions default to these rules. Read this document at the start of every 
session before writing anything.

---

## Prose style

Write in a neutral, encyclopedic register. Wikipedia-style: factual, restrained, 
and plain. Let facts carry the weight.

- Do not editorialize or use dramatic framing.
- Do not overuse adjectives.
- Do not use em dashes. Use commas, colons, or restructure the sentence.
- Do not use phrases like "one of the most," "perhaps the greatest," or 
  "widely regarded as." State the fact or omit it.
- Avoid rhetorical questions.
- The intro paragraph identifies what the subject is, its key facts, and its 
  significance. One to three sentences. No dramatic opening.

---

## Article titles

- Sentence case. The first letter is capitalized; other words are not unless 
  they would be capitalized in running text.
- Singular form. *Horse*, not *Horses*. Exceptions: nouns that are always 
  plural in English (scissors, trousers) and names of classes of objects.
- No definite or indefinite articles at the start of a title unless part of a 
  proper name: *The Old Man and the Sea* is acceptable; *The continental war* 
  is not.
- No abbreviations or acronyms in titles unless the subject is known primarily 
  by its abbreviation.

---

## Structure

Use `##` for top-level sections and `###` for subsections. Do not skip levels.

**Standard section order by article type:**

- **Country:** intro → `## Geography` → `## History` → `## Government` → 
  `## Economy` → `## Military` → `## Foreign Relations` → `## States` → 
  `## Culture` → `## See Also`
- **State:** intro → `## Geography` → `## History` → `## Economy` → 
  `## Major Cities` → `## Free Economic Zones` → `## Culture` → 
  `## Politics` → `## See Also`
- **City:** intro → `## Geography` → `## History` → `## Economy` → 
  `## Culture` → `## Politics` → `## See Also`
- **Company:** intro → `## History` → `## Operations` → 
  `## Free Economic Zones` → `## Corporate Culture` → 
  `## Notable Controversies` → `## See Also`
- **Person:** intro → `## Early Life` → `## [Primary activity, varies by role]`
  → `## Personal Life` → `## Legacy` → `## See Also`
- **Institution:** intro → `## History` → `## Structure` → 
  `## Powers and Limitations` → `## Culture` → `## Controversies` → 
  `## See Also`
- **Law:** intro → `## Background` → `## Provisions` → `## Effects` → 
  `## Controversy` → `## See Also`
- **Event:** intro → `## Background` → `## [Event body, varies]` → 
  `## Aftermath` → `## See Also`
- **Concept:** intro → `## Origins` → `## [Domain-specific sections]` → 
  `## Contemporary Relevance` → `## See Also`

Personal Life in person articles is its own section. Do not fold personal 
details into the main narrative unless they are directly politically relevant.

---

## Links

- Link every reference to a person, place, company, event, law, or institution 
  that has or could reasonably have its own article.
- Use aliased links when display text differs from the page name: 
  `[[Kaichet Satratonie|Satratonie]]`.
- Do not link the same term more than once per section. Once per major section 
  is acceptable in long articles.
- Always create a link on first reference even if the target page does not 
  exist. This flags it as a future article candidate.

**Main article callouts:** When a section covers a topic that has its own 
dedicated article, add a callout directly under the section header:

> *Main article: [[Page Name]]*

Use this when the section summarizes rather than treats the topic fully. Add 
the callout even if the target page does not yet exist.

---

## Numbers, dates, and currency

- Spell out numbers one through nine. Use numerals for 10 and above.
- Spell out numbers that begin a sentence regardless of size.
- Years are always numerals: *the 1977 ceasefire*, *born in 2031*.
- Approximate dates in prose use *circa* or *around*: *around 1820*, 
  *circa 1740*. Do not use *c.* abbreviation in body text.
- Approximate dates in frontmatter use the `~` prefix: `~1820`.
- The Susian currency is the drip. Symbol: D$. Example: *D$6.2 trillion*.
- All market caps and undated economic figures are as of 2080 unless a 
  specific year is stated.

---

## Frontmatter

Fill every applicable field. An incomplete frontmatter is a stub regardless of 
body length. For field-by-field guidance, read the companion reference file in 
`00 - Meta/Template reference/` alongside the raw template.

Legacy fields appear in older files. Remove them on sight when editing any 
file. The current schema is defined in the template reference files.

---

## Stubs

An empty or near-empty file is a stub. Always link to stubs. Do not omit a 
link because the target page has no content.

Index files using Dataview query blocks are unreadable as reference material. 
If adding an index or summary file, include a plain-text summary above any 
query blocks.

---

## Flags block

Every completed article ends with a flags block inside an Obsidian comment. 
The block records editorial decisions, gaps, and unresolved questions so they 
can be reviewed and corrected later.

Format:
%% FLAGS:

- [flag note]
- [flag note] %%

Record the following when applicable:

- Approximated dates and how they were calculated.
- Birthplaces assumed rather than sourced.
- Conflicts between vault articles, and which was treated as canonical.
- Inferences made to bridge gaps, labeled explicitly as inference.
- Main article links pointing to pages that do not yet exist.
- Fields left blank due to missing information.
- Terminology inconsistencies spotted across files.
- Session canon established during this session that has not yet been written 
  into a dedicated article.

If there is nothing to flag, write `FLAGS: None.`

---

## Editorial discipline

The editor does not invent facts. If a fact is not in the vault, it does not 
go in the article. Write around gaps and flag them.

If a request seems factually inconsistent with established canon, name the 
inconsistency before proceeding. Common examples: assigning Susia as a 
birthplace for someone born before 1954, linking a person to an institution 
that did not exist during their active years, citing a date that contradicts 
the vault record.