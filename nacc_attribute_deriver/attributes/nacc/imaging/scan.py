"""Derived variables that come from SCAN values."""
from typing import Optional

from nacc_attribute_deriver.attributes.base.base_attributes import (
    NACCAttribute,
    SCANAttribute,
)
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class NACCSCANAttribute(NACCAttribute, SCANAttribute):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def _create_scan_mri_year(self) -> Optional[str]:
        """Gets the date of the MRI scan - temporary derived variable.

        Location:
            subject.info.derived.scan_mri_dates
        Operation:
            set
        Type:
            longitudinal
        Description:
            Date of MRI SCAN
        """
        scandate = datetime_from_form_date(
            self.get_mri_value('scandt'))  # TODO: double check this is the date we want
        return str(scandate.date()) if scandate else None

    def _create_scan_pet_year(self) -> Optional[str]:
        """Gets the date of the PET scan - temporary derived variable

        Location:
            subject.info.derived.scan_pet_dates
        Operation:
            set
        Type:
            longitudinal
        Description:
            Date of PET SCAN
        """
        scandate = datetime_from_form_date(
            self.get_pet_value('scan_date'))  # TODO: double check this is the date we want
        return str(scandate.date()) if scandate else None
