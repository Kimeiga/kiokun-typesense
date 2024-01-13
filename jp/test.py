import json
import sys
from collections import defaultdict


file_path = "kanjidic2-en-3.5.0.json"
with open(file_path, "r", encoding="utf-8") as file:
    kanjidic_data = json.load(file)["characters"]

    # for kanji in kanjidic_data:
    #     if len(kanji["misc"]["strokeCounts"]) < 1:
    #         print(kanji["literal"], kanji["misc"]["strokeCounts"])

    # for kanji in kanjidic_data:
    #     for group in kanji["readingMeaning"]['groups']:
    #         for reading in group['readings']:
    #             # print(reading['onType'])
    #             if reading['onType']:
    #                 print(kanji["literal"], reading['onType'])
    #             if reading['status']:
    #                 print(kanji["literal"], reading['status'])

    for kanji in kanjidic_data:
        if len(kanji['readingMeaning']['nanori']):
            print(kanji["literal"], kanji['readingMeaning']['nanori'])
