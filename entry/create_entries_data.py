import process_zh_chars
import process_zh_words
import process_jp_words
import process_jp_chars
import process_jp_names
import process_char_in_word
import os
import json
from collections import defaultdict

from entry.frequency.get_words_with_kanji import get_words_with_kanji

import os
import sys

# Absolute path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Now you can use relative imports as if you executed the script from its own directory


# map of word/char string to list of indices and raw kanji/hanzi data
index = defaultdict(lambda: defaultdict(list))

# words from dong-chinese (cedict)
c_word_entries = {}

# words from jmdict
j_word_entries = {}

# words from jmnedict
n_word_entries = {}


if __name__ == "__main__":
    process_zh_words.process(index, c_word_entries)
    process_zh_chars.process(index, c_word_entries)
    process_jp_words.process(index, j_word_entries)
    process_jp_chars.process(index, j_word_entries)
    process_jp_names.process(index, n_word_entries)
    process_char_in_word.process(
        index, c_word_entries, j_word_entries, n_word_entries)

    # make new folder to put everything called entry_data
    output_folder = "entry_data"

    # make the directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # output all files for the server script to use to serve data to /word
    with open(os.path.join(output_folder, "entry_index_min.json"), "w", encoding="utf-8") as file:
        json.dump(index, file, ensure_ascii=False, separators=(',', ':'))

    with open(os.path.join(output_folder, "c_word_entries_min.json"), "w", encoding="utf-8") as file:
        json.dump(c_word_entries, file, ensure_ascii=False,
                  separators=(',', ':'))

    with open(os.path.join(output_folder, "j_word_entries_min.json"), "w", encoding="utf-8") as file:
        json.dump(j_word_entries, file, ensure_ascii=False,
                  separators=(',', ':'))

    with open(os.path.join(output_folder, "n_word_entries_min.json"), "w", encoding="utf-8") as file:
        json.dump(n_word_entries, file, ensure_ascii=False,
                  separators=(',', ':'))

    # for debugging
    with open(os.path.join(output_folder, "entry_index.json"), "w", encoding="utf-8") as file:
        json.dump(index, file, ensure_ascii=False, indent=2)

    with open(os.path.join(output_folder, "c_word_entries.json"), "w", encoding="utf-8") as file:
        json.dump(c_word_entries, file, ensure_ascii=False, indent=2)

    with open(os.path.join(output_folder, "j_word_entries.json"), "w", encoding="utf-8") as file:
        json.dump(j_word_entries, file, ensure_ascii=False, indent=2)

    with open(os.path.join(output_folder, "n_word_entries.json"), "w", encoding="utf-8") as file:
        json.dump(n_word_entries, file, ensure_ascii=False, indent=2)

# we want to make a search json for finding usage of kanjis in words in chinese and japanese...
# in order to do this, we need to use the keys of the index as keys, and have some indication if
# they are in japanese and/or chinese, just so that we can look them up efficiently...

# actually it would be good to precompute all this data too, but i was just thinking typesense
# would be a good way to get the lists

# so on each character entry there could be 3 top level arrays: jw, cw, jcw (japanese words that
# use this character, chinese words that use this character, words in both languages that use
# this character )

# and we would need to use traditional chinese representation of these words remember, since that's
# the key (i guess technically for jw's they will be using japanese shinjitai since it's determined)
# that they aren't in chinese...

# to do this we just need to put a list of all the words in typesense, that should be all the keys

# so i will just make that at the bottom of here:

# with open(os.path.join(output_folder, "index_key_search.jsonl"), "w", encoding="utf-8") as file:
#     for i in index:
#         file.write(json.dumps({'w': i}, ensure_ascii=False) + "\n")
#     # json.dump([{'w': i} for i in index.keys()],
#         #   file, ensure_ascii=False, indent=2)
