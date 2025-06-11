"""Derived variables that come from SCAN values."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCAN_REQUIRED_FIELDS,
    SCANNamespace,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.utils.date import datetime_from_form_date
from nacc_attribute_deriver.utils.scope import (
    SCANMRIScope,
    SCANPETScope,
)


class NACCSCANAttributeCollection(AttributeCollection):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def __init__(self, table):
        self.__scan = SCANNamespace(table)

    def _create_scan_mri_dates(self) -> str:
        """Gets the date of the MRI scan - temporary derived variable."""
        self.__scan.assert_required(SCAN_REQUIRED_FIELDS[SCANMRIScope.MRI_QC])
        scandate = self.__scan.get_value("study_date")

        scandate = datetime_from_form_date(scandate)

        if not scandate:
            raise MissingRequiredError(
                fields=["study_date"],
            )

        return str(scandate.date())

    def _create_scan_pet_dates(self) -> str:
        """Gets the date of the PET scan - temporary derived variable"""
        self.__scan.assert_required(SCAN_REQUIRED_FIELDS[SCANPETScope.PET_QC])
        scandate = self.__scan.get_value("scan_date")

        scandate = datetime_from_form_date(scandate)
        if not scandate:
            raise MissingRequiredError(
                fields=["scan_date"],
            )

        return str(scandate.date())
