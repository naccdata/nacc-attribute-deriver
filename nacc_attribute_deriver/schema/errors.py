"""Errors and exception handling."""

from typing import Optional


class AttributeDeriverError(Exception):
    pass


class InvalidFieldError(Exception):
    """Error for when a field is invalid."""

    pass


class MissingRequiredError(Exception):
    """Error for when a required field is missing."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field
