"""
Defines the curation schema. In JSON would look like the following:
{
    nacc_derived_vars: [
        {
            "function": "create_naccalzp",
            "events": [
                {
                    "location": "file.info.derived.naccalzp",
                    "type": "update"
                }
            ]
        }
    ],

    "mqt_derived_vars": [
        {
            "function": "contributing_diagnosis",
            "events": [
                {
                    "location": "subject.info.cognitive.uds.cognitive-status.initial",
                    "type": "initial"
                },
                {
                    "location": "subject.info.cognitive.uds.cognitive-status.latest",
                    "type": "latest"
                }
            ]
        }
    ]
}
"""
from enum import StrEnum
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator
)
from typing import List, Optional
from .operation import Operation


class DeriveEvent(BaseModel):
    """Defines a derive event, e.g. where something should go
    and the event to be applied onto it.
    """
    class Config:
        arbitrary_types_allowed = True
    
    location: str
    operation: Operation

    @field_validator('operation', mode='before')
    def generate_operation(cls, value: str) -> Operation:
        return Operation.create(value)


class AttributeSchema(BaseModel):
    """Defines the derive schema for a single attribute, e.g. how
    something should be derived.
    """
    function: str                 # Maps to an attribute function
    events: List[DeriveEvent]     # target DeriveEvents for that function

    # this is more for human readibility, not necessary for any processing
    type: Optional[str] = None
    description: Optional[str] = None


class CurationSchema(BaseModel):
    """Defines the overall curation schema, defining all attributes to
    be derived
    """
    nacc_derived_vars: List[AttributeSchema]
    mqt_derived_vars: List[AttributeSchema]

    date_key: str   # dot-notation string key that determines the order of
                    # longitudinal events like initial/latest

    def curation_order(self) -> List[AttributeSchema]:
        """Return the curation order.

        Should evaluate all NACC variables first, then MQT derived
        variables.
        """
        return self.nacc_derived_vars + self.mqt_derived_vars
