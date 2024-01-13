import json

file_path = "dictionary_char_2023-12-19.jsonl"
entries = {}

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)

        entries[data["char"]] = data
        # char = data["char"]
        # trad_variants = data.get("tradVariants", [])
        # simp_variants = data.get("simpVariants", [])
        # gloss = data.get("gloss", "")

        # # Check for existing entry in entries
        # for variant in trad_variants + simp_variants:
        #     if variant in entries:
        #         existing_entry = entries[variant]
        #         if "gloss" in existing_entry:
        #             if existing_entry["gloss"] != gloss:
        #                 print(
        #                     f"Differing gloss for {char} and its variant {variant}: {existing_entry['gloss']} vs {gloss}"
        #                 )

        # # Add or update entries
        # entries[char] = data
        # for variant in trad_variants + simp_variants:
        #     entries[variant] = data

        # Detect if a character has multiple simpVariants

        # if len(data.get("simpVariants", [])) > 1:
        #     print(data["char"], data.get("simpVariants", []))
        # for variant in data.get("simpVariants", []):
        #     if

for char, entry in entries.items():
    # check if every character in "simpVariants" in entries that have one is in entries
    # if so this means that we could probably just get rid of them for search purposes?

    if "variants" in entry:
        for variant in entry["variants"]:
            if variant["char"] and variant["char"] not in entries:
                print(char, variant["char"])

    # if "simpVariants" in entry and len(entry["simpVariants"]) > 1:
    #     if "pinyinFrequencies" not in entry:
    #         for variant in entry["simpVariants"]:
    #             if "pinyinFrequencies" in entries[variant]:
    #                 print(char, variant, entries[variant]["pinyinFrequencies"])
    # print(entry["char"], entry["simpVariants"])
    # For every character that has a "variants" field, check if each one of the variants has a "pinyinFrequencies" field
    # If not, print the character

    # if "simpVariants" in entry:
    #     l = list(filter(lambda x: x != char, entry["simpVariants"]))
    #     if len(l) > 1:
    #         print(char, entry["simpVariants"])

    # if (
    #     "simpVariants" in entry
    #     and "tradVariants" in entry
    #     and all(char != c for c in entry["simpVariants"])
    #     and all(char != c for c in entry["tradVariants"])
    # ):
    #     print(char)

    # if "simpVariants" in entry:
    #     for variant in entry["simpVariants"]:
    #         # print(entry, variant)
    #         if variant != entry and variant != "" and variant != None:
    #             # print(variant["char"])
    #             # check if the variant and the entry have the same pronunciation
    #             if (
    #                 "pinyinFrequencies" in entry
    #                 and "pinyinFrequencies" in entries[variant]
    #                 and set(
    #                     map(
    #                         lambda x: x["pinyin"], entries[variant]["pinyinFrequencies"]
    #                     )
    #                 )
    #                 != set(map(lambda x: x["pinyin"], entry["pinyinFrequencies"]))
    #             ):
    #                 print(
    #                     variant,
    #                     char,
    #                     set(
    #                         map(
    #                             lambda x: x["pinyin"],
    #                             entries[variant]["pinyinFrequencies"],
    #                         )
    #                     ),
    #                     set(map(lambda x: x["pinyin"], entry["pinyinFrequencies"])),
    #                 )

    # if "tradVariants" in entry:
    #     for variant in entry["tradVariants"]:
    #         # print(entry, variant)
    #         if variant != entry and variant != "" and variant != None:
    #             # print(variant)
    #             # check if the variant and the entry have the same pronunciation
    #             if (
    #                 "pinyinFrequencies" in entry
    #                 and "pinyinFrequencies" in entries[variant]
    #                 and entries[variant]["pinyinFrequencies"]
    #                 != entry["pinyinFrequencies"]
    #             ):
    #                 print(
    #                     variant,
    #                     char,
    #                     entries[variant]["pinyinFrequencies"],
    #                     entry["pinyinFrequencies"],
    #                 )
    # if "variants" in entry:
    #     for variant in entry["variants"]:
    #         # print(entry, variant)
    #         if (
    #             variant["char"] != entry
    #             and variant["char"] != ""
    #             and variant["char"] != None
    #         ):
    #             # print(variant["char"])
    #             # check if the variant and the entry have the same pronunciation
    #             if (
    #                 "pinyinFrequencies" in entry
    #                 and "pinyinFrequencies" in entries[variant["char"]]
    #                 and entries[variant["char"]]["pinyinFrequencies"]
    #                 != entry["pinyinFrequencies"]
    #             ):
    #                 print(
    #                     variant,
    #                     char,
    #                     entries[variant["char"]]["pinyinFrequencies"],
    #                     entry["pinyinFrequencies"],
    #                 )
