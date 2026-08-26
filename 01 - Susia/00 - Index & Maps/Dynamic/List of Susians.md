---
type: index
summary:
aliases:
  -
era:
  -
tags:
  - society/demographics
meta:
  stub: true
  verified: false
  image: null
---

Every vault article of `type: person` whose nationality includes Susia, newest
birth first. Sourced from frontmatter; a blank cell means the field is empty on
that person's article, not that the fact is unknown to canon.

```dataviewjs
const clean = v =>
  typeof v === "string" ? v.replace(/\[\[|\]\]/g, "").split("|")[0].trim() : ""

const series = (arr, key) =>
  Array.isArray(arr)
    ? arr.map(o => clean(o?.[key]) || (typeof o?.[key] === "string" ? o[key] : ""))
         .filter(Boolean).join(", ")
    : ""

dv.table(
  ["Name", "Born", "Died", "Occupation", "Known for", "Birthplace"],
  dv.pages()
    .where(p => {
      const nat = Array.isArray(p.nationality)
        ? p.nationality
        : p.nationality ? [p.nationality] : []
      return p.type === "person" &&
             nat.some(n => typeof n === "string" && n.includes("Susia"))
    })
    .sort(p => p.birth?.year ?? -9999, "desc")
    .map(p => {
      const city  = clean(p.birth?.city)
      const state = clean(p.birth?.state)
      const place = city && state ? `${city}, ${state}` : city || state || ""
      return [
        p.file.link,
        p.birth?.year ?? "",
        p.death?.year ?? "",
        series(p.occupation, "title"),
        series(p.known_for, "item"),
        place
      ]
    })
)
```
