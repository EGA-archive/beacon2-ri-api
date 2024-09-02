import logging
from typing_extensions import Self
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
    Field,
    PrivateAttr)
from strenum import StrEnum
from typing import List, Optional, Union
from beacon import conf
from humps.main import camelize
from aiohttp.web_request import Request
from aiohttp import web
import html

LOG = logging.getLogger(__name__)


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


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

class Granularity(StrEnum):
    BOOLEAN = "boolean",
    COUNT = "count",
    RECORD = "record"

class OntologyFilter(CamelModel):
    id: str
    scope: Optional[str] = None
    include_descendant_terms: bool = False
    similarity: Similarity = Similarity.EXACT


class AlphanumericFilter(CamelModel):
    id: str
    value: Union[str, int, List[int]]
    scope: Optional[str] = None
    operator: Operator = Operator.EQUAL


class CustomFilter(CamelModel):
    id: str
    scope: Optional[str] = None


class Pagination(CamelModel):
    skip: int = 0
    limit: int = 10


class RequestMeta(CamelModel):
    requested_schemas: List[str] = []
    api_version: str = conf.api_version


class RequestQuery(CamelModel):
    filters: List[dict] = []
    include_resultset_responses: IncludeResultsetResponses = IncludeResultsetResponses.HIT
    pagination: Pagination = Pagination()
    request_parameters: Union[list,dict] = {}
    test_mode: bool = False
    requested_granularity: Granularity = Granularity(conf.default_beacon_granularity)
    scope: str = None


class RequestParams(CamelModel):
    meta: RequestMeta = RequestMeta()
    query: RequestQuery = RequestQuery()

class SequenceQuery(BaseModel):
    referenceName: Union[str,int]
    start: Union[int, str]
    alternateBases:str
    referenceBases: str
    clinicalRelevance: Optional[str] =None
    mateName: Optional[str] =None
    assemblyId: Optional[str] =None

class RangeQuery(BaseModel):
    referenceName: Union[str,int]
    start: Union[int, str, list]
    end: Union[int, str, list]
    variantType: Optional[str] =None
    alternateBases: Optional[str] =None
    aminoacidChange: Optional[str] =None
    variantMinLength: Optional[int] =None
    variantMaxLength: Optional[int] =None
    clinicalRelevance: Optional[str] =None
    mateName: Optional[str] =None
    assemblyId: Optional[str] =None

class GeneIdQuery(BaseModel):
    geneId: str
    variantType: Optional[str] =None
    alternateBases: Optional[str] =None
    aminoacidChange: Optional[str] =None
    variantMinLength: Optional[int] =None
    variantMaxLength: Optional[int] =None
    assemblyId: Optional[str] =None

class BracketQuery(BaseModel):
    referenceName: Union[str,int]
    start: list
    end: list
    variantType: Optional[str] =None
    clinicalRelevance: Optional[str] =None
    mateName: Optional[str] =None
    assemblyId: Optional[str] =None
    @field_validator('start')
    @classmethod
    def start_must_be_array_of_integers(cls, v: list) -> list:
        for num in v:
            if isinstance(num, int):
                pass
            else:
                raise ValueError
    @field_validator('end')
    @classmethod
    def end_must_be_array_of_integers(cls, v: list) -> list:
        for num in v:
            if isinstance(num, int):
                pass
            else:
                raise ValueError

class GenomicAlleleQuery(BaseModel):
    genomicAlleleShortForm: str
    assemblyId: Optional[str] =None

class AminoacidChangeQuery(BaseModel):
    aminoacidChange: str
    geneId: str
    assemblyId: Optional[str] =None

class RequestParams(CamelModel):
    meta: RequestMeta = RequestMeta()
    query: RequestQuery = RequestQuery()

    def from_request(self, request: Request) -> Self:
        request_params={}         
        for k, v in request.query.items():
            if k == "requestedSchema":
                self.meta.requested_schemas = [html.escape(v)] # comprovar si és la sanitització recomanada
            elif k == "skip":
                self.query.pagination.skip = int(html.escape(v))
            elif k == "limit":
                self.query.pagination.limit = int(html.escape(v))
            elif k == "includeResultsetResponses":
                self.query.include_resultset_responses = IncludeResultsetResponses(html.escape(v))
            elif k == 'filters':
                self.query.request_parameters[k] = html.escape(v)
            elif k in ["start", "end", "assemblyId", "referenceName", "referenceBases", "alternateBases", "variantType","variantMinLength","variantMaxLength","geneId","genomicAlleleShortForm","aminoacidChange","clinicalRelevance", "mateName"]:
                try:
                    if ',' in v:
                        v_splitted = v.split(',')
                        request_params[k]=[int(v) for v in v_splitted]
                    else:
                        request_params[k]=int(v)
                except Exception as e:
                    request_params[k]=v
                self.query.request_parameters[k] = html.escape(v)
            else:
                raise web.HTTPBadRequest(text='request parameter introduced is not allowed')
        if request_params != {} or self.query.request_parameters != {}:
            request_params = self.query.request_parameters
            try:
                RangeQuery(**request_params)
                return self
            except Exception as e:
                LOG.debug('holaaaaaa')
                pass
            try:
                SequenceQuery(**request_params)
                return self
            except Exception as e:
                pass
            try:
                BracketQuery(**request_params)
                return self
            except Exception as e:
                pass
            try:
                GeneIdQuery(**request_params)
                return self
            except Exception as e:
                pass
            try:
                AminoacidChangeQuery(**request_params)
                return self
            except Exception as e:
                pass
            try:
                GenomicAlleleQuery(**request_params)
                return self
            except Exception as e:
                pass
            raise web.HTTPBadRequest(text='set of parameters not allowed')
        return self

    def summary(self):
        list_of_filters=[]
        for item in self.query.filters:
            for k,v in item.items():
                if v not in list_of_filters:
                    list_of_filters.append(v)
        #reqparams=self.query.request_parameters
        #del reqparams["filters"]
        return {
            "apiVersion": self.meta.api_version,
            "requestedSchemas": self.meta.requested_schemas,
            "filters": list_of_filters,
            "requestParameters": self.query.request_parameters,
            "includeResultsetResponses": self.query.include_resultset_responses,
            "pagination": self.query.pagination.dict(),
            "requestedGranularity": self.query.requested_granularity,
            "testMode": self.query.test_mode
        }
