"""Errors and exception handling."""

from typing import List, Optional


class AttributeDeriverError(Exception):
    pass


class OperationError(Exception):
    pass


class InvalidFieldError(Exception):
    """Error for when a field is invalid."""

    pass


class MissingRequiredError(Exception):
    """Error for when a required field is missing."""

    def __init__(self, fields: Optional[List[str]] = None):
        super().__init__("missing required attributes")
        self.fields: List[str] = fields if fields else []

    def __str__(self) -> str:
        return f"{super().__str__()}: {', '.join(self.fields)}"
