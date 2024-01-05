from japanese_law_search.client import Client
from japanese_law_search.model import Response
import japanese_law_search.sentents_bert as sentents_bert


def search_law(es_host: str, index_name: str, keyword: str, size: int) -> Response:
    client = Client(index=index_name, host=es_host)
    model = sentents_bert.SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens-v2")
    sentence_embeddings = model.encode([keyword]).cpu().detach().numpy()
    query = {
        "field": "law_title_embedding_512",
        "query_vector": sentence_embeddings[0].tolist(),
        "k": 10,
        "num_candidates": 100,
    }
    
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
        knn=query,
        size=size,
    )
