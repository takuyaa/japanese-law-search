from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Document:
    law_num: str
    law_title: str
    law_title_embedding_512: Optional[list[float]]
    enact_statement: str
    main_provision: str


@dataclass
class HitDoc:
    id: str
    law_num: str
    law_title: str
    highlight: dict[str, list[str]]


@dataclass
class Response:
    total_hits: int
    docs: list[HitDoc]
