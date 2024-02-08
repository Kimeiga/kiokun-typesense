from collections import defaultdict
from email.policy import default
import json

index = defaultdict(list)
entries = {}

with open("jmdict-eng-3.5.0.json", "r", encoding="utf-8") as file:
    data = json.load(file)["words"]

    for entry in data:
        for kanji in entry["kanji"]:
            index[kanji["text"]].append(entry["id"])
            entries[entry["id"]] = entry
        for kana in entry["kana"]:
            index[kana["text"]].append(entry["id"])
            entries[entry["id"]] = entry

with open("jmdict-index.json", "w") as file:
    json.dump(index, file, separators=(',', ':'))
with open("jmdict-entries.json", "w") as file:
    json.dump(entries, file, separators=(',', ':'))
