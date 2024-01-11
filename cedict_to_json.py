# # Convert the processed data to JSON
# import json

# # Read the file and process the data into the specified JSON format
# file_path = "cedict_ts.u8"

# # Dictionary to store the processed entries
# entries = {}

# import romkan


# # Processing the file
# with open(file_path, "r", encoding="utf-8") as file:
#     for line in file:
#         # Skip comments and empty lines
#         if line.startswith("#") or not line.strip():
#             continue

#         # Split the line into components
#         parts = line.strip().split(" ")
#         traditional, simplified = parts[0], parts[1]

#         # Extracting pronunciation and definitions
#         remaining = " ".join(parts[2:])
#         pronunciation_start = remaining.find("[")
#         pronunciation_end = remaining.find("]")
#         pronunciation = remaining[pronunciation_start + 1 : pronunciation_end]

#         definitions = remaining[pronunciation_end + 2 :].strip("/").split("/")

#         # Process traditional entry if different
#         if traditional not in entries:
#             entries[traditional] = {
#                 "c": {
#                     "s": simplified,
#                     "t": traditional,
#                     "p": [pronunciation],
#                     "d": [definitions],
#                 }
#             }
#         else:
#             entries[traditional]["c"]["p"].append(pronunciation)
#             entries[traditional]["c"]["d"].append(definitions)

# # output to jsonl
# with open("cedict.jsonl", "w", encoding="utf-8") as file:
#     for entry in entries.values():
#         file.write(json.dumps(entry) + "\n")


import json


def parse_cedict_line(line):
    if line.startswith("#"):
        return None

    parts = line.strip().split(" ")
    traditional = parts[0]
    simplified = parts[1]

    # Extracting pronunciation and definitions
    remaining = " ".join(parts[2:])
    pronunciation_start = remaining.find("[")
    pronunciation_end = remaining.find("]")
    pronunciation = remaining[pronunciation_start + 1 : pronunciation_end]

    definitions = remaining[pronunciation_end + 2 :].strip("/").replace("|", " ")

    # rest = " ".join(parts[2:])
    # pinyin_start = rest.find("[")
    # pinyin_end = rest.find("]")
    # pinyin = rest[pinyin_start + 1 : pinyin_end]
    # definitions = rest[pinyin_end + 2 :].strip("/").split("/")
    return {
        "t": traditional,
        "s": simplified,
        "p": pronunciation,
        "d": definitions,
    }


def convert_cedict_to_jsonl(cedict_file_path, output_file_path):
    with open(cedict_file_path, "r", encoding="utf-8") as cedict_file, open(
        output_file_path, "w", encoding="utf-8"
    ) as output_file:
        for line in cedict_file:
            parsed_line = parse_cedict_line(line.strip())
            if parsed_line:
                json_line = json.dumps(parsed_line, ensure_ascii=False)
                output_file.write(json_line + "\n")


# Usage
convert_cedict_to_jsonl("cedict_ts.u8", "output.jsonl")
