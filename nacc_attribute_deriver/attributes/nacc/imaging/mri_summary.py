"""Derives variables using MRI summary data."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class MRISummaryAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__mri_summary = RawNamespace(table)

    def _get_valid_float_value(self, attribute: str) -> Optional[float]:
        """Get valid float values; ignores values like 9999.9999 or 8888.8888
        and return None instead for those cases.

        Args:
            attribute: Name of attribute to grab; expected to be float
        """
        value = self.__mri_summary.get_value(attribute, float)

        if value in MRI_SUMMARY_INVALID_VALUES:
            return None

        return value

    def _create_naccmvol(self) -> int:
        """Creates NACCMVOL: Calculated summary data available (y / n).

        Set to 1 if ANY of the summary values are not invalid/missing, 0
        otherwise. If this create method is called at all, assumes the
        MRI exists. This variable will be set to 8 for missingness if
        the MRI does not exist.
        """
        for field in MRI_SUMMARY_FIELDS:
            if self._get_valid_float_value(field) is not None:
                return 1

        return 0

    def _create_naccicv(self) -> float:
        """Creates NACCICV: Total intracranial volume (cc)

        Sums the intracranial volume fields, or 9999.999 if cannot
        be calculated.

        If this create method is called at all, assumes the MRI exists.
        This variable will be set to 8888.888 for missingness if the
        MRI does not exist.
        """
        gray = self._get_valid_float_value("grayvol")
        white = self._get_valid_float_value("whitevol")
        csf = self._get_valid_float_value("csfvol")
        wmh = self._get_valid_float_value("wmhvol")

        if all(v is not None for v in [gray, white, csf, wmh]):
            return round(gray + white + csf + wmh, 3)  # type: ignore

        return 9999.999

    def _create_naccwmvl(self) -> float:
        """Create the NACCWMVL variable: Total white matter volume (cc)

        Sums the white matter volume fields, or 9999.999 if cannot
        be calculated.

        If this create method is called at all, assumes the MRI exists.
        This variable will be set to 8888.888 for missingness if the
        MRI does not exist.
        """
        white = self._get_valid_float_value("whitevol")
        wmh = self._get_valid_float_value("wmhvol")

        if white is not None and wmh is not None:
            return round(white + wmh, 3)

        return 9999.999

    def _create_naccbrnv(self) -> float:
        """Create the NACCBRNV variable: Total brain volume (cc)

        Sums the brain volume fields, or 9999.999 if cannot
        be calculated.

        If this create method is called at all, assumes the MRI exists.
        This variable will be set to 8888.888 for missingness if the
        MRI does not exist.
        """
        gray = self._get_valid_float_value("grayvol")
        white = self._get_valid_float_value("whitevol")

        if gray is not None and white is not None:
            return round(gray + white, 3)

        return 9999.999


# TODO: from the RDD is appears we can have either 3 or 4 decimal spots
# from the tens to thousands.
# hopefully this covers all cases; if not something more programmatic
# might need to be done here instead
MRI_SUMMARY_INVALID_VALUES = {
    None,
    9999.9999,
    999.9999,
    99.9999,
    9.9999,
    9999.999,
    999.999,
    99.999,
    9.999,
    8888.8888,
    888.8888,
    88.8888,
    8.8888,
    8888.888,
    888.888,
    88.888,
    8.888,
}


MRI_SUMMARY_FIELDS = {
    "csfvol",
    "grayvol",
    "whitevol",
    "wmhvol",
    "hippovol",
    "cereall",
    "ceretiss",
    "cerecsf",
    "ceregr",
    "cerewh",
    "lhippo",
    "rhippo",
    "llatvent",
    "rlatvent",
    "latvent",
    "thirvent",
    "lfrcort",
    "rfrcort",
    "frcort",
    "loccort",
    "roccort",
    "occcort",
    "lparcort",
    "rparcort",
    "parcort",
    "ltempcor",
    "rtempcor",
    "tempcor",
    "lcac",
    "lcacm",
    "lcmf",
    "lcmfm",
    "lcun",
    "lcunm",
    "lent",
    "lentm",
    "lfus",
    "lfusm",
    "linfpar",
    "linfparm",
    "linftemp",
    "linftemm",
    "linsula",
    "linsulam",
    "listhc",
    "listhcm",
    "llatocc",
    "llatoccm",
    "llatorbf",
    "llatorbm",
    "lling",
    "llingm",
    "lmedorbf",
    "lmedorbm",
    "lmidtemp",
    "lmidtemm",
    "lparcen",
    "lparcenm",
    "lparhip",
    "lparhipm",
    "lparsop",
    "lparsopm",
    "lparorb",
    "lparorbm",
    "lpartri",
    "lpartrim",
    "lpercal",
    "lpercalm",
    "lposcen",
    "lposcenm",
    "lposcin",
    "lposcinm",
    "lprecen",
    "lprecenm",
    "lprecun",
    "lprecunm",
    "lrosanc",
    "lrosancm",
    "lrosmf",
    "lrosmfm",
    "lsupfr",
    "lsupfrm",
    "lsuppar",
    "lsupparm",
    "lsuptem",
    "lsuptemm",
    "lsupmar",
    "lsupmarm",
    "ltrtem",
    "ltrtemm",
    "rcac",
    "rcacm",
    "rcmf",
    "rcmfm",
    "rcun",
    "rcunm",
    "rent",
    "rentm",
    "rfus",
    "rfusm",
    "rinfpar",
    "rinfparm",
    "rinftemp",
    "rinftemm",
    "rinsula",
    "rinsulam",
    "risthc",
    "risthcm",
    "rlatocc",
    "rlatoccm",
    "rlatorbf",
    "rlatorbm",
    "rling",
    "rlingm",
    "rmedorbf",
    "rmedorbm",
    "rmidtemp",
    "rmidtemm",
    "rparcen",
    "rparcenm",
    "rparhip",
    "rparhipm",
    "rparsop",
    "rparsopm",
    "rparorb",
    "rparorbm",
    "rpartri",
    "rpartrim",
    "rpercal",
    "rpercalm",
    "rposcen",
    "rposcenm",
    "rposcin",
    "rposcinm",
    "rprecen",
    "rprecenm",
    "rprecun",
    "rprecunm",
    "rrosanc",
    "rrosancm",
    "rrosmf",
    "rrosmfm",
    "rsupfr",
    "rsupfrm",
    "rsuppar",
    "rsupparm",
    "rsuptem",
    "rsuptemm",
    "rsupmar",
    "rsupmarm",
    "rtrtem",
    "rtrtemm",
}
