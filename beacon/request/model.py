from dataclasses import dataclass, field
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
    operator: Operator = Operator.EQUAL


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
    requested_schemas: List[str] = field(default_factory=list)
    api_version: str = conf.api_version


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RequestQuery:
    filters: List[Union[OntologyFilter, AlphanumericFilter, CustomFilter]] = field(default_factory=list)
    include_resultset_responses: IncludeResultsetResponses = IncludeResultsetResponses.HIT
    pagination: Pagination = field(default_factory=Pagination)
    request_parameters: dict = field(default_factory=dict)
    test_mode: bool = False
    requested_granularity: str = conf.beacon_granularity


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RequestParams:
    meta: RequestMeta = field(default_factory=RequestMeta)
    query: RequestQuery = field(default_factory=RequestQuery)
