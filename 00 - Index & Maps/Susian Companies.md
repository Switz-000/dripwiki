```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Sector", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.sector,
      p.company_type,
      p.headquarters,
    ])
)
````
```dataviewjs
const company = dv.pages()
  .where(p => p.type === "company" && p.market_cap)
  .sort(p => p.market_cap, "desc"); // largest first

const labels = company.map(c => c.file.name);
const data = company.map(c => c.market_cap);

// Generate a color per city using HSL
const colors = company.map((_, i) => `hsl(${i * 360 / company.length}, 70%, 50%)`);

// Output chart block
dv.paragraph(`
\`\`\`chart
type: pie
labels: [${labels.map(l => `"${l}"`).join(", ")}]
series:
  - title: Market Cap of Susian Companies
    data: [${data.join(", ")}]
    colors: [${colors.map(c => `"${c}"`).join(", ")}]
\`\`\`
`);

```
