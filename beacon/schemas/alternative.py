from .. import conf


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
        "organization": {
            'name': conf.org_name,
            'url': conf.org_welcome_url
        },
        'contactUrl': conf.org_contact_url,
        'documentationUrl': conf.documentation_url,
        'createDateTime': conf.create_datetime,
        'updateDateTime': conf.update_datetime,
        'environment': conf.environment,
        'version': conf.version,
        'url': conf.service_url,
    }
