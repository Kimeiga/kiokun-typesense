import json

with open('jmdict_furigana.json', 'r') as f:
    jmdict_furigana = json.load(f)

with open('jmdict-eng-3.5.0.json', 'r') as f:
    jmdict_data = json.load(f)['words']

count = 0

for entry in jmdict_data:
    for kanji in entry['kanji']:

        try:
            furigana_object = jmdict_furigana[kanji['text']]
        except:
            print("No furigana for", kanji)

        for kana in entry['kana']:
            try:
                furigana_object[kana['text']]
            except:
                print("No furigana for", kana)
                count += 1

print(count)
