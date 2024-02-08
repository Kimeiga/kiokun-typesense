import json

# import index.idx

# with open("words.idx", "r", encoding="utf-8") as file:
#     plaintext = file.read()
#     with open("output/search_data.json", "w", encoding="utf-8") as output:
#         # get data from output

#         data = json.load(output)

#         # for each line
#         for line in plaintext:
#             # split line into word and index
#             word, index = line.split(",")
#             # print(word, index)
#             # print(index.idx.in
#             if word not in data:
#                 print(word)

# import json

# with open("jp/jmdict-eng-3.5.0.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
#     for entry in data['words']:
#         for sense in entry['sense']:

#             if len(sense['related']) > 1:
#                 print(entry)

# key = "ABC"

# list_of_valid_substrings = [key[i:j] for i in range(len(key))
#                             for j in range(i + 1, len(key) + 1)
#                             if len(key[i:j]) > 1 and (i != 0 or j != len(key))]

# print(list_of_valid_substrings)

# import json

# with open("entry_data/entry_index_min.json", "r", encoding="utf-8") as file:
#     index = json.load(file)

#     for key, value in index.items():
#         if 'j' in value and 'c' in value:
#             if 'components' not in value['c']:
#                 print(f'{key} has no components')
#             else:
#                 print(
#                     f"{key} = {'+'.join([c['character'] for c in value['c']['components']])}")
#         if 'j' in value and 'c' not in value:
#             if len(key) > 1:
#                 print(f'{key} has j and no c and is len > 1')
#             else:
#                 print(f'{key} has j and no c and is len == 1')

import json

with open("all_data2.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        entry = json.loads(line)
        if 'k' in entry:
            if len(entry['k']['m']['g']) > 1:
                print(entry)

from collections import Counter

c = Counter()

d = 0
print('k')
with open('jp/kanjidic2-en-3.5.0.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for entry in data['characters']:
        d += 1
        c.update(str(len(entry['readingMeaning']['groups'])))

        if len(entry['readingMeaning']['groups']) > 1:
            print(entry)

print(c)
print(d)
