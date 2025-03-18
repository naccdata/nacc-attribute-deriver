"""Defines the curation schema."""
from typing import List, Optional

from pydantic import BaseModel, field_validator

from .operation import Operation


class DeriveEvent(BaseModel):
    """Defines a derive event, e.g. where something should go and the event to
    be applied onto it."""

    class Config:
        arbitrary_types_allowed = True

    location: str
    operation: Operation

    @field_validator('operation', mode='before')
    def generate_operation(cls, value: str) -> Operation:
        return Operation.create(value)


class AttributeSchema(BaseModel):
    """Defines the derive schema for a single attribute, e.g. how something
    should be derived."""
    function: str  # Maps to an attribute function
    events: List[DeriveEvent]  # target DeriveEvents for that function

    # this is more for human readibility, not necessary for any processing
    type: Optional[str] = None
    description: Optional[str] = None
