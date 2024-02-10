import json

file_path = "../zh/dictionary_char_2023-12-19.jsonl"


def process(index, c_word_entries):

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
