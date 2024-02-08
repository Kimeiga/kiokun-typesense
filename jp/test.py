import json
import sys
from collections import defaultdict


# file_path = "kanjidic2-en-3.5.0.json"
# with open(file_path, "r", encoding="utf-8") as file:
#     kanjidic_data = json.load(file)["characters"]

#     # for kanji in kanjidic_data:
#     #     if len(kanji["misc"]["strokeCounts"]) < 1:
#     #         print(kanji["literal"], kanji["misc"]["strokeCounts"])

#     # for kanji in kanjidic_data:
#     #     for group in kanji["readingMeaning"]['groups']:
#     #         for reading in group['readings']:
#     #             # print(reading['onType'])
#     #             if reading['onType']:
#     #                 print(kanji["literal"], reading['onType'])
#     #             if reading['status']:
#     #                 print(kanji["literal"], reading['status'])

#     for kanji in kanjidic_data:
#         if len(kanji['readingMeaning']['nanori']):
#             print(kanji["literal"], kanji['readingMeaning']['nanori'])


'''
jmdict_file_path = "jmdict-eng-3.5.0.json"

j2ch_path = "../j2ch.json"

c_word_path = "../zh/dictionary_word_2023-12-19.jsonl"

with open(j2ch_path, "r", encoding="utf-8") as file:
    j2ch = json.load(file)

with open(c_word_path, "r", encoding="utf-8") as file:
    c_words = [json.loads(line) for line in file]

with open(jmdict_file_path, "r", encoding="utf-8") as file:
    jmdict = json.load(file)["words"]

    for entry in jmdict:
        # I want to check for every entry that has non common kanji representations
        # Are they in the c_words?

        if 'kanji' in entry:
            for kanji in entry['kanji']:
                if kanji['common'] == False:
                    # candidate

         
                    
'''
