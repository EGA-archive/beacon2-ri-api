from .. import conf
from ..utils.json import jsonb


def ga4gh_service_info_v10(row):
    return {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'type': {
            'group': conf.ga4gh_service_type_group,
            'artifact': conf.ga4gh_service_type_artifact,
            'version': conf.ga4gh_service_type_version
        },
        'description': conf.description,
        'organization': {
            'name': conf.org_name,
            'url': conf.org_welcome_url
        },
        'contactUrl': conf.org_contact_url,
        'documentationUrl': conf.documentation_url,
        'createDateTime': conf.create_datetime,
        'updateDateTime': conf.update_datetime,  # to be updated and fetched from the request['app']['update_time']
        'environment': conf.environment,
        'version': conf.version,
        'url': conf.service_url,
    }


def ga4gh_phenopackets_biosamples_v10(row):
    return {
        'id': None, # required
        'subject': {
            'id': None, # required
            'alternate_ids': None,
            'date_of_birth': None,
            'age': None,
            'sex': None,
            'karyotypic_sex': None,
            'taxonomy': None,
        },
        'phenotypic_features': None,
        'biosamples': None,
        'genes': None,
        'variants': None,
        'diseases': None,
        'hts_files': None,
        'meta_data': None, # required
    }


def ga4gh_phenopackets_individual_v10(row):
    return {
        'phenopacket': {
            'id': None, # required
            'subject': {
                'id': row['individual_stable_id'], # required
                'alternate_ids': None,
                'date_of_birth': None,
                'age': None,
                'sex': row['sex'].upper() if row['sex'] else None,
                'karyotypic_sex': None,
                'taxonomy': {
                    'id': row['taxon_id_ontology'],
                    'label': row['taxon_id_ontology_label'],
                }
            },
            'phenotypic_features': jsonb(row['phenotypic_features']),
            'diseases': {},
        },
        'family': {
            'id': None,
            'proband': None,
            'pedigree': None,
        }
    }