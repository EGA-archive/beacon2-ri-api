import logging

from aiohttp.web import json_response

from ... import conf
from ...utils.db import fetch_filtering_terms
from ...utils.stream import json_stream

LOG = logging.getLogger(__name__)

# If not defined in conf.py
autocomplete_limit = getattr(conf, 'autocomplete_limit', 16)
autocomplete_ellipsis = getattr(conf, 'autocomplete_ellipsis', '...')


ontologyTerms = None # cache

def get_filters(word):
    count = 0
    global ontologyTerms
    for record in ontologyTerms:
        label = record['label']
        if not word or word.lower() in label.lower():
            count+=1
            
            if count > autocomplete_limit: # last word in the list
                yield {'value': autocomplete_ellipsis, 'label': autocomplete_ellipsis }
                break
            
            yield {'value': '{}:{}'.format(record['ontology'], record['term']),
                   'label': label }

async def handler(request):

    term = request.match_info.get('term')
    if term is None:
        return await json_stream(request, [])
    
    # we get them all. Not too many!
    global ontologyTerms
    if not ontologyTerms:
        LOG.debug('Fetching ontology terms')
        ontologyTerms = [record async for record in fetch_filtering_terms()] 

    return await json_stream(request, get_filters(term))
