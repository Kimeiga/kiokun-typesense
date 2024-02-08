import itertools
import json
import sys
from collections import defaultdict

# instead of cedict, we will use dong-chinese char and word dictionaries since they encompass cedict and other sources
# and we will use them for the backend of the app anyways

# this script can prepare the

import re
# import pykakasi

# kks = pykakasi.kakasi()
import romkan
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


file_path = "zh/dictionary_word_2023-12-19.jsonl"

entries = defaultdict(lambda: defaultdict(list))

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        # print(data)

        items_dict = {}
        for item in data["items"]:
            if 'definitions' not in item:
                continue
            pinyin = convert_pinyin(item.get("pinyin", ""))
            if pinyin in items_dict and items_dict[pinyin] != "":
                items_dict[pinyin] += "; " + \
                    ("; ".join(item.get("definitions", [])))
            else:
                items_dict[pinyin] = "; ".join(item.get("definitions", []))

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

file_path = "zh/dictionary_char_2023-12-19.jsonl"

char_mapping = {}

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)

        char_mapping[data["char"]] = data


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
                # TODO: check if there are any "" glosses
                glosses.append(entries[variant].get("gloss", ""))

        cv = list(
            filter(lambda x: x != char and x != "" and x != None, [v["char"]
                   for v in data.get("variants", [])])
        )

        if char in entries:
            # combine in the data
            entries[char]["c_t"] = char
            if "simpVariants" in data:
                entries[char]["c_s"] = data["simpVariants"]
            if len(glosses):
                entries[char]["c_g"] = '; '.join(glosses)
            if list(set_of_pinyin):
                entries[char]["c_p"] = ', '.join(list(set_of_pinyin))
            if cv:
                entries[char]["c_v"] = ', '.join(cv)
        else:
            obj = {
                "c_t": char,
            }
            if "simpVariants" in data:
                obj["c_s"] = data["simpVariants"]
            if len(glosses):
                obj["c_g"] = '; '.join(glosses)
            if list(set_of_pinyin):
                obj["c_p"] = ', '.join(list(set_of_pinyin))
            if cv:
                obj["c_v"] = ', '.join(cv)
            entries[char] = obj


def cartesian_product(lists):
    return list(itertools.product(*lists))


def generate_combinations(key, j2ch):
    char_arrays = [[char] + j2ch.get(char, []) for char in key]
    return [''.join(comb) for comb in cartesian_product(char_arrays)]


def filter_entries(combinations, entries, key, j_entry):

    matched_entries = defaultdict(list)
    for comb in combinations:
        if comb in entries:
            entry = entries[comb]
            # print(comb)
            # print(entry.get('w', {})
            #       and entry['w']['items'][0]['definitions'][0])
            # print(j_entry['sense'][0]['gloss'][0]['text'])
            if 'w' in entry:
                if key in entry['w'].get('simpVariants', []) or entry['w'].get('simp', '') == key:
                    matched_entries['same_simplified'].append(comb)
                else:
                    matched_entries['general'].append(comb)

                entry_definition = entry.get('w', {}).get('items', [])[
                    0].get('definitions', [entry.get('gloss', '')])[0]
                if not (entry_definition.startswith('variant') or any(entries[c].get('c', {}).get('hint', '').startswith(('Variant', 'variant')) for c in comb)):
                    if j_entry.get('sense', []) and (entry_definition in j_entry['sense'][0]['gloss'][0]['text']):
                        matched_entries['same_definition'].append(
                            comb)
                    else:
                        matched_entries['non_variant'].append(comb)
    return matched_entries


def print_results(matched_entries, entry, key):

    # if(matched_entries['same_definition']):
    #     return

    # print(matched_entries)
    if matched_entries['same_definition']:
        if len(matched_entries['same_definition']) > 1:
            print(
                f"Multiple same_definition matches found for key {key} ({entry['id']}) with same simplified that aren't variants: {matched_entries['same_definition']}")
        return

    if matched_entries['non_variant']:
        if len(matched_entries['non_variant']) > 1:
            print(
                f"Multiple non_variant matches found for key {key} ({entry['id']}) with same simplified that aren't variants: {matched_entries['non_variant']}")
        return

    if matched_entries['same_simplified']:
        if len(matched_entries['same_simplified']) > 1:
            print(
                f"Multiple matches found for key {key} ({entry['id']}) with same simplified: {matched_entries['same_simplified']}")
        return

    if matched_entries['general']:
        if len(matched_entries['general']) > 1:
            print(
                f"Multiple general matches found for key {key} ({entry['id']}): {matched_entries['general']}")
        return

    # if not any(matched_entries.values()):
    #     print(f"No matches found for key {key}.")


# with open('zh/char_word_dict.json', 'r', encoding='utf-8') as file:
#     entries = json.load(file)

file_path = "jp/jmdict-eng-3.5.0.json"
j2ch_path = "j2ch.json"

with open(j2ch_path, 'r', encoding='utf-8') as file:
    j2ch = json.load(file)

