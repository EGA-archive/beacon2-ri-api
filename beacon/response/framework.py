"""
Beacon Framework Configuration Endpoints.
"""

# import logging

from beacon import conf

# LOG = logging.getLogger(__name__)

from beacon.utils.stream import json_stream


def get_entry_types():
    return {
        "dataset": {
            "id": "dataset",
            "name": "Dataset",
            "ontologyTermForThisType": {
                "id": "NCIT:C47824",
                "label": "Data set"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "A Dataset is a collection of records, like rows in a database or cards in a cardholder.",
            "defaultSchema": {
                "id": "ga4gh-beacon-dataset-v2.0.0-draft.3",
                "name": "Default schema for datasets",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/datasets/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "aCollectionOf": [{"id": "genomicVariant", "name": "Genomic Variants"}],
            "additionalSupportedSchemas": []
        },
        "cohort": {
            "id": "cohort",
            "name": "Cohort",
            "ontologyTermForThisType": {
                "id": "NCIT:C61512",
                "label": "Cohort"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "A group of individuals, identified by a common characteristic. [ NCI ]",
            "defaultSchema": {
                "id": "ga4gh-beacon-cohort-v2.0.0-draft.3",
                "name": "Default schema for cohorts",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/cohorts/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "aCollectionOf": [{"id": "individual", "name": "Individuals"}],
            "additionalSupportedSchemas": []
        },
        "genomicVariant": {
            "id": "genomicVariant",
            "name": "Genomic Variants",
            "ontologyTermForThisType": {
                "id": "SO:0000735",
                "label": "sequence_location"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "The location of a sequence.",
            "defaultSchema": {
                "id": "ga4gh-beacon-variant-v2.0.0-draft.3",
                "name": "Default schema for a genomic variation",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/genomicVariations/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        },
        "variantAnnotation": {
            "id": "variantAnnotation",
            "name": "Genomic Variant Annotation",
            "ontologyTermForThisType": {
                "id": "SO:0000110",
                "label": "sequence_feature"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "Any extent of continuous biological sequence.",
            "defaultSchema": {
                "id": "ga4gh-beacon-variant-annotation-v2.0.0-draft.3",
                "name": "Default schema for variant annotations",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantAnnotations/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        },
        "variantInterpretation": {
            "id": "variantInterpretation",
            "name": "Genomic Variant Interpretation",
            "ontologyTermForThisType": {
                "id": "SO:0000400",
                "label": "sequence_attribute"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "An attribute describes a quality of sequence  .",
            "defaultSchema": {
                "id": "ga4gh-beacon-variant-interpretation-v2.0.0-draft.3",
                "name": "Default schema for variant Interpretations",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantInterpretations/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        },
        "variantInSample": {
            "id": "variantInSample",
            "name": "Genomic Variant in a Sample",
            "ontologyTermForThisType": {
                "id": "SO:0001507",
                "label": "variant_collection"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "A collection of one or more sequences of an individual.",
            "defaultSchema": {
                "id": "ga4gh-beacon-variant-in-sample-v2.0.0-draft.3",
                "name": "Default schema for variant in sample",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantsInSample/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
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
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "A human being. It could be a Patient, a Tissue Donor, a Participant, a Human Study Subject, etc.",
            "defaultSchema": {
                "id": "ga4gh-beacon-individual-v2.0.0-draft.3",
                "name": "Default schema for an individual",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/individuals/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
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
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "Any material sample taken from a biological entity for testing, diagnostic, propagation, treatment or research purposes, including a sample obtained from a living organism or taken from the biological object after halting of all its life functions. Biospecimen can contain one or more components including but not limited to cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory products. [ NCI ]",
            "defaultSchema": {
                "id": "ga4gh-beacon-biosample-v2.0.0-draft.3",
                "name": "Default schema for a biological sample",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/biosamples/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
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
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "The valid and completed operation of a high-throughput sequencing instrument for a single sequencing process. [ NCI ]",
            "defaultSchema": {
                "id": "ga4gh-beacon-run-v2.0.0-draft.3",
                "name": "Default schema for a sequencing run",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/runs/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        },
        "analysis": {
            "id": "analysis",
            "name": "Bioinformatics analysis",
            "ontologyTermForThisType": {
                "id": "edam:operation_2945",
                "label": "Analysis"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "Apply analytical methods to existing data of a specific type.",
            "defaultSchema": {
                "id": "ga4gh-beacon-analysis-v2.0.0-draft.3",
                "name": "Default schema for a bioinformatics analysis",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/analysis/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        },
        "interactor": {
            "id": "interactor",
            "name": "Interactor",
            "ontologyTermForThisType": {
                "$comment": "TO REVIEW: No ontology term has been found to describe this entry type. Specific relationship are defined, e.g. Host-parasite (NCIT:C16697), but none found so far that is as generic as described below.",
                "id": "NCIT:C14376",
                "label": "Other Organism Groupings",
                "comment": "A non-taxonomic grouping of organisms based on a shared characteristic. [ NCI ]"
            },
            "partOfSpecification": "Beacon v2.0.0-draft.3",
            "description": "An organism that is having an interaction with the individual, could be a parasite, an infectious agent or similar.",
            "defaultSchema": {
                "id": "ga4gh-beacon-interactor-v2.0.0-draft.3",
                "name": "Default schema for an interactor",
                "referenceToSchemaDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/interactors/defaultSchema.json",
                "schemaVersion": "v2.0.0-draft.3"
            },
            "additionallySupportedSchemas": []
        }
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
            "dataset": {
                "entryType": "dataset",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/datasets/endpoints.json",
                "rootUrl": conf.uri + "/api/datasets",
                "singleEntryUrl": conf.uri + "/api/datasets/{id}",
                "filteringTermsUrl": conf.uri + "/api/datasets/{id}/filtering_terms",
                "endpoints": {
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "/api/datasets/{id}/g_variants"
                    },
                    "biosample": {
                        "returnedEntryType": "biosample",
                        "url": conf.uri + "/api/datasets/{id}/biosamples"
                    },
                    "individual": {
                        "returnedEntryType": "individual",
                        "url": conf.uri + "/api/datasets/{id}/individuals"
                    }
                }
            },
            "cohort": {
                "entryType": "cohort",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/cohorts/endpoints.json",
                "rootUrl": conf.uri + "/api/cohorts",
                "singleEntryUrl": conf.uri + "/api/cohorts/{id}",
                "filteringTermsUrl": conf.uri + "/api/cohorts/{id}/filtering_terms",
                "endpoints": {
                    "individual": {
                        "returnedEntryType": "individual",
                        "url": conf.uri + "/api/cohorts/{id}/individuals"
                    }
                }
            },
            "genomicVariant": {
                "entryType": "genomicVariant",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/genomicVariations/endpoints.json",
                "rootUrl": conf.uri + "/api/g_variants",
                "singleEntryUrl": conf.uri + "/api/g_variants/{id}",
                "endpoints": {
                    "variantAnnotation": {
                        "returnedEntryType": "variantAnnotation",
                        "url": conf.uri + "/api/g_variants/{id}/variant_annotations"
                    },
                    "variantInterpretation": {
                        "returnedEntryType": "variantInterpretation",
                        "url": conf.uri + "/api/g_variants/{id}/variant_interpretations"
                    },
                    "variantInSample": {
                        "returnedEntryType": "variantInSample",
                        "url": conf.uri + "/api/g_variants/{id}/variants_in_sample"
                    }
                }
            },
            "individual": {
                "entryType": "individual",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/individuals/endpoints.json",
                "rootUrl": conf.uri + "/api/individuals",
                "singleEntryUrl": conf.uri + "/api/individuals/{id}",
                "filteringTermsUrl": conf.uri + "/api/individuals/{id}/filtering_terms",
                "endpoints": {
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "/api/individuals/{id}/g_variants"
                    },
                    "variantInSample": {
                        "returnedEntryType": "variantInSample",
                        "url": conf.uri + "/api/individuals/{id}/variants_in_sample"
                    },
                    "biosample": {
                        "returnedEntryType": "biosample",
                        "url": conf.uri + "/api/individuals/{id}/biosamples"
                    },
                    "interactor": {
                        "returnedEntryType": "interactor",
                        "url": conf.uri + "/api/individuals/{id}/interactors"
                    }
                }
            },
            "biosample": {
                "entryType": "biosample",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/biosamples/endpoints.json",
                "rootUrl": conf.uri + "/api/biosamples",
                "singleEntryUrl": conf.uri + "/api/biosamples/{id}",
                "endpoints": {
                    "run": {
                        "returnedEntryType": "run",
                        "url": conf.uri + "/api/biosamples/{id}/runs"
                    },
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "/api/biosamples/{id}/analysis"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "/api/biosamples/{id}/g_variants"
                    },
                    "variantInSample": {
                        "returnedEntryType": "variantInSample",
                        "url": conf.uri + "/api/biosamples/{id}/variants_in_sample"
                    }
                }
            },
            "run": {
                "entryType": "run",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/runs/endpoints.json",
                "rootUrl": conf.uri + "/api/runs",
                "singleEntryUrl": conf.uri + "/api/runs/{id}",
                "endpoints": {
                    "analysis": {
                        "returnedEntryType": "analysis",
                        "url": conf.uri + "/api/runs/{id}/analysis"
                    },
                    "genomicVariant": {
                        "returnedEntryType": "genomicVariant",
                        "url": conf.uri + "/api/runs/{id}/g_variants"
                    },
                    "variantInSample": {
                        "returnedEntryType": "variantInSample",
                        "url": conf.uri + "/api/analysis/{id}/variants_in_sample"
                    }
                }
            },
            "analysis": {
                "entryType": "analysis",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/analysis/endpoints.json",
                "rootUrl": conf.uri + "/api/analysis",
                "singleEntryUrl": conf.uri + "/api/analysis/{id}",
                "endpoints": {
                    "variantInSample": {
                        "returnedEntryType": "variantInSample",
                        "url": conf.uri + "/api/analysis/{id}/variants_in_sample"
                    }
                }
            },
            "interactor": {
                "entryType": "interactor",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/interactors/endpoints.json",
                "rootUrl": conf.uri + "/api/interactors",
                "singleEntryUrl": conf.uri + "/api/interactors/{id}"
            },
            "variantAnnotation": {
                "entryType": "variantAnnotation",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantAnnotations/endpoints.json",
                "rootUrl": conf.uri + "/api/variantAnnotations",
                "singleEntryUrl": conf.uri + "/api/variantAnnotations/{id}"
            },
            "variantInterpretation": {
                "entryType": "variantInterpretation",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantInterpretations/endpoints.json",
                "rootUrl": conf.uri + "/api/variantInterpretations",
                "singleEntryUrl": conf.uri + "/api/variantInterpretations/{id}"
            },
            "variantInSample": {
                "entryType": "variantInSample",
                "openAPIEndpointsDefinition": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2-Models/main/BEACON-V2-draft3-Model/variantsInSample/endpoints.json",
                "rootUrl": conf.uri + "/api/variants_in_sample",
                "singleEntryUrl": conf.uri + "/api/variants_in_sample/{id}"
            }
        }
    }

    beacon_map_json = {
        'meta': meta,
        'response': response
    }

    return await json_stream(request, beacon_map_json)
