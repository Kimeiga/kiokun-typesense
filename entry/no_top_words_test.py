import json
import typesense

with open('entry_data/entry_index_min.json', 'r', encoding='utf-8') as file:
    index = json.load(file)

with open('list_of_no_top_words_characters.json', 'r', encoding='utf-8') as file:
    no_top_words_characters = json.load(file)


client = typesense.Client({
    'nodes': [{
        'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
        'port': '8108',      # For Typesense Cloud use 443
        'protocol': 'http'   # For Typesense Cloud use https
    }],
    'api_key': 'GSV3UjDj0By3HYzmgWSiCsprcn7khNRY3EVyVfHcOXOMaV3y',
    'connection_timeout_seconds': 2
})


def fetch_all_documents(collection_name, search_parameters):
    all_documents = []
    page = 1
    per_page = 50  # Adjust based on your needs and Typesense limits

    while True:
        search_parameters['per_page'] = per_page
        search_parameters['page'] = page
        response = client.collections[collection_name].documents.search(
            search_parameters)
        hits = response['hits']

        if not hits:
            break

        all_documents.extend(hits)
        page += 1

    return all_documents


# for all kanji/hanzis add the words that they appear in, we can choose 'a' as in AppearsIn
for key, value in index.items():
    if len(key) == 1:
        # this is a hanzi/kanji
        # search typesense index dictionary to see everything
        search_parameters = {
            'q': key,
            'query_by': 'w',
            'infix': 'always'
        }

        all_results = fetch_all_documents('index', search_parameters)
        value['a'] = [item['document']['w'] for item in all_results]


for character in no_top_words_characters:
    search_parameters = {
        'q': character,
        'query_by': 'w',
        'infix': 'always'
    }

    all_results = fetch_all_documents('index', search_parameters)
    for item in all_results:
        if item['document']['w'] != character:
            print(item['document']['w'], character)

    # value['a'] = [item['document']['w'] for item in all_results]
