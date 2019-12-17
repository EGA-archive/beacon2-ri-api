"""
The ``beacon_api`` package contains code to start an EGA Beacon API.

.. note:: In this file the information about the ``Beacon`` is registered.
         The information is parsed from :file:`beacon_api.conf.config.ini`
"""
import datetime

from .conf import CONFIG_INFO

# Beacon general info
__id__ = CONFIG_INFO.id
__beacon_name__ = CONFIG_INFO.beacon_name
__apiVersion__ = CONFIG_INFO.apiVersion

#  Organization info
__org_id__ = CONFIG_INFO.org_id
__org_name__ = CONFIG_INFO.org_name
__org_description__ = CONFIG_INFO.org_description
__org_adress__ = CONFIG_INFO.org_adress
__org_welcomeUrl__ = CONFIG_INFO.org_welcomeUrl
__org_contactUrl__ = CONFIG_INFO.org_contactUrl
__org_logoUrl__ = CONFIG_INFO.org_logoUrl
__org_info__ = CONFIG_INFO.org_info

# Project info
__description__ = CONFIG_INFO.description
__version__ = CONFIG_INFO.version
__welcomeUrl__ = CONFIG_INFO.welcomeUrl
__alternativeUrl__ = CONFIG_INFO.alternativeUrl
__createDateTime__ = CONFIG_INFO.createDateTime
__updateDateTime__ = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # Every restart of the application means an update to it

# Service
__service__ = CONFIG_INFO.service
__serviceUrl__ = CONFIG_INFO.serviceUrl 
__entryPoint__ = CONFIG_INFO.entryPoint 
__open__ = CONFIG_INFO.open 
__service_type__ = CONFIG_INFO.service_type 
__documentationUrl__ = CONFIG_INFO.documentationUrl
__environment__ = CONFIG_INFO.environment