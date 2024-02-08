import itertools
import json
import sys
from collections import defaultdict

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


file_path = "zh/dictionary_word_2023-12-19.jsonl"

entries = defaultdict(lambda: defaultdict(list))

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        # print(data)

        items_dict = {}
        for item in data["items"]:
            pinyin = convert_pinyin(item.get("pinyin", ""))
            if pinyin in items_dict:
                items_dict[pinyin] += "/" + \
                    ("/".join(item.get("definitions", [])))
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

file_path = "zh/dictionary_char_2023-12-19.jsonl"

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
            filter(lambda x: x != char, [v["char"]
                   for v in data.get("variants", [])])
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

# # we will add the jp data in the following way:
# # go through index.json, if jp char is in entries, add

# jp_index_path = 'jp/output/index_min.json'
# jmdict_path = 'jp/output/jmdict_min.json'
# jmnedict_path = 'jp/output/jmnedict_min.json'

# j2ch_path = "j2ch.json"

# with open(jp_index_path, 'r', encoding='utf-8') as file:
#     jp_index = json.load(file)

#     with open(jmdict_path, 'r', encoding='utf-8') as file:
#         jmdict = json.load(file)

#         with open(jmnedict_path, 'r', encoding='utf-8') as file:
#             jmnedict = json.load(file)

#             with open(j2ch_path, 'r', encoding='utf-8') as file:
#                 j2ch = json.load(file)

#                 for word, index_data in jp_index.items():

#                     for w in j2ch.get(word, [word]):

#                         if w in entries:

#                             entries[w]['j'] = [
#                                 jmdict[str(j)] for j in index_data.get('j', [])]

#                             entries[w]['n'] = [
#                                 jmnedict[str(j)] for j in index_data.get('n', [])]

#                             if 'k' in index_data:
#                                 entries[w]['k'] = index_data['k']
#                         else:
#                             entries[w] = {
#                                 **({'j': [jmdict[str(j)] for j in index_data.get('j', [])]} if 'j' in index_data else {}),
#                                 **({'n': [jmnedict[str(j)] for j in index_data.get('n', [])]} if 'n' in index_data else {}),
#                                 **({'k': index_data['k']} if 'k' in index_data else {}),
#                             }


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
                trueKey = matched_entries

        else:
            trueKey = exceptions[key]


# with open('jp/jmdict-index.json', 'r', encoding='utf-8') as file:
#     jmdict_index = json.load(file)
# with open('jp/jmdict-entries.json', 'r', encoding='utf-8') as file:
#     jmdict_entries = json.load(file)

# key = '悪心'

# for index in jmdict_index[key]:

#     # Generate combinations and filter entries
#     combinations = generate_combinations(key, j2ch)
#     matched_entries = filter_entries(
#         combinations, entries, key, jmdict_entries[index])

#     # Print results based on matches
#     print_results(matched_entries, key)


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

        if key in entries:
            # Skip if there's an exact match
            continue

        # if key != '悪心':
        #     continue

        # Generate combinations and filter entries
        if (key not in exceptions):
            combinations = generate_combinations(key, j2ch)
            matched_entries = filter_entries(combinations, entries, key, entry)

            # Print results based on matches
            print_results(matched_entries, entry, key)
        else:
            trueKey = exceptions[key]

with open("all_data.jsonl", "w", encoding="utf-8") as file:
    for entry in entries.values():
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
