import json
from utils import j2ch_new

file_path = "../jp/kanjidic2-en-3.5.0.json"


def process(index, j_word_entries):
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
