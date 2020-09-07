import asynctest
from unittest import mock

from beacon_api.utils.polyvalent_functions import filter_exists, fetch_datasets_access, prepare_filter_parameter

from .test_db_load import Connection


class TestPolyvalentFunctions(asynctest.TestCase):
    """Test Polyvalent Functions:
            filter_exists, prepare_filter_parameter, access_resolution, fetch_datasets_access"""

    # ------- Test basic functions ------- #

    def test_filter_exists(self):
        """Test filtering hits and miss datasets."""
        datasets = [{"exists": True, "name": "DATASET1"}, {"exists": False, "name": "DATASET2"}]
        hits = filter_exists("HIT", datasets)
        misses = filter_exists("MISS", datasets)
        all = filter_exists("ALL", datasets)
        nothing = filter_exists("NONE", datasets)
        self.assertEqual(hits, [{"exists": True, "name": "DATASET1"}])
        self.assertEqual(misses, [{"exists": False, "name": "DATASET2"}])
        self.assertEqual(all, datasets)
        self.assertEqual(nothing, [])

    # ------- Test access related functions ------- #

    async def test_datasets_access_call_public(self):
        """Test db call of getting public datasets access."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'access_type': 'PUBLIC', 'id': 'mock:public:id', 'stable_id': 'mock:public:stable_id'}])
        result = await fetch_datasets_access(pool, "null")

        self.assertEqual(result, (['mock:public:id'], [], []))

    async def test_datasets_access_call_registered(self):
        """Test db call of getting registered datasets access."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'access_type': 'REGISTERED', 'id': 'mock:registered:id', 'stable_id': 'mock:registered:stable_id'}])
        result = await fetch_datasets_access(pool, "null")

        self.assertEqual(result, ([], ['mock:registered:id'], []))

    async def test_datasets_access_call_controlled(self):
        """Test db call of getting controlled datasets access."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'access_type': 'CONTROLLED', 'id': 'mock:controlled:id', 'stable_id': 'mock:controlled:stable_id'}])
        result = await fetch_datasets_access(pool, "null")

        self.assertEqual(result, ([], [], ['mock:controlled:id']))

    async def test_datasets_access_call_multiple(self):
        """Test db call of getting controlled and public datasets access."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'access_type': 'CONTROLLED', 'id': 'mock:controlled:id', 'stable_id': 'mock:controlled:stable_id'},
                                                                        {'access_type': 'PUBLIC', 'id': 'mock:public:id', 'stable_id': 'mock:public:stable_id'}])
        result = await fetch_datasets_access(pool, "null")

        self.assertEqual(result, (['mock:public:id'], [], ['mock:controlled:id']))

    # ------- Test filtering terms management ------- #

    async def test_prepare_filter_parameter(self):
        """Test the parsing of the filters parameter from the request."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'column_name': 'technology', 'column_value': 'Illumina Genome Analyzer II'},
                                                                        {'column_name': 'technology', 'column_value': 'Illumina HiSeq 2000'}])

        filters_request = "['ega.dataset.technology:3', 'ega.dataset.technology:4']"
        result = await prepare_filter_parameter(pool, filters_request)
        self.assertEqual(result, "(technology)::jsonb ?& array['Illumina Genome Analyzer II', 'Illumina HiSeq 2000']")




if __name__ == '__main__':
    asynctest.main()