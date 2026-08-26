---
type: index
summary:
aliases:
  -
era:
  -
tags:
  -
meta:
  stub: true
  verified: false
  image: null
---

```dataviewjs
dv.table(
  ["City", "State", "Population (thousands)"],
  dv.pages()
    .where(p => p.type === "city" && p.population_2080)
    .sort(p => p.population_2080, "desc")
    .map(p => [
      p.file.link,
      p.state,
      (p.population_2080 / 1_000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "k"
    ])
)
````
```dataviewjs
const cities = dv.pages()
  .where(p => p.type === "city" && p.population_2080)
  .sort(p => p.population_2080, "desc"); // largest first

const labels = cities.map(c => c.file.name);
const data = cities.map(c => c.population_2080);

// Generate a color per city using HSL
const colors = cities.map((_, i) => `hsl(${i * 360 / cities.length}, 70%, 50%)`);

// Output chart block
dv.paragraph(`
\`\`\`chart
type: pie
labels: [${labels.map(l => `"${l}"`).join(", ")}]
series:
  - title: Population
    data: [${data.join(", ")}]
    colors: [${colors.map(c => `"${c}"`).join(", ")}]
\`\`\`
`);

```
	
