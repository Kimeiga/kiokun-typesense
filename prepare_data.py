import json
import sys

# instead of cedict, we will use dong-chinese char and word dictionaries since they encompass cedict and other sources
# and we will use them for the backend of the app anyways

# this script can prepare the

import re

# Mapping of Pinyin tone marks to tone numbers and unmarked vowels
pinyin_tone_mapping = {
    "ā": ("a", "1"),
    "á": ("a", "2"),
    "ǎ": ("a", "3"),
    "à": ("a", "4"),
    "ē": ("e", "1"),
    "é": ("e", "2"),
    "ě": ("e", "3"),
    "è": ("e", "4"),
    "ī": ("i", "1"),
    "í": ("i", "2"),
    "ǐ": ("i", "3"),
    "ì": ("i", "4"),
    "ō": ("o", "1"),
    "ó": ("o", "2"),
    "ǒ": ("o", "3"),
    "ò": ("o", "4"),
    "ū": ("u", "1"),
    "ú": ("u", "2"),
    "ǔ": ("u", "3"),
    "ù": ("u", "4"),
    "ǖ": ("ü", "1"),
    "ǘ": ("ü", "2"),
    "ǚ": ("ü", "3"),
    "ǜ": ("ü", "4"),
}


def convert_pinyin(pinyin):
    if not pinyin:
        return ""

    # Remove any non-letter characters (like spaces, numbers, etc.)
    pinyin = re.sub(r"[^a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", "", pinyin)

    # Convert the pinyin with tone marks
    no_tone = pinyin
    tone_number = ""
    for char in pinyin:
        if char in pinyin_tone_mapping:
            no_tone_char, tone = pinyin_tone_mapping[char]
            no_tone = no_tone.replace(char, no_tone_char)
            tone_number = tone

    # Combine results
    return f"{pinyin} {no_tone}"


file_path = "dictionary_word_2023-12-19.jsonl"

entries = {}

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        # print(data)

        items_dict = {}
        for item in data["items"]:
            pinyin = convert_pinyin(item.get("pinyin", ""))
            if pinyin in items_dict:
                items_dict[pinyin] += "/" + ("/".join(item.get("definitions", [])))
            else:
                items_dict[pinyin] = "/".join(item.get("definitions", []))

        # new_items = []
        # for item in data["items"]:
        #     p = convert_pinyin(item.get("pinyin", ""))
        #     for idx, i in enumerate(new_items):
        #         if i["p"] == p:
        #             new_items[idx]["d"].extend(item.get("definitions", []))
        #             break
        #     else:
        #         new_items.append({"p": p, "d": item.get("definitions", [])})

        # if len(items_dict.values()) > 1:
        #     print(items_dict.values())
        #     print(list(items_dict.values()))

        pinyins = list(items_dict.keys())
        definitions = list(items_dict.values())

        # using a flattened structure for typesense querying performance
        obj = {
            "w_s": data["simp"],
            "w_t": data["trad"],
        }
        if len(pinyins) > 0:
            obj["w_p"] = pinyins
        if len(definitions) > 0:
            obj["w_d"] = definitions

        entries[data["trad"]] = obj

        # entries[data["trad"]] = {
        #     "w_s": data["simp"],
        #     "w_t": data["trad"],
        #     "w_p": list(items_dict.keys()),
        #     "w_d": list(items_dict.values()),
        # }

file_path = "dictionary_char_2023-12-19.jsonl"

