---
type: person
full_name:
aliases:
birth_year:
birth_city:
birth_state:
birth_country:
citizenship:
death_year:
death_city:
death_state:
death_country:
death_cause:
ethnicity:
religion:
education:
  - degree:
    institution:
    year:
occupation:
  -
party:
political_alignment:
organization:
  -
employer:
  -
known_for:
  -
historical_period:
spouse:
children:
criminal_charges:
enhanced: false
offices:
  - title:
    start:
    end:
    appointer:
    party:
    notes:
---

```dataviewjs
// ── helpers ──────────────────────────────────────────────────────────────────
const p = dv.current();
const row = (label, val) => {
  if (!val && val !== 0) return "";
  return `<tr><td class="ib-label">${label}</td><td class="ib-val">${val}</td></tr>`;
};
const join = (arr, sep = ", ") =>
  Array.isArray(arr) ? arr.filter(Boolean).join(sep) : arr ?? "";

// ── derived values ────────────────────────────────────────────────────────────
const name   = p.full_name || p.file.name;
const aliases = join(p.aliases);

const born = [p.birth_year, [p.birth_city, p.birth_state, p.birth_country].filter(Boolean).join(", ")]
  .filter(Boolean).join(" · ");

const died = p.death_year
  ? [p.death_year, [p.death_city, p.death_state, p.death_country].filter(Boolean).join(", "), p.death_cause]
      .filter(Boolean).join(" · ")
  : null;

// Education rows
const eduRows = (p.education || [])
  .filter(e => e && (e.degree || e.institution))
  .map(e => `${[e.degree, e.institution, e.year].filter(Boolean).join(", ")}`)
  .join("<br>");

// Offices table
const officeRows = (p.offices || [])
  .filter(o => o && o.title)
  .map(o => {
    const term = [o.start, o.end].filter(Boolean).join("–");
    const meta = [term, o.party, o.appointer ? `App. by ${o.appointer}` : null, o.notes]
      .filter(Boolean).join(" · ");
    return `<tr><td class="ib-label">${o.title}</td><td class="ib-val">${meta}</td></tr>`;
  }).join("");

// ── CSS ───────────────────────────────────────────────────────────────────────
const css = `
<style>
.ib-wrap {
  float: right;
  clear: right;
  margin: 0 0 1em 1.5em;
  border: 1px solid var(--background-modifier-border);
  border-radius: 8px;
  background: var(--background-secondary);
  min-width: 260px;
  max-width: 320px;
  font-size: 0.85em;
  overflow: hidden;
}
.ib-title {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
  text-align: center;
  font-weight: bold;
  font-size: 1.1em;
  padding: 8px 10px;
}
.ib-aliases {
  text-align: center;
  font-style: italic;
  padding: 4px 10px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--background-modifier-border);
}
.ib-section {
  background: var(--background-modifier-border);
  text-align: center;
  font-weight: bold;
  font-size: 0.9em;
  padding: 4px 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.ib-wrap table { width: 100%; border-collapse: collapse; }
.ib-label {
  padding: 4px 8px;
  color: var(--text-muted);
  vertical-align: top;
  white-space: nowrap;
  width: 38%;
  border-top: 1px solid var(--background-modifier-border);
}
.ib-val {
  padding: 4px 8px;
  vertical-align: top;
  border-top: 1px solid var(--background-modifier-border);
}
</style>`;

// ── HTML ──────────────────────────────────────────────────────────────────────
let html = `${css}
<div class="ib-wrap">
  <div class="ib-title">${name}</div>
  ${aliases ? `<div class="ib-aliases">${aliases}</div>` : ""}
  <table>
`;

// Personal info
const personalRows = [
  row("Born",        born || null),
  row("Died",        died),
  row("Citizenship", join(p.citizenship)),
  row("Ethnicity",   join(p.ethnicity)),
  row("Religion",    join(p.religion)),
  row("Spouse",      join(p.spouse)),
  row("Children",    join(p.children)),
].join("");

if (personalRows) {
  html += `<tr><td colspan="2" class="ib-section">Personal</td></tr>${personalRows}`;
}

// Political info
const politicalRows = [
  row("Party",       join(p.party)),
  row("Alignment",   p.political_alignment),
  row("Organization",join(p.organization)),
].join("");

if (politicalRows) {
  html += `<tr><td colspan="2" class="ib-section">Political</td></tr>${politicalRows}`;
}

// Offices
if (officeRows) {
  html += `<tr><td colspan="2" class="ib-section">Offices Held</td></tr>${officeRows}`;
}

// Career
const careerRows = [
  row("Occupation",  join(p.occupation)),
  row("Employer",    join(p.employer)),
  row("Known For",   join(p.known_for)),
  row("Period",      p.historical_period),
].join("");

if (careerRows) {
  html += `<tr><td colspan="2" class="ib-section">Career</td></tr>${careerRows}`;
}

// Education
if (eduRows) {
  html += `<tr><td colspan="2" class="ib-section">Education</td></tr>
           <tr><td colspan="2" class="ib-val">${eduRows}</td></tr>`;
}

// Legal
if (p.criminal_charges) {
  html += `<tr><td colspan="2" class="ib-section">Legal</td></tr>
           ${row("Charges", join(p.criminal_charges))}`;
}

// Enhanced flag
if (p.enhanced) {
  html += `<tr><td colspan="2" class="ib-section" style="background:var(--color-orange);color:#fff;">⚡ Cognitively Enhanced</td></tr>`;
}

html += `</table></div>`;

dv.el("div", html, { cls: "ib-container" });
```






