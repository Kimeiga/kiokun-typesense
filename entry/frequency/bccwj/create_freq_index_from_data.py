import json
from entry.utils import get_j2ch_word
# module = __import__("kiokun-server.j2ch.utils", fromlist=["j2ch_get"])

# we want to also add in to each entry's information whether or not it is a chinese word or not
with open("entry/entry_data/entry_index_min.json", "r", encoding="utf-8") as file:
    entry_index = json.load(file)


def process_tsv_to_json(filepath):
    # Initialize an empty dictionary to hold our data
    data_dict = {}

    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file):
            # Skip first line
            if line_num == 0:
                continue

            fields = line.strip().split("\t")
            # Assuming 'lemma' is at index 2, 'lForm' at index 1, and 'frequency' at index 6
            lemma, lForm, frequency = fields[2], fields[1], fields[6]

            is_chinese = 0

            trad_words = get_j2ch_word(lemma, entry_index)

            if len(trad_words) > 1:
                print(trad_words)
                print(lemma)

            # if lemma == "図":
            #     print(lemma)
            #     print(trad_word)

            # # Check if the word is a chinese word
            # if trad_word in entry_index and 'c_w' in entry_index[trad_word] and 'j_w' in entry_index[trad_word]:
            #     is_chinese = 1

            # # Populate the dictionary
            # if lemma not in data_dict:
            #     data_dict[lemma] = {"p": lForm,
            #                         "f": frequency, 'i': is_chinese}

    # Convert the dictionary to a JSON string
    return data_dict


# Path to your TSV file
filepath = 'entry/frequency/bccwj/BCCWJ_frequencylist_luw2_ver1_0.tsv'

# Process the file and get the JSON output
json_data = process_tsv_to_json(filepath)


with open("index_key_search.jsonl", "w", encoding="utf-8") as file:
    for word, value in json_data.items():
        file.write(json.dumps(
            {'w': word, 'p': value['p'], 'f': int(value['f']), 'i': value['i']}, ensure_ascii=False) + "\n")
