from dataclasses import dataclass
from enum import Enum


@dataclass
class Document:
    law_num: str
    law_title: str
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
