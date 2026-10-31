#!/usr/bin/env python3
"""
Interactive Indus Script CLI Translator
Author: Shashwat Aggarwal (Nabha, Punjab, India)
Date: October 2026
License: MIT License

Usage:
  python indus_translator_cli.py 176 342
  python indus_translator_cli.py 99 242 176 342
  python indus_translator_cli.py --list-signs
  python indus_translator_cli.py --interactive
"""

import sys
import argparse

# Syllabic Dictionary (8x5 Matrix + Core Determinatives)
SIGN_LEXICON = {
    # /m-/ family
    242: {"name": "Plain Fish", "syl": "ma", "root": "*mīn", "meaning": "exalted / chief / fish"},
    245: {"name": "Bisected Fish", "syl": "mi", "root": "*mī-an", "meaning": "superintendent / overseer"},
    244: {"name": "Roof Fish", "syl": "mu", "root": "*mey-mīn", "meaning": "sanctuary guardian / shelter"},
    247: {"name": "Fin Fish", "syl": "me", "root": "*mēl-mīn", "meaning": "high / maritime authority"},
    249: {"name": "Horned Fish", "syl": "mo", "root": "*kō-mīn", "meaning": "royal sacred dignitary"},
    
    # /k-/ family
    267: {"name": "Human Bearer", "syl": "ka", "root": "*kūli", "meaning": "authorized steward / bearer"},
    268: {"name": "Yoke Man", "syl": "ki", "root": "*kāvaṭi", "meaning": "customs / yoke steward"},
    269: {"name": "Bow Man", "syl": "ku", "root": "*vil/*kāmaṭhi", "meaning": "sanctuary archer / warden"},
    274: {"name": "Staff Man", "syl": "ke", "root": "*kōl-an", "meaning": "magistrate / sceptre-bearer"},
    285: {"name": "Horned Priest", "syl": "ko", "root": "*kō", "meaning": "sovereign / temple high lord"},

    # /c-/ family
    176: {"name": "Ribbed Comb", "syl": "ca", "root": "*cīr", "meaning": "standard / rank / order"},
    211: {"name": "Comb-4 Variant", "syl": "ci", "root": "*cir", "meaning": "administrative rank standard"},
    212: {"name": "Roof Comb", "syl": "cu", "root": "*cu-cīr", "meaning": "elevated rank dignity"},
    213: {"name": "Fin Comb", "syl": "ce", "root": "*ce-cīr", "meaning": "provincial civic order"},
    214: {"name": "Horned Comb", "syl": "co", "root": "*kō-cīr", "meaning": "sovereign royal standard"},

    # Commodities, Metrology & Civic Signs
    389: {"name": "Double Ellipse", "syl": "pa", "root": "*parutti", "meaning": "cotton textiles guild"},
    99:  {"name": "Water Vessel", "syl": "va", "root": "*ūr", "meaning": "sovereign city / settlement"},
    102: {"name": "Fortress Enclosure", "syl": "vu", "root": "*kōṭṭam", "meaning": "walled citadel / district"},
    48:  {"name": "Cultivated Field", "syl": "la", "root": "*kar", "meaning": "agricultural estate / registry"},
    87:  {"name": "Spoked Wheel", "syl": "lo", "root": "*vaṭṭam", "meaning": "administrative circle / province"},
    400: {"name": "Upright Loom", "syl": "tari", "root": "*tari", "meaning": "textile workshop / loom"},
    125: {"name": "Twin Slashes", "syl": "ciccā", "root": "*ciccā", "meaning": "timber / forestry outpost"},
    162: {"name": "Measuring Staff", "syl": "kōl", "root": "*kōl", "meaning": "standard weight / chert measure"},

    # Numerical Measure Strokes (Cubical Chert Weight Series)
    12: {"name": "Two Strokes", "syl": "iru", "root": "*iru", "meaning": "2x standard weight unit (1.72g)"},
    13: {"name": "Three/Four Strokes", "syl": "mu", "root": "*mu/*nālu", "meaning": "4x standard weight unit (3.44g)"},
    14: {"name": "Eight Strokes", "syl": "nālu", "root": "*eṇ", "meaning": "8x standard weight unit (6.88g)"},
    18: {"name": "Sixteen Strokes", "syl": "en", "root": "*patin-aṟu", "meaning": "16x standard base unit (13.72g)"},
    59: {"name": "Six Strokes", "syl": "āṟu", "root": "*aṟu", "meaning": "six-fold administrative division"},

    # Terminal Case Markers
    342: {"name": "Sacred Jar", "syl": "-in", "root": "*-in", "meaning": "[Personal Genitive: 'Property/Authority of']"},
    328: {"name": "Barbed Arrow", "syl": "-ku", "root": "*-ku", "meaning": "[Consignment Allative: 'Allotted quota for']"}
}


