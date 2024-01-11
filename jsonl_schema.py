import json
import sys


def analyze_jsonl_schema(file_path):
    properties_types = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            json_obj = json.loads(line)
            for key, value in json_obj.items():
                value_type = type(value).__name__
                if key not in properties_types:
                    properties_types[key] = set()
                properties_types[key].add(value_type)

    return properties_types


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path_to_jsonl_file")
        sys.exit(1)

    file_path = sys.argv[1]
    properties = analyze_jsonl_schema(file_path)

    for prop, types in properties.items():
        print(f"{prop}: {', '.join(types)}")
