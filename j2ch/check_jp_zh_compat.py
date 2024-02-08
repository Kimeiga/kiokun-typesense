# import json
# from collections import defaultdict

# # entries = defaultdict(dict)
# # with open("zh/dictionary_char_2023-12-19.jsonl", "r", encoding="utf-8") as file:
# #     for line in file:
# #         data = json.loads(line)

# #         # Exclude specific fields
# #         excluded_fields = {'_id', 'codepoint', 'char'}
# #         filtered_data = {key: value for key, value in data.items()
# #                          if key not in excluded_fields}

# #         entries[data['char']]['c'] = filtered_data

# # with open("zh/dictionary_word_2023-12-19.jsonl", "r", encoding="utf-8") as file:
# #     for line in file:
# #         data = json.loads(line)

# #         # Exclude specific fields
# #         excluded_fields = {'_id', 'trad'}
# #         filtered_data = {key: value for key, value in data.items()
# #                          if key not in excluded_fields}

# #         entries[data['trad']]['w'] = filtered_data

# # # output to file
# # with open("zh/char_word_dict.json", "w", encoding="utf-8") as file:
# #     json.dump(entries, file, ensure_ascii=False, indent=2)
# import itertools
# with open('zh/char_word_dict.json', 'r', encoding='utf-8') as file:
#     entries = json.load(file)

# file_path = "jp/jmdict-eng-3.5.0.json"

# j2ch_path = "j2ch.json"


# def cartesian_product(lists):
#     return list(itertools.product(*lists))


# with open(j2ch_path, 'r', encoding='utf-8') as file:
#     j2ch = json.load(file)

# with open(file_path, "r", encoding="utf-8") as file:
#     jmdict_data = json.load(file)["words"]

#     for index, entry in enumerate(jmdict_data):
#         # First, decide on the key

#         key = ""

#         common_kanjis = list(filter(lambda x: x["common"], entry["kanji"]))
#         common_kanas = list(filter(lambda x: x["common"], entry["kana"]))

#         if len(common_kanjis) > 0:
#             key = common_kanjis[0]["text"]
#         elif len(common_kanas) > 0:
#             key = common_kanas[0]["text"]
#         elif len(entry["kanji"]) > 0:
#             key = entry["kanji"][0]["text"]
#         elif len(entry["kana"]) > 0:
#             key = entry["kana"][0]["text"]

#         if key == "":
#             print("No key found for entry", entry)
#             continue

#         # now check if there is more than one key that this could translate to in the entries in the chinese prepared dictionary

#         if key in entries:
#             # only look if there isn't an exact match
#             continue

#         # Generate combinations
#         char_arrays = []
#         for char in key:
#             if char in j2ch:
#                 char_arrays.append(j2ch[char] + [char])
#             else:
#                 char_arrays.append([char])

#         all_combinations = cartesian_product(char_arrays)

#         # Join each tuple into a string
#         string_combinations = [''.join(comb) for comb in all_combinations]
#         # Check for multiple matches in entries
#         matched_entries_with_same_simplified_that_arent_variant = [
#             comb for comb in string_combinations
#             if comb in entries and (any(simp == key for simp in entries[comb].get('w', {}).get('simpVariants', [])) or
#                                     entries[comb].get('w', {}).get('simp', '') == key)
#             and (len(entries[comb].get('w', {}).get('items', [])) and
#                  len(entries[comb].get('w', {}).get('items', [])[0].get('definitions')) and
#                  not entries[comb].get('w', {}).get('items', [])[0].get('definitions')[0].startswith('variant'))
#         ]

#         matched_entries_with_same_simplified = [
#             comb for comb in string_combinations
#             if comb in entries and (any(simp == key for simp in entries[comb].get('w', {}).get('simpVariants', [])) or
#                                     entries[comb].get('w', {}).get('simp', '') == key)
#         ]

#         matched_entries = [
#             comb for comb in string_combinations if ''.join(comb) in entries]

#         if len(matched_entries_with_same_simplified_that_arent_variant) > 1:
#             print(
#                 f"Multiple matches found for key {key} with same simplified that aren't variants: {matched_entries_with_same_simplified_that_arent_variant}")

#         if len(matched_entries_with_same_simplified_that_arent_variant) == 0 and len(matched_entries_with_same_simplified) > 1:
#             print(
#                 f"Multiple matches found for key {key} with same simplified: {matched_entries_with_same_simplified}")
#         if len(matched_entries_with_same_simplified) == 0 and len(matched_entries) > 1:
#             print(f"Multiple matches found for key {key}: {matched_entries}")


# # key = "区画"

# # char_arrays = []
# # for char in key:
# #     if char in j2ch:
# #         char_arrays.append(j2ch[char] + [char])
# #     else:
# #         char_arrays.append([char])

# # all_combinations = cartesian_product(char_arrays)

# # # Join each tuple into a string
# # string_combinations = [''.join(comb) for comb in all_combinations]
# # # Check for multiple matches in entries
# # matched_entries_with_same_simplified = [
# #     comb for comb in string_combinations
# #     if comb in entries and (any(simp == key for simp in entries[comb].get('w', {}).get('simpVariants', [])) or
# #                             entries[comb].get('w', {}).get('simp', '') == key)
# # ]

# # print(matched_entries_with_same_simplified)

# # matched_entries = [
# #     comb for comb in string_combinations if ''.join(comb) in entries]

# # if len(matched_entries_with_same_simplified) > 1:
# #     print(
# #         f"Multiple matches found for key {key} with same simplified: {matched_entries_with_same_simplified}")
# # if len(matched_entries_with_same_simplified) == 0 and len(matched_entries) > 1:
# #     print(f"Multiple matches found for key {key}: {matched_entries}")


import json
import itertools
from collections import defaultdict

with open('zh/char_word_dict.json', 'r', encoding='utf-8') as file:
    entries = json.load(file)


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

    # print(trueKey)


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

        # # Generate combinations and filter entries
        # if (key not in exceptions):
        #     combinations = generate_combinations(key, j2ch)
        #     matched_entries = filter_entries(combinations, entries, key, entry)

        #     # Print results based on matches
        #     print_results(matched_entries, entry, key)
        # else:
        #     trueKey = exceptions[key]
        trueKey = ''

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


# now we need to combine in the kanijdic

# with open('jp/kanjidic2-en-3.5.0.json', 'r', encoding='utf-8') as file:
#     kanjidic = json.load(file)['characters']

#     for entry in kanjidic:
#         zh_variants = j2ch[entry['literal']]

#         for variant in zh_variants:

#             entries[variant] =
