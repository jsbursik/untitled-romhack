# Pokemon Errant — Concept Document

## Overview
**Game:** Pokemon Errant
**Region:** Solenne
**Tone:** Dark — war, corruption, a legendary pokemon as the ultimate threat. Comparable in vibe to Pokemon Unbound.

---

## Core Design Philosophy
Inspired by *The Legend of Zelda: The Minish Cap* — a hub-and-spoke world where the player radiates outward from a central point, gains tools/capabilities along the way, and uses those to unlock further areas. The experience is exploratory rather than linear.

**What this is NOT:**
- No 8-gym badge system
- No Team Rocket-style villain-of-the-week story
- No scripted linear progression through towns

---

## World Structure

### The Hub — The Stronghold
A castle-like stronghold sits at the center of Solenne, divided by a natural geographic feature (river, chasm, or mountain spine) with three zones on each side. The stronghold is the only crossing point, making it naturally the hub of all activity.

**Medieval aesthetic throughout.** Key services are re-skinned accordingly:
- **Pokemon Center → Apothecary / Infirmary** — healers using remedies and herbs
- **PC Storage → The Menagerie / Stables** — a keeper/warden manages your roster
- **Pokemarts → Quartermaster / Armory** — supplies, salves, tonics, equipment
- **Pokedex → Bestiary** — given by a scholar, fills in as you encounter pokemon

### The Six Zones (3 per side)
Each zone is a distinct biome. Rough split:

**West Side**
- Dark Forest
- Marshland
- Highland / Crags

**East Side**
- Coastal / Cliffs
- Ash Wastes (volcanic, late-game feel)
- Tundra

Zones are not meant to be completed in strict order. The villain's encroaching darkness manifests differently per biome (forest corruption, unnatural cold in the tundra, etc.), escalating as the story progresses.

---

## Progression & Player Agency

### HM Gates
HM moves serve as the "tools" that unlock access to deeper parts of each zone — matching the Minish Cap model where new tools open new paths.

### Tool-Within-Zone Design
Each zone contains the tool/HM needed to complete it. A player can enter any zone at any time:
- **Without the tool:** Longer, harder path through the zone
- **With the tool from a prior zone:** Faster, more direct route

This preserves player agency — no zone is hard-locked behind another — while rewarding players who explore broadly.

### Level Scaling
- Trainers and wild pokemon in each zone sit in a soft level range
- Environmental cues and hub NPCs signal relative difficulty without hard locks
- The hub area is where the player recuperates and levels between excursions

### Quest Tracker / Map
A UI element tracking discovered zones, items gathered, and objectives outstanding. Critical for a non-linear structure.

---

## Story

### The Villain
An ultimate villain threatening Solenne with darkness, using a legendary pokemon as their weapon. Not yet fully defined.

**End-game structure:** The player gathers 6 items/relics (one per zone, guarded by whoever/whatever lives there) that are needed to confront and defeat the final villain.

### Battle Structure (Gym Replacement)
No gym leaders or badges. Instead, each zone's key item is held or guarded by a person, creature, or corrupted guardian relevant to that zone's lore. Earning or taking it involves a battle, but it's organic to the world rather than a formal gym challenge.

---

## Open Questions
- Villain identity and motivation
- What the 6 gathered items/relics are
- Whether any end-game content unlocks additional regions post-credits
- Exact geographic layout and which biomes neighbor each other
- Name and personality of the scholar who gives the Bestiary
