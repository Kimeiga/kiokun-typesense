import json

with open("japanese_to_chinese.json", "r", encoding="utf-8") as file:
    japanese_to_chinese = json.load(file)

with open("zh/char_word_dict.json", "r", encoding="utf-8") as file:
    zh = json.load(file)

j2ch = {char: values['T'] for char, values in japanese_to_chinese.items()}

j2ch_new = {}

# now try to do it only for characters that are in japanese

# for c, e in zh.items():
#     if 'w' in e and 'c' in e:
#         definitions = [definition for item in e['w']['items']
#                        if 'definitions' in item for definition in item['definitions']]

#         variant_definition = next(
#             (definition for definition in definitions if definition.startswith("variant of")), None)
#         if variant_definition:
#             variant_character = variant_definition[len('variant of ')]
#             print(c, variant_character, variant_definition)

# if any(definition.startswith("variant of") for definition in definitions):
#     print(c, next(x for x in definitions if x.startswith("variant of")))


# j2ch_new = {}

def get_original_character(j, cs):
    # for c in [c for c in cs if 'w' in zh[c]]:
    for c in cs:
        if c in zh and 'w' in zh[c]:
            definitions = [definition for item in zh[c]['w']['items']
                           if 'definitions' in item for definition in item['definitions']]

            variant_definition = next(
                (definition for definition in definitions if definition.startswith("variant of")), None)
            if variant_definition:
                variant_character = variant_definition[len('variant of ')]
                print(j, c, variant_character, variant_definition)
                return get_original_character(j, variant_character)
            else:
                return c
    # if ch in zh:
    #     if 'w' not in zh[ch]:
    #         print(ch, "no w")
        # if 'w' in zh[ch] and any(definition.startswith("variant of") for definition in zh[ch]['w']['items']["definitions"]):
        #     return get_original_character(next(x for x in zh[ch]['w']['items']["definitions"] if x.startswith("variant of")).split(" ")[-1])


# # remember it's J -> T
# # referencing wiktionary for this
# manually_chosen = {
#     "罔":  '網', # incorrect, 罔 means deceive, 網 means net, 罔 was an old variant...
#     "餘":  '餘',
#     "豫": "豫",
#     "余": "余",
#     "予": "豫"
#     # "並":  '並',
#     # "懷":  '懷',
# }

manually_chosen = {
    "幺": "幺",
    "画": "畫",
    "勲": "勛",
    "尅": "剋",
    "巌": "岩",
    "栢": "柏",
    "汚": "污",
    "艶": "豔",
    "蘯": "蕩",
    "讃": "讚",
    "簔": "蓑",
    "籘": "籐",
    "弁": "辨",
    "廻": "迴",
    "拝": "拜",
    "侭": "儘",
    "尽": "盡",
    "余": "餘",
    "証": "證",
}


for j, cs in j2ch.items():
    # print(j, cs)
    if j in manually_chosen:
        j2ch_new[j] = manually_chosen[j]
    elif len(cs) == 1:
        if cs[0] == "N/A":
            continue
        j2ch_new[j] = cs[0]
    else:
        same_char = next((c for c in cs if c == j), None)

        if same_char:
            j2ch_new[j] = same_char
            # actually don't put this in the database since we
            # continue
        else:
            # pick one
            # print(j, cs)

            j2ch_new[j] = get_original_character(j, cs)

            # if 'w' in zh[c] and any(definition.startswith("variant of") for definition in zh[c]['w']['items']["definitions"]):
            # if 'w' not in zh[cs[0]]:
            #     print(j, cs, cs[0], "no w")
            # get_original_character(cs[0])

with open("j2ch_new_min.json", "w", encoding="utf-8") as file:
    json.dump(j2ch_new, file, ensure_ascii=False, separators=(",", ":"))
with open("j2ch_new.json", "w", encoding="utf-8") as file:
    json.dump(j2ch_new, file, ensure_ascii=False, indent=2)

j2ch_new_different = {k: v for k, v in j2ch_new.items() if k != v}

with open("j2ch_new_different.json", "w", encoding="utf-8") as file:
    json.dump(j2ch_new_different, file, ensure_ascii=False, indent=2)


# print(j2ch_new['並'])
# print(j2ch_new['汚'])
# print(j2ch_new['並'])

# dong-chinese dataset actually has all of the japanese characters,
# so we have to try converting no matter what
# if j in zh:
#     continue
# print(j, cs)
