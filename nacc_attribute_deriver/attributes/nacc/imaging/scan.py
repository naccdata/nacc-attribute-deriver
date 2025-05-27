"""Derived variables that come from SCAN values."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCANNamespace,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date
from nacc_attribute_deriver.utils.scope import (
    SCANMRIScope,
    SCANPETScope,
)


class NACCSCANAttributeCollection(AttributeCollection):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table)

    def _create_scan_mri_dates(self) -> str:
        """Gets the date of the MRI scan - temporary derived variable."""
        scandate = self.__scan.scope(name=SCANMRIScope.MRI_QC).get_value("study_date")

        scandate = datetime_from_form_date(scandate)

        if not scandate:
            raise MissingRequiredError(
                message="study_date (from SCAN_MRI_QC) required",
                field="study_date",
            )

        return str(scandate.date())

    def _create_scan_pet_dates(self) -> str:
        """Gets the date of the PET scan - temporary derived variable"""
        scandate = self.__scan.scope(name=SCANPETScope.PET_QC).get_value("scan_date")

        scandate = datetime_from_form_date(scandate)
        if not scandate:
            raise MissingRequiredError(
                message="scan_date (from SCAN_PET_QC) required",
                field="scan_date",
            )

        return str(scandate.date())
