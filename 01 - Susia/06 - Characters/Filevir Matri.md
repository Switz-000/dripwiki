---
type: person
full_name: Filevir Matri
aliases:
birth_year: 1924
birth_city:
  - - Duolij
birth_state:
  - - Postia
birth_country:
  - - Susia
citizenship:
  - - Susia|Susian
death_year: 2002
death_city:
  - - Duolij
death_state:
  - - Postia
death_country:
  - - Susia
death_cause: Natural Causes
ethnicity: Gaiyanese (West)
religion: Reformed Armotism
education:
  - degree: Bachelor in Law
    institution: [[Universty of Duolij]]
    year: 1948
occupation:
  - Politician
  - Lawyer
  - Businessman
party:
  - "[[Susian Democratic Union]]"
political_alignment:
organization:
  - "[[Susian Democratic Union]]"
employer:
  - "[[Soites Group]]"
known_for:
  - 
historical_period: Republican Era (1954–2038)
spouse: "[[Yavna Matri]]"
children: Two (Unamed)
criminal_charges:
enhanced: false
offices:
  - title: Governor of Postia
    start: 1954
    end: 1962
    party: [[Susian Democratic Union]]
  - title: Senator for Postia
    start: 1962
    end: 1966
    party: [[Susian Democratic Union]]
  - title: Secretary of Justice
    start: 1966
    end: 1970
    appointer: [[Sergio Fimoises]]
    party: [[Susian Democratic Union]]
    notes:
  - title: Senator for Postia
    start: 1970
    end: 1974
    appointer:
    party: [[Susian Democratic Union]]
    notes:
  - title: Vice President of Susia
    start: 1974
    end: 1982
    appointer:
    party: [[Susian Democratic Union]]
    notes:
  - title: President of Susia
    start: 1982
    end: 1984
    appointer:
    party: [[Susian Democratic Union]]
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
**Filevir Matri** (1924–2002) was a Susian lawyer, statesman, and politician who served as the fifth President of Susia from 1982 to 1986. He came to the presidency after a long career in Postian and federal politics: governor of [[Postia]] during the republic's founding decade, senator, [[Secretary of Justice]] under [[Sergio Fimoises]], and Vice President under [[Cássio Bonfim]]. He is generally remembered as a competent but unremarkable president, sandwiched between a war hero and an idealist, whose achievements were either attributed to his predecessor or claimed by administrations that came after him.

## Early Life and Education

Matri was born in [[Duolij]] in 1924 to a middle-class family. His upbringing was comfortable without being privileged, and from an early age he understood that advancement required effort his background would not provide on its own. He studied law, graduating with distinction, and established himself in Duolij's legal and civic circles before entering politics at thirty.

He cultivated the mannerisms of a class slightly above his own. He spoke formal Susian with precision, dressed carefully, and moved through rooms with the composed deliberateness of a man who had decided what impression he intended to make. Those who knew him well noted the effort behind the performance without finding it dishonest, it was simply who he was: a man who understood that in Susian political life, appearing to belong somewhere was most of the work of belonging there.

His preferred arena was never the podium or the Senate floor. Matri did his politics at the [[Lobster table]], over [[Vitrikan wine]], in the kind of afternoon conversations that ended with a walk in the park and an understanding between gentlemen. He was a networker of exceptional skill, the sort of man who remembered birthdays, sent the right letter at the right moment, and knew which families needed to be brought together over dinner before a vote was called. His wife was central to this operation, managing relationships with other political families with the same quiet efficiency that Matri brought to legal briefs. He rarely discussed his family in public. He didn't need to. The family's presence in his political life was total and carefully managed.

## Governor of Postia (1954–1962)

Matri was elected Governor of [[Postia]] in 1954, part of the founding generation that took charge of Susian institutions at an age that would have seemed impossibly young under the old imperial system. He was thirty years old. Postia was the republic's most economically significant state, and the job was not a ceremonial one.

His governorship was defined almost immediately by the [[Minutemen]] crisis. In the chaotic early years of the republic, anarcho-syndicalist cells operating under this name conducted a campaign of bombings and political assassinations across Susia. Their most notorious act was the [[Neoveli Stock Exchange Bombing]] of 1955, which killed 43 people and sent shockwaves through the republic's financial and political establishment. Postia, as the industrial and commercial heartland of the country, was a primary target.

Matri's response was swift, unsentimental, and not entirely clean. He authorized aggressive union surveillance, mass arrests of suspected sympathizers, and crackdowns on labor organizations deemed too close to syndicalist ideology. Clashes between security forces and workers turned violent on multiple occasions. His methods drew sharp criticism from Postia's working class, who viewed him as using the bombings as a pretext to suppress legitimate labor organizing alongside genuine terrorism, a criticism that was not entirely without merit. He was unmoved by it. His position was simple and he stated it often: the syndicalists would exploit any tolerance shown to them.

