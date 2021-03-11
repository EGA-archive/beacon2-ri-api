import logging
import re
import json

from .... import conf

under_pat = re.compile(r'_([a-z])')

LOG = logging.getLogger(__name__)

def snake_case_to_camelCase(j):
    return j if j is None else json.loads(under_pat.sub(lambda x: x.group(1).upper(), j))

def beacon_info_v30(datasets, authorized_datasets=[]):
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
        'datasets': [beacon_dataset_info_v30(row, authorized_datasets) for row in datasets],
        'info': None,
    }


def beacon_dataset_info_v30(row, authorized_datasets=[]):
    dataset_id = row['stable_id']
    is_authorized = dataset_id in authorized_datasets

    return {
        'id': dataset_id,
        'name': row['name'],
        'description': row['description'],
        'assemblyId': row['reference_genome'],
        'createDateTime': row['created_at'].strftime(conf.datetime_format) if row['created_at'] else None,
        'updateDateTime': row['updated_at'].strftime(conf.datetime_format) if row['updated_at'] else None,
        'dataUseConditions': None,
        'version': None,
        'variantCount': row['variant_count'],
        'callCount': row['call_count'],
        'sampleCount': row['sample_count'],
        'externalURL': None,
        'handovers': row['handovers'],
        'info': {
            'accessType': row['access_type'],
            'authorized': True if row['access_type'] == 'PUBLIC' else is_authorized,
            'datasetSource': row['dataset_source'],
            'datasetType': row['dataset_type']
        }
    }


def beacon_variant_v30(row):
    return {
            'variantId': row['variant_id'],
            'assemblyId': row['assembly_id'],
            'refseqId': row['refseq_id'],
            'start': row['start'],
            'end': row['end'],
            'ref': row['reference'],
            'alt': row['alternate'],
            'variantType': row['variant_type'],
            'info': None,
        }


def beacon_variant_annotation_v30(row):
    return {
            'variantId': row['variant_id'],
            'variantAlternativeId': [row['alternative_id']],
            'genomicHGVSId': row['genomic_hgvs_id'],
            'transcriptHGVSId': row['transcript_hgvs_ids'],
            'proteinHGVSId': row['protein_hgvs_ids'],
            'genomicRegion': row['genomic_regions'],
            'genomicFeatures': row['genomic_features_ontology'],
            'annotationToolVersion': 'SnpEffVersion=5.0d (build 2021-01-28 11:39)',
            'molecularEffect': row['molecular_effects'],
            #'molecularConsequence': row['molecular_consequence'],
            'aminoacidChange': row['aminoacid_changes'],
            'info': {
                'aaref': row['aaref'],
                #'aapos': row['aapos'],
                'aaalt': row['aaalt'],
                'aa_pos_aa_length': row['functional_classes'],
                'rank': row['exon_ranks'],
                'annotation_impact': row['genomic_regions']
            }
        }

def beacon_biosample_v30(row):
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


def beacon_individual_v30(row):
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
        'treatments': None,
        'interventions': None,
        'measures': None,
        'exposures': None,
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


def beacon_cohort_v31(row):
    return {
        'cohortId': row['id'],
        'cohortName': row['cohort_name'],
        'cohortType': row['cohort_type'],
        'cohortDesign': row['cohort_design'],
        'cohortInclusionCriteria': row['cohort_inclusion_criteria'],
        'cohortExclusionCriteria': row['cohort_exclusion_criteria'],
        'cohortLicense': row['cohort_license'],
        'cohortContact': row['cohort_contact'],
        'cohortRights': row['cohort_rights'],
        'cohortSize': row['cohort_size'],
        'cohortDataTypes': row['cohort_data_types'],
        'collectionEvents': snake_case_to_camelCase(row['collection_events']),
    }