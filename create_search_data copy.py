# This file is to minify the jmdict file by removing all fields that are populated with null or default values
# And each entry will follow a convention of which representation to choose as the key in the dictionary:
# - common, kanji if it exists
# - common, kana if it exists
# - 1st kanji if it exists
# - 1st kana

# We will also create a mapping of all other representations to that key
# So we will have 1 master dictionary, and 1 fallback index mapping for when the given string is not found in the master dictionary

# Then we will combine in the other dictionaries like kanjidic2 and jmnedict
# And then we will combine in the decomposition information from the krad file
# And then we will combine in the used in information from the radkfile

import json
import sys
from collections import defaultdict
import os
import pykakasi

kks = pykakasi.kakasi()

file_path = "jp/jmdict-eng-3.5.0.json"

entries = defaultdict(list)

with open(file_path, "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)["words"]

    for index, entry in enumerate(jmdict_data):
        # First, decide on the key

        key = ""

        common_kanjis = list(filter(lambda x: x["common"], entry["kanji"]))
        common_kanas = list(filter(lambda x: x["common"], entry["kana"]))

        if len(common_kanjis) > 0:
            key = common_kanjis[0]["text"]
        elif len(common_kanas) > 0:
            key = common_kanas[0]["text"]
        elif len(entry["kanji"]) > 0:
            key = entry["kanji"][0]["text"]
        elif len(entry["kana"]) > 0:
            key = entry["kana"][0]["text"]

        if key == "":
            print("No key found for entry", entry)
            continue

        # if key in entries:
        #     try:
        #         print("Duplicate key found for entry",
        #               key, obj['s'][0]['g'][0]['t'])
        #     except:
        #         print("Duplicate key found for entry", key)
        #     continue

        entries[key].append({
            **(
                {
                    "j_k": [
                        {
                            **({"c": True} if kanji["common"] else {}),
                            **({"t": kanji["text"]} if kanji["text"] else {}),
                            **({"g": kanji["tags"]} if len(kanji["tags"]) else {}),
                        }
                        for kanji in entry["kanji"]
                    ]
                }
                if entry["kanji"]
                else {}
            ),
            **(
                {
                    "j_r": [
                        {
                            **({"c": True} if kana["common"] else {}),
                            **({"t": kana["text"]} if kana["text"] else {}),
                            **({"g": kana["tags"]} if len(kana["tags"]) else {}),
                            **({"a": kana["appliesToKanji"]} if kana["appliesToKanji"] != ["*"] else {}),
                            **({"r": ''.join(i['hepburn'] for i in kks.convert(kana["text"]))} if kana["text"] else {})
                        }
                        for kana in entry["kana"]
                    ]
                }
                if entry["kana"]
                else {}
            ),
            **({
                "j_s": [
                    {
                        **({"n": sense["antonym"]} if len(sense["antonym"]) else {}),
                        **({"k": sense["appliesToKana"]} if sense["appliesToKana"] != ["*"] else {}),
                        **({"a": sense["appliesToKanji"]} if sense["appliesToKanji"] != ["*"] else {}),
                        **({"d": sense["dialect"]} if len(sense["dialect"]) else {}),
                        **({"f": sense["field"]} if len(sense["field"]) else {}),
                        "g": [
                            {
                                **({"g": gloss["gender"]} if gloss["gender"] else {}),
                                **({"y": gloss["type"]} if gloss["type"] else {}),
                                **({"t": gloss["text"]} if gloss["text"] else {}),
                            }
                            for gloss in sense["gloss"]
                        ]
                        if "gloss" in sense else [],
                        ** ({"i": sense["info"]} if len(sense["info"]) else {}),
                        **({"l": sense["languageSource"]} if len(sense["languageSource"]) else {}),
                        **({"m": sense["misc"]} if len(sense["misc"]) else {}),
                        **({"p": sense["partOfSpeech"]} if len(sense["partOfSpeech"]) else {}),
                        **({"r": sense["related"]} if len(sense["related"]) else {}),
                    }
                    for sense in entry["sense"]
                ]
            }
                if entry["sense"]
                else {}
            ),
        })

        # # Then, populate the entry
        # jmdict_entries[key] = {"k": entry["kanji"], "r": entry["kana"], "s": entry["sense"]}

        # For every kanji and kana representation, add a mapping in the word index from that to the id of the word


file_path = "jp/kanjidic2-en-3.5.0.json"
with open(file_path, "r", encoding="utf-8") as file:
    kanjidic_data = json.load(file)["characters"]

    for entry in kanjidic_data:
        # they are all unique, so can just add straight to the index

        entries[entry['literal']].append(
            {
                "k_i": {
                    **({"f": entry["misc"]["frequency"]} if entry["misc"]["frequency"] else {}),
                    **({"g": entry["misc"]["grade"]} if entry["misc"]["grade"] else {}),
                    **({"j": entry["misc"]["jlptLevel"]} if entry["misc"]["jlptLevel"] else {}),
                    **({"r": entry["misc"]["radicalNames"]} if len(entry["misc"]["radicalNames"]) else {}),
                    "s": entry["misc"]["strokeCounts"],
                    **({"v": entry["misc"]["variants"]} if len(entry["misc"]["variants"]) else {}),
                },
                "k_r": [
                    {"t": radical['type'],
                     'v': radical['value']}
                    for radical in entry['radicals']
                ],
                "k_m": {
                    "g": [{
                        **({"m": [{
                            **({"v": meaning['value']} if meaning else {})
                        } for meaning in group['meanings']]}),
                        "r": [
                            {
                                "t": reading['type'],
                                "v": reading['value'],
                            } for reading in group['readings']
                        ]
                    } for group in entry['readingMeaning']['groups']],
                    **({"n": entry['readingMeaning']['nanori']} if len(entry['readingMeaning']['nanori']) else {}),
                }
            }
        )

file_path = "jp/jmnedict-all-3.5.0.json"

jmnedict_entries = {}

with open(file_path, "r", encoding="utf-8") as file:
    jmnedict_data = json.load(file)["words"]

    for index, entry in enumerate(jmnedict_data):

        key = ""

        if len(entry["kanji"]) > 0:
            key = entry["kanji"][0]["text"]
        elif len(entry["kana"]) > 0:
            key = entry["kana"][0]["text"]

        if key == "":
            print("No key found for entry", entry)
            continue

        entries[key].append({
            **(
                {
                    "n_r": [
                        {
                            **({"a": kana["appliesToKanji"]} if kana["appliesToKanji"] != ["*"] else {}),
                            **({"g": kana["tags"]} if len(kana["tags"]) else {}),
                            **({"t": kana["text"]} if kana["text"] else {}),
                            **({"r": ''.join(i['hepburn'] for i in kks.convert(kana["text"]))} if kana["text"] else {})
                        }
                        for kana in entry["kana"]
                    ]
                }
                if entry["kana"]
                else {}
            ),
            **(
                {
                    "n_k": [
                        {
                            **({"g": kanji["tags"]} if len(kanji["tags"]) else {}),
                            **({"t": kanji["text"]} if kanji["text"] else {}),
                        }
                        for kanji in entry["kanji"]
                    ]
                }
                if entry["kanji"]
                else {}
            ),
            **({
                "n_t": [
                    {
                        **({'r': translation['related']} if len(translation['related']) else {}),
                        **({'t': [
                            t['text']
                            for t in translation['translation']
                        ]} if len(translation['translation']) else {}),
                        **({'y': translation['type']} if translation['type'] else {})
                    }
                    for translation in entry['translation']
                ]
                if entry['translation'] else {}
            })
        })


output_folder = "output"

# make the directory
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(os.path.join(output_folder, "search_data_min.json"), "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, separators=(",", ":"))
with open(os.path.join(output_folder, "search_data.json"), "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=2)
