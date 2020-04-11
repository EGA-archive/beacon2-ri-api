"""
Field classes.
"""

import logging
import os
# from decimal import Decimal, DecimalException

from ..conf import database_schema
from .validators import (ValidationError,
                         EnumValidator,
                         RegexValidator,
                         MinValueValidator,
                         MaxValueValidator)
from ..utils.db import fetch_datasets_access

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

    def validate(self, value): # converted value
        if value in EMPTY_VALUES and self.required:
            raise FieldError(self.name, 'required field')
        if value in EMPTY_VALUES:
            # LOG.debug('%s: %s is an empty value', self.name, value)
            return
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError as e:
                errors.append(str(e))
        if errors:
            if len(errors) == 1:
                raise FieldError(self.name, errors[0])
            else:
                raise FieldError(self.name, '\n' + '\n'.join([f'* {err}' for err in errors]))

    async def convert(self, value):
        if value in EMPTY_VALUES:
            return self.default
        return value

    async def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise FieldError for any errors.
        """
        value = await self.convert(value)
        self.validate(value)
        return value


class ChoiceField(Field):

    def __init__(self, *args, **kwargs):
        self.choices = args
        if not self.choices:
            raise FieldError(self.name, 'You should select some choices')
        super().__init__(**kwargs)
        self.item_type = type(self.choices[0])
        self.validators.append(EnumValidator(self.choices))

    async def convert(self, value: str):
        if value in EMPTY_VALUES:
            return self.default
        try:
            return self.item_type(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, f'{value} is not among {self.item_type}')


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

    async def convert(self, value: str) -> int:
        """
        Validate that int() can be called on the input. Return the result
        of int() or None for empty values.
        """
        # value = super().convert(value)
        if value in EMPTY_VALUES:
            return self.default
        try:
            return int(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, self.error_message)


class BooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str) -> bool:
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('false', '0'):
            return False
        return bool(value)


class NullBooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str) -> bool:
        # value = super().convert(value)
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

    async def convert(self, value: str) -> set:
        # value = super().convert(value)
        if value in EMPTY_VALUES:
            return self.default
        values = value.split(self.separator)
        return set(self.item_type.convert(v) for v in values)

    def validate(self, values):
        if values in EMPTY_VALUES:
            return
        for value in values:
            self.item_type.validate(value)
        return values

# class CommaSeparatedListField(ListField):
#     def __init__(self, **kwargs):
#         kwargs['separator'] = ','
#         super().__init__(**kwargs)

class DatasetIdsField(ListField):

    async def convert(self, value: str) -> list:
        # value = super().convert(value)
        # if value in EMPTY_VALUES:
        #     return self.default
        values = value.split(self.separator) if value not in EMPTY_VALUES else []
        # remove duplicates
        datasets = list(set(values)) # we know they should be strings
        return await fetch_datasets_access(datasets=datasets)

