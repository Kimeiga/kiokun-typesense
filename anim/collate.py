import json
from os import sep

j_entries = {}
s_entries = {}
t_entries = {}

with open("dictionaryJa.txt", "r", encoding="utf-8") as file:
    dictionary = file.read().split("\n")
    
    for i, entry in enumerate(dictionary):
        if entry:
            print(i, entry)
            json_entry = json.loads(entry)
            j_entries[json_entry["character"]] = json_entry

with open("dictionaryZhHans.txt", "r", encoding="utf-8") as file:

    dictionary = file.read().split("\n")
    for entry in dictionary:
        if entry:
            json_entry = json.loads(entry)
            s_entries[json_entry["character"]] = json_entry

with open("dictionaryZhHant.txt", "r", encoding="utf-8") as file:
    dictionary = file.read().split("\n")
    for entry in dictionary:
        if entry:
            json_entry = json.loads(entry)
            t_entries[json_entry["character"]] = json_entry

# Extract the keys (characters) from each dictionary and convert them to sets
j_characters = set(j_entries.keys())
s_characters = set(s_entries.keys())
t_characters = set(t_entries.keys())

# Find unique characters
unique_to_j = j_characters - (s_characters.union(t_characters))
unique_to_s = s_characters - (j_characters.union(t_characters))
unique_to_t = t_characters - (j_characters.union(s_characters))

# Print the unique characters
print("Unique to Japanese:", unique_to_j)
print("Unique to Simplified Chinese:", unique_to_s)
print("Unique to Traditional Chinese:", unique_to_t)


with open("dictionaryJa.json", "w", encoding="utf-8") as file:
    json.dump(j_entries, file, ensure_ascii=False, separators=(',', ':'))
with open("dictionaryZhHans.json", "w", encoding="utf-8") as file:
    json.dump(s_entries, file, ensure_ascii=False, separators=(',', ':'))
with open("dictionaryZhHant.json", "w", encoding="utf-8") as file:
    json.dump(t_entries, file, ensure_ascii=False, separators=(',', ':'))
