from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from typing import (
    Callable,
    Iterable
)

@deconstructible
class ValidateAgainstBlacklist (object):
    """
    Validator that checks given values against a list that serves as a blacklist, raising a
    ValidationError if that value is in the list.
    """
    def __init__ (self, blacklist: Iterable [str]):
        self.blacklist = blacklist

    def __call__ (self, value: str):
        """
        Raises a ValidationError if the given value is contained in the blacklist.

        value -- The value to check against a blacklist
        """
        if value in self.blacklist:
            raise ValidationError ("Prohibited value", params = { "value": value })