def translate_sequence(sign_ids):
    """Parses and translates an Indus sign sequence read Right-to-Left."""
    tokens = []
    syllables = []
    roots = []
    meanings = []
    
    is_titular = False
    is_tally = False

    for sid in sign_ids:
        info = SIGN_LEXICON.get(sid, {
            "name": f"Unclassified Glyph ({sid})",
            "syl": f"[{sid}]",
            "root": f"*[s{sid}]",
            "meaning": "unattested root"
        })
        tokens.append(info["name"])
        syllables.append(info["syl"])
        roots.append(info["root"])
        meanings.append(info["meaning"])

    # Determine grammatical case
    terminal_sid = sign_ids[-1] if sign_ids else None
    if terminal_sid == 342:
        case_info = "Animate Personal Genitive (*-in: 'Property / Official Custody of')"
        is_titular = True
    elif terminal_sid == 328:
        case_info = "Inanimate Consignment Allative/Dative (*-ku: 'Allotted Quota / Destination for')"
        is_tally = True
    else:
        case_info = "Autonomous Civic Monogram / Uninflected Proclamation"

    # Construct Translation
    if is_titular:
        core_title = " ".join([m for m in meanings[:-1]])
        translation = f"Official Seal belonging to the Authorized {core_title.title()} Magistrate."
    elif is_tally:
        measure = meanings[0] if len(meanings) > 1 else "Standard weight"
        translation = f"Warehouse Consignment: {measure} officially allotted for transit and delivery."
    else:
        core = " / ".join(meanings)
        translation = f"Civic Proclamation / Sovereign Emblem: [{core}]."

    return {
        "signs": sign_ids,
        "names": " → ".join(tokens),
        "transcription": "-".join(syllables),
        "proto_roots": " + ".join(roots),
        "case": case_info,
        "translation": translation
    }


def main():
    parser = argparse.ArgumentParser(description="Indus Valley Script Interactive CLI Translator")
    parser.add_argument("signs", nargs="*", type=int, help="Parpola sign numbers read Right-to-Left (e.g. 176 342)")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt")
    parser.add_argument("--list-signs", action="store_true", help="List all classified signs in dictionary")
    args = parser.parse_args()

    if args.list_signs:
        print("\n=== CLASSIFIED INDUS SYLLABIC & LOGOGRAPHIC DICTIONARY ===")
        print(f"{'Sign ID':<8} | {'Phonetic':<10} | {'Proto-Root':<14} | {'Glyph Description':<22} | {'Administrative Meaning'}")
        print("-" * 88)
        for sid, info in sorted(SIGN_LEXICON.items()):
            print(f"{sid:<8} | {info['syl']:<10} | {info['root']:<14} | {info['name']:<22} | {info['meaning']}")
        print()
        return

    if args.interactive or not args.signs:
        print("\n=======================================================")
        print(" INDUS SCRIPT INTERACTIVE TRANSLATION INTERFACE")
        print(" Author: Shashwat Aggarwal · Nabha, Punjab, India")
        print(" Enter sign IDs separated by spaces (e.g., '99 242 176 342')")
        print(" Type 'exit' or 'quit' to terminate.")
        print("=======================================================\n")
        while True:
            try:
                line = input("Indus Signs (R → L) > ").strip()
                if not line or line.lower() in ["exit", "quit"]:
                    break
                sids = [int(x) for x in line.replace(",", " ").replace("+", " ").split()]
                res = translate_sequence(sids)
                print("\n" + "-" * 60)
                print(f"  Signs:          {res['signs']}")
                print(f"  Glyphs:         {res['names']}")
                print(f"  Transcription:  {res['transcription']}")
                print(f"  Proto-Roots:    {res['proto_roots']}")
                print(f"  Grammar:        {res['case']}")
                print(f"  Translation:    \"{res['translation']}\"")
                print("-" * 60 + "\n")
            except Exception as e:
                print(f"Error parsing input: {e}")
        return

    # Direct CLI invocation
    res = translate_sequence(args.signs)
    print("\n" + "=" * 65)
    print(f"  Indus Sequence: {res['signs']} (Read Right-to-Left)")
    print(f"  Glyphs:         {res['names']}")
    print(f"  Phonetic:       {res['transcription']}")
    print(f"  Proto-Roots:    {res['proto_roots']}")
    print(f"  Morphosyntax:   {res['case']}")
    print(f"  Translation:    \"{res['translation']}\"")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
