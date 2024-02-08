import json

a = "possessive, adjectival suffix/of/~'s (possessive particle)/(used after an attribute)/(used to form a nominal expression)/(used at the end of a declarative sentence for emphasis)"

# output this to json file

with open("test_1_string.json", "w", encoding="utf-8") as file:
    json.dump({'a': a}, file, ensure_ascii=False)

with open("test_array.json", "w", encoding="utf-8") as file:
    json.dump({'a': [el for el in a.split('/')]}, file, ensure_ascii=False)
