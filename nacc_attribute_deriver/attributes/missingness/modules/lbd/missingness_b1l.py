"""Class to handle LBD B1l missingness values. Mainly done for the 777 (provided at
previous visit) values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)


class LBDFormB1lMissingness(FormMissingnessCollection):
    def __handle_provided_at_prev_visit(self, field: str) -> T:
        """Defines general missingness for LBD form variables."""
        return self.generic_missingness(field, attr_type)
