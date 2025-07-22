"""Derived variables from MP form."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_days,
    calculate_months,
    datetime_from_form_date,
)

from .mp_summary import MP_SUMMARY_VALUES


class MPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an MP form.

        TODO: figure out what is a required/expected variable for MP
        """
        self.__mp = FormNamespace(table=table)

        # TODO: not sure MP will have a module field
        # module = self.__mp.get_required("module", str)
        # if not module or module.upper() != "MP":
        #     msg = f"Current file is not an MP form: found {module}"
        #     raise InvalidFieldError(msg)

    def _create_naccnift(self) -> int:
        """Create the NACCNIFT variable.

        NIFTI image file available (y/n)
        """
        nifti = self.__mp.get_value("nifti", int)
        return 1 if nifti == 1 else 0

    def _create_naccapnm(self) -> int:
        """Create the NACCAPNM variable.

        Amyloid PET scan in chronological order
        """
        is_first_file = self.__mp.get_value("is_first_file", int)
        prev_value = self.__mp.get_value("prev_naccapnm", int)

        # TODO - figure out valid "true" values for these
        if is_first_file is not None and is_first_file:
            return 1
        if prev_value is not None:
            return prev_value + 1

        return 8

    def _create_naccmrfi(self) -> Optional[str]:
        """Create the NACCMRFI variable.

        File locator variable
        """
        filename = self.__mp.get_value("filename", str)
        if filename and filename.strip():
            return filename.strip()

        # change default to None since empty string is not useful
        return None

    def _create_naccaptf(self) -> Optional[str]:
        """Create the NACCAPTF variable.

        Amyloid PET scan file locator variable
        """
        filename = self.__mp.get_value("filename", str)
        if filename and filename.strip():
            return filename.strip()

        # Didn't have a default return variable
        return None

    def _create_naccdico(self) -> int:
        """Create the NACCDICO variable.

        DICOM image file available (y/n)
        """
        value = self.__mp.get_value("naccdico", int)
        return value if value is not None else 0

    def _create_naccnmri(self) -> int:
        """Create the NACCNMRI variable.

        Total number of MRI sessions
        """
        value = self.__mp.get_value("naccnmri", int)
        return value if value is not None else 88

    def _create_naccmnum(self) -> int:
        """Create the NACCMNUM variable.

        MRI session in chronological order
        """
        value = self.__mp.get_value("naccmnum", int)
        return value if value is not None else 0

    def _create_naccmrdy(self) -> int:
        """Create the NACCMRDY variable.

        Days between MRI session and closest UDS visit
        """
        # TODO: don't know if dates are in the expected format
        mridate = datetime_from_form_date(self.__mp.get_value("mridate", str))
        visitdate = datetime_from_form_date(self.__mp.get_value("visitdate", str))
        days = calculate_days(mridate, visitdate)

        return days if days is not None else 8888

    def _create_naccmria(self) -> int:
        """Create the NACCMRIA variable.

        Subject age at time of MRI
        """
        # TODO: don't know if dates are in the expected format
        birthdate = datetime_from_form_date(self.__mp.get_value("birthdate", str))
        tmridate = datetime_from_form_date(self.__mp.get_value("tmridate", str))
        months = calculate_months(birthdate, tmridate)

        return months if months is not None else 888

    def _create_naccapta(self) -> Optional[int]:
        """Create the NACCAPTA variable.

        Subject age at time of amyloid PET scan
        """
        # TODO: don't know if dates are in the expected format
        birthdate = datetime_from_form_date(self.__mp.get_value("birthdate", str))
        tpetdate = datetime_from_form_date(self.__mp.get_value("tpetdate", str))
        months = calculate_months(birthdate, tpetdate)

        # TODO no specified default; use 888 for now like NACCMRIA
        return months if months is not None else 888

    def _create_naccaptd(self) -> int:
        """Create the NACCAPTD variable.

        Days between amyloid PET scan and closest UDS visit
        """
        # TODO: don't know if dates are in the expected format
        apetdate = datetime_from_form_date(self.__mp.get_value("apetdate", str))
        visitdate = datetime_from_form_date(self.__mp.get_value("visitdate", str))
        days = calculate_days(apetdate, visitdate)

        return days if days is not None else 8

    def _get_valid_float_value(self, attribute: str) -> Optional[float]:
        """Get valid float values; ignores values like 9999.9999 or 8888.8888
        and return None instead for those cases.

        Args:
            attribute: Name of attribute to grab; expected to be float
        """
        value = self.__mp.get_value(attribute, float)
        if value in [None, 9999.9999, 8888.8888, 888.888, 88.888, 8.888]:
            return None

        return value

    def _create_naccicv(self) -> float:
        """Create the NACCICV variable.

        Total intercranial volume (cc)
        """
        gray = self._get_valid_float_value("grayvol")
        white = self._get_valid_float_value("whitevol")
        csf = self._get_valid_float_value("csfvol")
        wmh = self._get_valid_float_value("wmhvol")

        if all(v is not None for v in [gray, white, csf, wmh]):
            return round(gray + white + csf + wmh, 3)  # type: ignore

        return 9999.999

    def _create_naccwmvl(self) -> float:
        """Create the NACCWMVL variable.

        Total white matter volume (cc)
        """
        white = self._get_valid_float_value("whitevol")
        wmh = self._get_valid_float_value("wmhvol")

        if white is not None and wmh is not None:
            return round(white + wmh, 3)

        return 9999.999

    def _create_naccbrnv(self) -> float:
        """Create the NACCBRNV variable.

        Total brain volume (cc)
        """
        gray = self._get_valid_float_value("grayvol")
        white = self._get_valid_float_value("whitevol")

        if gray is not None and white is not None:
            return round(gray + white, 3)

        return 9999.999

    def _create_naccmvol(self) -> int:
        """Create the NACCMVOL variable.

        Calculated summary data available (y/n)
        """
        if all(self._get_valid_float_value(x) for x in MP_SUMMARY_VALUES):
            return 0

        return 1

    # These three are seemingly just returning a different variable. From derive.sas
    # TODO: these might instead be uds/cross-sectional variables that look at derived
    # variables? However these don't seem to be actual variables

    def _create_naccmrsa(self) -> int:
        """Create the NACCMRSA variable.

        At least one MRI scan available
        """
        naccmri = self.__mp.get_value("naccmri", int)

        if naccmri is None:
            return 0
        return naccmri

    def _create_naccnapa(self) -> int:
        """Create the NACCNAPA variable.

        Total number of amyloid PET scans available
        """
        naccnapt = self.__mp.get_value("naccnapt", int)

        if naccnapt == 1:
            return 1
        return 0

    def _create_naccapsa(self) -> int:
        """Create the NACCAPSA variable.

        At least one amyloid PET scan available (y/n)
        """
        naccapet = self.__mp.get_value("naccapet", int)

        if naccapet == 1:
            return 1
        return 0
