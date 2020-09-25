import logging
import collections

from .fields import Field, MultipleField
from .validators import ValidationError
from ..utils.exceptions import BeaconBadRequest

LOG = logging.getLogger(__name__)


class DeclarativeFieldsMetaclass(type):
    """Collect Fields declared on the base classes."""

    # @classmethod
    # def __prepare__(self, name, bases):
    #     return collections.OrderedDict()
    # As of Python 3.7, dict are ordered

    def __new__(mcs, name, bases, attrs):

        # Collect fields from current class.
        current_fields = []
        # print('------------- ATTRS: ', attrs)
        # print('------------- BASES: ', bases)

        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                if value.name is None:
                    value.set_name(key)
                current_fields.append((key, value))
                attrs.pop(key)
        d = dict(current_fields)
        attrs['__fields__'] = d
        #keys = tuple([key for key, value in current_fields])
        keys = [k for k,v in current_fields]
        current_names = [v.name for k,v in current_fields]
        attrs['__keys__'] = keys
        attrs['__names__'] = collections.namedtuple(name, keys)(*current_names)

        new_class = super().__new__(mcs, name, bases, attrs)

        # We walk through the MRO with "for base in reversed(new_class.__mro__)"
        # to fetch the fields from parent classes.
        fields = {}
        # print('----- MRO for', name, ':', new_class.__mro__)
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, '__fields__'):
                fields.update(base.__fields__)
        
            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in fields:
                    fields.pop(attr)
        
        new_class.__fields__ = fields
        # Dict are ordered since python 3.6
        keys = [k for k in fields.keys()]
        names = [v.name for v in fields.values()]
        new_class.__keys__ = keys
        new_class.__names__ = collections.namedtuple(name, keys)(*names)

        # print('------------- FIELDS for',name,':', fields)
        # print('-------------   KEYS for',name,':', keys)
        # print('-------------  NAMES for',name,':', names)

        return new_class


# def flatten_dict(d):
#     """
#     Iterates through the post dictionary and
#     it flattens it to mimic the get request. 

#     We expect keys of the dictionary (and all sub-dict) to be unique
#     """
#     for key, val in d.items():
#         if isinstance(val, dict):
#             yield from flatten_dict(val) # recursion. Hopefully not too deep.
#         else:
#             yield (key, val)

class RequestParameters(metaclass=DeclarativeFieldsMetaclass):
    """
    The main implementation of all the query parameters logic.
    """
    _str = None
    api_error = True

    def __init__(self, api_error=True):
        self.api_error = api_error

    def __str__(self):
        if self._str is None:
            self._str = ';'.join([str(f) for f in self.__fields__])
        return f'<{self.__class__.__name__}: self._str>'

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.__fields__)

    async def _get_query_parameters(self, req):
        if req.method == 'GET':
            return req.rel_url.query
        elif req.method == 'POST':
            if req.headers.get('Content-Type') == 'application/json':
                # post_data = await req.json()
                # return dict(flatten_dict(post_data))
                return req.json()
            return await req.post()
        else:
            return {}

    async def clean_fields(self, req, qparams):

        # Are there extra undesired parameters
        invalid_keys = []
        for qkey in qparams.keys():
            #if qkey not in self.__keys__:
            if qkey not in self.__names__:
                invalid_keys.append(qkey)

        if invalid_keys:
            raise ValidationError('Invalid keys: %s' % invalid_keys)

        # Loop in order through the parameters
        for key in self.__keys__:
            field = self.__fields__[key]
            _get = qparams.getall if isinstance(field, MultipleField) else qparams.get
            _default = [] if isinstance(field, MultipleField) else None
            name = getattr(self.__names__, key)
            qval = _get(name, _default)

            if key == 'targetIdReq':
                qval = req.match_info.get('target_id_req')
                # LOG.debug('targetIdReq=%s', qval)
            # LOG.debug('key %s | val %s | field %s', key, qval, field.__class__.__name__)
            val = await field.clean(req, qval)
            # LOG.debug('\t -> %s', val)
            yield val

    def correlate(self, req, values):
        pass

    async def fetch(self, req):
        qparams = await self._get_query_parameters(req)
        LOG.debug("Original Query Parameters: %s", qparams)

        try:
            # Collect the values and validate them
            values = [v async for v in self.clean_fields(req, qparams)]

            values = collections.namedtuple(self.__class__.__name__, self.__keys__)(*values)
            # does not take more space than a tuple

            # Further validation: correlate the values
            self.correlate(req, values)

            # return the values in the order of the keys
            return qparams, values # or qparams?
        except ValidationError as e:
            raise BeaconBadRequest(str(e), fields=qparams, api_error=self.api_error)


def print_qparams(qparams_db, proxy, logger):
    logger.debug('{:-^50}'.format(" Query Parameters for DB "))
    for key in proxy.__keys__:
        val = getattr(qparams_db, key)
        t = ' ' if val is None else str(type(val))
        name = getattr(proxy.__names__, key)
        logger.debug(f"{key:>20} | {name:<20} : {str(val):<8} {t}")
