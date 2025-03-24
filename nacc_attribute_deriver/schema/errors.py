"""Errors and exception handling."""


class AttributeDeriverError(Exception):
    pass


class MissingRequiredError(Exception):
    def __init__(self, field: str, message: str = ""):
        super().__init__(message)
        self.field = field
