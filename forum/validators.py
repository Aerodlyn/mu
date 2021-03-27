from collections.abc import Iterable

from django.core.exceptions import ValidationError

from typing import Callable

def validate_against_blacklist (blacklist: Iterable [str]) -> Callable [[str], None]:
    """
    Returns a validator function that checks if a given string is contained within the given
    blacklist, raising a ValidationError if so.

    blacklist -- The blacklist of string values that should not be allowed
    """
    def validator (value: str):
        """
        Validator function that raises a ValidationError if the given value is contained in the
        given blacklist used in the construction of this function.

        value -- The value to check against a blacklist
        """
        if value in blacklist:
            raise ValidationError ("Prohibited value", params = { "value": value })
    return validator
