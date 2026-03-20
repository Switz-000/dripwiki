# Vault Writing Guidelines

A reference document for writing character files and articles in the Susia vault. Follow these rules consistently across all files.

## General Style

- Write in a **Wikipedia-style prose**: neutral, factual, and restrained. Avoid editorializing.
- Do not overuse adjectives. Let facts speak for themselves.
- Do not use em dashes (—). Use commas, colons, or restructure the sentence instead.
- Avoid flowery or dramatic language. Prefer plain, direct sentences.
- The vault files take precedence for specific details like dates and names. The docs (the large legacy .txt files) are treated as older, potentially outdated reference material. When the two conflict, flag the discrepancy rather than silently picking one.

## Article Titles

For simplicity sake, all examples listed will be real life examples.

Titles are written in sentence case. The initial letter of a title is always capitalized by default; otherwise, words are not capitalized unless they would be so in running text

Article titles are generally singular in form, e.g. Horse, not Horses. Exceptions include nouns that are always in a plural form in English (e.g. scissors or trousers) and the names of classes of objects.

Abbreviations and acronyms should be avoided unless the subject is known primarily by its abbreviation (e.g. NATO, Laser). Acronyms may be used for parenthetical disambiguation (e.g. Conservative Party (UK), Georgia (U.S. state)).

Do not place definite or indefinite articles (the, a, and an) at the beginning of titles unless they are part of a proper name (e.g. The Old Man and the Sea)



## Stubs and Missing Content

- Empty or near-empty files are stubs.
- When writing a file that references a stub, still link to it. Do not omit the link just because the target page has no content yet.
- Index files that use Dataview queries (javascript blocks) are unreadable as reference material. If adding a summary or index file, include a plain-text summary at the top before any query blocks.
- all market caps and undated economic data are as of 2080 unless a specific year is stated otherwise.

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
- ALWAYS, fill the YALM with the most information available and use the most recent templates. Read the YALM and Tags guide as well


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

## Standard section order by article type

**Country:** intro → `## Geography` → `## History` → `## Government` → `## Economy` → `## Military` → `## Foreign Relations` → `## States` → `## Culture` → `## See Also`

**State:** intro → `## Geography` → `## History` → `## Economy` → `## Major Cities` → `## Free Economic Zones` → `## Culture` → `## Politics` → `## See Also`

**City:** intro → `## Geography` → `## History` → `## Economy` → `## Culture` → `## Politics` → `## See Also`

**Company:** intro → `## History` → `## Operations` → `## Free Economic Zones` → `## Corporate Culture` → `## Notable Controversies` → `## See Also`

**Person:** intro → `## Early Life` → `## [Primary activity — varies by role]` → `## Legacy` → `## See Also`

**Institution:** intro → `## History` → `## Structure` → `## Powers and Limitations` → `## Culture` → `## Controversies` → `## See Also`

**Law:** intro → `## Background` → `## Provisions` → `## Effects` → `## Controversy` → `## See Also`

**Event:** intro → `## Background` → `## [Event body — varies]` → `## Aftermath` → `## See Also`

**Concept:** intro → `## Origins` → `## [Domain-specific sections]` → `## Contemporary Relevance` → `## See Also