"""Derived variables that come from SCAN values."""
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import NACCAttribute
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class SCANRawAttribute(NACCAttribute):
    """Class to collect raw SCAN attributes needed to derive MQT."""

    def _create_scan_mri_year(self) -> Optional[int]:
        """Gets the year of the MRI scan.

        Location:
            subject.info.derived.scan_mri_years
        Operation:
            set
        Type:
            longitudinal
        Description:
            Year of MRI SCAN
        """
        scandate = datetime_from_form_date(
            self.get_value('TODO GET SCAN DATE'))
        return scandate.year if scandate else None

    def _create_scan_pet_year(self) -> Optional[int]:
        """Gets the year of the PET scan.

        Location:
            subject.info.derived.scan_pet_years
        Operation:
            set
        Type:
            longitudinal
        Description:
            Year of PET SCAN
        """
        scandate = datetime_from_form_date(
            self.get_value('TODO GET SCAN DATE'))
        return scandate.year if scandate else None
