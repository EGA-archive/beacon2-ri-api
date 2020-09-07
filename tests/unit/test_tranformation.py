import asynctest
from unittest import mock

from beacon_api.api.query import transform_record, transform_misses
from beacon_api.api.genomic_query import transform_record as transform_record_region
from beacon_api.api.genomic_query import transform_misses as transform_misses_region

from .test_db_load import Connection


class Record:
    """Record Class.

    Mimic asyncpg Record object.
    """

    def __init__(self, datasetId=None, accessType=None, stableId=None, id=None, dataset_id=None, variant_cnt=0, call_cnt=0, sample_cnt=0, frequency=None, num_variants=0,
                 referenceBases=None, alternateBases=None, start=None, end=None, variantCount=0, variantType=None, variant_composite_id=None, chromosome=None, variant_id=None,
                 reference=None, alternate=None, variant_type=None, matching_sample_cnt=None):
        """Initialise things."""
        self.data = {}
        if datasetId:
            self.data["datasetId"] = datasetId
        if accessType:
            self.data["accessType"] = accessType
        if stableId:
            self.data["stableId"] = stableId
        if id:
            self.data["id"] = id
        if dataset_id:
            self.data["dataset_id"] = dataset_id
        if variant_cnt or variant_cnt == 0:
            self.data["variant_cnt"] = variant_cnt
        if call_cnt or call_cnt == 0:
            self.data["call_cnt"] = call_cnt
        if sample_cnt or sample_cnt == 0:
            self.data["sample_cnt"] = sample_cnt
        if frequency:
            self.data["frequency"] = frequency
        if num_variants:
            self.data["num_variants"] = num_variants
        if referenceBases:
            self.data["referenceBases"] = referenceBases
        if alternateBases:
            self.data["alternateBases"] = alternateBases
        if start:
            self.data["start"] = start
        if end:
            self.data["end"] = end
        if variantCount or variantCount == 0:
            self.data["variantCount"] = variantCount
        if variantType:
            self.data["variantType"] = variantType
        if variant_composite_id:
            self.data["variant_composite_id"] = variant_composite_id
        if chromosome:
            self.data["chromosome"] = chromosome
        if variant_id:
            self.data["variant_id"] = variant_id
        if reference:
            self.data["reference"] = reference
        if alternate:
            self.data["alternate"] = alternate
        if variant_type:
            self.data["variant_type"] = variant_type
        if matching_sample_cnt or matching_sample_cnt == 0:
            self.data["matching_sample_cnt"] = matching_sample_cnt
        # if createDateTime:
        #     self.data["createDateTime"] = createDateTime
        # if updateDateTime:
        #     self.data["updateDateTime"] = updateDateTime

    def __iter__(self):
        """Return attribute."""
        return iter(self.data)

    def __getitem__(self, name):
        """Return attribute."""
        return self.data[name]

    def keys(self):
        """Return attribute."""
        return self.data.keys()

    def items(self):
        """Return attribute."""
        return self.data.items()

    def values(self):
        """Return attribute."""
        return self.data.values()



class TestTransformationFunctions(asynctest.TestCase):
    """Test Functions related to transforming Records
        Those functions are slighly different between the query and the genomic_snp endpoints and very different from the genomic_regions endpoint."""

    # ------- Test query endpoint (almost the same as genomic_snp) ------- #

    async def test_transform_record(self):
        """Test transform DB record (query and genomic_snp endpoints)."""
        response = {'datasetId': 'EGAD00001000741', 'internalId': 21, 'exists': True, 'variantCount': 2702, 'callCount': 3708, 'sampleCount': 1854, 'frequency': 0.7287, 'numVariants': 2, 'info': {'access_type': 'PUBLIC'}}
        record = Record(id='212702370818540.72869471412', dataset_id=21, variant_cnt=2702, call_cnt=3708, sample_cnt=1854, frequency=0.7286947141, num_variants=2)
        
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData={'stable_id': 'EGAD00001000741', 'access_type': 'PUBLIC'})

        result = await transform_record(pool, record)
        self.assertEqual(result, response)
        
    def test_transform_misses(self):
        """Test transform DB misses, (query and genomic_snp endpoints)."""
        response = {'datasetId': 'EGAD00001000740', 'internalId': 20, 'exists': False, 'variantCount': 0, 'callCount': 0, 'sampleCount': 0, 'frequency': 0, 'numVariants': 0, 'info': {'access_type': 'PUBLIC'}}
        record = Record(datasetId=20, accessType='PUBLIC', stableId='EGAD00001000740')
        
        result = transform_misses(record)
        self.assertEqual(result, response)

    # ------- Test genomic_region endpoint ------- #

    async def test_transform_record_region(self):
        """Test transform DB record (query and genomic_snp endpoints)."""
        response = {'frequency': 0, 'datasetId': 'EGAD00001000740', 'internalId': 20, 'exists': True, 'variantCount': 0, 'callCount': 3854, 'sampleCount': 1927, 'numVariants': 0, 'info': {'accessType': 'PUBLIC', 'matchingSampleCount': 0}, 'datasetHandover': [{'handoverType': {'id': 'CUSTOM', 'label': 'Dataset info'}, 'note': 'Dataset information and DAC contact details in EGA Website', 'url': 'https://ega-archive.org/datasets/EGAD00001000740'}]}
        record = Record(id='2010.TAGT100006353100006355DEL', variant_composite_id='10.TAGT100006353100006355DEL', chromosome='10', variant_id='.', reference='TAG', alternate='T', start=100006353, end=100006355, variant_type='DEL', variant_cnt=0, call_cnt=3854, sample_cnt=1927, matching_sample_cnt=0, frequency=None, dataset_id=20)
        
        pool = asynctest.CoroutineMock()
        pool.acquire().__aenter__.return_value = Connection(accessData={'stable_id': 'EGAD00001000740', 'access_type': 'PUBLIC'})

        result = await transform_record_region(pool, record)
        self.assertEqual(result, response)

    def test_transform_misses(self):
        """Test transform DB misses, (query and genomic_snp endpoints)."""
        response = {'frequency': 0, 'datasetId': 'EGAD00001000740', 'internalId': 20, 'exists': False, 'variantCount': 0, 'callCount': 0, 'sampleCount': 0, 'numVariants': 0, 'info': {'accessType': 'PUBLIC', 'matchingSampleCount': 0}, 'datasetHandover': [{'handoverType': {'id': 'CUSTOM', 'label': 'Dataset info'}, 'note': 'Dataset information and DAC contact details in EGA Website', 'url': 'https://ega-archive.org/datasets/EGAD00001000740'}]}
        record = Record(datasetId=20, accessType='PUBLIC', stableId='EGAD00001000740')
        
        result = transform_misses_region(record)
        self.assertEqual(result, response)


#     def test_transform_metadata(self):
#         """Test transform medata record."""
#         response = {"createDateTime": "2018-10-20T20:33:40Z", "updateDateTime": "2018-10-20T20:33:40Z",
#                     "info": {"accessType": "PUBLIC"}}
#         record = Record("PUBLIC", createDateTime=datetime.strptime("2018-10-20 20:33:40+00", '%Y-%m-%d %H:%M:%S+00'),
#                         updateDateTime=datetime.strptime("2018-10-20 20:33:40+00", '%Y-%m-%d %H:%M:%S+00'))
#         result = transform_metadata(record)
#         self.assertEqual(result, response)



if __name__ == '__main__':
    asynctest.main()