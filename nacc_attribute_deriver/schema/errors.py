"""Errors and exception handling."""

from typing import Any


class AttributeDeriverError(Exception):
    pass


class MissingRequiredError(Exception):
    """Error for when a required field is missing."""

    def __init__(self, field: str, message: str = ""):
        if not message:
            message = f"Missing required field: {field}"

        super().__init__(message)
        self.field = field


class InvalidFieldError(Exception):
    """Error for when a field is invalid."""

    def __init__(self, field: str, expected: Any, value: Any, message: str = ""):
        if not message:
            message = f"Invalid field {field}, expected {expected} but found {value}"

        super().__init__(message)
        self.field = field
        self.expected = expected
        self.value = value
