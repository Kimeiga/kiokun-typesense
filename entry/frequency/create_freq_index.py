import json
import os

# with open("entry/entry_data/entry_index_min.json", "r", encoding="utf-8") as file:
#     index = json.load(file)

output_folder = "entry_data"

# add info from freq dataset
print(os.getcwd())


# Open the CSV file
with open('./jp_word_to_freq.csv', 'r') as file:
    # Read the CSV data
    csv_data = file.read()

# Split the data into lines
lines = csv_data.strip().split('\n')

# Extract the first and last element from each line
extracted_words = [line.split(',')[0] for line in lines]

extracted_word_pronunciations = [line.split(',')[-2] for line in lines]
extracted_word_freqs = [line.split(',')[-1] for line in lines]

words = {}

for i, word in enumerate(extracted_words):
    if word in words:
        print(word)
    words[word] = {"pronunciation":  extracted_word_pronunciations[i],
                   "freq": int(extracted_word_freqs[i])}

# duplicates = [
#     word for word in extracted_words if extracted_words.count(word) > 1]
# print(duplicates)


# print(len(extracted_words) == len(set(extracted_words)))
# print(len(extracted_words) == len(set(extracted_words)))

# # print(extracted_words)
# # print(extracted_word_freqs)

# longest = ''
# longest_len = 0

# for i, word in enumerate(extracted_words):
#     if word in index:
#         index[word]['f'] = int(extracted_word_freqs[i])

# for i in index:
#     if 'c_w' in index[i] and 'j_w' in index[i] and len(index[i]['c_w']) > 0 and len(index[i]['j_w']) > 0:
#         # mark ones that are in both languages
#         index[i]['i'] = 1

#         if len(i) > longest_len:
#             longest = i
#             longest_len = len(i)
#     else:
#         index[i]['i'] = 0

# print(longest, longest_len)

# with open("index_key_search.jsonl", "w", encoding="utf-8") as file:
#     for i, entry in index.items():
#         file.write(json.dumps({'w': i, 'i': entry['i'], 'f': (
#             entry['f'] if 'f' in entry else 0)}, ensure_ascii=False) + "\n")
#     # json.dump([{'w': i} for i in index.keys()],
#         #   file, ensure_ascii=False, indent=2)
