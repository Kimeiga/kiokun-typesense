import typesense


def process(index, c_word_entries, j_word_entries, n_word_entries):
    # At this point we need to compute for all japanese words, japanese names, chinese words: all substrings with length > 1 that are in the index
    # since we need to serve them on demand

    for key, value in index.items():
        list_of_valid_substrings = [key[i:j] for i in range(len(key))
                                    for j in range(i + 1, len(key) + 1) if key[i:j] in index and len(key[i:j]) > 1 and (i != 0 and j != len(key))]
        if len(list_of_valid_substrings):
            value['s'] = list_of_valid_substrings

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
