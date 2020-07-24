"""
Functions and dictionaries used to shape diverse objects according to the spec. 
"""

from .. import conf

# ----------------------------------------------------------------------------------------------------------------------
#                                                 BEACON INFO 
# ----------------------------------------------------------------------------------------------------------------------

organization = {
    'id': conf.beacon_id,
    'name': conf.beacon_name,
    'description': conf.org_description,
    'address': conf.org_adress,
    'welcomeUrl': conf.org_welcome_url,
    'contactUrl': conf.org_contact_url,
    'logoUrl': conf.org_logo_url,
    'info': conf.org_info,
}

sample_allele_requests = [ {
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

Beacon_v1 = {
    'id': conf.beacon_id,
    'name': conf.beacon_name,
    'serviceType': conf.service,
    'apiVersion': conf.api_version,
    'serviceUrl': conf.service_url,
    'entryPoint': conf.entry_point,
    'organization': organization,
    'description': conf.description,
    'version': conf.version,
    'open': conf.is_open,
    'welcomeUrl': conf.welcome_url,
    'alternativeUrl': conf.alternative_url,
    'createDateTime': conf.create_datetime,
    'updateDateTime': conf.update_datetime, # to be updated and fetched from the request['app']['update_time']
}

GA4GH_ServiceInfo_v01 = {
    'id': conf.beacon_id,
    'name': conf.beacon_name,
    'type': conf.service_type,
    'description': conf.description,
    "organization": {'name': conf.org_name,
                     'url': conf.org_welcome_url},
    'contactUrl': conf.org_contact_url,
    'documentationUrl': conf.documentation_url,
    'createDateTime': conf.create_datetime,
    'updateDateTime': conf.update_datetime, # to be updated and fetched from the request['app']['update_time']
    'environment': conf.environment,
    'version': conf.version,
}


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

    age = {
        "age": sample_info.get("individual_age_at_collection_age"),
        "ageGroup": sample_info.get("individual_age_at_collection_age_group")
    } 

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
                "bioSampleId": sample_info.get("sample_stable_id"),
                "individualId": sample_info.get("patient_stable_id"),
                "description": sample_info.get("description"),
                "biosampleStatus": sample_info.get("biosample_status"),
                "individualAgeAtCollection": age,
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
    processed_request = processed_request if processed_request else {}
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
    Shapes the objects using the names return by custom SQL queries. 
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

    diseases = [
        {
            "diseaseId": disease.get("disease"),
            "ageOfOnset": disease.get("age"),
            "stage": disease.get("stage"),
            "familyHistory": disease.get("family_history")
        }
        for disease in individual_info.get("diseases")
    ]

    pedigrees = [
        {
            "pedigreeId": pedigree.get("pedigree_id"),
            "pedigreeRole": pedigree.get("pedigree_role"),
            "numberOfIndividualsTested": pedigree.get("number_of_individuals_tested"),
            "diseaseId": pedigree.get("pedigree_disease")

        }
        for pedigree in individual_info.get("pedigrees")
        if any(pedigree.values())
    ]

    beacon_individual_v1_0 = {
    "version": "beacon-individual-v1.0",
    "value": 
        {
            "individualId": individual_info.get("patient_stable_id"),
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
                    "label": individual_info.get("ethnicity")
                    },
                }, {
                "geographicOrigin": {
                    "id": "",
                    "label": individual_info.get("geographic_origin")
                }
                }],

                "diseases": [{
                    "term": {
                        "id": "",
                        "label": disease.get("disease")
                        },
                    "ageOfOnset": {
                        "age": disease.get("age")
                        },
                    "diseaseStage": {
                        "id": "",
                        "label": disease.get("stage")
                        }
                }
                for disease in individual_info.get("diseases")]
            }
        }


    # Equivalence dict
    name2dict = {
        "ga4gh-phenopacket-individual-v0.1" : ga4gh_phenopacket_individual_v0_1
    }

    # Request
    processed_request = processed_request if processed_request else {}
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



def individual_object_rest(individual_info, alternative_schemas):
    """
    Shapes the objects using the names return by the query_patients() SQL funciton. 
    """
    
    # Accepted alternative models
    accepted_list = ["ga4gh-phenopacket-individual-v0.1"]

    diseases = [
        {
            "diseaseId": disease.get("disease_id"),
            "ageOfOnset": {
                "age": disease.get("disease_age_of_onset_age"),
                "ageGroup": disease.get("disease_age_of_onset_age_group")
            },
            "stage": disease.get("disease_stage"),
            "familyHistory": disease.get("disease_family_history")
        }
        for disease in individual_info.get("diseases")
    ]

    pedigrees = [
        {
            "pedigreeId": pedigree.get("pedigree_stable_id"),
            "pedigreeRole": pedigree.get("pedigree_role"),
            "numberOfIndividualsTested": pedigree.get("pedigree_no_individuals_tested"),
            "diseaseId": pedigree.get("pedigree_disease_id")

        }
        for pedigree in individual_info.get("pedigrees")
        if any(pedigree.values())
    ]

    beacon_individual_v0_1 = {
    "version": "beacon-individual-v0.1",
    "value": 
        {
            "individualId": individual_info.get("individual_stable_id"),
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
                    "id": individual_info.get("individual_stable_id"),
                    "ageAtBaseline": {
                        "age": ""
                    },
                    "sex": individual_info.get("sex")
                },

                "phenotypicFeatures": [{
                "ethnicity": {
                    "id": "",
                    "label": individual_info.get("ethnicity")
                    },
                }, {
                "geographicOrigin": {
                    "id": "",
                    "label": individual_info.get("geographic_origin")
                }
                }],

                "diseases": [{
                    "term": {
                        "id": "",
                        "label": disease.get("disease_id")
                        },
                    "ageOfOnset": {
                        "age": disease.get("disease_age_of_onset_age")
                        },
                    "diseaseStage": {
                        "id": "",
                        "label": disease.get("disease_stage")
                        }
                }
                for disease in individual_info.get("diseases")]
            }
        }

    # Equivalence dict
    name2dict = {
        "ga4gh-phenopacket-individual-v0.1" : ga4gh_phenopacket_individual_v0_1
    }

    # Request
    if "beacon-individual-v0.1" in alternative_schemas:
        alternative_schemas.remove("beacon-individual-v0.1")

    if not alternative_schemas:
        return {"default": beacon_individual_v0_1,
                "alternativeSchemas": [] }
    else:
        alt_resp_list = [name2dict[alt] for alt in alternative_schemas if alt in accepted_list]
        return {"default": beacon_individual_v0_1,
                "alternativeSchemas": alt_resp_list }