char_mapping = {}

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)

        char_mapping[data["char"]] = data

        # if "gloss" not in data:
        #     print(data)

        # if "pinyinFrequencies" in data and "pinyin" not in data["pinyinFrequencies"][0]:
        #     print(data)

        # If this entry is for a simplified character, it will have a tradVariants array
        # For each of those tradVariants, make an entry in entries where the key is the tradVariant
        # and the value is the entry where we populate c_s as the simplified character and c_t as the tradVariant
        # If there already exists a key in entries for the tradVariant, it means that we processed the traditional character first

        # If this entry is for a traditional character, it will have a simpVariants array
        # For each of those simpVariants, make an entry in entries where the key is the traditional character
        # and the value is the entry where we populate c_s as the simpVariant and c_t as the traditional character
        # If there already exists a key in entries for the traditional character, it means that we processed the simplified character first

        # We could also not combine the data? idk
        # or maybe we can basically create a variants dictionary

        # The issue is that a simplified character can have multiple traditional variants and vice versa

        # if "tradVariants" in data:
        #     for tradVariant in data["tradVariants"]:
        #         if tradVariant in entries:
        #             entries[tradVariant]["c_t"] = tradVariant
        #             entries[tradVariant]["c_g"] = data.get("gloss", "")
        #             entries[tradVariant]["c_s"] = data["char"]
        #             entries[tradVariant]["c_p"] = (
        #                 [d["pinyin"] for d in data["pinyinFrequencies"]]
        #                 if "pinyinFrequencies" in data
        #                 else []
        #             )
        #         else:
        #             entries[tradVariant] = {
        #                 "c_s": data["char"],
        #                 "c_t": tradVariant,
        #                 "c_g": data.get("gloss", ""),
        #                 "c_p": (
        #                     [d["pinyin"] for d in data["pinyinFrequencies"]]
        #                     if "pinyinFrequencies" in data
        #                     else []
        #                 ),
        #             }

        # if "variants" in data:
        #     # for each variant, check if it is in entries
        #     # if it is, then update the entry
        #     # if it is not, then create a new entry
        #     for variant in data["variants"]:

        # if data["char"] in entries:
        #     print(data["char"])
        #     entries[data["char"]]["c_s"] = data.get("simpVariants", [])
        #     entries[data["char"]]["c_t"] = data.get("tradVariants", [])
        #     entries[data["char"]]["c_g"] = data.get("gloss", "")
        #     entries[data["char"]]["c_p"] = (
        #         [d["pinyin"] for d in data["pinyinFrequencies"]]
        #         if "pinyinFrequencies" in data
        #         else []
        #     )

        # else:
        #     entries[data["char"]] = {
        #         "c_s": data.get("simpVariants", []),
        #         "c_t": data.get("tradVariants", []),
        #         "c_g": data.get("gloss", ""),
        #         "c_p": [d["pinyin"] for d in data["pinyinFrequencies"]]
        #         if "pinyinFrequencies" in data
        #         else [],
        #     }

        # c_t
        # c_g = ""
        # c_s = []
        # c_d = []

for char, data in char_mapping.items():
    if "tradVariants" not in data:
        # This means it's a traditional character which either
        # 1. has no simplified variants
        # 2. has simplified variants (via simpVariants)
        #    (and we confirmed that all simp variants and all variants are in entries)

        # We need to find the union of the pronunciations of this character from it's own pinyinFrequencies
        # and that of it's simpVariants

        # Start with trad's pronunciations, if present
        set_of_pinyin = set(
            [d["pinyin"] for d in data["pinyinFrequencies"]]
            if "pinyinFrequencies" in data
            else []
        )

        for variant in data.get("simpVariants", []):
            if variant in entries:
                # Add the pronunciations of the simpVariant
                set_of_pinyin.update(
                    [d["pinyin"] for d in entries[variant]["pinyinFrequencies"]]
                    if "pinyinFrequencies" in entries[variant]
                    else []
                )

        glosses = [data.get("gloss", "")]

        # We also need to get the list of all glosses for each simpVariant
        for variant in data.get("simpVariants", []):
            if variant in entries:
                # Add the pronunciations of the simpVariant
                glosses.append(entries[variant].get("gloss", ""))

        cv = list(
            filter(lambda x: x != char, [v["char"] for v in data.get("variants", [])])
        )

        if char in entries:
            # combine in the data
            entries[char]["c_t"] = char
            if "simpVariants" in data:
                entries[char]["c_s"] = data["simpVariants"]
            if len(glosses) > 1:
                entries[char]["c_g"] = glosses
            if list(set_of_pinyin):
                entries[char]["c_p"] = list(set_of_pinyin)
            if cv:
                entries[char]["c_v"] = cv
        else:
            obj = {
                "c_t": char,
            }
            if "simpVariants" in data:
                obj["c_s"] = data["simpVariants"]
            if len(glosses) > 1:
                obj["c_g"] = glosses
            if list(set_of_pinyin):
                obj["c_p"] = list(set_of_pinyin)
            if cv:
                obj["c_v"] = cv
            entries[char] = obj


with open("all_data.jsonl", "w", encoding="utf-8") as file:
    for entry in entries.values():
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
