"""Defines the curation schema."""

from typing import List, Optional

from pydantic import BaseModel, field_validator

from .operation import Operation


class AttributeAssignment(BaseModel):
    """Defines an assignment of a derived value to an attribute.

    Location is the target attribute operation is how the value is
    assigned to the attribute
    """

    class Config:
        arbitrary_types_allowed = True

    attribute: str
    operation: Operation

    @field_validator("operation", mode="before")
    def generate_operation(cls, value: str) -> Operation:
        return Operation.create(value)


class CurationRule(BaseModel):
    """Defines the curation rules for a single attribute expression.

    Each derived attribute is determined by an assignment operation,
    and an expression for computing the value.
    This rule defines the update of several derived attributes by one expression:

    - `function` is the name of a method of an AttributeCollection that
       implements an attribute expression.
    - `assignments` is the list of AttributeAssignments that indicate how the
       value should be assigned to each target attribute.
    """

    function: str  # Name of the attribute function
    assignments: List[AttributeAssignment]

    # this is more for human readability, not necessary for any processing
    type: Optional[str] = None
    description: Optional[str] = None


class RuleFileModel(BaseModel):
    """Model for loading serialized rule definitions."""

    function: str
    location: str
    operation: str
    type: str
    description: str

    @property
    def assignment(self) -> AttributeAssignment:
        """Creates an attribute assignment from this rule model."""
        return AttributeAssignment(attribute=self.location, operation=self.operation)
