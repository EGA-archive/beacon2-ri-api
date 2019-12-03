"""Beacon Python Application Configuration."""

import json
import os
from configparser import ConfigParser
from collections import namedtuple
from distutils.util import strtobool


def parse_drspaths(paths):
    """Parse handover configuration."""
    return [p.strip().split(',', 2) for p in paths.split('\n') if p.split()]


def parse_config_file(path):
    """Parse configuration file."""
    config = ConfigParser()
    config.read(path)
    config_vars = {
        # Beacon general info
        'id': config.get('beacon_general_info', 'id'),
        'beacon_name': config.get('beacon_general_info', 'beacon_name'),
        'apiVersion': config.get('beacon_general_info', 'apiVersion'),
        
        #  Organization info
        'org_id': config.get('organization_info', 'org_id'),
        'org_name': config.get('organization_info', 'org_name'),
        'org_description': config.get('organization_info', 'org_description'),
        'org_adress': config.get('organization_info', 'org_adress'),
        'org_welcomeUrl': config.get('organization_info', 'org_welcomeUrl'),
        'org_contactUrl': config.get('organization_info', 'org_contactUrl'),
        'org_logoUrl': config.get('organization_info', 'org_logoUrl'),
        'org_info': config.get('organization_info', 'org_info'),

        # Project info
        'description': config.get('project_info', 'description'),
        'version': config.get('project_info', 'version'),
        'welcomeUrl': config.get('project_info', 'welcomeUrl'),
        'alternativeUrl': config.get('project_info', 'alternativeUrl'),
        'createDateTime': config.get('project_info', 'createDateTime'),
        'updateDateTime': config.get('project_info', 'updateDateTime'),

        # Service
        'service': config.get('services', 'service'),
        'serviceUrl': config.get('services', 'serviceUrl'),
        'entryPoint': config.get('services', 'entryPoint'),
        'open': config.get('services', 'open'),
        'service_type': config.get('services', 'service_type'),
        'documentationUrl': config.get('services', 'documentationUrl'),
        'environment': config.get('services', 'environment')


    }
    return namedtuple("Config", config_vars.keys())(*config_vars.values())


CONFIG_INFO = parse_config_file(os.environ.get('CONFIG_FILE', os.path.join(os.path.dirname(__file__), 'config.ini')))
