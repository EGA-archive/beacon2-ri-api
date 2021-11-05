import json

import asyncpg
import asynctest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from beacon_api.app import init

# from test.support import EnvironmentVarGuard


PARAMS = {'assemblyId': 'GRCh37',
          'referenceName': '19',
          'start': 53077410, 
          'referenceBases': 'T', 
          'alternateBases': 'C'} 




async def create_db_mock(app):
    """Mock the db connection pool."""
    app['pool'] = asynctest.mock.Mock(asyncpg.create_pool())
    return app


async def mock_parse_request_object(request):
    """Mock parse request object."""
    return 'GET', json.dumps(PARAMS)

async def mock_special_dataset(pool):
    """ Mock special datasets"""
    return {}, {}

async def mock_fetch_services(pool, request):
    """ Mock fetch services"""
    return {}




class AppTestEndpointsSyntax(AioHTTPTestCase):
    """Test for Web app.

    Testing web app endpoints.
    """

    @asynctest.mock.patch('beacon_api.app.initialize', side_effect=create_db_mock)
    async def get_application(self, pool_mock):
        """Retrieve web Application for test."""
        return await init()


    #-----------------------------
    #       INFO ENDPOINT
    #-----------------------------
    @unittest_run_loop
    async def test_info(self):
        """Test the info endpoint.

        The status should always be 200.
        """
        with asynctest.mock.patch('beacon_api.app.info_handler', side_effect={"smth": "value"}):
            resp = await self.client.request("GET", "/")
        assert 200 == resp.status


    @unittest_run_loop
    async def test_post_info(self):
        """Test the info endpoint with POST.

        The status should always be 405.
        """
        resp = await self.client.request("POST", "/")
        assert 405 == resp.status


    #-----------------------------
    #  FILTERTING TERMS ENDPOINT
    #-----------------------------
    @unittest_run_loop
    async def test_filtering_terms(self):
        """Test the filtering terms endpoint.

        The status should always be 200.
        """
        with asynctest.mock.patch('beacon_api.app.filtering_terms_handler', side_effect={"smth": "value"}):
            resp = await self.client.request("GET", "/filtering_terms")
        assert 200 == resp.status
    
    @unittest_run_loop
    async def test_post_filtering_terms(self):
        """Test the filtering terms endpoint with POST.

        The status should always be 405.
        """
        resp = await self.client.request("POST", "/filtering_terms")
        assert 405 == resp.status

    #-----------------------------
    #  SERVICES ENDPOINT
    #----------------------------- 
    @asynctest.mock.patch('beacon_api.api.services.fetch_filtered_services', side_effect=mock_fetch_services)
    @unittest_run_loop
    async def test_services(self, mock_fetch):
        """Test the services endpoint.

        The status should always be 200.
        """
        resp = await self.client.request("GET", "/services")
        assert 200 == resp.status
    
    @asynctest.mock.patch('beacon_api.api.services.fetch_filtered_services', side_effect=mock_fetch_services)
    @unittest_run_loop
    async def test_post_services(self, mock_fetch):
        """Test the services endpoint with POST.
        """
        PARAMS = {} 
        resp = await self.client.request("POST", "/services", data=json.dumps(PARAMS))
        assert 200 == resp.status  

    @asynctest.mock.patch('beacon_api.api.services.fetch_filtered_services', side_effect=mock_fetch_services)
    @unittest_run_loop
    async def test_request_services(self, mock_fetch):
        """Test the services endpoint with POST.
        """
        PARAMS = {'serviceType': 'GA4GHBeacon'} 
        resp = await self.client.request("POST", "/services", data=json.dumps(PARAMS))
        assert 200 == resp.status  
        PARAMS = {'apiVersion': 'v1.0'} 
        resp = await self.client.request("POST", "/services", data=json.dumps(PARAMS))
        assert 200 == resp.status  

    @asynctest.mock.patch('beacon_api.api.services.fetch_filtered_services', side_effect=mock_fetch_services)
    @unittest_run_loop
    async def test_badrequest_services(self, mock_fetch):
        """Test the services endpoint with POST.
        """
        PARAMS = {'wrong_parameter': 'test'}  
        resp = await self.client.request("POST", "/services", data=json.dumps(PARAMS))
        assert 400 == resp.status  


    #-----------------------------
    #   ACCESS LEVELS ENDPOINT
    #-----------------------------
    @asynctest.mock.patch('beacon_api.api.access_levels.special_datasets', side_effect=mock_special_dataset)
    @unittest_run_loop
    async def test_access_levels(self, mock_special):
        """Test the access levels endpoint.

        The status should always be 200.
        """
        resp = await self.client.request("GET", "/access_levels")
        assert 200 == resp.status
    
    @asynctest.mock.patch('beacon_api.api.access_levels.special_datasets', side_effect=mock_special_dataset)
    @unittest_run_loop
    async def test_correct_extended_access_levels(self, mock_special):
        PARAMS = {'includeFieldDetails': 'true'} 
        resp = await self.client.request("POST", "/access_levels", data=json.dumps(PARAMS))
        assert 200 == resp.status  

    @asynctest.mock.patch('beacon_api.api.access_levels.special_datasets', side_effect=mock_special_dataset)
    @unittest_run_loop
    async def test_badrequest2_extended_access_levels(self, mock_special):
        PARAMS = {'wrong_parameter': 'test'} 
        resp = await self.client.request("POST", "/access_levels", data=json.dumps(PARAMS))
        assert 400 == resp.status  

    #-----------------------------
    #       QUERY ENDPOINT
    #-----------------------------
    @unittest_run_loop
    async def test_empty_get_query(self):
        """Test empty GET query endpoint."""
        resp = await self.client.request("GET", "/query")
        assert 400 == resp.status

    @unittest_run_loop
    async def test_empty_post_query(self):
        """Test empty POST query endpoint."""
        resp = await self.client.request("POST", "/query", data=json.dumps({}))
        assert 400 == resp.status

    
    @asynctest.mock.patch('beacon_api.app.parse_request_object', side_effect=mock_parse_request_object)
    @asynctest.mock.patch('beacon_api.app.query_request_handler', side_effect=json.dumps(PARAMS))
    @unittest_run_loop
    async def test_valid_get_query(self, mock_handler, mock_object):
        """Test valid GET query endpoint."""
        params = '?assemblyId=GRCh38&referenceName=1&start=10000&referenceBases=A&alternateBases=T'
        with asynctest.mock.patch('beacon_api.app.initialize', side_effect=create_db_mock):
            resp = await self.client.request("GET", f"/query{params}")
        assert 200 == resp.status

    @asynctest.mock.patch('beacon_api.app.query_request_handler', side_effect=json.dumps(PARAMS))
    @unittest_run_loop
    async def test_valid_get_query2(self, mock_object):
        """Test valid GET query endpoint."""
        params = '?assemblyId=GRCh38&referenceName=1&start=10000&referenceBases=A&alternateBases=T'
        resp = await self.client.request("GET", f"/query{params}")
        assert 200 == resp.status

    @asynctest.mock.patch('beacon_api.app.parse_request_object', side_effect=mock_parse_request_object)
    @asynctest.mock.patch('beacon_api.app.query_request_handler', side_effect=json.dumps(PARAMS))
    @unittest_run_loop
    async def test_valid_post_query(self, mock_handler, mock_object):
        """Test valid POST query endpoint."""
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 200 == resp.status

    # ------- Test the different checks done in the futher validation ------- #

    ## All 'referenceName', 'referenceBases' and/or 'assemblyId' are required
    @unittest_run_loop
    async def test_requirements1(self):
        PARAMS = {'assemblyId': 'GRCh37',
                        'start': 53077410, 
                        'referenceBases': 'T', 
                        'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    @unittest_run_loop
    async def test_requirements2(self):
        PARAMS = {'referenceName': '19',
                        'start': 53077410, 
                        'referenceBases': 'T', 
                        'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status   

    @unittest_run_loop
    async def test_requirements3(self):
        PARAMS = {'assemblyId': 'GRCh37',
                        'referenceName': '19',
                        'start': 53077410, 
                        'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status        

    ## Either 'alternateBases' or 'variantType' is required
    @unittest_run_loop
    async def test_alterORvar_required(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'
    @unittest_run_loop
    async def test_varNOTalt(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'variantType': 'SNP',
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'start' is required if 'end' is provided
    @unittest_run_loop
    async def test_endANDstart(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'end': 53077410, 
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## Either 'start' or all of 'startMin', 'startMax', 'endMin' and 'endMax' are required
    @unittest_run_loop
    async def test_maxmincombo(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'endMin': 53077411,
                'endMax': 53077418,
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## All of 'startMin', 'startMax', 'endMin' and 'endMax' are required
    @unittest_run_loop
    async def test_maxminall(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'startMin': 53077410, 
                'endMin': 53077411,
                'endMax': 53077418,                
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'start' cannot be provided at the same time as 'startMin', 'startMax', 'endMin' and 'endMax'
    @unittest_run_loop
    async def test_notstart(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410,
                'startMin': 53077409,
                'startMax': 530774010,
                'endMin': 53077411,
                'endMax': 53077418,                 
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'referenceBases' cannot be 'N' if 'start' is provided and 'end' is missing
    @unittest_run_loop
    async def test_refbase_req(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'end' must be greater than 'start'
    @unittest_run_loop
    async def test_startendcombo(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'end': 53077400, 
                'referenceBases': 'T', 
                'alternateBases': 'C'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'endMin' must be smaller than 'endMax'
    @unittest_run_loop
    async def test_endminmaxcombo(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'startMin': 53077409,
                'startMax': 53077410,
                'endMin': 53077415,
                'endMax': 53077412,                 
                'referenceBases': 'T', 
                'alternateBases': 'C'}         
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## 'startMin' must be smaller than 'startMax'
    @unittest_run_loop
    async def test_startminmaxcombo(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'startMin': 53077410,
                'startMax': 53077409,
                'endMin': 53077411,
                'endMax': 53077418,                 
                'referenceBases': 'T', 
                'alternateBases': 'C'}         
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status    

    ## Queries using 'mateName' are not implemented
    @unittest_run_loop
    async def test_alterORvar_required(self):
        PARAMS = {'assemblyId': 'GRCh37',
                'referenceName': '19',
                'start': 53077410, 
                'referenceBases': 'T', 
                'alternateBases': 'C',
                'mateName': 'test'} 
        resp = await self.client.request("POST", "/query", data=json.dumps(PARAMS))
        assert 400 == resp.status
    

    # ------- Test different queries ? ------- #


