import logging
import re

LOG = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

class RegexValidator:

    def __init__(self, pattern):
        self.pattern = pattern
        self.regex = re.compile(pattern) # no flags

    def __call__(self, value):
        """
        Validate that the input contains a match for the regular expression.
        """
        regex_matches = self.regex.search(str(value))
        if not regex_matches:
            raise ValidationError(f'{value} does not follow the pattern {self.pattern}')


class EnumValidator:
    enums = None
    choices = None

    def __init__(self, enums=None):
        self.enums = enums or []
        self.choices = set(self.enums)

    def __call__(self, value):
        """
        Validate that the input is in the given enumeration.
        """
        if value not in self.choices:
            raise ValidationError(f'{value} is not in {self.enums}')


class MinValueValidator:

    def __init__(self, minimum=None):
        assert isinstance(minimum, int), "Why don't you use an integer?"
        self.minimum = minimum

    def __call__(self, value):
        if value < self.minimum:
            raise ValidationError(f'{value} < {self.minimum}')

class MaxValueValidator:

    def __init__(self, maximum=None):
        assert isinstance(maximum, int), "Why don't you use an integer"
        self.maximum = maximum

    def __call__(self, value):
        if value > self.maximum:
            raise ValidationError(f'{value} > {self.maximum}')

# class ArrayValidator:
#     item_validator = None
#     message = 'Invalid item in the list.'

#     def __init__(self, item=None, message=None):
#         if item is not None:
#             self.item_validator = item
#         if message is not None:
#             self.message = message

#     def __call__(self, value):
#         """
#         Validate that the input is greater than the given minimum.
#         """
#         if item_validator:
#             for item in value:
#                 item_validator(item)
