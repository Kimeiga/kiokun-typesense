import typesense
import os
import enum
import itertools
import json
import sys
from collections import defaultdict
import re
import romkan

from get_words_with_kanji import get_words_with_kanji

# map of word/char string to list of indices and raw kanji/hanzi data
index = defaultdict(lambda: defaultdict(list))

# words from dong-chinese (cedict)
c_word_entries = {}

# words from jmdict
j_word_entries = {}

# words from jmnedict
n_word_entries = {}


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


file_path = "../zh/dictionary_word_2023-12-19.jsonl"

with open(file_path, "r", encoding="utf-8") as file:
    for idx, line in enumerate(file):

        data = json.loads(line)
        # print(data['trad'])
        # print(data)

        # items_dict = {}
        # for item in data["items"]:
        #     pinyin = convert_pinyin(item.get("pinyin", ""))
        #     if pinyin in items_dict:
        #         items_dict[pinyin] += "/" + \
        #             ("/".join(item.get("definitions", [])))
        #     else:
        #         items_dict[pinyin] = "/".join(item.get("definitions", []))

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

        # pinyins = list(items_dict.keys())
        # definitions = list(items_dict.values())

        # using a flattened structure for typesense querying performance
        # obj = {
        #     "w_s": data["simp"],
        #     "w_t": data["trad"],
        # }
        # if len(pinyins) > 0:
        #     obj["w_p"] = pinyins
        # if len(definitions) > 0:
        #     obj["w_d"] = definitions

        c_word_entries[idx] = data
        index[data["trad"]]['c_w'].append(idx)
        # print(data["trad"])

        # entries[data["trad"]] = {
        #     "w_s": data["simp"],
        #     "w_t": data["trad"],
        #     "w_p": list(items_dict.keys()),
        #     "w_d": list(items_dict.values()),
        # }

file_path = "../zh/dictionary_char_2023-12-19.jsonl"

char_mapping = {}

noTopWords = []

with open(file_path, "r", encoding="utf-8") as file:
    for idx, line in enumerate(file):
        data = json.loads(line)

        # print(data["char"])
        # char_mapping[data["char"]] = data
        index[data['char']]['c_c'] = data

        if 'statistics' in data and 'topWords' not in data['statistics']:
            print(data['char'])

            noTopWords.append(data['char'])

print(len(noTopWords))


# for char, data in char_mapping.items():
#     if "tradVariants" not in data:
#         # This means it's a traditional character which either
#         # 1. has no simplified variants
#         # 2. has simplified variants (via simpVariants)
#         #    (and we confirmed that all simp variants and all variants are in entries)

#         # We need to find the union of the pronunciations of this character from it's own pinyinFrequencies
#         # and that of it's simpVariants

#         # Start with trad's pronunciations, if present
#         set_of_pinyin = set(
#             [d["pinyin"] for d in data["pinyinFrequencies"]]
#             if "pinyinFrequencies" in data
#             else []
#         )

#         for variant in data.get("simpVariants", []):
#             if variant in index:
#                 # Add the pronunciations of the simpVariant
#                 set_of_pinyin.update(
#                     [d["pinyin"] for d in index[variant]['c']["pinyinFrequencies"]]
#                     if "pinyinFrequencies" in index[variant]['c']
#                     else []
#                 )

#         glosses = [data.get("gloss", "")]

#         # We also need to get the list of all glosses for each simpVariant
#         for variant in data.get("simpVariants", []):
#             if variant in index:
#                 # Add the pronunciations of the simpVariant
#                 glosses.append(index[variant]['c'].get("gloss", ""))

#         cv = list(
#             filter(lambda x: x != char, [v["char"]
#                    for v in data.get("variants", [])])
#         )

