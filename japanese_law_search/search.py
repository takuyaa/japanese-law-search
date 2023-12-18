from japanese_law_search.client import Client
from japanese_law_search.model import Response


def search_law(es_host: str, index_name: str, keyword: str, size: int) -> Response:
    client = Client(index=index_name, host=es_host)
    return client.search(
        query={
            "multi_match": {
                "query": keyword,
                "type": "phrase",
                "fields": ["law_num", "law_title", "main_provision"],
            }
        },
        fields=["law_num.keyword", "law_title.keyword"],
        highlight={
            "fields": {"*": {"pre_tags": [" **"], "post_tags": ["** "]}},
            "number_of_fragments": 1,
        },
        size=size,
    )
