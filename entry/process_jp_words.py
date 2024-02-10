import json
from utils import generate_combinations, generate_combinations2, filter_entries, get_j2ch_word, jmdict_furigana, j_exceptions
import romkan


file_path = "../jp/jmdict-eng-3.5.0.json"
with open(file_path, "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)["words"]


def process(index, j_word_entries):

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
            zh_keys = get_j2ch_word(key, index)

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
