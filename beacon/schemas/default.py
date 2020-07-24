"""It will raise an exception if the fields are not found in the record."""

def beacon_variant_v01(row):
    return {
            'chromosome': None,
            'referenceBases': row['reference'],
            'alternateBases': row['alternate'],
            'variantType': row['variant_type'],
            'start': row['start'],
            'end': row['end'],
            'assemblyId': row['assembly_id'],
            'info': None,
        }


def beacon_variant_annotation_v01(row):
    return {
            'genomicHGVSId': None,
            'proteinHGVSIds': None,
            'molecularConsequence': row['effect'],
            'geneIds': [row['gene_name']] if row['gene_name'] is not None else None,
            'transcriptIds': [row['transcript_id']] if row['transcript_id'] is not None else None,
            'variantGeneRelationship': None,
            'clinicalRelevance': None,
            'alternativeIds': None,
            'info': {
                'effect': row['effect'],
                'effectImpact': row['effect_impact'],
                'functionalClass': row['functional_class'],
                'codonChange': row['codon_change'],
                'aminoacidChange': row['aminoacid_change'],
                'aminoacidLength': row['aminoacid_length'],
                'geneName': row['gene_name'],
                'transcriptBiotype': row['transcript_biotype'],
                'geneCoding': row['gene_coding'],
                'transcriptId': row['transcript_id'],
                'exonRank': row['exon_rank'],
                'genotype': row['genotype'],
            }
        }

def beacon_biosample_v01(row):
    return {
        'biosampleId': row['biosample_id'],
        'individualId': row['individual_id'],
        'description': None,
        'biosampleStatus': None,
        'obtentionProcedure': row['procedure'],
        'info': {
            'collectionDate': str(row['collection_date']),
            'biosampleType': row['biosample_type'],
        }
    }


def beacon_individual_v01(row):
    return {
        'individualId': row['individual_id'],
        'sex': row['individual_sex'],
        'ethnicity': None,
        'geographicOrigin': row['geo_origin'],
        'diseases': [ # TODO: This needs to gather info from different rows
            {
                'diseaseId': row['disease'],
                'ageOfOnset': {
                    'age': row['individual_age'],
                    'ageGroup': None,
                },
                'stage': row['disease_stage'],
                'familyHistory': False,
            }
        ],
        'pedigrees': [ # TODO: This needs to gather info from different rows
            {
                'pedigreeId': None,
                'pedigreeRole': None,
                'numberOfIndividualsTested': None,
                'diseaseId': None,
            }
        ],
        'info': None,
    }

