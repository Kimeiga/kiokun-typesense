import json

file_path = "../zh/dictionary_word_2023-12-19.jsonl"


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


def process(index, c_word_entries):

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
