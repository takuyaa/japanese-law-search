from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Generator, Protocol

from tqdm import tqdm

from ja_law_parser.model import Law
from ja_law_parser.parser import LawParser
from japanese_law_search.client import Client
from japanese_law_search.model import Document
import japanese_law_search.sentents_bert as sentents_bert


def index_law(es_host: str, index_name: str, path: str) -> None:
    batch_size = 32
    parser = LawParser()
    client = Client(index=index_name,host=es_host)

    print(f"Indexing laws to index {index_name}")
    files = [str(file) for file in Path(path).glob("**/*.xml")]
    model = sentents_bert.SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens-v2")
    for batch_files in tqdm(iterable=[files[i : i + batch_size] for i in range(0, len(files), batch_size)]):
        law_titles = []
        ids = [Path(file).stem for file in batch_files]
        documents = []
        for file in batch_files:
            file_name = Path(file).stem
            enforce_date = date.fromisoformat(file_name.split(sep="_")[1])
            today = date.today()
            if today < enforce_date:
                continue
            try:
                law: Law = parser.parse(path=file)
                law_title = text_or_none(law.law_body.law_title)
                law_titles.append(law_title if law_title is not None else "")
                document = Document(
                    law_num=law.law_num,
                    law_title=law_title,
                    law_title_embedding_512=None,
                    enact_statement=text_or_none(law.law_body.enact_statement),
                    main_provision=texts_or_none(law.law_body.main_provision),
                )
                documents.append(document)
            except Exception as e:
                raise e
        sentence_embeddings = model.encode(law_titles, batch_size=batch_size).cpu().detach().numpy()
        for document, sentence_embedding in zip(documents, sentence_embeddings):
            document.law_title_embedding_512 = sentence_embedding.tolist()
        client.bulk_index(ids=ids, documents=[asdict(document) for document in documents])

    client.refresh()


class Text(Protocol):
    @property
    def text(self) -> str:
        ...


class Texts(Protocol):
    def texts(self) -> Generator[str, None, None]:
        ...


def text_or_none(obj: Text | None) -> str | None:
    if obj is None:
        return None
    return obj.text


def texts_or_none(obj: Texts | None) -> str | None:
    if obj is None:
        return None
    return " ".join(obj.texts())
