# What to import still needs to be defined.

"""Derived variables from MP form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver. # ...

class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an MP form."""
        self.__mp = FormNamespace(table)

        module = self.__mp.get_value("module")
        if not module or module.upper() != "MP":
            msg = f"Current file is not an MP form: found {module}"
            raise InvalidFieldError(msg)

    def _map_naccdico(self, existing_value) -> int:
        """Create the NACCDICO variable.

        DICOM image file available (y/n)
        """

        if existing_value is None:
            return 0

        return existing_value

    def _map_naccnift(self) -> int:
        """Create the NACCNIFT variable.

        NIFTI image file available (y/n)
        """
        nifti = self.__mp.get_value("nifti")
        return 1 if nifti == 1 else 0

    def _map_naccmria(self) -> int:
        """Create the NACCMRIA variable.

        Subject age at time of MRI
        """
        birthdate = self.__mp.get_value("birthdate")
        tmridate = self.__mp.get_value("tmridate")

        if birthdate and tmridate:
            months_diff = (tmridate.year - birthdate.year) * 12 + (tmridate.month - birthdate.month)
            return int(months_diff // 12)
        return 888

    def _map_naccmrfi(self) -> str:
        """Create the NACCMRFI variable.

        File locator variable
        """
        filename = self.__mp.get_value("filename")
        return filename.strip() if filename else ""

    def _map_naccnmri(self) -> int:
        """Create the NACCNMRI variable.

        Total number of MRI sessions
        """
        value = self.__mp.get_value("naccnmri")
        return 88 if value is None else value

    def _map_naccmnum(self) -> int:
        """Create the NACCMNUM variable.

        MRI session in chronological order    
        """
        return self.__mp.get_value("naccmnum")  

    def _map_naccmrdy(self) -> int:
        """Create the NACCMRDY variable.

        Days between MRI session and closest UDS visit   
        """
        mridate = self.__mp.get_value("mridate")
        visitdate = self.__mp.get_value("visitdate")

        if mridate and visitdate:
            return (mridate - visitdate).days
        return 8888

    def _map_naccmvol(self) -> int:
        """Create the NACCMVOL variable.

        Calculated summary data available (y/n)  
        """
        naccmvol = self.__mp.get_value("naccmvol")
        return 1 if naccmvol == 1 else 0

    def _map_naccicv(self) -> float:
        """Create the NACCICV variable.

        Total intercranial volume (cc)
        """
        gray = self.__mp.get_value("grayvol")
        white = self.__mp.get_value("whitevol")
        csf = self.__mp.get_value("csfvol")
        wmh = self.__mp.get_value("wmhvol")

        if all(v not in [None, 9999.9999, 8888.8888] for v in [gray, white, csf, wmh]):
            return round(gray + white + csf + wmh, 3)
        return 9999.999

    def _map_naccwmvl(self) -> float:
        """Create the NACCWMVL variable.

        Total white matter volume (cc) 
        """
        white = self.__mp.get_value("whitevol")
        wmh = self.__mp.get_value("wmhvol")

        if white not in [None, 9999.9999, 8888.8888] and wmh not in [None, 999.9999, 888.8888]:
            return round(white + wmh, 3)
        return 9999.999

    def _map_naccbrnv(self) -> float:
        """Create the NACCBRNV variable.

        Total brain volume (cc)
        """
        gray = self.__mp.get_value("grayvol")
        white = self.__mp.get_value("whitevol")

        if gray not in [None, 9999.9999, 8888.8888] and white not in [None, 9999.9999, 8888.8888]:
            return round(gray + white, 3)
        return 9999.999

    def _create_naccapta(self) -> int:
        """Create the NACCAPTA variable.

        Subject age at time of amyloid PET scan
        """
        birthdate = self.__mp.get_value("birthdate")  
        tpetdate = self.__mp.get_value("tpetdate") 

        if birthdate and tpetdate:
            months_diff = (tpetdate.year - birthdate.year) * 12 + (tpetdate.month - birthdate.month)
            return int(months_diff // 12)
        return None # Didn't have a default return variable

    def _create_naccaptf(self) -> str:
        """Create the NACCAPTF variable.

        Amyloid PET scan file locator variable
        """
        filename = self.__mp.get_value("filename")
        if filename:
            return filename.strip()
        return None # Didn't have a default return variable

    def _create_naccapnm(self) -> int:
        """Create the NACCAPNM variable.

        Amyloid PET scan in chronological order
        """
        is_first_file = self.__mp.get_value("is_first_file") 
        prev_value = self.__mp.get_value("prev_naccapnm") 

        if is_first_file:
            return 1
        if prev_value is not None:
            return prev_value + 1
        return 8  

    def _create_naccaptd(self) -> int:
        """Create the NACCAPTD variable.

        Days between amyloid PET scan and closest UDS visit
        """
        apetdate = self.__mp.get_value("apetdate")
        visitdate = self.__mp.get_value("visitdate")

        if apetdate and visitdate:
            return (apetdate - visitdate).days
        return 8 

# These three are seemingly just returning a different variable. From derive.sas

    def _create_naccmrsa(self) -> int:
        """Create the NACCMRSA variable.

        At least one MRI scan available
        """
        naccmri = self.__mp.get_value("naccmri") 

        if naccmri is None:
            return 0 
        return naccmri

    def _create_naccnapa(self) -> int:
        """Create the NACCNAPA variable.

        Total number of amyloid PET scans available
        """
        naccnapt = self.__mp.get_value("naccnapt")

        if naccnapt == 1:
            return 1
        return 0

    def _create_naccapsa(self) -> int:
        """Create the NACCAPSA variable.

        At least one amyloid PET scan available (y/n)
        """
        naccapet = self.__mp.get_value("naccapet") 

        if naccapet == 1:
            return 1
        return 0 

