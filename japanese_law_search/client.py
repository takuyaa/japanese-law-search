from typing import Any, Optional
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch

from japanese_law_search.model import HitDoc, Response


class Client:
    def __init__(self, index: str, host: Optional[str], client: Optional[Elasticsearch] = None) -> None:
        if client is None:
            client = self.get_client(host=host)
        self._client = client
        self.index_name = index

    @staticmethod
    def get_client(host: str) -> Elasticsearch:
        return Elasticsearch(hosts=host)

    def index(self, id: str, document: dict) -> None:
        self._client.index(index=self.index_name, id=id, document=document)

    def bulk_index(self, ids: list[str], documents: list[dict]) -> None:
        actions = []
        for id, document in zip(ids, documents):
            actions.append({"index": {"_index": self.index_name, "_id": id}})
            actions.append(document)
        self._client.bulk(body=actions)

    def refresh(self) -> None:
        self._client.indices.refresh(index=self.index_name)

    def search(self, query: dict[str, Any], fields: list[str], highlight: dict[str, Any], size: int, knn: dict[str, Any]) -> Response:
        res: ObjectApiResponse[Any] = self._client.search(
            index=self.index_name,
            query=query,
            size=size,
            fields=fields,
            highlight=highlight,
            knn=knn,
        )
        total_hits = res["hits"]["total"]["value"]
        docs = []
        for hit in res["hits"]["hits"]:
            highlight = hit["highlight"] if "highlight" in hit else {}
            doc = HitDoc(
                id=hit["_id"],
                law_num=hit["fields"]["law_num.keyword"][0],
                law_title=hit["fields"]["law_title.keyword"][0],
                highlight=highlight,
            )
            docs.append(doc)
        return Response(total_hits=total_hits, docs=docs)
