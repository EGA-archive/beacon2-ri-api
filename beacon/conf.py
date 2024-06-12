import yaml

with open("beacon/api_version.yml") as api_version_file:
    api_version = yaml.safe_load(api_version_file)

"""Beacon Configuration."""



#
# Beacon general info
#
beacon_id = 'org.ega-archive.gdi-spain-beacon'  # ID of the Beacon
beacon_name = 'GDI Spain Beacon'  # Name of the Beacon service
api_version = api_version['api_version']  # Version of the Beacon implementation
uri = 'https://beacon-spain.ega-archive.org/api/'

#
# Beacon granularity
#
default_beacon_granularity = "record"
max_beacon_granularity = "record"

#
#  Organization info
#
org_id = 'GDI Spain'  # Id of the organization
org_name = 'GDI and Federated EGA (FEGA) Spain'  # Full name
org_description = ('The GDI and Federated EGA (FEGA) Spanish node is co-managed by the Barcelona Supercomputing Center (BSC) and the Centre de Regulacio Genomica (CRG). It '
                   'is a service for permanent archiving and sharing '
                   'of all types of personally identifiable genetic '
                   'and phenotypic data resulting from biomedical research projects.')
org_welcome_url = ''
org_contact_url = 'mailto:beacon.ega@crg.eu'
org_logo_url = 'https://legacy.ega-archive.org/images/logo.png'
org_info = ''

#
# Project info
#
description = r"This Beacon is based on synthetic data hosted at GDI Spain Node. It includes three datasets: the B1MG one million genomes, 2504 samples from CINECA UK1 synthetic dataset and the rare diseases dataset from rd-connect."
version = 'v2.0'
welcome_url = 'https://beacon-spain.ega-archive.org/'
alternative_url = 'https://beacon-spain.ega-archive.org/api'
create_datetime = '2021-11-29T12:00:00.000000'
update_datetime = ''
# update_datetime will be created when initializing the beacon, using the ISO 8601 format

#
# Service
#
service_type = 'org.ga4gh:beacon:1.0.0'  # service type
service_url = 'https://beacon-spain.ega-archive.org/api/services'
entry_point = False
is_open = True
documentation_url = 'https://github.com/EGA-archive/beacon-2.x/'  # Documentation of the service
environment = 'test'  # Environment (production, development or testing/staging deployments)

# GA4GH
ga4gh_service_type_group = 'org.ga4gh'
ga4gh_service_type_artifact = 'beacon'
ga4gh_service_type_version = '1.0'

# Beacon handovers
beacon_handovers = [
    {
        'handoverType': {
            'id': 'CUSTOM:000001',
            'label': 'Project description'
        },
        'note': 'Project description',
        'url': 'https://www.nist.gov/programs-projects/genome-bottle'
    }
]

#
# Database connection
#
database_host = 'mongo'
database_port = 27021
database_user = 'root'
database_password = 'example'
database_name = 'beacon'
database_auth_source = 'admin'
# database_schema = 'public' # comma-separated list of schemas
# database_app_name = 'beacon-appname' # Useful to track connections

#
# Web server configuration
# Note: a Unix Socket path is used when behind a server, not host:port
#
beacon_host = '0.0.0.0'
beacon_port = 5050
beacon_tls_enabled = False
beacon_tls_client = False
beacon_cert = '/etc/ega/server.cert'
beacon_key = '/etc/ega/server.key'
CA_cert = '/etc/ega/CA.cert'

#
# Permissions server configuration
#
permissions_url = 'http://beacon-permissionSpain:5051/'
#permissions_url = 'http://localhost:5051/'

#
# IdP endpoints (OpenID Connect/Oauth2)
#
# or use Elixir AAI (see https://elixir-europe.org/services/compute/aai)
#

idp_url = 'http://idp:8080/'
#idp_url = 'http://localhost:8080/'

#
# UI
#
autocomplete_limit = 16
autocomplete_ellipsis = '...'

#
# Ontologies
#
ontologies_folder = "deploy/ontologies/"

#json_buffer_size = 10000

alphanumeric_terms = ['libraryStrategy', 'molecularAttributes.geneIds', 'diseases.ageOfOnset.iso8601duration']