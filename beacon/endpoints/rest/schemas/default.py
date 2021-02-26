import logging

from .... import conf

LOG = logging.getLogger(__name__)


def beacon_info_v20(datasets, authorized_datasets=[]):
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
        'updateDateTime': conf.update_datetime,
        'serviceType': conf.service_type,
        'serviceUrl': conf.service_url,
        'entryPoint': conf.entry_point,
        'open': conf.is_open,
        'datasets': [beacon_dataset_info_v20(row, authorized_datasets) for row in datasets],
        'info': None,
    }


def beacon_dataset_info_v20(row, authorized_datasets=[]):
    dataset_id = row['datasetId']
    is_authorized = dataset_id in authorized_datasets

    return {
        'id': dataset_id,
        'name': row['name'],
        'description': row['description'],
        'assemblyId': row['assemblyId'],
        'createDateTime': row['createdAt'].strftime(conf.datetime_format) if row['createdAt'] else None,
        'updateDateTime': row['updatedAt'].strftime(conf.datetime_format) if row['updatedAt'] else None,
        'dataUseConditions': None,
        'version': None,
        'variantCount': row['variantCount'],  # already coalesced
        'callCount': row['callCount'],
        'sampleCount': row['sampleCount'],
        'externalURL': None,
        'info': {
            'accessType': row['accessType'],
            'authorized': True if row['accessType'] == 'PUBLIC' else is_authorized,
            'datasetSource': row['datasetSource'],
            'datasetType': row['datasetType']
        }
    }


def beacon_variant_v20(row):
    return {
            'variantId': row['variant_id'],
            'refseqId': row['refseq_id'],
            'ref': row['reference'],
            'alt': row['alternate'],
            'variantType': row['variant_type'],
            'start': row['start'],
            'end': row['end'],
            'assemblyId': row['assembly_id'],
            'info': {
                'chromosome': row['chromosome'],
                'effect_impacts': row['effect_impacts'],
                'functional_classes': row['functional_classes'],
                'genomic_regions_ontology': row['genomic_regions_ontology'],
                'molecular_effects_ontology': row['molecular_effects_ontology'],
                'ontologies_used': row['ontologies_used']
            },
        }


def beacon_variant_annotation_v20(row):
    return {
            'variantId': row['variant_id'],
            'variantAlternativeIds': [row['variant_name']],
            'transcriptHGVSIds': row['transcript_hgvs_ids'],
            'proteinHGVSIds': row['protein_hgvs_ids'],
            'genomicRegions': row['genomic_regions'],
            'genomicFeatures': row['genomic_features_ontology'],
            'molecularEffect': row['molecular_effects'],
            #'molecularConsequence': row['molecular_consequence'],
            'aminoacidChange': row['aminoacid_changes'],
            'info': None
        }

def beacon_biosample_v20(row):
    return {
        'biosampleId': row['biosample_stable_id'],
        'subjectId': row['individual_stable_id'],
        'description': row['description'],
        'biosampleStatus': row['biosample_status_ontology'],
        'collectionDate':  str(row['collection_date']) if row['collection_date'] else None,
        'subjectAgeAtCollection': row['individual_age_at_collection'],
        'sampleOriginDescriptors': row['sample_origins_ontology'],
        'obtentionProcedure': row['obtention_procedure_ontology'],
        'cancerFeatures': {
            'tumorProgression': row['tumor_progression_ontology'],
            'tumorGrade': row['tumor_grade_ontology'],
        },
        'handovers': row['handovers'],
        'info': {
            'alternativeIds': row['alternative_ids'],
            'studyId': row['study_id'],
            'bioprojectId': row['bioproject_id'],
            'files': row['files'],
        }
    }


def beacon_individual_v20(row):
    return {
        'individualId': row['individual_stable_id'],
        'taxonId': row['taxon_id'],
        'sex': row['sex_ontology'],
        'ethnicity': row['ethnicity_ontology'],
        'geographicOrigin': row['geographic_origin_ontology'],
        'phenotypicFeatures': row['phenotypic_features'],
        'diseases': row['diseases'],
        'pedigrees': row['pedigrees'],
        'handovers': row['handovers'],
        #'interventions': row['interventions'],
        'info': {
            'sraFamilyId': row['sra_family_id'],
            'alternativeIds': row['alternative_ids'],
            'race': row['race'],
            'weightKg': row['weight_kg'],
            'heightCm': row['height_cm'],
            'bloodType': row['blood_type'],
            'medications': row['medications'],
            'procedures': row['procedures'],
        },
    }

