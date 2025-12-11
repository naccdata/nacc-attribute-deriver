"""Derived variables for MP scans (MRI and PET).

NOTE: This curation works a little differently, since
these derived variables are associated with a session, which
in turn has several scans/acquisitions. Since we curate by
acquisition/file, many of these variables may not update
with any "new" information if a previous image/acquisition
has already been evaluated, and everything is associated by
the scan date.

In short, it's pretty inefficient, because we only really
need to know about the session and not loop over each image
in the series. There are probably better ways to go about this,
but for now, this is the quick and dirty way that fits into
the current framework.
"""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.image_namespace import (
    MixedProtocolNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    date_from_form_date,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class MPAttributeCollection(AttributeCollection):
    """Attribute collection for mixed protocol."""

    def __init__(self, table: SymbolTable) -> None:
        self.__mp = MixedProtocolNamespace(table=table)
        self.__working = WorkingNamespace(table=table)
        self.__subject = SubjectDerivedNamespace(table=table)

    @property
    def mp(self) -> MixedProtocolNamespace:
        return self.__mp

    @property
    def working(self) -> WorkingNamespace:
        return self.__working

    def get_date(self) -> Optional[date]:
        return self.__mp.study_date

    def calculate_age_at_scan(self) -> int:
        """Calculate age at scan from UDS DOB."""
        uds_dob = self.__working.get_cross_sectional_value("uds-date-of-birth", str)

        if not uds_dob:
            return 888

        age = calculate_age(date_from_form_date(uds_dob), self.__mp.study_date)
        # only allow 18-120
        return min(max(age, 18), 120) if age is not None else 888

    def calculate_days_from_closest_uds_visit(self) -> int:
        """Create the NACCMRDY variable.

        Days between session and closest UDS visit. We assume
        all of UDS has been curated by the time we are looking
        at imaging data.

        For sessions before the closest visidate, days < 0.
        For sessions after the closeset visitdate, days > 0.
        8888 If not applicable/no image available.
        """
        visitdates = self.__working.get_cross_sectional_value("uds-visitdates", list)
        if not visitdates:
            return 8888

        # basically return whatever has the smallest absolute value
        # could probably put in some checks to stop early, but honestly
        # trivial to just loop through all of them
        lowest = None
        for visit_str in visitdates:
            visit = date_from_form_date(visit_str)
            if not visit:
                raise AttributeDeriverError(
                    f"Unable to parse UDS visitdate {visit_str}"
                )

            result = (self.__mp.study_date - visit).days
            if lowest is None or abs(result) < abs(lowest):
                lowest = result

        return lowest if lowest is not None else 8888

    def get_filename(self, attribute: str) -> str:
        """File locator variable.

        NOTE: FILENAME IS DIFFERENT IN LEGACY VS NEW. In the legacy system,
        this was the name of the aggregate zip file in S3. However, in FW,
        each image is attached as a separate file to the session. So instead
        we are aggregating each curated dicom as a comma-deliminated list.

        Args:
            attribute: The attribute name to grab current longitudinal
                date from
        """
        # grab attribute if it already exists and append filename to it
        filenames = self.__subject.get_corresponding_longitudinal_value(
            str(self.__mp.study_date), attribute, str
        )
        if filenames is not None:
            return f"{filenames.strip()},{self.__mp.filename}"

        return self.__mp.filename

    def get_num_sessions(self, sessions_field: str) -> int:
        """Get total number of sessions.

        sessions_field: Cross-sectional working field to get session
        dates form; should be mri-sessions or pet-sessions.
        """
        sessions = self.__working.get_cross_sectional_value(sessions_field, list)
        if not sessions:
            return 88

        # only allow 1-20
        return min(len(sessions), 20)

    def generate_image_session(self) -> str:
        """Create variable to keep track of unique sessions, based on study
        date."""
        return str(self.__mp.study_date)


class MPMRIAttributeCollection(MPAttributeCollection):
    """Attribute collection for MP MRIs."""

    def _create_naccdico(self) -> int:
        """Create the NACCDICO variable.

        DICOM image file available (y/n). True if the current thing
        we're curating is NOT a nifti file (since at the moment we only
        curate on DICOMs and NIfTIs). Needs to check if another image in
        the session has already set this value to 1.

        This should only ever be called in the context of a DICOM image/scope,
        so always return 1.
        """
        return 1

    def _create_naccnift(self) -> int:
        """Create the NACCNIFT variable.

        NIFTI image file available (y/n). True if the current thing
        we're curating is a nifti file. Needs to check if another image
        in the session has already set this value to 1.

        This should only ever be called in the context of a NIFTI image/scope,
        so always return 1.
        """
        return 1

    def _create_naccmria(self) -> int:
        """Create the NACCMRIA variable.

        Subject age at time of MRI. Derives from UDS DOB.
        """
        return self.calculate_age_at_scan()

    def _create_naccmrfi(self) -> Optional[str]:
        """Create the NACCMRFI variable.

        File locator variable.
        """
        return self.get_filename("naccmrfi")

    def _create_naccnmri(self) -> int:
        """Create the NACCNMRI variable.

        Total number of MRI sessions
        """
        return self.get_num_sessions("mri-sessions")

    def _create_naccmnum(self) -> int:
        """Create the NACCMNUM variable.

        MRI session in chronological order. This corresponds to how many
        mri-sessions we have logged at the given point in time, which
        happens to also be NACCNMRI (but NACCNMRI gets updated with each
        session to eventually account for the grand total).
        """
        return self._create_naccnmri()

    def _create_naccmrdy(self) -> int:
        """Create the NACCMRDY variable.

        Days between MRI session and closest UDS visit.
        """
        return self.calculate_days_from_closest_uds_visit()

    def _create_naccmrsa(self) -> int:
        """Create the NACCMRSA variable.

        At least one MRI scan available. If this is called at all then
        that means an MRI exists, so set to 1.
        """
        return 1

    def _create_mri_image_session(self) -> str:
        """Create variable to keep track of unique MRI sessions, based on study
        date."""
        return self.generate_image_session()


class MPPETAttributeCollection(MPAttributeCollection):
    """Attribute collection for MP PETs."""

    def _create_naccapta(self) -> Optional[int]:
        """Create the NACCAPTA variable.

        Subject age at time of amyloid PET scan. Derives from UDS DOB.
        """
        return self.calculate_age_at_scan()

    def _create_naccaptf(self) -> Optional[str]:
        """Create the NACCAPTF variable.

        Amyloid PET scan file locator variable
        """
        return self.get_filename("naccaptf")

    def _create_naccnapa(self) -> int:
        """Create the NACCNAPA variable.

        Total number of amyloid PET scans available.
        """
        return self.get_num_sessions("pet-sessions")

    def _create_naccapnm(self) -> int:
        """Create the NACCAPNM variable.

        PET sessions in chronological order. This corresponds to how
        many pet-sessions we have logged at the given point in time,
        which happens to also be NACCNAPA (but NACCNAPA gets updated
        with each session to eventually account for the grand total).
        """
        return self._create_naccnapa()

    def _create_naccaptd(self) -> int:
        """Create the NACCAPTD variable.

        Days between PET session and closest UDS visit.
        """
        return self.calculate_days_from_closest_uds_visit()

    def _create_naccapsa(self) -> int:
        """Create the NACCAPSA variable.

        At least one PET scan available. If this is called at all then
        that means a PET exists, so set to 1.
        """
        return 1

    def _create_pet_image_session(self) -> str:
        """Create variable to keep track of unique PET sessions, based on study
        date."""
        return self.generate_image_session()
