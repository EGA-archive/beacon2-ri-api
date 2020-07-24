import logging
import re

LOG = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

class RegexValidator:

    def __init__(self, pattern, ignore_case):
        self.pattern = pattern
        flags = re.I if ignore_case else 0
        self.regex = re.compile(pattern, flags=flags)

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
            if len(self.enums) == 1:
                message = f'{value} =/= {self.enums[0]}'
            else:
                message = f'{value} not an element of {self.enums}'
            raise ValidationError(message)


class MinValueValidator:

    def __init__(self, minimum=None):
        assert isinstance(minimum, (int,float)), "Why don't you use an integer or a float?"
        self.minimum = minimum

    def __call__(self, value):
        if value < self.minimum:
            raise ValidationError(f'{value} < {self.minimum}')


class MaxValueValidator:

    def __init__(self, maximum=None):
        assert isinstance(maximum, (int,float)), "Why don't you use an integer or a float?"
        self.maximum = maximum

    def __call__(self, value):
        if value > self.maximum:
            raise ValidationError(f'{value} > {self.maximum}')
