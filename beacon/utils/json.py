import inspect
import logging
from dataclasses import is_dataclass
from decimal import Decimal
from json.encoder import py_encode_basestring_ascii
from bson.objectid import ObjectId

from asyncpg import Record

from json import loads as parse_json

from pymongo.cursor import Cursor

LOG = logging.getLogger(__name__)

_INFINITY = float('inf')


def is_cursor(o):
    return isinstance(o, Cursor)


def is_list(o):
    return (isinstance(o, (list, set, tuple)) or
            inspect.isgenerator(o) or
            inspect.isgeneratorfunction(o))


def is_dict(o):
    return isinstance(o, (dict, Record))


def is_asyncgen(o):
    return (inspect.isasyncgen(o) or
            inspect.isasyncgenfunction(o))


class jsonb(str):
    __parsed = None

    @property
    def parsed(self):
        """Return a JSON deserializing of itself."""
        if self.__parsed is None:
            self.__parsed = parse_json(self)
        return self.__parsed


def json_encoder(v):
    raise NotImplementedError('We should not use json encoding')


def json_decoder(v):
    return jsonb(v)  # just "tag" it


# we make it compact
_ITEM_SEPARATOR = ','
_KEY_SEPARATOR = ':'


def _atom(o):
    if isinstance(o, jsonb):
        return o
    elif isinstance(o, str):
        return py_encode_basestring_ascii(o)
    elif o is None:
        return 'null'
    elif o is True:
        return 'true'
    elif o is False:
        return 'false'
    elif isinstance(o, int):
        return int.__repr__(o)
    elif isinstance(o, float):
        if o != o:
            return 'NaN'
        elif o == _INFINITY:
            return 'Infinity'
        elif o == -_INFINITY:
            return '-Infinity'
        else:
            return float.__repr__(o)
    elif isinstance(o, Decimal):
        return str(o)  # keeps the decimals, float would truncate them
    elif isinstance(o, ObjectId):
        return py_encode_basestring_ascii(str(o))
    # not a common type
    return None


async def _compound(o, circulars):
    if is_dict(o):
        async for i in _iterencode_dict(o, circulars):
            yield i
    elif is_list(o):
        async for i in _iterencode_list(o, circulars):
            yield i
    elif is_asyncgen(o):
        async for i in _iterencode_async_gen(o, circulars):
            yield i
    elif is_dataclass(o):
        async for i in _iterencode_dataclass(o, circulars):
            yield i
    elif is_cursor(o):
        async for i in _iterencode_cursor(o, circulars):
            yield i
    else:
        raise TypeError(f'Unsupported type: {o.__class__.__name__}')


async def _iterencode_list(items, circulars):
    yield '['
    marker = id(items)
    if marker in circulars:
        raise ValueError("Circular reference detected")
    circulars[marker] = items
    first = True
    for item in items:
        if first:
            first = False
        else:
            yield _ITEM_SEPARATOR
        async for i in _iterencode(item, circulars):
            yield i
    yield ']'
    del circulars[marker]


async def _iterencode_dict(d, circulars):
    yield '{'
    marker = id(d)
    if marker in circulars:
        raise ValueError("Circular reference detected")
    circulars[marker] = d
    first = True
    for key, value in d.items():
        atom_key = _atom(key)
        if atom_key is None:
            raise TypeError(f'keys must be str, int, float or bool, not {key.__class__.__name__}')
        if first:
            first = False
        else:
            yield _ITEM_SEPARATOR
        yield atom_key
        yield _KEY_SEPARATOR
        async for item in _iterencode(value, circulars):
            yield item
    yield '}'
    del circulars[marker]


async def _iterencode_async_gen(g, circulars):
    yield '['
    marker = id(g)
    if marker in circulars:
        raise ValueError("Circular reference detected")
    circulars[marker] = g
    first = True
    async for item in g:
        if first:
            first = False
        else:
            yield _ITEM_SEPARATOR
        async for i in _iterencode(item, circulars):
            yield i
    yield ']'
    del circulars[marker]


async def _iterencode_cursor(g, circulars):
    yield '['
    marker = id(g)
    if marker in circulars:
        raise ValueError("Circular reference detected")
    circulars[marker] = g
    first = True

    try:
        item = g.next()
    except:
        item = None
    while item:
        if first:
            first = False
        else:
            yield _ITEM_SEPARATOR
        async for i in _iterencode(item, circulars):
            yield i
        try:
            item = g.next()
        except:
            item = None
    yield ']'
    del circulars[marker]


async def _iterencode_dataclass(d, circulars):
    yield '{'
    marker = id(d)
    if marker in circulars:
        raise ValueError("Circular reference detected")
    circulars[marker] = d
    first = True
    for key in d.__dataclass_fields__:
        value = getattr(d, key)
        atom_key = _atom(key)
        if atom_key is None:
            raise TypeError(f'keys must be str, int, float or bool, not {key.__class__.__name__}')
        if first:
            first = False
        else:
            yield _ITEM_SEPARATOR
        yield atom_key
        yield _KEY_SEPARATOR
        async for item in _iterencode(value, circulars):
            yield item
    yield '}'
    del circulars[marker]

async def _iterencode(o, circulars):
    atom = _atom(o)
    if atom is not None:
        yield atom
    else:  # not an atom type
        async for item in _compound(o, circulars):
            yield item


async def json_iterencode(o):
    async for i in _iterencode(o, {}):
        yield i
