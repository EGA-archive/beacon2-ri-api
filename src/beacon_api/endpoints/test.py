import logging

from aiohttp import web

from ..validation.request import RequestParameters
from ..validation.fields import Field, RegexField, ChoiceField, IntegerField, ListField, DatasetIdsField

LOG = logging.getLogger(__name__)

class TestParameters(RequestParameters):
    param1 = ChoiceField("1", "2", "3", required=True)
    hello = Field(default="You")
    int1 = IntegerField(min_value=0)
    int2 = IntegerField(min_value=0)
    regex = RegexField(r'^([ABCD]+)$')
    # datasetIds = ListField(items=RegexField(r'^[^<>"/;%{}+=]*$'))
    datasetIds = DatasetIdsField()
    includeDatasetResponses = ChoiceField("ALL", "HIT", "MISS", "NONE", default="NONE")
    filters = ListField(items=RegexField(r'.*:.+=?>?<?[0-9]*$'))

proxy = TestParameters()

async def test(request):

    LOG.info('Running a test request')
    qparams_org, qparams_db = await proxy.fetch(request)

    print('{:-^50}'.format(" Query Parameters for DB "))
    for key in proxy.__keys__:
        val = getattr(qparams_db, key)
        t = ' ' if val is None else str(type(val))
        print(f"{key:>30} : {str(val):<8} {t}")

    return web.Response(text=f"\nHello, {qparams_db.hello}\n")

# @validate("test")
# async def test(method, query_parameters, request):
#     db_pool = request.app['pool']

#     raise web.HTTPBadRequest(reason='Marta is tired now')

#     LOG.info("This is the %s query parameters: %s", method, query_parameters)

#     def log_listener(c,m):
#         print('------------', m)

#     async with db_pool.acquire(timeout=180) as connection:

#         connection.add_log_listener(log_listener)
#         # query = f"""SELECT * FROM {__DB_SCHEMA__}.query_data_summary_response(
# 	# $1::text,
# 	# $2::integer,
# 	# $3::integer,
# 	# $4::integer,
# 	# $5::integer,
# 	# $6::integer,
# 	# $7::integer,
# 	# $8::varchar,
# 	# $9::text,
# 	# $10::text,
# 	# $11::text,
# 	# $12::text,
# 	# $13::text);"""
#         query = f"""SELECT * FROM {conf.database_schema}.query_data_summary_response({create_prepstmt_variables(13)});"""
#         values = [None, 2655179, None, None, None, None, None, '7', 'G', 'A', 'GRCh37', '1,2,3,4', None]

#         # query = f"""SELECT * from public.test_marta($1::varchar, $2::text);"""
#         # values = [query_parameters.get('referenceBases'), query_parameters.get('toto')]

#         LOG.debug("QUERY to fetch hits: %s", query)
#         statement = await connection.prepare(query)
#         print(statement)
#         db_response = await statement.fetch(*values)

#         if db_response:
#             print("------------------ SPARTA")
#             return web.json_response([])

#         response = [record for record in db_response]
#         return web.json_response(response)