with open(file_path, "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)["words"]

# exceptions = {
#     1187830: "假託",  # 仮託
#     1221280: "歸依",  # 帰依, chosen because 歸依 is HSK 4, and 皈依 is not in HSK
#     1254980: "結髮",  # 結髪, 髮 and 髮 differ by one tiny stroke on top right of the 犮
#     1260770: "元勛",  # 元勲, src: wiktionary
#     1278580: "廣州",  # 広州
#     1282050: "行政區劃",  # 行政区画
#     1304210: "贊同",  # 賛同
#     1380670: "製圖",  # 製図
#     1397410: "素麵",  # 素麺
#     1421750: "痴呆",  # 痴呆 https://zh.wikipedia.org/wiki/%E5%A4%B1%E6%99%BA%E7%97%87
#     1513000: "辯證",  # 弁証
#     1517600: "炮擊",  # 砲撃
#     # 招来 apparently 招來 is an alternate form (src wiktionary) and baike's 招徠 entry is way longer
#     1619210: "招徠",
#     1626190: "發布",  # 発布
#     1946380: "分佈圖",
#     1955250: "冷麵",  # 冷麺
#     2133000: "身份證",  # 身分証
#     2438440: "檯子"  # 台子
# }
exceptions = {
    "仮託": "假託",  # 仮託
    "帰依": "歸依",  # 帰依, chosen because 歸依 is HSK 4, and 皈依 is not in HSK
    "結髪": "結髮",  # 結髪, 髮 and 髮 differ by one tiny stroke on top right of the 犮
    "元勲": "元勛",  # 元勲, src: wiktionary
    "広州": "廣州",  # 広州
    "行政区画": "行政區劃",  # 行政区画
    "賛同": "贊同",  # 賛同
    "製図": "製圖",  # 製図
    "素麺": "素麵",  # 素麺
    "痴呆": "痴呆",  # 痴呆 https://zh.wikipedia.org/wiki/%E5%A4%B1%E6%99%BA%E7%97%87
    "弁証": "辯證",  # 弁証
    "砲撃": "炮擊",  # 砲撃
    # 招来 apparently 招來 is an alternate form (src wiktionary) and baike's 招徠 entry is way longer
    "招来": "招徠",
    "発布": "發布",  # 発布
    "分布図": "分佈圖",
    "冷麺": "冷麵",  #
    "身分証": "身份證",  #
    "台子": "檯子",  #

    # jmnedict
    "円月": "元月",
    "径直": "徑直",
    "広安": "廣安",
    "広元": "廣元",
    "広陽": "廣陽",
    "日円": "日元",
    "弁別": "辨別",
    "輪廻": "輪迴"
}

for index, entry in enumerate(jmdict_data):
    key = ""

    common_kanjis_in_chinese = list(
        filter(lambda x: x["common"] and x['text'] in entries, entry["kanji"]))
    kanjis_in_chinese = list(
        filter(lambda x: x['text'] in entries, entry["kanji"]))
    common_kanjis = list(filter(lambda x: x["common"], entry["kanji"]))
    common_kanas = list(filter(lambda x: x["common"], entry["kana"]))

    if len(common_kanjis_in_chinese) > 0:
        key = common_kanjis_in_chinese[0]["text"]
    elif len(kanjis_in_chinese) > 0:
        key = kanjis_in_chinese[0]["text"]
    elif len(common_kanjis) > 0:
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

    # if key != '悪心':
    #     continue
        # if (entry['id'] == "1635160"):
        #     print("持論")
        #     print(matched_entries)

    trueKey = ''

    if key in entries:
        # Skip if there's an exact match
        trueKey = key
    else:
        # Generate combinations and filter entries
        if (key not in exceptions):
            combinations = generate_combinations(key, j2ch)
            matched_entries = filter_entries(combinations, entries, key, entry)

            # Print results based on matches
            # print_results(matched_entries, entry, key)

            # based on the matched results, choose a key:
            if matched_entries['same_definition']:
                trueKey = matched_entries['same_definition'][0]
            elif matched_entries['non_variant']:
                trueKey = matched_entries['non_variant'][0]
            elif matched_entries['same_simplified']:
                trueKey = matched_entries['same_simplified']
            elif matched_entries['generic']:
                trueKey = matched_entries['generic']
            else:
                trueKey = key
        else:
            trueKey = exceptions[key]

    print(trueKey)

    # At this point hopefully you have the true key

    entries[trueKey].setdefault('j', []).append(
        {
            **(
                {
                    "k": [
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
                    "r": [
                        {
                            **({"c": True} if kana["common"] else {}),
                            **({"t": kana["text"]} if kana["text"] else {}),
                            **({"g": kana["tags"]} if len(kana["tags"]) else {}),
                            **({"a": kana["appliesToKanji"]} if kana["appliesToKanji"] != ["*"] else {}),
                            **({"r":  romkan.to_roma(kana["text"])} if kana["text"] else {})
                        }
                        for kana in entry["kana"]
                    ]
                }
                if entry["kana"]
                else {}
            ),
            **({
                "s": [
                    {
                        **({"n": list(map(lambda inner: list(map(str, inner)), sense["antonym"]))} if len(sense["antonym"]) else {}),
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
                        **({"r": list(map(lambda inner: list(map(str, inner)), sense["related"]))
                            } if len(sense["related"]) else {}),
                    }
                    for sense in entry["sense"]
                ]
            }
                if entry["sense"]
                else {}
            ),
        }
    )

file_path = "jp/kanjidic2-en-3.5.0.json"
with open(file_path, "r", encoding="utf-8") as file:
    kanjidic_data = json.load(file)["characters"]

    for entry in kanjidic_data:
        # they are all unique, so can just add straight to the index

        zh_variants = []
        if entry['literal'] in j2ch:
            zh_variants = j2ch[entry['literal']]

        e = {
            "k": entry['literal'],
            "m": {

                **({"m": [meaning['value'] for meaning in entry['readingMeaning']['groups'][0]['meanings']]} if len(entry['readingMeaning']['groups'][0]['meanings']) else {}),
                # **({"k": [reading['value'] for reading in group['readings'] if reading['type'] == "ja_kun"]} if len([r for r in group['readings'] if r['type'] == "ja_kun"]) else {}),
                # **({"o": [reading['value'] for reading in group['readings'] if reading['type'] == "ja_on"]} if len([r for r in group['readings'] if r['type'] == "ja_on"]) else {}),

                # k: kunyomis
                # o: onyomis
                **({
                    key: [reading['value'] for reading in entry['readingMeaning']['groups'][0]['readings']
                          if reading['type'] == reading_type]
                    for reading_type, key in (("ja_kun", "k"), ("ja_on", "o"))
                    if any(reading['type'] == reading_type for reading in entry['readingMeaning']['groups'][0]['readings'])
                }),
                # "r": [
                #     {
                #         "t": "o" if reading['type'] == "ja_on" else "k", # we only need onyomis and kunyomis for the search page
                #         "v": reading['value'],
                #     } for reading in group['readings'] if (reading['type'] == "ja_on" or reading['type'] == "ja_kun")
                # ]

                **({"n": entry['readingMeaning']['nanori']} if len(entry['readingMeaning']['nanori']) else {}),
            },
            **({"v": zh_variants} if len(zh_variants) else {})
        }

        entries[entry["literal"]]['k'] = e

        # for the chinese equivalents of
        for variant in zh_variants:
            entries[variant].setdefault('v', []).append(e)


# ok now time to try the jmnedict

file_path = "jp/jmnedict-all-3.5.0.json"

with open(file_path, "r", encoding="utf-8") as file:
    jmnedict_data = json.load(file)["words"]

    for index, entry in enumerate(jmnedict_data):
        key = ""

        kanjis_in_chinese = list(
            filter(lambda x: x['text'] in entries, entry["kanji"]))

        if len(kanjis_in_chinese) > 0:
            key = kanjis_in_chinese[0]["text"]
        elif len(entry["kanji"]) > 0:
            key = entry["kanji"][0]["text"]
        elif len(entry["kana"]) > 0:
            key = entry["kana"][0]["text"]

        if key == "":
            print("No key found for entry", entry)
            continue

        # if (entry['id'] == "1592110"):
        #     print("区画")
        #     print(key)

        # if key != '悪心':
        #     continue

        # Generate combinations and filter entries
        # if (key not in exceptions):
        #     combinations = generate_combinations(key, j2ch)
        #     matched_entries = filter_entries(combinations, entries, key, entry)

        #     # Print results based on matches
        #     print_results(matched_entries, entry, key)
        # else:
        #     trueKey = exceptions[key]
        if key in entries:
            # Skip if there's an exact match
            trueKey = key
        else:
            # Generate combinations and filter entries
            if (key not in exceptions):
                combinations = generate_combinations(key, j2ch)
                matched_entries = filter_entries(
                    combinations, entries, key, entry)

                # Print results based on matches
                # print_results(matched_entries, entry, key)

                # based on the matched results, choose a key:
                if matched_entries['same_definition']:
                    trueKey = matched_entries['same_definition'][0]
                elif matched_entries['non_variant']:
                    trueKey = matched_entries['non_variant'][0]
                elif matched_entries['same_simplified']:
                    trueKey = matched_entries['same_simplified']
                elif matched_entries['generic']:
                    trueKey = matched_entries['generic']
                else:
                    trueKey = key
            else:
                trueKey = exceptions[key]

        print(trueKey)

        entries[trueKey].setdefault('n', []).append({
            **(
                {
                    "r": [
                        {
                            **({"a": kana["appliesToKanji"]} if kana["appliesToKanji"] != ["*"] else {}),
                            **({"g": kana["tags"]} if len(kana["tags"]) else {}),
                            **({"t": kana["text"]} if kana["text"] else {}),
                            **({"r":  romkan.to_roma(kana["text"])} if kana["text"] else {})
                        }
                        for kana in entry["kana"]
                    ]
                }
                if entry["kana"]
                else {}
            ),
            **(
                {
                    "k": [
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
                "t": [
                    {
                        **({'r': list(map(lambda inner: list(map(str, inner)), translation["related"]))
                            } if len(translation['related']) else {}),
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

with open("all_data2.jsonl", "w", encoding="utf-8") as file:
    for key, entry in entries.items():
        entry["e"] = key
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
