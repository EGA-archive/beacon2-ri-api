"""
Functions and dictionaries used to shape diverse objects according to the spec. 
"""

import ast 

from .. import __id__, __beacon_name__, __apiVersion__, __org_id__, __org_name__, __org_description__, __org_adress__, __org_welcomeUrl__, __org_contactUrl__, __org_logoUrl__, __org_info__
from .. import __description__, __version__, __welcomeUrl__, __alternativeUrl__, __createDateTime__, __updateDateTime__
from .. import __service__, __serviceUrl__, __entryPoint__, __open__, __service_type__, __documentationUrl__, __environment__


# ----------------------------------------------------------------------------------------------------------------------
#                                                 BEACON INFO 
# ----------------------------------------------------------------------------------------------------------------------

organization = {
    'id': __id__,
    'name': __beacon_name__,
    'description': __org_description__,
    'address': __org_adress__,
    'welcomeUrl': __org_welcomeUrl__,
    'contactUrl': __org_contactUrl__,
    'logoUrl': __org_logoUrl__,
    'info': __org_info__,
}

sample_allele_request = [ {
    "alternateBases" : "A",
    "referenceBases" : "G",
    "referenceName" : "Y",
    "start" : 2655179,
    "startMin" : None,
    "startMax" : None,
    "end" : None,
    "endMin" : None,
    "endMax" : None,
    "variantType" : None,
    "assemblyId" : "GRCh37",
    "datasetIds" : None,
    "includeDatasetResponses" : None
  }, {
    "alternateBases" : None,
    "referenceBases" : "T",
    "referenceName" : "21",
    "start" : None,
    "startMin" : 45039444,
    "startMax" : 45039445,
    "end" : None,
    "endMin" : 45084561,
    "endMax" : 45084562,
    "variantType" : None,
    "assemblyId" : "GRCh37",
    "datasetIds" : [ "1000genomes" ],
    "includeDatasetResponses" : None
  }, {
    "alternateBases" : None,
    "referenceBases" : "G",
    "referenceName" : "21",
    "start" : 15399042,
    "startMin" : None,
    "startMax" : None,
    "end" : 15419114,
    "endMin" : None,
    "endMax" : None,
    "variantType" : None,
    "assemblyId" : "GRCh37",
    "datasetIds" : [ "1000genomes" ],
    "includeDatasetResponses" : None
  } ]


def Beacon_v1(host):
    Beacon_v1 = {
        'id': __id__,
        'name': __beacon_name__,
        'serviceType': __service__,
        'apiVersion': __apiVersion__,
        'serviceUrl': __serviceUrl__,
        'entryPoint': __entryPoint__,
        'organization': organization,
        'description': __description__,
        'version': __version__,
        'open': __open__,
        'welcomeUrl': __welcomeUrl__,
        'alternativeUrl': __alternativeUrl__,
        'createDateTime': __createDateTime__,
        'updateDateTime': __updateDateTime__,
    }
    return Beacon_v1

def GA4GH_ServiceInfo_v01(host):
    GA4GH_ServiceInfo_v01 = {
        'id': __id__,
        'name': __beacon_name__,
        'type': __service_type__,
        'description': __description__,
        "organization": {'name': __org_name__,
                        'url': __org_welcomeUrl__},
        'contactUrl': __org_contactUrl__,
        'documentationUrl': __documentationUrl__,
        'createDateTime': __createDateTime__,
        'updateDateTime': __updateDateTime__,
        'environment': __environment__,
        'version': __version__,
    }
    return GA4GH_ServiceInfo_v01


# ----------------------------------------------------------------------------------------------------------------------
#                                                   VARIANT 
# ----------------------------------------------------------------------------------------------------------------------

