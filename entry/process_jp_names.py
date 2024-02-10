
# ok now time to try the jmnedict
import romkan
import json
from utils import generate_combinations, filter_entries, j_exceptions
file_path = "../jp/jmnedict-all-3.5.0.json"


def process(index, n_word_entries):

    with open("../jp/jmnedict_furigana.json", "r", encoding="utf-8") as file:
        jmnedict_furigana = json.load(file)

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
                if (key not in j_exceptions):
                    combinations = generate_combinations(key)
                    matched_entries = filter_entries(
                        combinations, index, key, entry)
                    zh_keys.extend(matched_entries)
                else:
                    zh_keys.extend(j_exceptions[key])

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
