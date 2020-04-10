"""Beacon Configuration."""

import datetime

#
# Beacon general info
#
beacon_id   = 'ega-beacon'
beacon_name = 'EGA Beacon' # Name of the Beacon service
api_version = '2.0.0' # Version of the Beacon implementation

#
#  Organization info
#
org_id          = 'EGA' # Id of the organization
org_name        = 'European Genome-Phenome Archive (EGA)' # Full name
org_description = ('The European Genome-phenome Archive (EGA) '
                   'is a service for permanent archiving and sharing '
                   'of all types of personally identifiable genetic '
                   'and phenotypic data resulting from biomedical research projects.')
org_adress      = ''
org_welcome_url = 'https://ega-archive.org/'
org_contact_url = 'mailto:beacon.ega@crg.eu'
org_logo_url    = 'https://ega-archive.org/images/logo.png'
org_info        = ''

#
# Project info
#
description     = (r"This <a href='https://beacon-project.io/'>Beacon</a> "
                   r"is based on the GA4GH Beacon "
                   r"<a href='https://github.com/ga4gh-beacon/specification-v2/blob/master/beacon.yaml'>v2.0</a>")
version         = 'v2.0'
welcome_url     = 'https://beacon.ega-archive.org/'
alternative_url = 'https://beacon-api.ega-archive.org/'
create_datetime = '2019-08-15T12:00.000Z' # fixed
update_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # re-created at boot time

#
# Service
#
service           = 'GA4GHBeacon' # service type
service_url       = 'https://testv2-beacon-api.ega-archive.org/services'
entry_point       = False
is_open           = True
service_type      = 'org.ga4gh:beacon:1.0.0' # Service type in 'group:artifact:version' format
documentation_url = 'https://github.com/EGA-archive/beacon-2.x/' # Documentation of the service
environment       = 'test' # Environment (production, development or testing/staging deployments)


#
# Database connection
#
database_url = 'beacon-db'
database_port = 5432
database_user = 'beacon'
database_password = 'secretpassword'
database_name = 'beacon'
database_schema = 'public' # comma-separated list of schemas
