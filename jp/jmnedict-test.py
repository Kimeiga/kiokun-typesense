import json


with open("jmnedict-all-3.5.0.json", "r", encoding="utf-8") as file:
    jmnedict_data = json.load(file)["words"]

    for entry in jmnedict_data:
        # for kana in entry["kana"]:
        # if kana['appliesToKanji'] != ['*']:
        #     print(entry)
        #     break
        if len(entry["kanji"]) == 0:
            print(entry)