def variant_object(processed_request, variant_details, **kwargs):
    """
    Builds the variant object depending on the model the user has specified.
    Update the dictionaries given here if you want to use another model, remember to
    use the variant_details variables and complete it with kwargs if needed.
    Modify the accepted_list and the name2dict every time you add a new model.
    """
    # Accepted alternative models
    accepted_list = ["ga4gh-variant-representation-v0.1"]

    # kwargs variables
    for key, value in kwargs.items():
        variant_details.update({key: value})

    # Models responses
    beacon_variant_v1_0 = {
        "version": "beacon-variant-v1.0",
        "value": {
                "variantDetails": {
                    "chromosome": variant_details.get("referenceName") if variant_details.get("referenceName") else variant_details.get("chromosome"),
                    "referenceBases": variant_details.get("referenceBases"),
                    "alternateBases": variant_details.get("alternateBases"),
                    "variantType": variant_details.get("variantType"),
                    "start": variant_details.get("start"),
                    "end": variant_details.get("end"),
                    "assemblyId": processed_request.get("assemblyId")
                },
                "info": {'rsID': variant_details.get("variantId")},
            }
        }

    ga4gh_variant_representation_v0_1 = {
        "version": "ga4gh-variant-representation-v0.1",
        "value": 
            {
            "location": {
                "interval": {
                "end": variant_details.get("end"),
                "start": variant_details.get("start"),
                "type": "SimpleInterval"
                },
                "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
                "type": "SequenceLocation"
                },
            "state": {
                "sequence": variant_details.get("alternateBases"),
                "type": "SequenceState"
                },
            "type": "Allele"
            }
        }

    # Equivalence dict
    name2dict = {
        "ga4gh-variant-representation-v0.1" : ga4gh_variant_representation_v0_1
    }

    # Request
    alternatives = processed_request.get("variant").split(",") if processed_request.get("variant") else []
    if "beacon-variant-v1.0" in alternatives:
        alternatives.remove("beacon-variant-v1.0")

    if not alternatives:
        return {"default": beacon_variant_v1_0,
                "alternativeSchemas": [] }
    else:
        alt_resp_list = [name2dict[alt] for alt in alternatives if alt in accepted_list]
        return {"default": beacon_variant_v1_0,
                "alternativeSchemas": alt_resp_list }



# ----------------------------------------------------------------------------------------------------------------------
#                                               VARIANT METADATA
# ----------------------------------------------------------------------------------------------------------------------

# DEPRECATED

# def variantMetadata_object(processed_request):
#     """
#     Builds the variantAnnotation object.
#     Since we only have one model for this object we keep it simple.
#     """ 
    
#     beacon_variant_metadata_v1_0 = {
#                 "default": {
#                     "version": "beacon-variant-metadata-v1.0",
#                     "value": {
#                         "geneId": "",
#                         "HGVSId": "",
#                         "transcriptId": "",
#                         "alleleId": "",
#                         "variantClassification": "",
#                         "variantType": "",
#                         "disease": "",
#                         "proteinChange": "",
#                         "clinVarId": "",
#                         "pubmedId": "",
#                         "timestamp": "",
#                         "info": { }
#                     } 
#                 },
#                 "alternativeSchemas": []
#             }

#     return beacon_variant_metadata_v1_0


# ----------------------------------------------------------------------------------------------------------------------
#                                               VARIANT ANNOTATION
# ----------------------------------------------------------------------------------------------------------------------

def variantAnnotation_object(processed_request, cellBase, dbSNP, clinVar):
    """
    Builds the variantAnnotation object.
    Since we only have one model for this object we keep it simple.
    """ 

    clinical_relevance = {
        "variantClassification": "",
        "diseaseId": "",
        "references": []
    }

    beacon_variant_annotation_v1_0 =  {
				"default": {
					"version": "beacon-variant-annotation-v1.0",
					"value": {
                        "variantId": "",
                        "alternativeIds": [],
                        "genomicHGVSId": "",
                        "proteinHGVSIds": [],
                        "molecularConsequence": "",
                        "variantGeneRelationship": "",
                        "geneId": [],
                        "transcriptIds": [],
                        "clinicalRelevance": clinical_relevance,
                        "alleleOrigin": [],
						"info": {
							"cellBase": cellBase,
							"dbSNP": dbSNP,
							"clinVar": clinVar
						}
					}
				},
				"alternativeSchemas": []		
			}

    return beacon_variant_annotation_v1_0


# ----------------------------------------------------------------------------------------------------------------------
#                                                    SAMPLE 
# ----------------------------------------------------------------------------------------------------------------------

