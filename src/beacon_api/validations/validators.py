class RegexValidator:
    regex = ''
    message = 'Invalid pattern.'
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None, flags=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags
        if self.flags and not isinstance(self.regex, str):
            raise TypeError("If the flags are set, regex must be a regular expression string.")

        self.regex = re.compile(self.regex, self.flags)

    def __call__(self, value):
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        regex_matches = self.regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message)


class EnumValidator:
    enums = set()
    message = 'Not in the enumeration.'

    def __init__(self, enums=None, message=None):
        self.enums = set(enums or [])
        if message is not None:
            self.message = message

    def __call__(self, value):
        """
        Validate that the input is in the given enumeration.
        """
        if value not in self.enums:
            raise ValidationError(self.message)


class MinIntegerValidator:
    minimum = None
    message = 'Too low.'

    def __init__(self, minimum=None, message=None):
        if minimum is not None:
            assert(isinstance(minimum, int))
            self.minimum = minimum
        if message is not None:
            self.message = message

    def __call__(self, value):
        """
        Validate that the input is greater than the given minimum.
        """
        if self.minimum is not None and value < self.minimum:
            raise ValidationError(self.message)

class NonNegativeIntegerValidator(MinIntegerValidator):
    minimum = 0

    def __init__(self, message=None):
        if message is not None:
            self.message = message


class ArrayValidator:
    item_validator = None
    message = 'Invalid item in the list.'

    def __init__(self, item=None, message=None):
        if item is not None:
            self.item_validator = item
        if message is not None:
            self.message = message

    def __call__(self, value):
        """
        Validate that the input is greater than the given minimum.
        """
        if item_validator:
            for item in value:
                item_validator(item)
