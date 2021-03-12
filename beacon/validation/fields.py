"""
Field classes.
"""

import logging

from datetime import datetime

from .. import conf
from .validators import (ValidationError,
                         EnumValidator,
                         RegexValidator,
                         MinValueValidator,
                         MaxValueValidator)
from ..utils import db
from ..endpoints.rest.schemas import supported_schemas

__all__ = (
    'Field', 'StringField', 'IntegerField', 'FloatField', 'DecimalField',
    'RegexField', 'BooleanField', 'NullBooleanField', 'ChoiceField', 'BoundedListField'
)

LOG = logging.getLogger(__name__)

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
        self.name = None

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

class Filter(Field):
    def __init__(self, name, *args, **kwargs):
        # Using Beacon compliant field names
        super().__init__(*args, **kwargs)
        self.name = name

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
    def __init__(self, pattern, ignore_case=False, **kwargs):
        self.pattern = pattern
        self.ignore_case = ignore_case
        super().__init__(**kwargs)
        self.validators = [RegexValidator(pattern, ignore_case)]


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

class FloatField(Field):
    error_message = 'not a float'

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super().__init__(**kwargs)

        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))

    async def convert(self, value: str, **kwargs) -> int:
        """
        Validate that float() can be called on the input. Return the result
        of float() or None for empty values.
        Also works for scientific notation.
        """
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        try:
            return float(value)
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


class DateField(Field):
    error_message = 'Invalid parsing date format'

    def __init__(self, *, parse_format='%m/%d/%Y', **kwargs):
        self.parse_format = parse_format
        super().__init__(**kwargs)

    async def convert(self, value: str, **kwargs) -> datetime:
        if value in EMPTY_VALUES:
            return self.default
        try:
            return datetime.strptime(value, self.parse_format)
        except ValueError:
            raise FieldError(self.name, self.error_message)


class NullBooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str, **kwargs) -> bool:
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('true', '1', 'on'):
            return True
        if value.lower() in ('false', '0', 'off'):
            return False
        return self.default


class ListField(Field):

    def __init__(self, *, items=None, separator=',', trim=True, **kwargs):
        self.separator = separator
        self.item_type = items or Field()
        self.trim = trim or True
        super().__init__(**kwargs)

    async def convert(self, value: str, **kwargs) -> set:
        if value in EMPTY_VALUES:
            return self.default
        try:
            values = value.split(self.separator)
        except:
            values = value
        res = set()
        for v in values:
            if self.trim:
                v = v.strip()
            converted_v = await self.item_type.convert(v, **kwargs)
            res.add(converted_v)
        return res

    async def validate(self, values):
        if values in EMPTY_VALUES:
            return
        for value in values:
            await self.item_type.validate(value)

class MultipleField(Filter):
    pass

class RangeField(Filter, ListField):
    '''aka a pair of values'''

    def __init__(self, name, *args, sort_key=None, reverse=False, **kwargs):
        ListField.__init__(self, *args, **kwargs)
        self.sort_key = sort_key
        self.reverse = reverse
        self.name = name

    async def convert(self, value: str, **kwargs):
        if value in EMPTY_VALUES:
            return self.default
        values = await super().convert(value)
        if len(values) == 1:
            val = values[0]
            return [val,val] # repeat it
        if len(values) != 2:
            raise FieldError(self.name, "must contain exactly two values")
        return sorted(values, key=self.sort_key, reverse=self.reverse)

class BoundedListField(ListField):

    def __init__(self, name, *args, min_items=1, max_items=1, **kwargs):
        super().__init__(**kwargs)
        #ListField.__init__(self, *args, **kwargs)
        self.name = name
        self.min_items = min_items
        self.max_items = max_items

    async def convert(self, value: str, **kwargs) -> list:
        LOG.debug('field=%s', self.name)

        if value in EMPTY_VALUES:
            return list()

        try:
            values = value.split(self.separator)
        except:
            values = value
        res = list()

        for v in values:
            if self.trim:
                v = v.strip()
            if v:
                converted_v = await self.item_type.convert(v, **kwargs)
                res.append(converted_v)

        if len(res) < self.min_items:
            raise FieldError(self.name, f'must contain {self.min_items} value(s) at least')

        if len(res) > self.max_items:
            raise FieldError(self.name, f'must contain {self.max_items} value(s) at most')

        LOG.debug('field %s, res=%s, len(res)=%s', self.name, res, len(res))
        return res

class DatasetsField(Field):

    def __init__(self, *, separator=',', trim=True, **kwargs):
        self.separator = separator
        self.trim = trim or True
        super().__init__(**kwargs)

    async def get_datasets(self):
        datasets = getattr(conf, 'datasets', None)
        if datasets is None:
            datasets = set( [name async for _,_,name in db.fetch_datasets_access()] )
            setattr(conf, 'datasets', datasets)
        else:
            LOG.debug('Using cached datasets: %s', datasets)
        return datasets

    async def convert(self, value: str, **kwargs) -> (set, set):
        if value in EMPTY_VALUES:
            return set()
        try:
            values = value.split(self.separator)
        except:
            values = value
        valid, invalid = set(), set() # avoid repetitions
        datasets = await self.get_datasets()
        for value in values:
            if self.trim:
                value = value.strip()
            if value in datasets:
                valid.add(value)
            else:
                invalid.add(value)
        invalid_size = len(invalid)
        if invalid_size > 0:
            error = 'are invalid datasets' if invalid_size > 1 else 'is an invalid dataset'
            raise ValidationError(f'"{invalid}" {error}')
        return valid

class SchemaField(Field):

    def __init__(self, *schemas, **kwargs):
        if not schemas:
            raise FieldError(self.name, 'You should select some schemas')
        for schema in schemas:
            if not isinstance(schema, str):
                raise FieldError(self.name, f'{schema} must be a str')
            if not schema in supported_schemas:
                raise FieldError(self.name, f'{schema} is not a supported schema')
        super().__init__(**kwargs)
        self.schemas = schemas
        self.validate_schemas = EnumValidator(schemas)

    async def validate(self, value): # converted value
        try:
            self.validate_schemas(value[0]) # skip the func
        except ValidationError as e:
            raise FieldError(self.name, str(e))

    async def convert(self, value: str, **kwargs) -> (set, set):
        if value in EMPTY_VALUES:
            if self.required:
                raise FieldError(self.name, 'required field')
            value = self.default
        func = supported_schemas.get(value)
        if func is None:
            raise FieldError(self.name, f'{value} is not a supported schema')
        return (value, func)
