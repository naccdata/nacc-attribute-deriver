"""All SCAN MQT derived variables.

Assumes NACC-derived variables are already set
"""
from typing import Optional

from nacc_attribute_deriver.attributes.base.base_attributes import (
    MQTAttribute,
    SCANAttribute,
)
from nacc_attribute_deriver.utils.date import get_unique_years


class MQTSCANAttribute(MQTAttribute, SCANAttribute):
    """Class to collect MQT SCAN attributes."""

    def _create_scan_mri_scan_types(self) -> Optional[str]:
        """Access SeriesType (scan_mridashboard file)

        Location:
            subject.info.mri.scan.types
        Operation:
            set
        Type:
            scan
        Description:
            SCAN MRI scan types available
        """
        return self.get_mri_value('seriestype')

    # Warning: The max operation operates on ints, so there
    # feels like some awkwardness with operating on a bool
    # Warning: Perhaps need to be careful about pulling
    # cerebrumtcv from the table and casting as a float
    # --could generate exceptions. Similar story below
    # with casting as int() and bool() as well. Perhaps
    # worth wrapping the cast:
    # https://stackoverflow.com/questions/6330071/safe-casting-in-python
    # Note: Might not need to explicitly check on scan type here,
    # as non-null cerebrumtcv probably implies the type
    def _create_volume_analysis_indicator(self) -> bool:
        """Access SeriesType (scan_mridashboard file) and cerebrumtcv
        (ucdmrisbm file)

        Location:
            subject.info.imaging.mri.scan.t1.brain-volume
        Operation:
            max
        Type:
            scan
        Description:
            SCAN T1 brain volume analysis results available
        """
        if self.get_mri_value('seriestype') != 'T1w':
            return False

        try:
            cerebrumtcv = float(self.get_mri_value("cerebrumtcv"))
        except (ValueError, TypeError):
            return False

        return bool(cerebrumtcv)

    def _create_t1_wmh_indicator(self) -> bool:
        """Access SeriesType (scan_mridashboard file) and wmh (ucdmrisbm file)

        Location:
            subject.info.imaging.mri.scan.t1.wmh
        Operation:
            max
        Type:
            scan
        Description:
            SCAN T1 WMH analysis available available
        """
        if self.get_mri_value('seriestype') != 'T1w':
            return False

        try:
            wmh = float(self.get_mri_value("wmh"))
        except (ValueError, TypeError):
            return False

        return bool(wmh)

    def _create_flair_wmh_indicator(self) -> bool:
        """Access SeriesType (scan_mridashboard file) and wmh (ucdmrisbm file)

        Location:
            subject.info.imaging.mri.scan.flair.wmh
        Operation:
            max
        Type:
            scan
        Description:
            SCAN FLAIR WMH analysis available
        """
        if self.get_mri_value('seriestype') != 'T2w':
            return False

        try:
            wmh = float(self.get_mri_value("wmh"))
        except (ValueError, TypeError):
            return False

        return bool(wmh)

    def _create_flair_volume_analysis_indicator(self) -> bool:
        """Access SeriesType (scan_mridashboard file) and cerebrumtcv
        (ucdmrisbm file)

        Location:
            subject.info.imaging.mri.scan.flair.brain-volume
        Operation:
            max
        Type:
            scan
        Description:
            SCAN FLAIR brain volume analysis results available
        """
        if self.get_mri_value('seriestype') != 'T2w':
            return False

        try:
            cerebrumtcv = float(self.get_mri_value("cerebrumtcv"))
        except (ValueError, TypeError):
            return False

        return bool(cerebrumtcv)

    # Note: Probably should be "tracer_types"
    def _create_scan_pet_scan_types(self) -> Optional[str]:
        """Access radiotracer (scan_petdashboard) and map to.

        {amyloid, tau, fdg}

        Location:
            subject.info.pet.scan.types
        Operation:
            set
        Type:
            scan
        Description:
            SCAN PET types available
        """
        return self.get_tracer()

    def _create_scan_pet_amyloid_tracers(self) -> Optional[str]:
        """Access radiotracer (scan_petdashboard) and map to names of tracers.

        Location:
            subject.info.pet.scan.amyloid.tracers
        Operation:
            set
        Type:
            scan
        Description:
            SCAN Amyloid tracers available
        """
        if self.get_scan_type() == "amyloid":
            return self.get_tracer()

        return None

    # Note: Be careful about the float return type here with the min computation.
    def _create_scan_pet_centaloid(self) -> Optional[float]:
        """Access CENTILOIDS in UC Berkeley GAAIN analysis.

        Location:
            subject.info.imaging.pet.scan.amyloid.centiloid.min
        Operation:
            min
        Type:
            scan
        Description:
            SCAN Amyloid PET scans centiloid min
        """
        return self.get_centiloid()

    def _create_scan_pet_centaloid_pib(self) -> Optional[float]:
        """Access CENTILOIDS in UC Berkeley GAAIN analysis.

        Location:
            subject.info.imaging.pet.scan.amyloid.pib.centiloid.min
        Operation:
            min
        Type:
            scan
        Description:
            SCAN Amyloid PET scans with PIB centiloid min
        """
        if self.get_tracer() == "pib":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetapir(self) -> Optional[float]:
        """A ccess CENTILOIDS in UC Berkeley GAAIN analysis.

        Location:
            subject.info.imaging.pet.scan.amyloid.florbetapir.centiloid.min
        Operation:
            min
        Type:
            scan
        Description:
            SCAN Amyloid PET scans with Florbetapir centiloid min
        """
        if self.get_tracer() == "florbetapir":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetaben(self) -> Optional[float]:
        """Access CENTILOIDS in UC Berkeley GAAIN analysis.

        Location:
            subject.info.imaging.pet.scan.amyloid.florbetaben.centiloid.min
        Operation:
            min
        Type:
            scan
        Description:
            SCAN Amyloid PET scans with Florbetaben centiloid min
        """
        if self.get_tracer() == "florbetaben":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_nav4694(self) -> Optional[float]:
        """Access CENTILOIDS in UC Berkeley GAAIN analysis.

        Location:
            subject.info.imaging.pet.scan.amyloid.nav4694.centiloid.min
        Operation:
            min
        Type:
            scan
        Description:
            SCAN Amyloid PET scans with NAV4694 centiloid min
        """
        if self.get_tracer() == "nav4694":
            return self.get_centiloid()

        return None

    def _create_scan_pet_amyloid_positivity_indicator(self) -> Optional[bool]:
        """Access AMYLOID_STATUS in UC Berkeley GAAIN analysis
        TODO: is this a string/int value> may need to cast to int first since
        strings always evaluate to true?

        Location:
            subject.info.imaging.pet.scan.amyloid.positive-scans
        Operation:
            max
        Type:
            scan
        Description:
            SCAN Amyloid positive scans available
        """
        return bool(self.get_mri_value("amyloid_status"))

    def _create_scan_pet_tau_tracers(self) -> Optional[str]:
        """Access radiotracer (scan_petdashboard) and map to names of tracers.

        Location:
            subject.info.imaging.pet.scan.tau.tracers
        Operation:
            set
        Type:
            scan
        Description:
            SCAN tau tracers available
        """
        if self.get_scan_type() == "tau":
            return self.get_tracer()

        return None

    def _create_scan_mri_count(self):
        """Number of SCAN MRI scans available.

        TODO: Where to to get count?

        Location:
            subject.info.imaging.mri.scan.count
        Operation:
            count
        Type:
            scan
        Description:
            Number of SCAN MRI scans available
        """
        pass

    def _create_scan_pet_count(self):
        """Number of SCAN PET scans available.

        TODO: Where to to get count?

        Location:
            subject.info.imaging.pet.scan.count
        Operation:
            count
        Type:
            scan
        Description:
            Number of SCAN PET scans available
        """
        pass

    def _create_scan_mri_year_count(self) -> int:
        """Years of SCAN MRI scans available.

        Does this similar to years of UDS where it keeps track of a
        "NACC" derived variable scan_years which is a list of all
        years a participant has SCAN data in. This create method
        then just counts the distinct years.

        Location:
            subject.info.imaging.mri.scan.year-count
        Operation:
            max
        Type:
            scan
        Description:
            Years of SCAN MRI scans available
        """
        result = self.assert_required(['scan_mri_dates'],
                                      prefix='subject.info.derived.')
        return len(get_unique_years(result['scan_mri_dates']))

    def _create_scan_pet_year_count(self) -> int:
        """Years of SCAN PET scans available.

        Location:
            subject.info.imaging.pet.scan.year-count
        Operation:
            max
        Type:
            scan
        Description:
            Years of SCAN PET scans available
        """
        result = self.assert_required(['scan_pet_dates'],
                                      prefix='subject.info.derived.')
        return len(get_unique_years(result['scan_pet_dates']))
