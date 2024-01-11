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
    return f"{pinyin} {no_tone}{tone_number} {no_tone}"


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
                items_dict[pinyin].append(item.get("definitions", []))
            else:
                items_dict[pinyin] = [item.get("definitions", [])]

        entries[data["trad"]] = {
            "w": {
                "s": data["simp"],
                "t": data["trad"],
                "i": items_dict,
            }
        }

with open("all_data.jsonl", "w", encoding="utf-8") as file:
    for entry in entries.values():
        file.write(json.dumps(entry) + "\n")
