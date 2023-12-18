from fire import Fire
from japanese_law_search.index import index_law
from japanese_law_search.search import search_law


class Index:
    def index(self, index_name: str = "ja_law", path: str = "./data", es_host = "http://localhost:9200/") -> None:
        return index_law(es_host=es_host, index_name=index_name, path=path)

    def search(
        self, index_name: str = "ja_law", keyword: str = "test", size: int = 10, es_host = "http://localhost:9200/"
    ) -> None:
        return search_law(es_host=es_host, index_name=index_name, keyword=keyword, size=size)


def main() -> None:
    Fire(Index)


if __name__ == "__main__":
    main()
