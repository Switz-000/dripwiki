# Technology
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Technology") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Industrials
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Industrials") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Consumer Discretionary (wants)
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Consumer Discretionary") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Consumer Staples (needs)
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Consumer Staples") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Financials
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Financials") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Healthcare
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Healthcare") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Materials
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Materials") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Energy
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Energy") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
# Telecomm
```dataviewjs
dv.table(
  ["Company", "Market cap (billions)", "Founded", "Company Type", "Headquarters Location"],
  dv.pages()
    .where(p => p.type === "company" && p.sector && p.sector.includes("Telecomm") && p.market_cap)
    .sort(p => p.market_cap, "desc")
    .map(p => [
      p.file.link,
      (p.market_cap / 1_000000000).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }) + "B",
      p.founded,
      p.company_type,
      p.headquarters,
    ])
)
````
 