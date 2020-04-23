"""
Field classes.
"""

import logging
import os
# from decimal import Decimal, DecimalException

from aiohttp import ClientSession

from ..conf import database_schema, permissions_url
from .validators import (ValidationError,
                         EnumValidator,
                         RegexValidator,
                         MinValueValidator,
                         MaxValueValidator)
from ..api.db import fetch_datasets_access

LOG = logging.getLogger(__name__)

__all__ = (
    'Field', 'StringField', 'IntegerField', 'FloatField', 'DecimalField',
    'RegexField', 'BooleanField', 'NullBooleanField', 'ChoiceField', 
)

# These values, if given to validate(), will trigger the self.required check.
EMPTY_VALUES = (None, '', [], (), {}, set())

class FieldError(ValidationError):
    def __init__(self, key, message):
        msg = '{} for {}: {}'.format(self.__class__.__name__, key, message)
        super().__init__(msg)

class Field:

    error_message = 'Field not follow its specification'

    def __init__(self, *, required=False, default=None, error_message=None, validators=()):
        # required -- Boolean that specifies whether the field is required.
        # error_message -- optional
        # validators -- List of additional validators to use
        self.required = required
        self.validators = list(validators)
        if error_message is not None:
            self.error_message = error_message or self.error_message
        self.default = default
        # Using assertion: we don't start the beacon
        assert not required or default is None, 'required and default are mutually exclusive'
        self.name = 'Unknown'

    def set_name(self, n):
        self.name = n

    def run_validators(self, value):
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError as e:
                errors.append(str(e))
        if errors:
            message = errors[0] if len(errors) == 1 else '\n' + '\n'.join([f'* {err}' for err in errors])
            raise FieldError(self.name, message)

    async def validate(self, value): # converted value
        if value in EMPTY_VALUES:
            if self.required:
                raise FieldError(self.name, 'required field')
            # LOG.debug('%s: %s is an empty value', self.name, value)
            return
        self.run_validators(value)

    async def convert(self, value, **kwargs):
        if value in EMPTY_VALUES:
            return self.default
        return value

    async def clean(self, req, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise FieldError for any errors.
        """
        value = await self.convert(value, request=req)
        await self.validate(value)
        return value


class ChoiceField(Field):

    def __init__(self, *args, **kwargs):
        self.choices = args
        if not self.choices:
            raise FieldError(self.name, 'You should select some choices')
        super().__init__(**kwargs)
        self.item_type = type(self.choices[0])
        self.validators.append(EnumValidator(self.choices))

    async def convert(self, value: str, **kwargs):
        if value in EMPTY_VALUES:
            return self.default
        try:
            return self.item_type(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, f'{value} is not of type {self.item_type}')


class RegexField(Field):
    def __init__(self, pattern, **kwargs):
        super().__init__(**kwargs)
        self.validators = [RegexValidator(pattern)]


class IntegerField(Field):
    error_message = 'not a number'

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super().__init__(**kwargs)

        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))

    async def convert(self, value: str, **kwargs) -> int:
        """
        Validate that int() can be called on the input. Return the result
        of int() or None for empty values.
        """
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        try:
            return int(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, self.error_message)


class BooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str, **kwargs) -> bool:
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('false', '0'):
            return False
        return bool(value)


class NullBooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str, **kwargs) -> bool:
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('true', '1'):
            return True
        if value.lower() in ('false', '0'):
            return False
        return self.default


class ListField(Field):

    def __init__(self, *, items=None, separator=',', **kwargs):
        self.separator = separator
        self.item_type = items or Field()
        super().__init__(**kwargs)

    async def convert(self, value: str, **kwargs) -> set:
        if value in EMPTY_VALUES:
            return self.default
        values = value.split(self.separator)
        res = set()
        for v in values:
            converted_v = await self.item_type.convert(v, **kwargs)
            res.add(converted_v)
        return list(res) # for the moment, cuz json.dumps not happy

    async def validate(self, values):
        if values in EMPTY_VALUES:
            return
        for value in values:
            await self.item_type.validate(value)
        return values


class DatasetsField(ListField):

    async def convert(self, value: str, request=None) -> list:

        # Requested datasets
        values = value.split(self.separator) if value not in EMPTY_VALUES else []
        datasets = list(set(values)) # remove duplicates, we know they should be strings

        # Get the token.
        # If the user is not authenticated (ie no token)
        # we pass (datasets, False) to the database function: it will filter out the datasets list, with the public ones

        header = request.headers.get('Authorization') if request else None
        LOG.debug('Access token: %s', header)
        if header is None:
            return datasets, False
            
        token = header.split(' ', 1)
        if len(token) < 2:
            return datasets, False

        # Otherwise, we have a token and resolve the datasets with the permissions server
        # The permissions server will:
        # * filter out the datasets list, with the ones the user has access to
        # * return _all_ the datasets the user has access to, in case the datasets list is empty
        token = token[1]
        async with ClientSession() as session:
            async with session.post(
                    permissions_url,
                    headers = { 'Authorization': header }, # only sending that header
                    json = { 'datasets': datasets }, # will set the Content-Type to application/json
            ) as resp:

                if resp.status > 200:
                    LOG.error('Permissions server error %d', resp.status)
                    return [], False # behave like it's not authenticated ?

                authorized_datasets = await resp.json()
                return authorized_datasets, True

