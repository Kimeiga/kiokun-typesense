from collections import defaultdict
import json

# to make this more performant, we need to turn jmdictFurigana and jmnedictFurigana into dictionaries so that we can look up the furigana for a given word in O(1)ish time
# during the creation of the entries...

# one question is if we even need the kana stuff after doing this.

# text -> reading -> furigana array
entries = defaultdict(lambda: defaultdict(list))

# open json file
with open('JmdictFurigana.json', 'r', encoding="utf-8-sig") as f:
    data = json.load(f)

    # check if there are any two entries that have the same text and reading
    for d in data:
        if d['text'] in entries and d['reading'] in entries[d['text']]:
            print(d)
        else:
            entries[d['text']][d['reading']] = d['furigana']

    # for d in data:
    #     entries[d['text']][d['reading']].append(d['furigana']})

# output entries to json
with open('jmdict_furigana.json', 'w') as f:
    json.dump(entries, f, ensure_ascii=False, separators=(',', ':'))

entries = defaultdict(lambda: defaultdict(list))


with open('JmnedictFurigana.json', 'r', encoding="utf-8-sig") as f:
    data = json.load(f)

    # check if there are any two entries that have the same text and reading
    for d in data:
        if d['text'] in entries and d['reading'] in entries[d['text']]:
            print(d)
        else:
            entries[d['text']][d['reading']] = d['furigana']

    # for d in data:
    #     entries[d['text']][d['reading']].append(d['furigana']})

# output entries to json
with open('jmnedict_furigana.json', 'w') as f:
    json.dump(entries, f, ensure_ascii=False, separators=(',', ':'))

# yay no output means that there are no two entries with the same text and reading