#         if char in index:
#             # combine in the data
#             entries[char]["c_t"] = char
#             if "simpVariants" in data:
#                 entries[char]["c_s"] = data["simpVariants"]
#             if len(glosses) > 1:
#                 entries[char]["c_g"] = glosses
#             if list(set_of_pinyin):
#                 entries[char]["c_p"] = list(set_of_pinyin)
#             if cv:
#                 entries[char]["c_v"] = cv
#         else:
#             obj = {
#                 "c_t": char,
#             }
#             if "simpVariants" in data:
#                 obj["c_s"] = data["simpVariants"]
#             if len(glosses) > 1:
#                 obj["c_g"] = glosses
#             if list(set_of_pinyin):
#                 obj["c_p"] = list(set_of_pinyin)
#             if cv:
#                 obj["c_v"] = cv
#             entries[char] = obj


with open('list_of_no_top_words_characters.json', 'w', encoding='utf-8') as file:
    json.dump(noTopWords, file, ensure_ascii=False, indent=4)

print('printed')


def cartesian_product(lists):
    return list(itertools.product(*lists))


def generate_combinations(key, j2ch):
    char_arrays = [[char] + j2ch.get(char, []) for char in key]
    return [''.join(comb) for comb in cartesian_product(char_arrays)]


def generate_combinations2(key, j2ch):
    # Map each character in key to its variant in j2ch, or to itself if not found
    return [''.join(j2ch.get(char, char) for char in key)]


def filter_entries(combinations, entries, key, j_entry):

    matched_entries = []
    for comb in combinations:
        if comb in entries:
            matched_entries.append(comb)
    return matched_entries


file_path = "../jp/jmdict-eng-3.5.0.json"
j2ch_path = "../j2ch.json"
j2ch_new_path = "../j2ch_new_min.json"

with open(j2ch_path, 'r', encoding='utf-8') as file:
    j2ch = json.load(file)

# for character mapping for now, but hopefully we can use this for word mapping too in the future
# for words that are 1 character long that is
with open(j2ch_new_path, 'r', encoding='utf-8') as file:
    j2ch_new = json.load(file)

with open(file_path, "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)["words"]

with open("../jp/jmdict_furigana.json", "r", encoding="utf-8") as file:
    jmdict_furigana = json.load(file)

with open("../jp/jmnedict_furigana.json", "r", encoding="utf-8") as file:
    jmnedict_furigana = json.load(file)

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
    "輪廻": "輪迴",

    '剣尖': '劍尖',
    '不穏': '不穩',
    '応変': '應變',
    '散発': '散發',
    '平穏': '平穩',
    '収獲': '收獲',
    '収穫': '收穫',
    '旧制': '舊制',
    '暗々': '暗暗',
    '声誉': '聲譽',
    '自尽': '自盡',
    '燻蒸剤': '燻蒸劑',
    '余熱': '餘熱',
    '余震': '餘震',
    '発毛': '發毛',
}