He was effective. By the late 1950s Postia was the most stable of Susia's major states, its syndicalist networks dismantled or driven underground, its institutions functioning. The working class never forgave him. The [[Susian Democratic Union|FVS]] establishment never forgot what he had done for them.

## Senate and Federal Career (1962–1974)

When [[Sergio Fimoises]] won the presidency in 1962 on the [[Susian Democratic Union|FVS]] ticket, Matri stepped down from the governorship and ran successfully for the [[Susian Senate|Senate]], representing Postia. The transition reflected a calculated decision: his record in Postia had given him a strong national profile within the party, and a Senate seat positioned him closer to federal power at a moment when the [[Continental Divide]] was shaping every dimension of Susian politics.

In 1966, Fimoises appointed him [[Secretary of Justice]], a natural fit for a lawyer with his background in security and institutional order. The appointment gave Matri four years of direct federal executive experience, overseeing law enforcement coordination and the legal machinery of a republic under continuous pressure from the [[Continental Divide]]. His tenure was unremarkable in the sense that nothing went wrong, which during the Fimoises years was itself an accomplishment. He returned to the Senate in 1970 following Fimoises' second term.

His four years in the Senate under [[Ergagério Sienes]] were defined by growing frustration. Matri was a consistent and vocal critic of Sienes' [[Detente Policy|détente]] approach toward [[Confia]], arguing that negotiating with the Lorelaj government from a position of strategic weakness was not diplomacy but capitulation. When the [[Sutsa-Fuhu Civil War (1972-1973)|Sutsa-Fuhu civil war]] unfolded and Sienes hesitated to intervene, Matri's position within the FVS hardened into something closer to contempt. He had spent his career arguing that any concession to syndicalism invited further encroachment. Sienes had offered years of concessions and received encirclement in return.

By the time [[Cássio Bonfim]] was building his presidential campaign in 1974, Matri was one of the most recognizable FVS figures in federal politics: a former governor, a former cabinet secretary, a sitting senator, and a man whose anti-syndicalist record was unimpeachable. He was fifty years old. The man who had fought the syndicalists in Postia would now fight them on the continent.

## Vice Presidency (1974–1982)

Matri served as Bonfim's Vice President through the entirety of one of the most consequential periods in Susian history: the final phase of the [[Continental Divide]], the [[Continental War]] (1975–1977), and the post-war reconstruction. His formal role was secondary to Bonfim's in every meaningful sense. Bonfim made the decisions. Matri managed the relationships, handled the legislative groundwork, kept the coalition intact, and attended the funerals of men who had died in a war his running mate had started and won.

The two men were not close at first. They were politically compatible rather than personally warm, a partnership of mutual usefulness. What changed them was the war itself. The pressure of governing a republic through an existential conflict produced something between them that was not quite friendship but was more than professional respect. Bonfim was demanding, blunt, and constitutionally incapable of pretending a situation was better than it was. Matri, who had spent his career managing appearances, found this quality simultaneously exhausting and clarifying. They drank together often. Bonfim drank whiskey in quantities that alarmed even Matri, which was saying something.

It was during the vice presidency that Matri's own drinking consolidated from a habit into something more structural. One to two bottles of wine per day, primarily from [[Vitrika]] and southern [[Postia]], whose vineyards he had developed strong opinions about over decades. The stress of the war years provided the occasion; the appetite had always been there. He never regarded it as a problem. He regarded it as one of the few remaining pleasures a man in his position could enjoy with complete sincerity.

By the end of Bonfim's presidency, Matri was publicly positioned as the natural successor. The war was won, the [[Flower Revolutions]] had reshaped the continent, and the post-war economic boom was running. The FVS established him as its candidate. Susia, it was assumed, would want continuity.

## Presidency (1982–1986)

### The Weight of Succession

No Susian president has had the misfortune of following Cássio Bonfim without being diminished by the comparison, and Matri followed Bonfim directly. Every decision he made was measured against a man whose defining act had been winning a continental war from a position of near encirclement. Matri's defining acts were procedural, diplomatic, and institutional. He was not wrong to pursue them. He was simply governing in a register that Susians, flushed with post-war confidence and Bonfim's legend, had little patience for.

He was fifty-eight when he took office. He spoke in the careful, qualified sentences of a lawyer who had spent thirty years never saying more than he needed to. Journalists found him frustrating to quote. There was always a subordinate clause, always a condition, always a nuance that softened the headline. He was not performing evasion. He simply believed that imprecision was a kind of dishonesty, and that most political questions were more complicated than the answers politicians gave them.

### The Lasman Groundwork

Matri's most consequential act as president was one that would not be recognized as consequential for nearly a decade. Beginning in 1983 he opened back-channel diplomatic contact with [[Confia]]'s government under [[Boris Serec]], with the aim of establishing a framework for economic normalization. The [[Continental War]] had ended six years earlier. The [[Flower Revolutions]] had transformed Confia from an ideological adversary into a fragile democracy. Matri's legal instincts told him that the relationship needed formal architecture before it could bear real weight.

