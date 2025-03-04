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
from typing import Callable, Dict, List, Optional

from nacc_attribute_deriver.attributes.attribute_map import ATTRIBUTE_MAP


class EventType(StrEnum):
    """Defines an event type, which defines how a variable is applied.
    """
    UPDATE = 'update'    # update value without any condition
    INITIAL = 'initial'  # only update value if earlier
    LATEST = 'latest'    # only update value if later
    COUNT = 'count'      # count the number of instances
    MAX = 'max'          # only update if greater than
    MIN = 'min'          # only update if less than
    SET = 'set'          # add value to a set

class DeriveEvent(BaseModel):
    """Defines a derive event, e.g. where something should go
    and the event to be applied onto it.
    """
    location: str
    event: EventType

    @field_validator('event', mode='before')
    def validate_event_type(cls, value: str) -> EventType:
        try:
            return EventType(value)
        except ValueError:
            raise ValidationError(f"Unrecognized event type: {value}")


class AttributeSchema(BaseModel):
    """Defines the derive schema for a single attribute, e.g. how
    something should be derived.
    """
    attribute: Dict[str, Callable]   # Maps to class/function attribute
    events: List[DeriveEvent]        # target DeriveEvents for that function

    # this is just more for human readibility, not necessary for any processing
    type: Optional[str] = None
    description: Optional[str] = None

    # should not be set? this is super ugly

    @field_validator('attribute', mode='before')
    def map_attribute(cls, name: str) -> Callable:
        """Maps the given string function name to an actual attribute class/function.
        Raises validation error if the function name is not known.

        Args:
            value: The function name to validate
        """
        name = name.lower()
        if name not in ATTRIBUTE_MAP:
            raise ValidationError(f"Unrecognized attribute function: {name}")

        return ATTRIBUTE_MAP[name]


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
