"""
Beacon Framework Configuration Endpoints.
"""

# import logging

from beacon import conf

# LOG = logging.getLogger(__name__)
from beacon.db.schemas import DefaultSchemas

from beacon.utils.stream import json_stream


def get_entry_types():
    return {
        "analysis": {
            "id": "analysis",
            "name": "Bioinformatics analysis",
            "ontologyTermForThisType": {
                "id": "edam:operation_2945",
                "label": "Analysis"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "Apply analytical methods to existing data of a specific type.",
            "defaultSchema": {
                "id": DefaultSchemas.ANALYSES.value['schema'],
                "name": "Default schema for a bioinformatics analysis",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/analyses/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "additionallySupportedSchemas": []
        },
        "biosample": {
            "id": "biosample",
            "name": "Biological Sample",
            "ontologyTermForThisType": {
                "id": "NCIT:C70699",
                "label": "Biospecimen"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "Any material sample taken from a biological entity for testing, diagnostic, propagation, treatment or research purposes, including a sample obtained from a living organism or taken from the biological object after halting of all its life functions. Biospecimen can contain one or more components including but not limited to cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory products. [ NCI ]",
            "defaultSchema": {
                "id": DefaultSchemas.BIOSAMPLES.value['schema'],
                "name": "Default schema for a biological sample",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/biosamples/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "additionallySupportedSchemas": []
        },
        "cohort": {
            "id": "cohort",
            "name": "Cohort",
            "ontologyTermForThisType": {
                "id": "NCIT:C61512",
                "label": "Cohort"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "A group of individuals, identified by a common characteristic. [ NCI ]",
            "defaultSchema": {
                "id": DefaultSchemas.COHORTS.value['schema'],
                "name": "Default schema for cohorts",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/cohorts/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "aCollectionOf": [{"id": "individual", "name": "Individuals"}],
            "additionalSupportedSchemas": []
        },
        "dataset": {
            "id": "dataset",
            "name": "Dataset",
            "ontologyTermForThisType": {
                "id": "NCIT:C47824",
                "label": "Data set"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "A Dataset is a collection of records, like rows in a database or cards in a cardholder.",
            "defaultSchema": {
                "id": DefaultSchemas.DATASETS.value['schema'],
                "name": "Default schema for datasets",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/datasets/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "aCollectionOf": [{"id": "genomicVariation", "name": "Genomic Variants"}],
            "additionalSupportedSchemas": []
        },
        "genomicVariant": {
            "id": "genomicVariation",
            "name": "Genomic Variants",
            "ontologyTermForThisType": {
                "id": "SO:0000735",
                "label": "sequence_location"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "The location of a sequence.",
            "defaultSchema": {
                "id": DefaultSchemas.GENOMICVARIATIONS.value['schema'],
                "name": "Default schema for a genomic variation",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "additionallySupportedSchemas": []
        },
        "individual": {
            "id": "individual",
            "name": "Individual",
            "ontologyTermForThisType": {
                "id": "NCIT:C25190",
                "label": "Person"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "A human being. It could be a Patient, a Tissue Donor, a Participant, a Human Study Subject, etc.",
            "defaultSchema": {
                "id": DefaultSchemas.INDIVIDUALS.value['schema'],
                "name": "Default schema for an individual",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/individuals/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "additionallySupportedSchemas": []
        },
        "run": {
            "id": "run",
            "name": "Sequencing run",
            "ontologyTermForThisType": {
                "id": "NCIT:C148088",
                "label": "Sequencing run"
            },
            "partOfSpecification": "Beacon v2.0.0",
            "description": "The valid and completed operation of a high-throughput sequencing instrument for a single sequencing process. [ NCI ]",
            "defaultSchema": {
                "id": DefaultSchemas.RUNS.value['schema'],
                "name": "Default schema for a sequencing run",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/runs/defaultSchema.json",
                "schemaVersion": "v2.0.0"
            },
            "additionallySupportedSchemas": []
        },

    }


async def configuration(request):
    meta = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/sections/beaconInformationalResponseMeta.json',
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'returnedSchemas': []
    }

    response = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/beaconConfigurationSchema.json',
        'maturityAttributes': {
            'productionStatus': 'DEV'
        },
        'securityAttributes': {
            'defaultGranularity': 'record',
            'securityLevels': ['PUBLIC', 'REGISTERED', 'CONTROLLED']
        },
        'entryTypes': get_entry_types()
    }

    configuration_json = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconConfigurationResponse.json',
        'meta': meta,
        'response': response
    }

    return await json_stream(request, configuration_json)


async def entry_types(request):
    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'returnedSchemas': []
    }

    response = {
        "entryTypes": get_entry_types()
    }

    entry_types_json = {
        'meta': meta,
        'response': response
    }

    return await json_stream(request, entry_types_json)


async def beacon_map(request):
    meta = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/sections/beaconInformationalResponseMeta.json',
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'returnedSchemas': []
    }

    response = {
        '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/beaconMapSchema.json',
        "endpointSets": {
            "analysis": {
                "entryType": "analysis",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/analyses/endpoints.json",
                "rootUrl": conf.uri + "analyses",
                "singleEntryUrl": conf.uri + "analyses/{id}",
                "endpoints": {
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "analyses/{id}/g_variants"
                    },
                }
            },
            "biosample": {
                "entryType": "biosample",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/biosamples/endpoints.json",
                "rootUrl": conf.uri + "biosamples",
                "singleEntryUrl": conf.uri + "biosamples/{id}",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "biosamples/{id}/analyses"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "biosamples/{id}/g_variants"
                    },
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "biosamples/{id}/runs"
                    },
                }
            },
            "cohort": {
                "entryType": "cohort",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/cohorts/endpoints.json",
                "rootUrl": conf.uri + "cohorts",
                "singleEntryUrl": conf.uri + "cohorts/{id}",
                "filteringTermsUrl": conf.uri + "cohorts/filtering_terms",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "cohorts/{id}/analyses"
                    },
                    "individual": {
                        "returnedEntryType": "individual",
                        "url": conf.uri + "cohorts/{id}/individuals"
                    },
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "cohorts/{id}/runs"
                    }
                }
            },
            "dataset": {
                "entryType": "dataset",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/datasets/endpoints.json",
                "rootUrl": conf.uri + "datasets",
                "singleEntryUrl": conf.uri + "datasets/{id}",
                "filteringTermsUrl": conf.uri + "datasets/filtering_terms",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "datasets/{id}/analyses"
                    },
                    "biosample": {
                        "returnedEntryType": "biosample",
                        "url": conf.uri + "datasets/{id}/biosamples"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "datasets/{id}/g_variants"
                    },
                    "individual": {
                        "returnedEntryType": "individual",
                        "url": conf.uri + "datasets/{id}/individuals"
                    },
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "datasets/{id}/runs"
                    }
                }
            },
            "genomicVariant": {
                "entryType": "genomicVariant",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/genomicVariations/endpoints.json",
                "rootUrl": conf.uri + "g_variants",
                "singleEntryUrl": conf.uri + "g_variants/{variantInternalId}",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "g_variants/{variantInternalId}/analyses"
                    },
                    "biosample": {
                        "returnedEntryType": "biosample",
                        "url": conf.uri + "g_variants/{variantInternalId}/biosamples"
                    },
                    "individual": {
                        "returnedEntryType": "individual",
                        "url": conf.uri + "g_variants/{variantInternalId}/individuals"
                    },
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "g_variants/{variantInternalId}/runs"
                    }
                }
            },
            "individual": {
                "entryType": "individual",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/individuals/endpoints.json",
                "rootUrl": conf.uri + "individuals",
                "singleEntryUrl": conf.uri + "individuals/{id}",
                "filteringTermsUrl": conf.uri + "individuals/filtering_terms",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "individuals/{id}/analyses"
                    },
                    "biosample": {
                        "returnedEntryType": "biosample",
                        "url": conf.uri + "individuals/{id}/biosamples"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "individuals/{id}/g_variants"
                    },
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "individuals/{id}/runs"
                    }
                }
            },
            "run": {
                "entryType": "run",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-Model/runs/endpoints.json",
                "rootUrl": conf.uri + "runs",
                "singleEntryUrl": conf.uri + "runs/{id}",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "runs/{id}/analyses"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "runs/{id}/g_variants"
                    },
                }
            },
        }
    }

    beacon_map_json = {
        'meta': meta,
        'response': response
    }

    return await json_stream(request, beacon_map_json)