The negotiations were slow, technical, and almost entirely invisible to the Susian public. He made no speeches about historic reconciliation. He sent lawyers and trade officials to meet their Confian counterparts in conference rooms in [[Niqueparje]] and [[Imgospalje]]. He met Serec himself at the [[Presidential Palace (Soiteslaj)|presidential palace]] at least once, possibly more. What they discussed produced no signed agreement during his term. What they produced was the groundwork that, nine years later, became the [[Lasman Economic Initiative]].

Matri knew he would not sign the treaty himself. He planted the tree.

### The Ditanian Intervention

Matri authorized Susia's participation in a multilateral intervention in [[Ditania]], alongside [[Confia]], [[Pierej]], and [[Kapiogg]], in response to the anarchy that had followed the failed [[Tulip Revolution]] of 1981. The intervention was messy in conception and messier in execution. Its aims were contested among the four participating nations, its mandate was unclear, and the situation on the ground resisted clean resolution. It was not Matri's finest hour, though it demonstrated something his detractors rarely acknowledged: getting newly democratic Confia to act jointly with Susia less than a decade after the Continental War required genuine diplomatic work.

### The Presidential Palace

The domestic record of Matri's presidency was steady: no dramatic failures, no transformative achievements, the boom continuing as it had under Bonfim, the institutions functioning. He managed rather than led.

What the historical record has preserved with greatest fidelity is the wine.

Matri ordered in excess of D$10,000 worth of the finest Vitrikan and southern Postian vintages per month during his time at the [[Presidential Palace (Soiteslaj)|presidential palace]], charged to public accounts. He also instructed palace staff to cover wine bottle labels before serving and to present guests with a cheaper supply, keeping the better bottles for himself.

The arrangement came to light after his term ended, disclosed by a palace staff member. Among the guests who had drunk from the cheaper supply was [[Boris Serec]], the Confian prime minister whose government Matri was at the same time cultivating as a diplomatic partner. When the account became public, Serec was reported to have said he could not tell the difference anyway.

## Electoral Defeat and Return to Postia

Matri sought re-election in 1986 and lost to [[Felipe Santiago]], the co-founder of the [[Susian Liberal Party]] whom [[Suizo Soites]] himself had sidelined during the founding era for being too rigid and too idealistic. Santiago had spent the better part of three decades outside government. He was awkward in public, constitutionally incapable of small talk, and gave speeches that were technically impeccable and personally compelling in inverse proportion. He won anyway.

Matri's private response to the result was not directed at Santiago, whom he regarded without particular animus. It was directed at Susia. He had watched [[Ergagério Sienes|Sienes']] idealism produce the encirclement that nearly ended the republic. He had watched Bonfim's hard-eyed pragmatism win the war that saved it. And now Susia had elected a man whose primary qualification was a philosophy that Soites himself had found unworkable in practice. Matri pitied the choice. He was a lawyer. He knew better than to argue with a verdict.

He returned to [[Duolij]]. After a period of quiet he opened a corporate law firm, drawing on decades of contacts at the intersection of Postian business, federal regulation, and institutional knowledge that only comes from having been in the rooms where decisions were made. The firm was successful. He was by all accounts an excellent lawyer: precise, well-connected, and unsentimental about the gap between what the law said and what it did. His client list was never published. It did not need to be.

In his private life, post-presidency, he drank openly and well. There were no labels to cover.

## Legacy

Matri is generally remembered as a competent but unremarkable president. His achievements are either attributed to Bonfim's foundation or claimed by later administrations that completed what he started. The [[Lasman Economic Initiative]], signed in 1995, is rarely associated with him in public memory despite the early groundwork his government laid. The [[Ditanian Intervention]] is recalled as a foreign policy muddle. The Serec wine story is in most of the surveys.

The more considered assessment is that he governed adequately through a period that required management rather than vision, that his early Confian diplomacy was substantive if unglamorous, and that his anti-syndicalist record in Postia, whatever its methods, was effective at a moment when the republic's stability was not assured.

Filevir Matri died in Duolij in 2002 at seventy-eight years old.

## See Also
- [[Cássio Bonfim]]
- [[Felipe Santiago]]
- [[Ergagério Sienes]]
- [[Sergio Fimoises]]
- [[Postia]]
- [[Susian Senate]]
- [[Secretary of Justice]]
- [[Continental War]]
- [[Continental Divide]]
- [[Lasman Economic Initiative]]
- [[Ditanian Intervention]]
- [[Minutemen]]
- [[Neoveli Stock Exchange Bombing]]
- [[Susian Democratic Union]]
- [[Detente Policy]]
- [[Sutsa-Fuhu Civil War (1972-1973)]]
- [[Flower Revolutions]]
- [[Vitrikan wine]]





