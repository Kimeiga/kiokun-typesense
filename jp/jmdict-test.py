import json

# appliesToKanas = set()

with open("jmdict-eng-3.5.0.json", "r", encoding="utf-8") as file:
    jmdict_data = json.load(file)["words"]

    for entry in jmdict_data:
        kanjis = entry['kanji']
        kanas = entry['kana']

        for kana in kanas:
            if kana['appliesToKanji'] != ['*']:
                print(entry)

        # Start with the assumption that kanjis are in common order
        # is_in_common_order = True
        # found_non_common = False

        # someKanjiIsCommon = any(kanji['common'] for kanji in kanjis)

        # first_is_common = False

        # for i, kana in enumerate(kanas):
        #     if i == 0:
        #         first_is_common = kana['common']
        #         continue
        #     elif not first_is_common and kana['common'] and someKanjiIsCommon:
        #         print(entry)
        #         break
        #     if found_non_common and kanji.get('common', False):
        #         # If a common kanji is found after a non-common kanji,
        #         # then the array is not in common order
        #         is_in_common_order = False
        #         break
        #     if not kanji.get('common', False):
        #         found_non_common = True

        # kana_is_in_common_order = True
        # kana_found_non_common = False

        # for kana in kanas:
        #     if kana_found_non_common and kana.get('common', False):
        #         # If a common kanji is found after a non-common kanji,
        #         # then the array is not in common order
        #         kana_is_in_common_order = False
        #         break
        #     if not kana.get('common', False):
        #         kana_found_non_common = True

        # if not kana_is_in_common_order:
        #     print(f"The entry {entry} is not in common order.")
        # for sense in entry['sense']:
            # print(gloss['appliesToKana'])
            # if len(sense['appliesToKana']) > 1:
            #     # appliesToKanas.add(sense['appliesToKana'])
            #     try:
            #         print(sense['appliesToKana'], entry['kanji'][0]['text'])
            #     except:
            #         pass
            # print(gloss['appliesToKana'])
            # if len(sense['dialect']) and sense['dialect'] != ["*"]:
            #     try:
            #         print(sense['dialect'], entry['kanji'][0]['text'])
            #     except:
            #         print(sense['dialect'])
        # for kana in entry["kana"]:
            # if len(kana['appliesToKanji']) and kana["appliesToKanji"] != ["*"]:
            #     # # Iterate through each kanji in appliesToKanji
            #     # for kanji in kana["appliesToKanji"]:
            #     #     # Check if the kanji is written in Katakana
            #     #     if regex.match(r'[\p{IsKatakana}]+', kanji):
            #     #         break
            #     # else:
            #     #     # If none of the kanji are Katakana, print the entry
            #     #     print(entry)
            #     #     break

            #     # important question: if a kana does apply to a certain kanji, does it have the exact same tags and the exact same common/not common?

            #     # Iterate through each kanji in appliesToKanji
            #     for kanji in kana["appliesToKanji"]:
            #         kanjiObj = next(
            #             (item for item in entry["kanji"] if item["text"] == kanji), None)

            #         if kanjiObj['common'] != kana['common'] or kanjiObj['tags'] != kana['tags']:
            #             print(entry)
            #             # break
# print(appliesToKanas)
