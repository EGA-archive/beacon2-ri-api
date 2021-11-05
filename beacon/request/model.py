from dataclasses import dataclass
from strenum import StrEnum
from typing import List, Union
from dataclasses_json import dataclass_json, LetterCase
from beacon import conf


class IncludeResultsetResponses(StrEnum):
    ALL = "ALL",
    HIT = "HIT",
    MISS = "MISS",
    NONE = "NONE"


class Similarity(StrEnum):
    EXACT = "exact",
    HIGH = "high",
    MEDIUM = "medium",
    LOW = "low"


class Operator(StrEnum):
    EQUAL = "=",
    LESS = "<",
    GREATER = ">",
    NOT = "!",
    LESS_EQUAL = "<=",
    GREATER_EQUAL = ">="


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OntologyFilter:
    id: str
    scope: str = None
    include_descendant_terms: bool = True
    similarity: Similarity = Similarity.EXACT


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AlphanumericFilter:
    id: str
    value: str
    scope: str = None
    operator: str = "="


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CustomFilter:
    id: str
    scope: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Pagination:
    skip: int = 0
    limit: int = 10


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RequestMeta:
    requested_schemas: List[str]
    api_version: str = conf.api_version
    requested_granularity: str = conf.beacon_granularity


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RequestQuery:
    request_parameters: dict
    filters: List[Union[OntologyFilter, AlphanumericFilter, CustomFilter]]
    include_resultset_responses: IncludeResultsetResponses
    pagination: Pagination


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RequestParams:
    meta: RequestMeta
    query: RequestQuery
