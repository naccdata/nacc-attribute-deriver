"""Handles the MEDS form.

This is mainly used to inform UDS A4 NACC derived variables.
"""

from typing import Dict, List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    BaseNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class MEDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__meds = BaseNamespace(
            table=table,
            attribute_prefix="file.info.forms.json",
            required=frozenset(["module", "formver"]),
        )
        module = self.__meds.get_required("module", str)
        if module.upper() != "MEDS":
            raise InvalidFieldError(
                f"Current file is not a MEDS form: found {module}",
            )

        # TODO: V1 does not have drugs_list and instead lists everything
        # explicitly - do not see it in pulled SAS code, will need to investigate
        self.__formver = self.__meds.get_value("formver", float)
        date_attribute = (
            "frmdatea4" if (self.__formver and self.__formver < 2) else "frmdatea4g"
        )
        self.__formdate = self.__meds.get_value(date_attribute, str)

        if not self.__formdate:
            raise AttributeDeriverError("Cannot determine MEDS form date")

        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _create_drugs_list(self) -> Dict[str, List[str]]:
        """Returns list of drugs for this visit, adding to overall mapping."""
        all_drugs = self.__subject_derived.get_value("drugs_list", dict)
        if all_drugs is None:
            all_drugs = {}

        if self.__formdate in all_drugs:
            raise AttributeDeriverError(
                f"Drugs list for frmdatea4g {self.__formdate} already exists"
            )

        drugs_list = self.__meds.get_value("drugs_list", str)
        all_drugs[self.__formdate] = (
            [x.strip().lower() for x in drugs_list.split(",")] if drugs_list else []
        )
        return all_drugs
