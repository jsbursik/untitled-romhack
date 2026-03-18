#!/usr/bin/env python3
"""
gen_dex_order.py
Generates a starting-point Solenne regional dex order C array from:
  - RevisedList.txt  (desired ordering)
  - include/config/species_enabled.h  (which families are disabled)
  - include/constants/pokedex.h  (full universe of NATIONAL_DEX_ constants)

Output: src/data/solenne_dex_order.c (edit by hand after generating)
"""

import re
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REVISED_LIST   = os.path.join(REPO_ROOT, "RevisedList.txt")
ENABLED_H      = os.path.join(REPO_ROOT, "include/config/species_enabled.h")
POKEDEX_H      = os.path.join(REPO_ROOT, "include/constants/pokedex.h")
OUTPUT         = os.path.join(REPO_ROOT, "src/data/solenne_dex_order.c")

# ---------------------------------------------------------------------------
# Form suffixes to strip when converting a display name to a base constant.
# Order matters — longer/more-specific first.
# ---------------------------------------------------------------------------
FORM_SUFFIXES = [
    "-red-striped", "-blue-striped", "-full-belly", "-disguised",
    "-standard", "-altered", "-pirouette", "-ordinary", "-resolute",
    "-incarnate", "-midday", "-midnight", "-dusk", "-plant", "-sandy",
    "-trash", "-normal", "-white", "-black", "-male", "-female",
    "-sky", "-land", "-aria", "-50", "-10",
]

# Names that don't follow the simple uppercase+underscore pattern.
SPECIAL_NAMES = {
    "nidoran-f":   "NIDORAN_F",
    "nidoran-m":   "NIDORAN_M",
    "farfetchd":   "FARFETCHD",
    "mr-mime":     "MR_MIME",
    "ho-oh":       "HO_OH",
    "mime-jr":     "MIME_JR",
    "porygon2":    "PORYGON2",
    "porygon-z":   "PORYGON_Z",
    "flabebe":     "FLABEBE",
    "type-null":   "TYPE_NULL",
    "jangmo-o":    "JANGMO_O",
    "hakamo-o":    "HAKAMO_O",
    "kommo-o":     "KOMMO_O",
    "tapu-koko":   "TAPU_KOKO",
    "tapu-lele":   "TAPU_LELE",
    "tapu-bulu":   "TAPU_BULU",
    "tapu-fini":   "TAPU_FINI",
    "mr-rime":     "MR_RIME",
    "sirfetchd":   "SIRFETCHD",
}

# Families whose P_FAMILY_ name doesn't directly map 1:1 to constants.
# Maps P_FAMILY_<key> → list of base NATIONAL_DEX_ suffix strings.
MULTI_FAMILY = {
    "NIDORAN":         ["NIDORAN_F", "NIDORAN_M"],
    "HITMONS":         ["HITMONLEE", "HITMONCHAN", "HITMONTOP"],
    "VOLBEAT_ILLUMISE":["VOLBEAT", "ILLUMISE"],
}

# ---------------------------------------------------------------------------

def name_to_constant(raw: str) -> str:
    """Convert a display name from RevisedList.txt to a NATIONAL_DEX_ constant."""
    name = raw.strip().lower()

    if name in SPECIAL_NAMES:
        return f"NATIONAL_DEX_{SPECIAL_NAMES[name]}"

    # Strip known form suffix
    for suffix in FORM_SUFFIXES:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break

    slug = name.upper().replace("-", "_").replace(" ", "_").replace("'", "")
    return f"NATIONAL_DEX_{slug}"


def parse_revised_list(path: str) -> list[str]:
    """Return ordered list of NATIONAL_DEX_ constants from RevisedList.txt."""
    constants = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: "123. PokemonName"
            m = re.match(r"^\d+\.\s+(.+)$", line)
            if m:
                constants.append(name_to_constant(m.group(1)))
    return constants


def parse_disabled_families(path: str) -> set[str]:
    """Return set of NATIONAL_DEX_ constants belonging to FALSE-disabled families."""
    disabled = set()
    with open(path) as f:
        for line in f:
            m = re.match(r"#define P_FAMILY_(\w+)\s+FALSE", line)
            if not m:
                continue
            family = m.group(1)
            if family in MULTI_FAMILY:
                for c in MULTI_FAMILY[family]:
                    disabled.add(f"NATIONAL_DEX_{c}")
            else:
                disabled.add(f"NATIONAL_DEX_{family}")
    return disabled


def parse_all_dex_constants(path: str) -> list[str]:
    """Return all NATIONAL_DEX_ enum members in order from pokedex.h."""
    constants = []
    with open(path) as f:
        for line in f:
            m = re.match(r"\s+(NATIONAL_DEX_\w+),", line)
            if m:
                c = m.group(1)
                if c != "NATIONAL_DEX_NONE":
                    constants.append(c)
    return constants


# ---------------------------------------------------------------------------

def main():
    ordered   = parse_revised_list(REVISED_LIST)
    disabled  = parse_disabled_families(ENABLED_H)
    all_consts = parse_all_dex_constants(POKEDEX_H)

    all_consts_set = set(all_consts)
    ordered_set    = set()

    # Build the primary ordered list, skipping disabled and unknown constants.
    primary = []
    skipped_unknown = []
    for c in ordered:
        if c in disabled:
            continue
        if c not in all_consts_set:
            skipped_unknown.append(c)
            continue
        if c not in ordered_set:
            primary.append(c)
            ordered_set.add(c)

    # Find enabled constants that weren't in the list at all.
    not_in_list = [c for c in all_consts if c not in ordered_set and c not in disabled]

    # Write output
    lines = []
    lines.append("// Solenne Regional Dex Order")
    lines.append("// Generated by tools/gen_dex_order.py — edit by hand after generating.")
    lines.append("//")
    lines.append("// Each entry is a national dex number in the order it appears in the Solenne Pokedex.")
    lines.append("// Regional forms share their base species entry — no separate line needed.")
    lines.append("// Legendaries are currently in national-dex position; move them as needed.")
    lines.append("")
    lines.append('#include "global.h"')
    lines.append('#include "constants/pokedex.h"')
    lines.append("")
    lines.append("const enum NationalDexOrder sSolenneToNationalOrder[] =")
    lines.append("{")

    for c in primary:
        lines.append(f"    {c},")

    if not_in_list:
        lines.append("")
        lines.append("    // ================================================================")
        lines.append("    // TODO: These were enabled but not in RevisedList.txt.")
        lines.append("    // Place them where they belong above and remove from this section.")
        lines.append("    // ================================================================")
        for c in not_in_list:
            lines.append(f"    {c},")

    lines.append("};")
    lines.append("")

    # Warn about names from the list that had no matching constant
    if skipped_unknown:
        lines.append("/*")
        lines.append(" * WARNING: These names from RevisedList.txt had no matching NATIONAL_DEX_ constant.")
        lines.append(" * They may be misspelled or removed from the ROM base. Check manually:")
        for c in skipped_unknown:
            lines.append(f" *   {c}")
        lines.append(" */")
        lines.append("")

    with open(OUTPUT, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Written: {OUTPUT}")
    print(f"  {len(primary)} ordered entries")
    print(f"  {len(not_in_list)} appended (enabled but not in list)")
    if skipped_unknown:
        print(f"  {len(skipped_unknown)} unrecognized names (see bottom of file)")
    if disabled:
        print(f"  Skipped {len(disabled)} constants from disabled families")


if __name__ == "__main__":
    main()
