import json
import typesense

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
        'port': '8108',      # For Typesense Cloud use 443
        'protocol': 'http'   # For Typesense Cloud use https
    }],
    'api_key': 'GSV3UjDj0By3HYzmgWSiCsprcn7khNRY3EVyVfHcOXOMaV3y',
    'connection_timeout_seconds': 2
})


def get_words_with_kanji(word):

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

            if any(item['document']['i'] == 0 or item['document']['f'] == 0 for item in hits):
                # time to stop since we hit a word not in both languages
                break

        return all_documents

    search_parameters = {
        'q': word,
        'query_by': 'w',  # Removed 'f' from here
        # You can still sort by 'f'
        'sort_by': 'i:desc,f:desc',
        'infix': 'always'
    }

    # response = client.collections['index'].documents.search(
    #     search_parameters)
    # hits = response['hits']

    all_results = fetch_all_documents('index', search_parameters)

    words = [item['document'] for item in all_results]

    # print(json.dumps(words, ensure_ascii=False, indent=4, sort_keys=True))
    # print(len(words))

    search_parameters = {
        'q': word,
        'query_by': 'w',  # Removed 'f' from here
        # You can still sort by 'f'
        'sort_by': 'f:desc,i:desc',
        'infix': 'always'
    }

    all_results2 = fetch_all_documents('index', search_parameters)

    # print(json.dumps(all_results, ensure_ascii=False, indent=4, sort_keys=True))

    words2 = [item['document'] for item in all_results]

    # print(json.dumps(words2, ensure_ascii=False, indent=4, sort_keys=True))
    # print(len(words2))

    combined_words = words[:40] + words2[:40]

    # Use a dictionary to preserve order and remove duplicates
    deduplicated_words = list(
        {word['id']: word for word in combined_words}.values())

    # Print results
    # print(json.dumps(deduplicated_words, ensure_ascii=False, indent=4, sort_keys=True))
    # print(len(deduplicated_words))
    return deduplicated_words


def test():
    deduplicated_words = get_words_with_kanji('水')
    print(json.dumps(deduplicated_words, ensure_ascii=False, indent=4, sort_keys=True))
    print(len(deduplicated_words))


if __name__ == "__main__":
    test()
