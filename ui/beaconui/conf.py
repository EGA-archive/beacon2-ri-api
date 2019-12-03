
########################################################################
## Beacon settings
########################################################################
import sys
import os
import configparser
import logging
from logging.config import dictConfig
import yaml

from django.conf import settings

LOG = logging.getLogger(__name__)

# Conf in INI format
conf_file = os.getenv('BEACON_UI_CONF')
if not conf_file:
    print('BEACON_UI_CONF environment variable is empty', file=sys.stderr)
    sys.exit(1)

CONF = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
if not conf_file.startswith('/'): # relative path
    conf_file = os.path.join(settings.BASE_DIR, conf_file)
CONF.read(conf_file)

# Logger in YML format
log_file = os.getenv('BEACON_UI_LOG')
if log_file and os.path.exists(log_file):
    with open(log_file, 'r') as stream:
        dictConfig(yaml.safe_load(stream))



# Initialize the list of Assembly Ids, with the Anonymous user.
# Since it's the same list for every user
from .api import get_info, get_filtering_terms

try:
    _info = get_info(None) # no user
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(2)

BEACON_ASSEMBLYIDS = set( (d['assemblyId'] for d in _info.get('datasets', [])) )


# Filtering terms
try:
    _terms = get_filtering_terms('filtering_terms') # kw for the cache
except Exception as e:
    print(e, file=sys.stderr)
    _terms = []
    # sys.exit(2)

FILTERING_TERMS = dict( ('{}:{}'.format(p.get('ontology'), p.get('term')),
                         p.get('label')) for p in _terms )

