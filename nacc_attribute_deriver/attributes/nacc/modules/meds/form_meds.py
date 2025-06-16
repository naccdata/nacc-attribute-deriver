"""Handles the MEDS form.

This is mainly used to inform UDS A4 NACC derived variables.
"""

from typing import Dict, List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


class MEDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        date_attribute = "frmdatea4g"
        self.__meds = FormNamespace(table=table, date_attribute=date_attribute)
        self.__formdate = self.__meds.get_required(date_attribute, str)

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
