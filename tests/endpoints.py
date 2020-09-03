import sys
import os

from aiohttp import ClientSession, BasicAuth, FormData

client_id = 'beacon'
client_secret = 'b26ca0f9-1137-4bee-b453-ee51eefbe7ba'
idp_token_endpoint = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token'

endpoints = [
    ('info'        , 'http://beacon:5050/api/info'),
    ('info_schema' , 'http://beacon:5050/api/info?requestedSchemasServiceInfo=ga4gh-service-info-v1.0'),
    ('service_info', 'http://beacon:5050/api/service-info'),
    ('info_model'  , 'http://beacon:5050/api/info?model=ga4gh-service-info-v1.0'),

    # Listing
    ('biosamples', 'http://beacon:5050/api/biosamples'),
    ('biosamples-1', 'http://beacon:5050/api/biosamples/SAMEA4806673'),
    ('biosamples-2', 'http://beacon:5050/api/biosamples/SAMEA4806673/individuals'),
    ('biosamples-3', 'http://beacon:5050/api/biosamples/SAMEA4806673/g_variants'),
    ('individuals', 'http://beacon:5050/api/individuals'),
    ('individuals-1', 'http://beacon:5050/api/individuals/NA24631'),
    ('individuals-2', 'http://beacon:5050/api/individuals/NA24631/biosamples'),
    ('individuals-3', 'http://beacon:5050/api/individuals/NA24631/g_variants'),
    ('gvariants', 'http://beacon:5050/api/g_variants'),
    ('gvariants-1', 'http://beacon:5050/api/g_variants/1'),
    ('gvariants-2', 'http://beacon:5050/api/g_variants/1/biosamples'),
    ('gvariants-3', 'http://beacon:5050/api/g_variants/1/individuals'),

    # Querying
    # Variants SNP query
    ('snp-gvariants', 'http://beacon:5050/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150&includeDatasetResponses=ALL'),
    # Biosamples by SNP
    ('snp-biosamples', 'http://beacon:5050/api/biosamples?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150'),
    # Individuals by SNP
    ('snp-individuals', 'http://beacon:5050/api/individuals?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150'),
    # Variants region query
    ('snp-region', 'http://beacon:5050/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&start=1&end=200'),
    
    # Filters
    ('filters-1', 'http://beacon:5050/api/individuals?filters=NCIT:C27083,PATO:0000383'), # no result
    ('filters-2', 'http://beacon:5050/api/individuals?filters=NCIT:C27083,PATO:0000384'), # 1 result
    ('filters-3', 'http://beacon:5050/api/individuals?filters=PATO:0000384'), # 2 results
    ('filters-4', 'http://beacon:5050/api/biosamples?filters=BTO:0000089'), # 3 results
    ('filters-5', 'http://beacon:5050/api/biosamples?filters=BTO:0000089,NCIT:C37967'), # 1 result

    # Other endpoints
    ('datasets', 'http://beacon:5050/api/datasets'),
    ('filtering_terms', 'http://beacon:5050/api/filtering_terms'),
]

endpoints_with_permissions = [
    ('gvariants-anonymous', None, None,
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21'),
    ('gvariants-john', 'john', 'john',
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21'),
    ('gvariants-jane', 'jane', 'jane',
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21'),
    #  unauthenticated user returns 2 rows, user john 8 rows, jane 4 rows

    # Filter by registered dataset
    ('datasets-registered-anonymous', None, None,
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered'),
    ('datasets-registered-john', 'john', 'john',
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered'),
    ('datasets-registered-jane', 'jane', 'jane',
     'http://beacon:5050/api/g_variants?start=9411318&end=9411338&assemblyId=grch37.p1&referenceName=21&datasetIds=dataset-registered'),
]

async def collect(dir_output):

    for output, endpoint in endpoints:

        print('Contacting', endpoint, file=sys.stderr)
        async with ClientSession() as session:
            async with session.get(endpoint, headers = { 'Accept': 'application/json' }) as resp:
                if resp.status > 200:
                    error = await resp.text()
                    print('Error', resp.status, ':', error, file=sys.stderr)
                    continue
            
                content = await resp.text()
                with open(os.path.join(dir_output, output + '.json'), 'w') as f:
                    if content: # handle empty responses
                        f.write(content)

async def collect_with_permissions(dir_output):

    for output, username, password, endpoint in endpoints_with_permissions:

        headers = { 'Accept': 'application/json' }

        if username:
            async with ClientSession() as session:
                params = { 'grant_type': 'password',
                           'username': username,
                           'password': password }

                async with session.post(idp_token_endpoint,
                                        auth=BasicAuth(client_id, password=client_secret),
                                        data=FormData(params, charset='UTF-8')
                ) as resp:
                    if resp.status > 200:
                        error = await resp.text()
                        print('Error getting a token for', john, ':', error, file=sys.stderr)
                        continue # next endpoint
                    content = await resp.json()
                    access_token = content.get('access_token')
                    if not access_token:
                        print('Error getting a token for', john, ':', error, file=sys.stderr)
                        continue # next endpoint

            headers['Authorization'] = 'Bearer ' + access_token

        print('Contacting', endpoint, file=sys.stderr)
        async with ClientSession() as session:
            async with session.get(endpoint, headers=headers) as resp:
                if resp.status > 200:
                    error = await resp.text()
                    print('Error', resp.status, ':', error, file=sys.stderr)
                    continue
            
                content = await resp.text()
                with open(os.path.join(dir_output, output + '.json'), 'w') as f:
                    if content:
                        f.write(content)


# curl -u 'beacon:b26ca0f9-1137-4bee-b453-ee51eefbe7ba' http://idp:8080/auth/realms/Beacon/protoc
# ol/openid-connect/token -X POST -d 'grant_type=password&username=john&password=john'

if __name__ == '__main__':
    import asyncio
    file_dir = os.path.dirname(os.path.realpath(__file__))
    dir_output = os.path.join(file_dir, 'responses')
    try:
        os.mkdir(dir_output)
    except FileExistsError as e:
        pass
    asyncio.run(collect(dir_output))
    asyncio.run(collect_with_permissions(dir_output))
