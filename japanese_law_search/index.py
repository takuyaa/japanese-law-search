from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Generator, Protocol

from tqdm import tqdm

from ja_law_parser.model import Law
from ja_law_parser.parser import LawParser
from japanese_law_search.client import Client
from japanese_law_search.model import Document


def index_law(es_host: str, index_name: str, path: str) -> None:
    parser = LawParser()
    client = Client(index=index_name,host=es_host)

    print(f"Indexing laws to index {index_name}")
    files = [str(file) for file in Path(path).glob("**/*.xml")]
    for file in tqdm(iterable=files):
        file_name = Path(file).stem

        enforce_date = date.fromisoformat(file_name.split(sep="_")[1])
        today = date.today()
        if today < enforce_date:
            continue

        try:
            law: Law = parser.parse(path=file)
            document = Document(
                law_num=law.law_num,
                law_title=text_or_none(law.law_body.law_title),
                enact_statement=text_or_none(law.law_body.enact_statement),
                main_provision=texts_or_none(law.law_body.main_provision),
            )
            client.index(
                id=Path(file).stem,
                document=asdict(document),
            )
        except Exception as e:
            print(file)
            raise e

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