for idx, entry in enumerate(jmdict_data):

    # just put the entry under every kanji and kana representation
    # reference "entries page" of kiokun notion for reasoning

    key = ""

    # We have a revelation! We are not going to use the "common" field in the kanji and kana entries
    # to determine the correct key. They are already in order of most commonly used.
    # So we will simply do all of the below (including checking if in chinese) but without consideration
    # for the "common" field, woohoo!

    # common_kanjis_in_chinese = list(
    #     filter(lambda x: x["common"] and x['text'] in index, entry["kanji"]))
    # kanjis_in_chinese = list(
    #     filter(lambda x: x['text'] in index, entry["kanji"]))
    # common_kanjis = list(filter(lambda x: x["common"], entry["kanji"]))
    # common_kanas = list(filter(lambda x: x["common"], entry["kana"]))

    # if len(common_kanjis_in_chinese) > 0:
    #     key = common_kanjis_in_chinese[0]["text"]
    # elif len(kanjis_in_chinese) > 0:
    #     key = kanjis_in_chinese[0]["text"]
    # elif len(common_kanjis) > 0:
    #     key = common_kanjis[0]["text"]
    # elif len(common_kanas) > 0:
    #     key = common_kanas[0]["text"]
    # elif len(entry["kanji"]) > 0:
    #     key = entry["kanji"][0]["text"]
    # elif len(entry["kana"]) > 0:
    #     key = entry["kana"][0]["text"]

    # if key == "":
    #     print("No key found for entry", entry)
    #     continue
    kanjis_in_chinese = list(
        filter(lambda x: x['text'] in index, entry["kanji"]))

    if len(kanjis_in_chinese) > 0:
        key = kanjis_in_chinese[0]["text"]
    elif len(entry["kanji"]) > 0:
        key = entry["kanji"][0]["text"]
    elif len(entry["kana"]) > 0:
        key = entry["kana"][0]["text"]

    if key == "":
        print("No key found for entry", entry)
        continue

    print(key)

    # if key == "分布図":
    #     print("分布図")
    #     print(entry)

    # if key != '悪心':
    #     continue
    # if (entry['id'] == "1635160"):
    #     print("持論")
    #     print(matched_entries)

    zh_keys = []
    combinations = []
    matched_entries = []

    if key not in index:
        # Generate combinations and filter entries
        if (key not in exceptions):
            # combinations = generate_combinations(key, j2ch)

            combinations = generate_combinations2(key, j2ch_new)
            matched_entries = filter_entries(combinations, index, key, entry)

            zh_keys.extend(matched_entries)
        else:
            zh_keys.append(exceptions[key])

    is_common = any(kanji['common'] for kanji in entry["kanji"]) or any(
        kana['common'] for kana in entry["kana"])

    kana_texts = [kana_obj['text'] for kana_obj in entry['kana']]
    kana_tags = [kana_obj['tags'] for kana_obj in entry['kana']]

    kanji_object = {}

    for j, kanji in enumerate(entry["kanji"]):
        if kanji['text'] not in jmdict_furigana:
            # あ・うんの呼吸 (??)
            for i, kana in enumerate(kana_texts):
                # TODO: 手纏 (can't believe its not there)
                # means you'll have to do this part yourself i guess.. (or patch the existing one) (or patch its code)
                entry['kanji'][j].setdefault('r', []).append({'f': [{'r': kanji['text'], 't': kana}], **(
                    {'t': kana_tags[i]} if kana_tags[i] else {}), 'o': romkan.to_roma(kana)})
            continue
        for i, kana in enumerate([kana for kana in jmdict_furigana[kanji['text']] if kana in kana_texts]):
            # this ensures that the furiganas on this kanji are only from the set of kanas included in the entry

            # r = readings, f = furigana, t = tags, k = kana (add later if you want for something), o = rOmaji
            entry['kanji'][j].setdefault('r', []).append({'f':  [{'r': item['ruby'], **({'t': item['rt']} if 'rt' in item else {})}
                                                                 for item in jmdict_furigana[kanji['text']][kana]], **({'t': kana_tags[i]} if kana_tags[i] else {}), 'o':  romkan.to_roma(kana)})

    o = {
        # this will make it easier to check is_common on the frontend, trust me
        **({'c': is_common} if is_common else {}),
        **(
            {
                "k": [
                    {
                        # still need to keep
                        **({"c": True} if kanji["common"] else {}),
                        **({"t": kanji["text"]} if kanji["text"] else {}),
                        **({"g": kanji["tags"]} if len(kanji["tags"]) else {}),
                        **({"r": kanji['r']} if 'r' in kanji else {})
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
                        **({"r": romkan.to_roma(kana["text"])} if kana["text"] else {})
                    }
                    for kana in entry["kana"]
                ]
            }
            # we no longer need Kana info if we have kanji info, woohoo!
            if entry["kana"] and not entry['kanji']
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
                            # **({"g": gloss["gender"]} if gloss["gender"] else {}),
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

    j_word_entries[idx] = o

    for kanji in entry["kanji"]:
        index[kanji["text"]]['j_w'].append(idx)

        # if 86943 in index[kanji["text"]]['j_w']:
        #     print(entry)

        if len(zh_keys):
            # just directly store the ids of the chinese words that this maps to...
            # index[kanji["text"]]['v_c_w'].extend(
            #     item for zh_key in zh_keys for item in index[zh_key]['c_w'])
            for zh_key in zh_keys:
                for item in index[zh_key]['c_w']:
                    if item not in index[kanji["text"]]['v_c_w']:
                        index[kanji["text"]]['v_c_w'].append(item)
    for kana in entry["kana"]:
        index[kana["text"]]['j_w'].append(idx)

        # if 'さいとう' == key:
        #     print(entry)
        # if 86943 in index[kana["text"]]['j_w']:
        #     print(entry)

        if len(zh_keys):
            # just directly store the ids of the chinese words that this maps to...
            for zh_key in zh_keys:
                for item in index[zh_key]['c_w']:
                    if item not in index[kana["text"]]['v_c_w']:
                        index[kana["text"]]['v_c_w'].append(item)
            # index[kana["text"]]['v_c_w'].extend(
            #     item for zh_key in zh_keys for item in index[zh_key]['c_w'])

    for zh_key in zh_keys:
        index[zh_key]['v_j_w'].append(idx)


file_path = "../jp/kanjidic2-en-3.5.0.json"
with open(file_path, "r", encoding="utf-8") as file:
    kanjidic_data = json.load(file)["characters"]

    for entry in kanjidic_data:
        print(entry['literal'])
        # they are all unique, so can just add straight to the index

        zh_variant = None
        if entry['literal'] in j2ch_new:
            zh_variant = j2ch_new[entry['literal']]

        e = {
            "i": {
                **({"f": entry["misc"]["frequency"]} if entry["misc"]["frequency"] else {}),
                **({"g": entry["misc"]["grade"]} if entry["misc"]["grade"] else {}),
                **({"j": entry["misc"]["jlptLevel"]} if entry["misc"]["jlptLevel"] else {}),
                **({"r": entry["misc"]["radicalNames"]} if len(entry["misc"]["radicalNames"]) else {}),
                "s": entry["misc"]["strokeCounts"],
                **({"v": entry["misc"]["variants"]} if len(entry["misc"]["variants"]) else {}),
            },
            "r": [
                {"t": radical['type'],
                    'v': radical['value']}
                for radical in entry['radicals']
            ],
            "m": {
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
            },


        }

        # j for japanese character, c for chinese character
        index[entry["literal"]]['j_c'] = e

        # if len(zh_variants):
        #     index[entry["literal"]]['v'] = zh_variants

        # for zh_variant in zh_variants:
        #     index[zh_variant]['a'].append(entry["literal"])
        if zh_variant:
            index[entry["literal"]]['v_c_c'] = zh_variant
            index[zh_variant]['v_j_c'].append(entry["literal"])

        # for the chinese equivalents of
        # for variant in zh_variants:
        #     entries[variant].setdefault('v', []).append(e)


# ok now time to try the jmnedict

file_path = "../jp/jmnedict-all-3.5.0.json"

with open(file_path, "r", encoding="utf-8") as file:
    jmnedict_data = json.load(file)["words"]

    for idx, entry in enumerate(jmnedict_data):
        key = ""

        kanjis_in_chinese = list(
            filter(lambda x: x['text'] in index, entry["kanji"]))

        if len(kanjis_in_chinese) > 0:
            key = kanjis_in_chinese[0]["text"]
        elif len(entry["kanji"]) > 0:
            key = entry["kanji"][0]["text"]
        elif len(entry["kana"]) > 0:
            key = entry["kana"][0]["text"]

        if key == "":
            print("No key found for entry", entry)
            continue

        print(key)
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

        zh_keys = []

        if key not in index:
            # Generate combinations and filter entries
            if (key not in exceptions):
                combinations = generate_combinations(key, j2ch)
                matched_entries = filter_entries(
                    combinations, index, key, entry)
                zh_keys.extend(matched_entries)
            else:
                zh_keys.extend(exceptions[key])

        kanji_object = {}

        kana_texts = [kana_obj['text'] for kana_obj in entry['kana']]
        kana_tags = [kana_obj['tags'] for kana_obj in entry['kana']]

        # if key == "手纏":
        #     print("手纏")
        #     print(entry)

        for j, kanji in enumerate(entry["kanji"]):
            if kanji['text'] not in jmnedict_furigana:
                # あ・うんの呼吸 (??)
                for i, kana in enumerate(kana_texts):
                    # TODO: 手纏 (can't believe its not there)
                    # means you'll have to do this part yourself i guess.. (or patch the existing one) (or patch its code)
                    entry['kanji'][j].setdefault('r', []).append({'f': [{'r': kanji['text'], 't': kana}], **(
                        {'t': kana_tags[i]} if kana_tags[i] else {}), 'o': romkan.to_roma(kana)})
                continue
            for i, kana in enumerate([kana for kana in jmnedict_furigana[kanji['text']] if kana in kana_texts]):
                # this ensures that the furiganas on this kanji are only from the set of kanas included in the entry

                # r = readings, f = furigana, t = tags, k = kana (add later if you want for something), o = rOmaji
                entry['kanji'][j].setdefault('r', []).append({'f':  [{'r': item['ruby'], **({'t': item['rt']} if 'rt' in item else {})}
                                                                     for item in jmnedict_furigana[kanji['text']][kana]], **({'t': kana_tags[i]} if kana_tags[i] else {}), 'o':  romkan.to_roma(kana)})

        o = {
            **(
                {
                    "r": [
                        {
                            **({"a": kana["appliesToKanji"]} if kana["appliesToKanji"] != ["*"] else {}),
                            **({"g": kana["tags"]} if len(kana["tags"]) else {}),
                            **({"t": kana["text"]} if kana["text"] else {}),
                            **({"r": romkan.to_roma(kana["text"])} if kana["text"] else {})
                        }
                        for kana in entry["kana"]
                    ]
                }
                if entry["kana"] and not entry['kanji']
                else {}
            ),
            **(
                {
                    "k": [
                        {
                            **({"g": kanji["tags"]} if len(kanji["tags"]) else {}),
                            **({"t": kanji["text"]} if kanji["text"] else {}),
                            **({"r": kanji['r']} if 'r' in kanji else {})
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
        }

        # 樫

        n_word_entries[idx] = o

        for kanji in entry["kanji"]:
            index[kanji["text"]]['j_n'].append(idx)

            if len(zh_keys):
                # just directly store the ids of the chinese words that this maps to...
                for zh_key in zh_keys:
                    for item in index[zh_key]['c_w']:
                        if item not in index[kanji["text"]]['v_c_w']:
                            index[kanji["text"]]['v_c_w'].append(item)

        for kana in entry["kana"]:
            index[kana["text"]]['j_n'].append(idx)

            if len(zh_keys):
                for zh_key in zh_keys:
                    for item in index[zh_key]['c_w']:
                        if item not in index[kana["text"]]['v_c_w']:
                            index[kana["text"]]['v_c_w'].append(item)

                # just directly store the ids of the chinese words that this maps to...
                # index[kana["text"]]['v_c_w'].extend(
                    # item for zh_key in zh_keys for item in index[zh_key]['c_w'])

        for zh_key in zh_keys:
            index[zh_key]['v_j_n'].append(idx)


# At this point we need to compute for all japanese words, japanese names, chinese words: all substrings with length > 1 that are in the index
# since we need to serve them on demand

for key, value in index.items():
    list_of_valid_substrings = [key[i:j] for i in range(len(key))
                                for j in range(i + 1, len(key) + 1) if key[i:j] in index and len(key[i:j]) > 1 and (i != 0 and j != len(key))]
    if len(list_of_valid_substrings):
        value['s'] = list_of_valid_substrings


client = typesense.Client({
    'nodes': [{
        'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
        'port': '8108',      # For Typesense Cloud use 443
        'protocol': 'http'   # For Typesense Cloud use https
    }],
    'api_key': 'GSV3UjDj0By3HYzmgWSiCsprcn7khNRY3EVyVfHcOXOMaV3y',
    'connection_timeout_seconds': 2
})


def fetch_all_documents(collection_name, search_parameters):
    all_documents = []
    page = 1
    per_page = 50  # Adjust based on your needs and Typesense limits

    while True:
        search_parameters['per_page'] = per_page
        search_parameters['page'] = page
        response = client.collections[collection_name].documents.search(
            search_parameters)
        hits = response['hits']

        if not hits:
            break

        all_documents.extend(hits)
        page += 1

    return all_documents


# for all kanji/hanzis add the words that they appear in, we can choose 'a' as in AppearsIn
for key, value in index.items():
    if len(key) == 1:
        # this is a hanzi/kanji
        # search typesense index dictionary to see everything
        search_parameters = {
            'q': key,
            'query_by': 'w',
            'infix': 'always'
        }

        all_results = fetch_all_documents('index', search_parameters)
        value['a'] = [item['document']['w'] for item in all_results]


# make new folder to put everything called entry_data

output_folder = "entry_data"

# make the directory
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# output all files for the server script to use to serve data to /word
with open(os.path.join(output_folder, "entry_index_min.json"), "w", encoding="utf-8") as file:
    json.dump(index, file, ensure_ascii=False, separators=(',', ':'))

with open(os.path.join(output_folder, "c_word_entries_min.json"), "w", encoding="utf-8") as file:
    json.dump(c_word_entries, file, ensure_ascii=False, separators=(',', ':'))

with open(os.path.join(output_folder, "j_word_entries_min.json"), "w", encoding="utf-8") as file:
    json.dump(j_word_entries, file, ensure_ascii=False, separators=(',', ':'))

with open(os.path.join(output_folder, "n_word_entries_min.json"), "w", encoding="utf-8") as file:
    json.dump(n_word_entries, file, ensure_ascii=False, separators=(',', ':'))

# for debugging
with open(os.path.join(output_folder, "entry_index.json"), "w", encoding="utf-8") as file:
    json.dump(index, file, ensure_ascii=False, indent=2)

with open(os.path.join(output_folder, "c_word_entries.json"), "w", encoding="utf-8") as file:
    json.dump(c_word_entries, file, ensure_ascii=False, indent=2)

with open(os.path.join(output_folder, "j_word_entries.json"), "w", encoding="utf-8") as file:
    json.dump(j_word_entries, file, ensure_ascii=False, indent=2)

with open(os.path.join(output_folder, "n_word_entries.json"), "w", encoding="utf-8") as file:
    json.dump(n_word_entries, file, ensure_ascii=False, indent=2)

# we want to make a search json for finding usage of kanjis in words in chinese and japanese...
# in order to do this, we need to use the keys of the index as keys, and have some indication if
# they are in japanese and/or chinese, just so that we can look them up efficiently...

# actually it would be good to precompute all this data too, but i was just thinking typesense
# would be a good way to get the lists

# so on each character entry there could be 3 top level arrays: jw, cw, jcw (japanese words that
# use this character, chinese words that use this character, words in both languages that use
# this character )

# and we would need to use traditional chinese representation of these words remember, since that's
# the key (i guess technically for jw's they will be using japanese shinjitai since it's determined)
# that they aren't in chinese...

# to do this we just need to put a list of all the words in typesense, that should be all the keys

# so i will just make that at the bottom of here:

# with open(os.path.join(output_folder, "index_key_search.jsonl"), "w", encoding="utf-8") as file:
#     for i in index:
#         file.write(json.dumps({'w': i}, ensure_ascii=False) + "\n")
#     # json.dump([{'w': i} for i in index.keys()],
#         #   file, ensure_ascii=False, indent=2)
