# Battle Type Icons & Effectiveness Indicators

## Type Icons (near HP bars)

**Config toggle:** `include/config/battle.h:395-399`
```c
#define B_SHOW_TYPES  SHOW_TYPES_ALWAYS
// Options: SHOW_TYPES_NEVER, SHOW_TYPES_ALWAYS, SHOW_TYPES_CAUGHT, SHOW_TYPES_SEEN
```

**Main implementation:** `src/type_icons.c`
- `LoadTypeIcons()` is called at `src/battle_controller_player.c:2152` when the move selection screen opens
- `sTypeIconPositions[][]` at line 38 controls X/Y pixel coordinates for each battler position (single vs double battle)
- `SpriteCB_TypeIcon()` at line 423 handles slide-in, bounce (tracks with the HP bar's `y2`), and slide-out animation
- `ShouldHideTypeIcon()` at line 499 — icons are visible only while actively in move selection controller functions

**Sprites/graphics:**

| File | Contents |
|---|---|
| `graphics/types/battle_icons1.png` | Sheet 1: Normal, Fighting, Flying, Poison, Ground, Rock, Bug, Ghost, Steel, Mystery |
| `graphics/types/battle_icons2.png` | Sheet 2: Fire, Water, Grass, Electric, Psychic, Ice, Dragon, Dark, Fairy |
| `graphics/types/battle_icons1.pal` / `.gbapal` | Palette for sheet 1 |
| `graphics/types/battle_icons2.pal` / `.gbapal` | Palette for sheet 2 |

Sprites are 8x16 pixels, 4bpp. Loaded via `gBattleIcons_Gfx1/2` and `gBattleIcons_Pal1/2` (`src/graphics.c:2128-2131`).

The two-sheet split exists because GBA palettes are 16 colors each. `useSecondTypeIconPalette` in `gTypesInfo[]` (`src/data/types_info.h`) controls which sheet each type uses.

---

## Effectiveness Icons (move selection screen, replaces PP text)

**Config toggle:** `include/config/battle.h:401-405`
```c
#define B_SHOW_EFFECTIVENESS  SHOW_EFFECTIVENESS_ALWAYS
// Options: SHOW_EFFECTIVENESS_NEVER, SHOW_EFFECTIVENESS_ALWAYS, SHOW_EFFECTIVENESS_CAUGHT, SHOW_EFFECTIVENESS_SEEN
```

**Implementation:** `src/battle_controller_player.c:2455-2491` — `MoveSelectionDisplayMoveEffectiveness()`

The icons are font characters, not sprites. They render into `B_WIN_PP` (the PP text window), replacing the "PP" label:

| Effectiveness | Character | Charmap code |
|---|---|---|
| Super effective | `{CIRCLE_DOT}` | `F9 15` |
| Normal | `{CIRCLE_HOLLOW}` | `F9 18` |
| Not very effective | `{TRIANGLE}` | `F9 16` |
| Immune | `{BIG_MULT_X}` | `F9 17` |
| Can't view / status move | *(empty)* | — |

Characters are defined in `charmap.txt:1078-1081`. To change the glyphs, edit the font tileset that maps those character codes.

**Logic flow:**
- `CheckTargetTypeEffectiveness()` at line 2437 — picks which foe to check (handles doubles; ghost-without-scope hides it)
- `CheckTypeEffectiveness()` at line ~2408 — calls `CalcTypeEffectivenessMultiplier()` and buckets the result
- Status moves always show no icon (`IsBattleMoveStatus()` check at line 2467)

---

## Key Tweak Points

| What | Where |
|---|---|
| Reposition type icons | `sTypeIconPositions[][]` in `src/type_icons.c:38-58` |
| Change effectiveness symbols | The 4 `static const u8` strings in `MoveSelectionDisplayMoveEffectiveness()` at `src/battle_controller_player.c:2457-2461` |
| Replace type icon sprites | Edit `graphics/types/battle_icons1.png` / `battle_icons2.png`, then `make` to repack `.4bpp.smol` |
| Show/hide behavior | `B_SHOW_TYPES` and `B_SHOW_EFFECTIVENESS` in `include/config/battle.h` |
