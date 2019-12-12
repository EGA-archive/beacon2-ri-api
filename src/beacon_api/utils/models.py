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
                    "chromosome": variant_details.get("referenceName"),
                    "referenceBases": variant_details.get("referenceBases"),
                    "alternateBases": variant_details.get("alternateBases"),
                    "variantType": variant_details.get("variantType"),
                    "start": variant_details.get("start"),
                    "end": variant_details.get("end")
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

def variantMetadata_object(processed_request):
    """
    Builds the variantAnnotation object.
    Since we only have one model for this object we keep it simple.
    """ 
    
    beacon_variant_metadata_v1_0 = {
                "default": {
                    "version": "beacon-variant-metadata-v1.0",
                    "value": {
                        "geneId": "",
                        "HGVSId": "",
                        "transcriptId": "",
                        "alleleId": "",
                        "variantClassification": "",
                        "variantType": "",
                        "disease": "",
                        "proteinChange": "",
                        "clinVarId": "",
                        "pubmedId": "",
                        "timestamp": "",
                        "info": { }
                    } 
                },
                "alternativeSchemas": []
            }

    return beacon_variant_metadata_v1_0


# ----------------------------------------------------------------------------------------------------------------------
#                                               VARIANT ANNOTATION
# ----------------------------------------------------------------------------------------------------------------------

def variantAnnotation_object(processed_request, cellBase, dbSNP, clinVar):
    """
    Builds the variantAnnotation object.
    Since we only have one model for this object we keep it simple.
    """ 

    beacon_variant_annotation_v1_0 =  {
				"default": {
					"version": "beacon-variant-annotation-v1.0",
					"value": {
						"variantMetadata": variantMetadata_object(processed_request),
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


# ----------------------------------------------------------------------------------------------------------------------
#                                                    INDIVIDUAL 
# ----------------------------------------------------------------------------------------------------------------------
