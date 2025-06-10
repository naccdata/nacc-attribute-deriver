"""Derived variables that come from SCAN values."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCAN_REQUIRED_FIELDS,
    SCANNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date
from nacc_attribute_deriver.utils.scope import (
    SCANMRIScope,
    SCANPETScope,
)


class SCANMRIAttributeCollection(AttributeCollection):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def __init__(self, table: SymbolTable):
        mri_required = SCAN_REQUIRED_FIELDS.get(SCANMRIScope.MRI_QC)
        self.__scan_mri = SCANNamespace(
            table=table,
            required=frozenset(mri_required),  # type: ignore
        )

    def _create_scan_mri_dates(self) -> str:
        """Gets the date of the MRI scan - temporary derived variable."""
        scandate = self.__scan_mri.get_value("study_date")
        assert scandate is not None

        scandate = datetime_from_form_date(scandate)

        return str(scandate.date())


class SCANPETAttributeCollection(AttributeCollection):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def __init__(self, table: SymbolTable):
        pet_required = SCAN_REQUIRED_FIELDS.get(SCANPETScope.PET_QC)
        self.__scan_pet = SCANNamespace(
            table=table,
            required=frozenset(pet_required),  # type: ignore
        )

    def _create_scan_pet_dates(self) -> str:
        """Gets the date of the PET scan - temporary derived variable"""
        scandate = self.__scan_pet.get_value("scan_date")
        assert scandate is not None

        scandate = datetime_from_form_date(scandate)

        return str(scandate.date())
