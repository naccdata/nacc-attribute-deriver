"""Derived variables that come from SCAN values."""

from typing import Optional

from nacc_attribute_deriver.attributes.base.base_attribute import NACCAttribute
from nacc_attribute_deriver.attributes.base.scan_attribute import (
    MRIPrefix,
    PETPrefix,
    SCANAttribute,
)
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class NACCSCANAttribute(NACCAttribute, SCANAttribute):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def _create_scan_mri_dates(self) -> Optional[str]:
        """Gets the date of the MRI scan - temporary derived variable."""
        # TODO: either studydate (mridashboard) or scandt (ucdmrisbm)
        # need to confirm how the data is represented in the table
        # do mridashboard then ucdmrisbm
        scandate = self.get_mri_value("studydate", MRIPrefix.SCAN_MRI_QC)
        if not scandate:
            scandate = self.get_mri_value("scandt", MRIPrefix.MRI_SBM)

        scandate = datetime_from_form_date(scandate)
        return str(scandate.date()) if scandate else None

    def _create_scan_pet_dates(self) -> Optional[str]:
        """Gets the date of the PET scan - temporary derived variable"""
        # TODO: either or scan_date(petdashboard) scandate (berkeley files)
        # need to confirm how the data is represented in the table
        # try petdashboard first, then berkeley files
        scandate = self.get_pet_value("scan_date", PETPrefix.SCAN_PET_QC)
        if not scandate:
            for subprefix in PETPrefix.analysis_files():
                scandate = self.get_pet_value("scandate", subprefix)

        scandate = datetime_from_form_date(scandate)
        return str(scandate.date()) if scandate else None
