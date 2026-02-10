"""Handles the B1a: Blood Pressure Addendum form.

This is a V3-specific UDS form that is attached separately, similar to
the MEDS file. Must correspond to an UDS visit.
"""

import datetime
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import date_from_form_date
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class B1aFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__b1a = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__b1a.get_required("module", str)
        if module.upper() != "B1A":
            msg = f"Current file is not a B1A form: found {module}"
            raise InvalidFieldError(msg)

        # ideally we externally link B1a to UDS file by UDS visitdate
        self.__visitdate = date_from_form_date(table.get("_uds_visitdate", None))

        # if no uds_visitdate, fall back to visitdate, then frmdateb1a
        if not self.__visitdate:
            formdate = self.__b1a.get_value("visitdate", str)
            if not formdate:
                formdate = self.__b1a.get_value("frmdateb1a", str)

            self.__visitdate = date_from_form_date(formdate)

        if not self.__visitdate:
            raise AttributeDeriverError("Cannot determine B1a form date")

    def get_date(self) -> datetime.date:
        """Get the corresponding UDS visitdate."""
        if not self.__visitdate:
            raise AttributeDeriverError("No B1a date set")

        return self.__visitdate

    def _create_bpsysl(self) -> Optional[int]:
        """Creates bpsysl."""
        return self.__b1a.get_value("bpsysl", int)

    def _create_bpsysr(self) -> Optional[int]:
        """Creates bpsysr."""
        return self.__b1a.get_value("bpsysr", int)

    def _create_bpdiasl(self) -> Optional[int]:
        """Creates bpdiasl."""
        return self.__b1a.get_value("bpdiasl", int)

    def _create_bpdiasr(self) -> Optional[int]:
        """Creates bpdiasr."""
        return self.__b1a.get_value("bpdiasr", int)

    def _create_bpdevice(self) -> Optional[int]:
        """Creates bpdevice."""
        return self.__b1a.get_value("bpdevice", int)
