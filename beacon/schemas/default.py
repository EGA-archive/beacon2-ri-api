"""It will raise an exception if the fields are not found in the record."""

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
        'phenotypicFeatures': [
            {
                'phenotypeId': row['phf_phenotype_id'],
                'dateOfOnset': row['phf_date_of_onset'],
                'onsetType': row['phf_onset_type'],
                'ageOfOnset': {
                    'age': row['phf_age_of_onset_age'],
                    'ageGroup': row['phf_age_of_onset_age_group'],
                },
                'severity': row['phf_severity']
        }],
        'diseases': [ # TODO: This needs to gather info from different rows
            {
                'diseaseId': row['dis_disease_id'],
                'dateOfOnset': row['dis_date_of_onset'],
                'onsetType': row['dis_onset_type'],
                'ageOfOnset': {
                    'age': row['dis_age_of_onset_age'],
                    'ageGroup': row['dis_age_of_onset_age_group'],
                },
                'stage': row['dis_stage'],
                'severity': row['dis_severity'],
                'familyHistory': row['dis_family_history'],
            }
        ],
        'pedigrees': [ # TODO: This needs to gather info from different rows
            {
                'pedigreeId': row['ped_pedigree_stable_id'],
                'pedigreeDisease': row['ped_disease_id'],
                'pedigreeRole': row['ped_role'],
                'affectedStatus': row['ped_affected_status'],
                'numberOfIndividualsTested': row['ped_no_individuals_tested'],
            }
        ],
        'info': None,
    }

