"""Derived variables that come from SCAN values."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCANMRINamespace,
    SCANPETNamespace,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.utils.date import date_from_form_date
from nacc_attribute_deriver.utils.scope import (
    SCANMRIScope,
    SCANPETScope,
)


class NACCSCANMRIAttributeCollection(AttributeCollection):
    """Class to collect NACC MRI SCAN attributes needed to derive MQT."""

    def __init__(self, table):
        self.__mri_qc = SCANMRINamespace(table, scope=SCANMRIScope.MRI_QC)

    def _create_scan_mri_dates(self) -> str:
        """Gets the date of the MRI scan - temporary derived variable."""
        raw_scandate = self.__mri_qc.get_required("study_date", str)
        scandate = date_from_form_date(raw_scandate)

        if not scandate:
            raise InvalidFieldError(f"Failed to parse scandate: {raw_scandate}")

        return str(scandate)


class NACCSCANPETAttributeCollection(AttributeCollection):
    """Class to collect NACC PET SCAN attributes needed to derive MQT."""

    def __init__(self, table):
        self.__pet_qc = SCANPETNamespace(table, scope=SCANPETScope.PET_QC)

    def _create_scan_pet_dates(self) -> str:
        """Gets the date of the PET scan - temporary derived variable"""
        raw_scandate = self.__pet_qc.get_required("scan_date", str)
        scandate = date_from_form_date(raw_scandate)

        if not scandate:
            raise InvalidFieldError(f"Failed to parse scandate: {raw_scandate}")

        return str(scandate)