def biosample_object(sample_info, processed_request):
    """
    """
    
    # Accepted alternative models
    accepted_list = ["ga4gh-phenopacket-biosample-v0.1"]

    # default

    # beacon_biosample_v1_0 = {
    # "version": "beacon-biosample-v1.0",
    # "value": 
    #     {
    #         "id": sample_info.get("sample_stable_id"),
    #         "tissue": sample_info.get("tissue"),
    #         "description": sample_info.get("description"),
    #         "info": { }
    #     }
    # }

    sample_origin = {
        "organ": sample_info.get("organ"),
        "tissue": sample_info.get("tissue"),
        "cellType": sample_info.get("cell_type")
    }

    cancer_features = {
        "tumorProgression": sample_info.get("tumor_progression"),
        "tumorGrade": sample_info.get("tumor_grade")
    }
    
    beacon_biosample_v1_0 = {
        "version": "beacon-biosample-v1.0",
        "value": 
            {
                "individualId": sample_info.get("patient_stable_id"),
                "bioSampleId": sample_info.get("sample_stable_id"),
                "description": sample_info.get("description"),
                "biosampleStatus": sample_info.get("biosample_status"),
                "individualAgeAtCollection": sample_info.get("individual_age_at_collection_age"),
                "sampleOrigin": sample_origin,
                "obtentionProcedure": sample_info.get("obtention_procedure"),
                "cancerFeatures": cancer_features,
                "info": ""
            }
    }

    # alternative
    ga4gh_phenopacket_biosample_v0_1 = {
        "version": "ga4gh-phenopacket-biosample-v0.1",
        "value": 
            { 
                "id": sample_info.get("sample_stable_id"),

                "individualId": sample_info.get("patient_stable_id"),

                "description": sample_info.get("description"),

                "sampledTissue": {
                    "id": "",
                    "label": sample_info.get("tissue")
                },
                
                "ageOfIndividualAtCollection": {
                    "age": sample_info.get("individual_age_at_collection_age")
                },
                
                "tumorProgression": {
                    "id": "",
                    "label": sample_info.get("tumor_progression")
                },
                
                "phenotypicFeatures": {
                    "id": "",
                    "label": ""
                },

                "procedure": {
                    "code": {
                    "id": "",
                    "label": sample_info.get("obtention_procedure")
                    }
                },

                "isControlSample": None
            }
        }

        

    # Equivalence dict
    name2dict = {
        "ga4gh-phenopacket-biosample-v0.1" : ga4gh_phenopacket_biosample_v0_1
    }

    # Request
    alternatives = processed_request.get("biosample").split(",") if processed_request.get("biosample") else []
    if "beacon-biosample-v1.0" in alternatives:
        alternatives.remove("beacon-biosample-v1.0")

    if not alternatives:
        return {"default": beacon_biosample_v1_0,
                "alternativeSchemas": [] }
    else:
        alt_resp_list = [name2dict[alt] for alt in alternatives if alt in accepted_list]
        return {"default": beacon_biosample_v1_0,
                "alternativeSchemas": alt_resp_list }



# ----------------------------------------------------------------------------------------------------------------------
#                                                    INDIVIDUAL 
# ----------------------------------------------------------------------------------------------------------------------


def individual_object(individual_info, processed_request):
    """
    """
    
    # Accepted alternative models
    accepted_list = ["ga4gh-phenopacket-individual-v0.1"]

    # default

    # beacon_individual_v1_0 = {
    # "version": "beacon-individual-v1.0",
    # "value": 
    #     {
    #         "id": individual_info.get("patient_stable_id"),
    #         "sex": individual_info.get("sex"),
    #         "ageOfOnset": individual_info.get("age_of_onset"),
    #         "disease": individual_info.get("disease"),
    #         "info": { }
    #     }
    # }

    age = {
        "age": "",
        "ageGroup": ""
    } 

    diseases = [
        {
            "disease": "",
            "ageOfOnset": "",
            "stage": "",
            "familyHistory": None
        }
    ]

    pedigrees = [
        {
            "pedigreeId": "",
            "disease": "",
            "pedigreeRole": "",
            "numberOfIndividualsTested": None
        }
    ]

    beacon_individual_v1_0 = {
    "version": "beacon-individual-v1.0",
    "value": 
        {
            "datasetId": "",
            "individualId": individual_info.get("patient_stable_id"),
            "age": age,
            "sex": individual_info.get("sex"),
            "ethnicity": individual_info.get("ethnicity"),
            "geographicOrigin": individual_info.get("geographic_origin"),
            "diseases": diseases,
            "pedigrees": pedigrees,
            "info": ""
        }
    }

    # alternative
    ga4gh_phenopacket_individual_v0_1 = {
        "version": "ga4gh-phenopacket-individual-v0.1",
        "value": 
            {
                "individual": {
                    "id": individual_info.get("patient_stable_id"),
                    "ageAtBaseline": {
                        "age": ""
                    },
                    "sex": individual_info.get("sex")
                },

                "phenotypicFeatures": [{
                "ethnicity": {
                    "id": "",
                    "label": ""
                    },
                }, {
                "geographicOrigin": {
                    "id": "",
                    "label": ""
                }
                }],

                "diseases": [{
                    "term": {
                    "id": "",
                    "label": individual_info.get("disease")
                    },
                    "ageOfOnset": {
                        "age": individual_info.get("age_of_onset")
                    },
                    "diseaseStage": [{
                    "id": "",
                    "label": ""
                    }],
                }]
            }
        }


    # Equivalence dict
    name2dict = {
        "ga4gh-phenopacket-individual-v0.1" : ga4gh_phenopacket_individual_v0_1
    }

    # Request
    alternatives = processed_request.get("individual").split(",") if processed_request.get("individual") else []
    if "beacon-individual-v1.0" in alternatives:
        alternatives.remove("beacon-individual-v1.0")

    if not alternatives:
        return {"default": beacon_individual_v1_0,
                "alternativeSchemas": [] }
    else:
        alt_resp_list = [name2dict[alt] for alt in alternatives if alt in accepted_list]
        return {"default": beacon_individual_v1_0,
                "alternativeSchemas": alt_resp_list }