import asynctest
from unittest import mock

from beacon_api.api.query import get_datasets
from beacon_api.api.genomic_query import get_datasets as get_datasets_region
from beacon_api.api.query import fetch_resulting_datasets
from beacon_api.api.genomic_query import fetch_resulting_datasets as fetch_resulting_datasets_region
from beacon_api.api.access_levels import special_datasets

from .test_db_load import Connection


class TestGetDataFunctions(asynctest.TestCase):
    """Test Functions related to fetching the results:
            get_datasets, fetch_resulting_datasets
        Those two functions are the same for the query and the genomic_snp endpoints, but not for the genomic_regions"""
    
    # ------- Test get_datasets ------- #

    @asynctest.mock.patch('beacon_api.api.query.fetch_resulting_datasets')
    async def test_get_datasets_query(self, mock_filtered):
        """Test find datasets."""
        mock_filtered.return_value = []
        query_parameters =  ['null', 53077410, None, None, None, None, None, '19', 'T', 'C', 'GRCh37', '21,20', "(technology)::jsonb ?& array['Illumina Genome Analyzer II', 'Illumina HiSeq 2000']"]
        result = await get_datasets(None, query_parameters, "NONE")
        self.assertEqual(result, [])
        # setting ALL should cover MISS call as well
        result_all = await get_datasets(None, query_parameters, "ALL")
        self.assertEqual(result_all, [])

    @asynctest.mock.patch('beacon_api.api.genomic_query.fetch_resulting_datasets')
    async def test_get_datasets_region(self, mock_filtered):
        """Test find datasets."""
        mock_filtered.return_value = []
        query_parameters =  ['null', 53077410, None, None, None, None, None, '19', 'T', 'C', 'GRCh37', '21,20', "(technology)::jsonb ?& array['Illumina Genome Analyzer II', 'Illumina HiSeq 2000']"]
        result = await get_datasets_region(None, query_parameters, "NONE")
        self.assertEqual(result, [])
        # setting ALL should cover MISS call as well
        result_all = await get_datasets_region(None, query_parameters, "ALL")
        self.assertEqual(result_all, [])

    # ------- Test fetch_resulting_datasets ------- #

    async def test_fetch_resulting_datasets_call(self):
        """Test db call for retrieving main data."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection()
        # for now it can return empty dataset
        # in order to get a response we will have to mock it
        # in Connection() class
        query_parameters =  ['null', 53077410, None, None, None, None, None, '19', 'T', 'C', 'GRCh37', '21,20', "(technology)::jsonb ?& array['Illumina Genome Analyzer II', 'Illumina HiSeq 2000']"]
    
        result = await fetch_resulting_datasets(pool, query_parameters)
        self.assertEqual(result, [])
        result_miss = await fetch_resulting_datasets(pool, query_parameters)
        self.assertEqual(result_miss, [])

    async def test_fetch_resulting_datasets_call_region(self):
        """Test db call for retrieving main data."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection()
        # for now it can return empty dataset
        # in order to get a response we will have to mock it
        # in Connection() class
        query_parameters =  ['null', 53077410, None, None, None, None, None, '19', 'T', 'C', 'GRCh37', '21,20', "(technology)::jsonb ?& array['Illumina Genome Analyzer II', 'Illumina HiSeq 2000']"]
    
        result = await fetch_resulting_datasets_region(pool, query_parameters)
        self.assertEqual(result, [])
        result_miss = await fetch_resulting_datasets_region(pool, query_parameters)
        self.assertEqual(result_miss, [])

    # ------- Test special access levels function ------- #

    async def test_special_access_levels(self):
        """Test db call of getting datasets with special access levels."""
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData=[{'stable_id': 'dataset1', 'parent_field': 'accessLevelSummary', 'field': '-', 'access_level': 'PUBLIC'},
                                                                        {'stable_id': 'dataset1', 'parent_field': 'beaconOrganization', 'field': 'accessLevelSummary', 'access_level': 'CONTROLLED'},
                                                                        {'stable_id': 'dataset2', 'parent_field': 'beaconDataset', 'field': 'id', 'access_level': 'REGISTERED'},
                                                                        {'stable_id': 'dataset2', 'parent_field': 'beaconDataset', 'field': 'description', 'access_level': 'REGISTERED'}])
        simple_datasets, datasets = await special_datasets(pool)
        print(simple_datasets)
        print(datasets)
        datasets_correct_result = {
            'dataset1': {
                'beaconOrganization': {'accessLevelSummary': 'CONTROLLED'}
            },
            'dataset2': {
                'beaconDataset': {'id': 'REGISTERED',
                                  'description': 'REGISTERED'}
            }
        }
        self.assertEqual(datasets, datasets_correct_result)

        simple_datasets_correct_result = {
            'dataset1': 'PUBLIC'
        }
        self.assertEqual(simple_datasets, simple_datasets_correct_result)


if __name__ == '__main__':
    asynctest.main()