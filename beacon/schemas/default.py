from .. import conf

"""It will raise an exception if the fields are not found in the record."""


def beacon_info_v20(datasets):
    return {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'apiVersion': conf.api_version,
        'environment': conf.environment,
        'organization': {
            'id': conf.org_id,
            'name': conf.org_name,
            'description': conf.org_description,
            'address': conf.org_adress,
            'welcomeUrl': conf.org_welcome_url,
            'contactUrl': conf.org_contact_url,
            'logoUrl': conf.org_logo_url,
            'info': conf.org_info,
        },
        'description': conf.description,
        'version': conf.version,
        'welcomeUrl': conf.welcome_url,
        'alternativeUrl': conf.alternative_url,
        'createDateTime': conf.create_datetime,
        'updateDateTime': conf.update_datetime, # to be updated and fetched from the request['app']['update_time']
        'serviceType': conf.service_type,
        'serviceUrl': conf.service_url,
        'entryPoint': conf.entry_point,
        'open': conf.is_open,
        'datasets': [beacon_dataset_info_v20(row) for row in datasets],
        'info': None,
    }


def beacon_dataset_info_v20(row):
    return {
        "id": row["datasetId"],
        "name": None,
        "description": row["description"],
        "assemblyId": row["assemblyId"],
        "createDateTime": None,
        "updateDateTime": None,
        "dataUseConditions": None,
        "version": None,
        "variantCount": row["variantCount"],  # already coalesced
        "callCount": row["callCount"],
        "sampleCount": row["sampleCount"],
        "externalURL": None,
        "info": {
            "accessType": row["accessType"],
            "authorized": True if row["accessType"] == "PUBLIC" else False
        }
    }


def beacon_variant_v20(row):
    return {
            'variantId': row['id'],
            'refseqId': row['refseq'],
            'ref': row['reference'],
            'alt': row['alternate'],
            'variantType': row['variant_type'],
            'start': row['start'],
            'end': row['end'],
            'assemblyId': row['assembly_id'],
            'info': None,
        }


def beacon_variant_annotation_v20(row):
    return {
            'variantId': row['id'],
            'variantAlternativeIds': row['variant_name'],
            'genomicHGVSId': row['genomic_hgvs_id'],
            'transcriptHGVSIds': row['transcript_hgvs_ids'],
            'proteinHGVSIds': row['protein_hgvs_ids'],
            'genomicRegions': row['genomic_regions'],
            'genomicFeatures': row['genomic_features'],
            'molecularEffects': row['molecular_effects'],
            'aminoacidChanges': row['aminoacid_changes'],
            'info': None
        }

def beacon_biosample_v20(row):
    return {
        'biosampleId': row['biosample_stable_id'],
        'individualId': row['individual_stable_id'],
        'description': row['description'],
        'biosampleStatus': row['biosample_status'],
        'collectionDAte':  str(row['collection_date']),
        'subjectAgeAtCollection': row['individual_age_at_collection'],
        'sampleOrigins': row['sample_origins'],
        'obtentionProcedure': row['obtention_procedure'],
        'cancerFeatures': {
            'tumorProgression': row['tumor_progression'],
            'tumorGrade': row['tumor_grade'],
        },
        'info': None
    }


def beacon_individual_v20(row):
    return {
        'individualId': row['individual_stable_id'],
        'sex': row['sex'],
        'ethnicity': row['ethnicity'],
        'geographicOrigin': row['geographic_origin'],
        'phenotypicFeatures': row['phenotypic_features'],
        'diseases': row['diseases'],
        'pedigrees': row['pedigrees'],
        'info': None,
    }

