"""Derived variables that come from SCAN values."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    REQUIRED_FIELDS,
    MRIPrefix,
    PETPrefix,
    SCANNamespace,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class NACCSCANAttributeCollection(AttributeCollection):
    """Class to collect NACC SCAN attributes needed to derive MQT."""

    def __init__(self, table):
        self.__scan = SCANNamespace(table)

    def _create_scan_mri_dates(self) -> str:
        """Gets the date of the MRI scan - temporary derived variable."""
        # TODO: either studydate (mridashboard) or scandt (ucdmrisbm)
        # need to confirm how the data is represented in the table
        # do mridashboard then ucdmrisbm
        self.__scan.assert_required(REQUIRED_FIELDS[MRIPrefix.SCAN_MRI_QC])
        scandate = self.__scan.get_value("study_date")
        # if not scandate:
        #     scandate = self.get_mri_value('scandt', MRIPrefix.MRI_SBM)

        scandate = datetime_from_form_date(scandate)

        if not scandate:
            raise MissingRequiredError("study_date (from SCAN_MRI_QC) required")

        return str(scandate.date())

    def _create_scan_pet_dates(self) -> str:
        """Gets the date of the PET scan - temporary derived variable"""
        # TODO: either or scan_date(petdashboard) scandate (berkeley files)
        # need to confirm how the data is represented in the table
        # try petdashboard first, then berkeley files
        self.__scan.assert_required(REQUIRED_FIELDS[PETPrefix.SCAN_PET_QC])
        scandate = self.__scan.get_value("scan_date")
        # if not scandate:
        #     for subprefix in PETPrefix.analysis_files():
        #         scandate = self.get_pet_value('scandate', subprefix)

        scandate = datetime_from_form_date(scandate)
        if not scandate:
            raise MissingRequiredError("scan_date (from SCAN_PET_QC) required")

        return str(scandate.date())
