---
# ── IDENTITY ─────────────────────────────────────────────────────────────────
type: product
summary:                  # one to two sentences: what it is, who made it, why it matters
aliases:
  -

# ── ORIGIN ───────────────────────────────────────────────────────────────────
manufacturer:              # wikilink to the company, institution or person that made it
category:                  # short plain-text classifier, not a controlled vocabulary.
                            # e.g. "Messaging platform", "Vesicant chemical weapon",
                            # "Private label retail brand", "Neural implant"
introduced:                 # year, bare integer
discontinued:                # year, bare integer. Blank if still in use.

# ── LINEAGE ──────────────────────────────────────────────────────────────────
predecessor:                 # wikilink, if this replaced an earlier product
successor:                   # wikilink, if this was replaced by a later one

# ── META ─────────────────────────────────────────────────────────────────────
era:
  -
tags:
  -
meta:
  stub: true
  verified: false
  image: null
---

%% Everything above IDENTITY/ORIGIN/LINEAGE/META is the whole fixed shape. `product`
covers wildly different things, an app, a drug, a weapon, a retail brand, so this
template stays deliberately thin: only the fields nearly every entry needs. Add
whatever the specific article needs beyond that, and nothing here is a controlled
vocabulary requiring the addition to match anything.

Precedent already in the vault: [[Eplevakt]] (a chemical weapon) adds chemical_name,
agent_class, country, and in_service_start/in_service_end on top of this shape. A
drug might add dosage and indication; a piece of hardware might add a spec sheet.
Don't force those into category or summary, give them their own fields. %%
