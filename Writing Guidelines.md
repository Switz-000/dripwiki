# Vault Writing Guidelines

A reference document for writing character files and articles in the Susia vault. Follow these rules consistently across all files.

---

## General Style

- Write in a **Wikipedia-style prose**: neutral, factual, and restrained. Avoid editorializing.
- Do not overuse adjectives. Let facts speak for themselves.
- Do not use em dashes (—). Use commas, colons, or restructure the sentence instead.
- Avoid flowery or dramatic language. Prefer plain, direct sentences.
- The vault files take precedence for specific details like dates and names. The docs (the large legacy .txt files) are treated as older, potentially outdated reference material. When the two conflict, flag the discrepancy rather than silently picking one.

---

## Terminology

When working with the author, the following terms have specific meanings:

- **Docs**: the large legacy .txt files (e.g. Susian_History.txt, Susian_Economy.txt). These are being deprecated and may contain outdated information.
- **Vault**: the individual wiki-style .md files that make up the current canonical source of truth.

When the docs and vault contradict each other, always flag it explicitly: "the docs say X but the vault says Y, which is current?" Do not silently resolve conflicts.

---

## Stubs and Missing Content

- Empty or near-empty files are stubs.
- When writing a file that references a stub, still link to it. Do not omit the link just because the target page has no content yet.
- Index files that use Dataview queries (javascript blocks) are unreadable as reference material. If adding a summary or index file, include a plain-text summary at the top before any query blocks.
- all market caps and undated economic data are as of 2080 unless a specific year is stated otherwise.

---

## Frontmatter

Follow the relevant template exactly for each file type. Fill in every field that has available information. Leave fields blank rather than guessing, except where a reasonable approximation can be calculated (e.g. birth year from death age).

- `birth_place` should list the city, state, country, and empire/nation at the time of birth. Do **not** add modern successor states anachronistically. Someone born in the Dripstanian Empire does not get Susia listed, even if Susia now occupies that territory.
- `citizenship` reflects political identity, not birthplace. A figure like Versij or Paroska gets both Dripstanian and Susian because they are foundational to Susia's national identity. Jartes II does not.
- `known_for` entries should be linked where a corresponding page exists or will exist.
- For state files, include a `political_lean` field in the frontmatter with party percentages. This should be consistent with the body text.

---

## Links

- Link every reference to a person, place, company, event, law, or institution that has or could reasonably have its own page in the vault.
- Use aliased links when the display text differs from the page name: `[[Kaichet Satratonie|Satratonie]]`.
- Do not link the same term more than once per section. Linking once per major section is acceptable for long articles.
- When referencing an explorer, institution, or named document for the first time, always create a link even if the page does not yet exist. This flags it as a future article candidate.

---

## Main Article Links

- When a section covers a topic substantial enough to have its own dedicated page, add a main article callout directly under the section header:
  > *Main article: [[Page Name]]*
- Use this for events, institutions, programs, and eras that are merely summarized in the current article but treated in full elsewhere.
- If the target page does not yet exist, still add the link. It flags a gap in the vault.

---

## Structure

- Use `##` for top-level sections and `###` for subsections.
- Standard sections for character files: intro paragraph, Early Life, Reign/Career (with subsections as needed), Personal Life (if relevant), Legacy.
- Standard sections for state files: intro paragraph, Identity, Geography, Economy, FEZs (if applicable), Major Cities, Politics.
- The intro paragraph should identify what the subject is, its key facts, and its significance in one to three sentences. No dramatic framing.
- Personal Life should be its own section in character files, not folded into the main narrative, unless the personal details are directly politically relevant.

---

## Source of Truth Hierarchy

1. Vault files (character pages, city pages, company pages, state pages)
2. Docs (legacy .txt files, treat as potentially outdated)
3. Reasonable inference from established facts (e.g. calculating birth year from death age and stated age)

When the docs and vault conflict, flag the discrepancy rather than silently picking one. Do not invent details not supported by either source.

---

## Push Back

- Always push back if a request seems factually inconsistent with established lore.
- Examples: adding Susia to a birth place for someone born before 1954, citing a work date that contradicts the vault bibliography, linking a person to an institution that did not exist during their lifetime.
- Flag judgment calls made during file creation so the author can correct them.

---

## Flagging Gaps

At the end of file creation, note:
- Dates that conflict between the docs and the vault.
- Approximated dates and how they were calculated.
- Birth places assumed rather than sourced.
- Main article links pointing to pages that do not yet exist.
- Any terminology inconsistencies spotted (e.g. the same group referred to by two different names across files).
- Any information that could not be sourced and was left blank.
