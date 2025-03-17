"""Derived variables that come from SCAN values."""
from typing import Optional

from nacc_attribute_deriver.attributes.base.base_attribute import NACCAttribute
from nacc_attribute_deriver.attributes.base.scan_attribute import SCANAttribute
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class NACCSCANAttribute(NACCAttribute, SCANAttribute):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def _create_scan_mri_dates(self) -> Optional[str]:
        """Gets the date of the MRI scan - temporary derived variable.

        Location:
            subject.info.derived.scan_mri_dates
        Operation:
            sortedlist
        Type:
            longitudinal
        Description:
            Date of MRI SCAN
        """
        # TODO: either studydate (mridashboard) or scandt (ucdmrisbm)
        # need to confirm how the data is represented in the table
        # do mridashboard then ucdmrisbm
        scandate = self.get_mri_value('studydate')
        if not scandate:
            scandate = self.get_mri_value('scandt')

        scandate = datetime_from_form_date(scandate)
        return str(scandate.date()) if scandate else None

    def _create_scan_pet_dates(self) -> Optional[str]:
        """Gets the date of the PET scan - temporary derived variable

        Location:
            subject.info.derived.scan_pet_dates
        Operation:
            sortedlist
        Type:
            longitudinal
        Description:
            Date of PET SCAN
        """
        # TODO: either or scan_date(petdashboard) scandate (berkeley files)
        # need to confirm how the data is represented in the table
        # try petdashboard first, then berkeley files
        scandate = self.get_pet_value('scan_date')
        if not scandate:
            scandate = self.get_pet_value('scandate')

        scandate = datetime_from_form_date(scandate)
        return str(scandate.date()) if scandate else None
