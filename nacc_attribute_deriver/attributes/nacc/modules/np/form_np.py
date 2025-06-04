"""Derived variables from neuropathology form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormNamespace(table)

        module = self.__np.get_value("module")
        if not module or module.upper() != "NP":
            msg = f"Current file is not an NP form: found {module}"
            raise InvalidFieldError(msg)

    def _map_gross(self, new) -> Optional[int]:
        npgross = self.__np.get_value("npgross")
        if npgross == 2:
            return 0
        if npgross == 9:
            return 9

        return new

    def _map_sub4(self, old) -> int:
        if old in [1, 2, 3, 4]:
            return 4 - old
        if old == 5:
            return 8

        return 9

    def _map_v9(self, old) -> int:
        if old == 1:
            return 1
        if old == 2:
            return 0
        if old == 3:
            return 8

        return 9

    def _map_vasc(self, new) -> int:
        npgross = self.__np.get_value("npgross")
        npvasc = self.__np.get_value("npvasc")
        if npgross == 2 or npvasc == 2:
            return 0
        if npgross == 9 or npvasc == 9:
            return 9
        if npvasc == 3:
            return 8

        return new

    def _map_sub1(self, old):
        if old in [1, 2, 3, 4]:
            return old - 1
        if old == 5:
            return 8

        return 9

    def _map_lewy(self) -> int:
        nplewy = self.__np.get_value("nplewy")
        if nplewy == 6:
            return 8
        if nplewy == 5:
            return 0

        return nplewy

    def _create_naccamy(self) -> int:
        """Create the NACCAMY variable.

        Cerebral amyloid angiopathy
        """
        formver = self.__np.get_value("formver")
        npamy = self.__np.get_value("npamy")
        naccamy = npamy

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccamy = self._map_sub1(npamy)
        elif formver == 1:
            if npamy:
                naccamy = self._map_sub1(npamy)
            else:
                naccamy = self._map_vasc(naccamy)

        return naccamy if naccamy is not None else 9
    
    def _create_naccavas(self) -> int:
        """Create the NACCAVAS variable.

        Severity of gross findings — atherosclerosis of the circle of Willis
        """
        formver = self.__np.get_value("formver")
        npavas = self.__np.get_value("npavas")
        naccavas = npavas

        if formver in [10, 11]:
            pass 
        elif formver in [7, 8, 9]:
            naccavas = npavas - 1
            if npavas == 5:
                naccavas = 8
            elif npavas == 9:
                naccavas = 9
        elif formver == 1:
            if npavas:
                naccavas = self._map_sub1(npavas)
            else:
                naccavas = self._map_vasc(naccavas)

        return naccavas if naccavas is not None else 9

    def _create_naccbrnn(self) -> int:
        """Create the NACCBRNN variable.

        No major neuropathologic change present
        """
        formver = self.__np.get_value("formver")
        npbrnn = self.__np.get_value("npbrnn")
        naccbrnn = npbrnn

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            if npbrnn == 7:
                naccbrnn = 0
        elif formver == 1:
            if npbrnn:
                if npbrnn == 7:
                    naccbrnn = 0
            else:
                naccbrnn = self._map_gross(naccbrnn)

        return naccbrnn if naccbrnn is not None else 9

    def _create_nacccbd(self) -> int:
        """Create the NACCCBD variable.

        FTLD-tau subtype — corticobasal degeneration (CBD)
        """
        formver = self.__np.get_value("formver")
        npcort = self.__np.get_value("npcort")
        npftdtau = self.__np.get_value("npftdtau")
        nacc_cbd = None

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            nacc_cbd = self._map_v9(npcort)
        elif formver == 1:
            nacc_cbd = self._map_v9(npcort) if npcort else self._map_vasc(nacc_cbd)

        return nacc_cbd if nacc_cbd is not None else 9
    
    def _create_naccdiff(self) -> int:
        """Create the NACCDIFF variable.

        Density of diffuse plaques (CERAD semi-quantitative score)
        """
        formver = self.__np.get_value("formver")
        npdiff = self.__np.get_value("npdiff")
        naccdiff = None

        if formver in [10, 11]:
            naccdiff = npdiff
        elif formver in [7, 8, 9]:
            naccdiff = self._map_sub4(npdiff)
        elif formver == 1:
            naccdiff = self._map_sub4(npdiff) if npdiff else self._map_gross(naccdiff)

        return naccdiff if naccdiff is not None else 9


    def _create_naccdown(self) -> int:
        """Create the NACCDOWN variable.

        Down syndrome
        """
        formver = self.__np.get_value("formver")
        npchrom = self.__np.get_value("npchrom")

        if formver in [10, 11]:
            np_down = 1 if npchrom == 11 else 7
        elif formver in [7, 8, 9]:
            np_down = 1 if npchrom == 11 else 7
        elif formver == 1:
            np_down = 1 if npchrom == 11 else 7

        return np_down

    # This one has a very complicated description in the rdd-np. This one will definitely need double checking.
    def _create_naccinf(self) -> int:
        """Create the NACCINF variable.

        infarcts or lacunes
        """
        formver = self.__np.get_value("formver")
        npinf = self.__np.get_value("npinf")
        nplinf = self.__np.get_value("nplinf")
        nplac = self.__np.get_value("nplac")
        npgross = self.__np.get_value("npgross")
        npvasc = self.__np.get_value("npvasc")

        if formver in [10, 11]:
            return npinf  
        
        elif formver in [7, 8, 9]:
            if nplinf == 1 or nplac == 1:
                return 1
            elif nplinf == 2 and nplac == 2:
                return 0
            elif nplinf == 3 and nplac == 3:
                return 8
            elif nplinf == 9 and nplac == 9:
                return 9
            else:
                return 9  
        
        elif formver == 1:
            if npgross == 2 or npvasc == 2:
                return 0
            elif npgross == 9:
                return 9
            elif npvasc == 3:
                return 8
            elif npvasc == 9:
                return 9
            else:
                return 9 
        
        return 9  # Fallback value

    # Tried to use all things described in the rdd-np. Many seemed not in the SAS code. Not sure if the MDS "vitalst" is passed through or not. 
    def _create_naccmod(self) -> int:
        """Create the NACCMOD variable.

        Month of death.
        """
        npdodmo = self.__np.get_value("npdodmo")
        deathmo = self.__np.get_value("deathmo")
        vitalst = self.__np.get_value("vitalst")

        if npdodmo is not None:
            return npdodmo  # Use NP
        elif deathmo is not None:
            return deathmo  # Use MDS form if NP data isn't available   
        elif vitalst == 2:  # If "Dead"
            return 99 if deathmo in [None, 99] else deathmo
        else:
            return 88  # "Not applicable" if the subject isn't deceased

    # additional cases where it should be blank found in the description in the PDF of rdd-np
    def _create_naccnec(self) -> int:
        """Create the NACCNEC variable.

        Laminar necrosis
        """
        formver = self.__np.get_value("formver")
        npnec = self.__np.get_value("npnec")
        nppath = self.__np.get_value("nppath")
        npgross = self.__np.get_value("npgross")
        npvasc = self.__np.get_value("npvasc")

        if formver in [10, 11]:
            if nppath == 8:
                return 8
            elif nppath == 9:
                return 9
            elif nppath == 0:
                return None  
            else:
                return npnec 
        
        elif formver in [7, 8, 9]:
            return self._map_v9(npnec)
        
        elif formver == 1:
            if npgross == 2 or npvasc == 2:
                return 0
            elif npgross == 9:
                return 9
            elif npvasc == 3:
                return 8
            elif npvasc == 9:
                return 9
            else:
                return 9 

        return 9 

    def _create_naccothp(self) -> int:
        """Create the NACCOTHP variable.

        Other pathologic diagnosis.
        """
        formver = self.__np.get_value("formver")
        nppdxr = self.__np.get_value("nppdxr")
        nppdxs = self.__np.get_value("nppdxs")
        nppdxt = self.__np.get_value("nppdxt")

        if formver in [10, 11]:
            if nppdxr == 1 or nppdxs == 1 or nppdxt == 1:
                return 1
            elif nppdxr == 0 and nppdxs == 0 and nppdxt == 0:
                return 0
            else:
                return 9 
            
        elif formver in [7, 8, 9]:
            return self._map_v9(self.__np.get_value("npmajor"))

        elif formver == 1:
            if self.__np.get_value("npmajor") is not None:
                return self._map_v9(self.__np.get_value("npmajor"))
            else:
                return self._map_gross(self.__np.get_value("naccothp"))

        return 9  
    
    def _create_naccpick(self) -> int:
        """Create the NACCPICK variable.

        FTLD-tau subtype — Pick’s (PiD).
        """
        formver = self.__np.get_value("formver")
        npftdtau = self.__np.get_value("npftdtau")
        nppick = self.__np.get_value("nppick")

        if formver in [10, 11]:
            if npftdtau == 8:
                return 8
            elif npftdtau == 9:
                return 9
            elif npftdtau == 0:
                return None 
            else:
                return self._map_v10(nppick, npftdtau)

        elif formver in [7, 8, 9]:
            return self._map_v9(nppick)

        elif formver == 1:
            npgross = self.__np.get_value("npgross")
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                return self._map_gross(nppick)

        return 9  # Default fallback


    def _create_naccprio(self) -> int:
        """Create the NACCPRIO variable.

        Prion disease.
        """
        formver = self.__np.get_value("formver")
        npcj = self.__np.get_value("npcj")
        npprion = self.__np.get_value("npprion")
        nppdxc = self.__np.get_value("nppdxc")
        npgross = self.__np.get_value("npgross")

        if formver in [10, 11]:
            return nppdxc  # unique
        elif formver in [7, 8, 9]:
            if npcj == 1 or npprion in [1, 2, 9]:
                return 1
            elif npcj == 2 and npprion == 2:
                return 0
            elif npcj == 3 and npprion == 3:
                return 8
            elif npcj == 9 and npprion == 9:
                return 9
            else:
                return 9  

        elif formver == 1:
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                return self._map_gross(npcj) 
            
        return 9 

    def _create_naccprog(self) -> int:
        """Create the NACCPROG variable.

        FTLD-tau subtype — progressive supranuclear palsy (PSP).
        """
        formver = self.__np.get_value("formver")
        npftdtau = self.__np.get_value("npftdtau")
        npprog = self.__np.get_value("npprog")
        npgross = self.__np.get_value("npgross")

        if formver in [10, 11]:
            if npftdtau == 8:
                return 8
            elif npftdtau == 9:
                return 9
            elif npftdtau == 0:
                return None  
            else:
                return self._map_v10(npprog, npftdtau) 

        elif formver in [7, 8, 9]:
            return self._map_v9(npprog)  

        elif formver == 1:
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                return self._map_gross(npprog) 

        return 9


      
    # Tons of skip patterns, and for all different versions utilizes almost every other variable. Really wasn't sure how to go about this. 
    def _create_naccvasc(self) -> int:
        """Create the NACCVASC variable.

        Cerebrovascular disease indicator
        """
        # I think this is the most variables we've needed and I don't think there's any way around that 
        formver = self.__np.get_value("formver")
        npinf = self.__np.get_value("npinf")
        nphemo = self.__np.get_value("nphemo")
        npold = self.__np.get_value("npold")
        npoldd = self.__np.get_value("npoldd")
        nparter = self.__np.get_value("nparter")
        npwmr = self.__np.get_value("npwmr")
        nppath = self.__np.get_value("nppath")
        npavas = self.__np.get_value("npavas")
        npamy = self.__np.get_value("npamy")

        naccvasc = 9 

        if formver in [10, 11]:
            if (npinf == 1 or nphemo == 1 or npold == 1 or
                npoldd == 1 or nparter in [1, 2, 3] or npwmr in [1, 2, 3] or
                nppath == 1 or npavas in [1, 2, 3] or npamy in [1, 2, 3]):
                naccvasc = 1
            elif (npinf == 0 and nphemo == 0 and npold == 0 and
                npoldd == 0 and nparter == 0 and npwmr == 0 and
                nppath == 0 and npavas == 0 and npamy == 0):
                naccvasc = 0

        elif formver in [7, 8, 9]:
            naccvasc = 9 
            if (self.__np.get_value("nplinf") == 1 or self.__np.get_value("npmicro") == 1 or
                self.__np.get_value("nplac") == 1 or nphemo == 1 or self.__np.get_value("npart") == 1 or
                self.__np.get_value("npnec") == 1 or self.__np.get_value("npscl") == 1 or
                npavas in [2, 3, 4] or nparter in [2, 3, 4] or npamy in [2, 3, 4] or
                self.__np.get_value("npoang") == 1 or self.__np.get_value("npvoth") == 1):
                naccvasc = 1
            elif (self.__np.get_value("nplinf") == 2 and self.__np.get_value("npmicro") == 2 and
                self.__np.get_value("nplac") == 2 and nphemo == 2 and self.__np.get_value("npart") == 2 and
                self.__np.get_value("npnec") == 2 and self.__np.get_value("npscl") == 2 and
                npavas == 1 and nparter == 1 and npamy == 1 and
                self.__np.get_value("npoang") == 2 and self.__np.get_value("npvoth") == 2):
                naccvasc = 0

        elif formver == 1:
            naccvasc = self._map_gross(naccvasc)

        return naccvasc if naccvasc is not None else 9

    def _create_naccwri1(self) -> str:
        """Create the NACCWRI1 variable.

        First other pathologic diagnosis write-in.
        """
        formver = self.__np.get_value("formver")
        nppdxrx = self.__np.get_value("nppdxrx")
        npmpath1 = self.__np.get_value("npmpath1")
        
        if formver in [10, 11]:
            naccwri1 = nppdxrx
        elif formver in [7, 8, 9]:
            naccwri1 = npmpath1
        elif formver == 1:
            naccwri1 = npmpath1
        
        return naccwri1 if naccwri1 else None


    def _create_naccwri2(self) -> str:
        """Create the NACCWRI2 variable.

        Second other pathologic diagnosis write-in.
        """
        formver = self.__np.get_value("formver")
        nppdxsx = self.__np.get_value("nppdxsx")
        npmpath2 = self.__np.get_value("npmpath2")

        if formver in [10, 11]:
            naccwri2 = nppdxsx
        elif formver in [7, 8, 9]:
            naccwri2 = npmpath2
        elif formver == 1:
            naccwri2 = npmpath2

        return naccwri2 if naccwri2 else None
    
    def _create_naccwri3(self) -> str:
        """Create the NACCWRI3 variable.

        Third other pathologic diagnosis write-in.
        """
        formver = self.__np.get_value("formver")
        naccothp = self.__np.get_value("naccothp")

        if naccothp != 1:
            return None  

        if formver in [10, 11]:
            return self.__np.get_value("nppdxtx")  

        elif formver in [7, 8, 9]:
            return self.__np.get_value("npmpath3") 

        return None

    # SAS seemingly sparse for this. Another one with potential MDS. 
    def _create_naccyod(self) -> int:
        """Create the NACCYOD variable.

        Year of death.
        """
        npdodyr = self.__np.get_value("npdodyr")  # NP
        deathyr = self.__np.get_value("deathyr")  # MDS
        vitalst = self.__np.get_value("vitalst")  # Vital from MDS

        if npdodyr: 
            naccyod = npdodyr
        elif deathyr: 
            naccyod = deathyr
        elif vitalst == 2:  
            naccyod = 9999
        else:  
            naccyod = 8888

        return naccyod if naccyod >= 1970 else 9999 # Explicitly states in rdd-np that this shouldn't precede 1970. Previously not mentioned in SAS code.


    def _create_naccbraa(self) -> int:
        """Create the NACCBRAA variable.

        Braak stage for neurofibrillary degeneration (B score)
        """
        formver = self.__np.get_value("formver")
        npbraak = self.__np.get_value("npbraak")
        naccbraa = npbraak

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            if npbraak == 7:
                naccbraa = 0
        elif formver == 1:
            if npbraak:
                if npbraak == 7:
                    naccbraa = 0
            else:
                naccbraa = self._map_gross(naccbraa)

        return naccbraa if naccbraa is not None else 9
    
    def _create_naccneur(self) -> int:
        """Create the NACCNEUR variable.

        Density of neocortical neuritic plaques (CERAD score) (C score)
        """
        formver = self.__np.get_value("formver")
        npneur = self.__np.get_value("npneur")
        naccneur = npneur

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccneur = self._map_sub4(npneur)
        elif formver == 1:
            naccneur = self._map_sub4(npneur) if npneur else self._map_gross(naccneur)

        return naccneur if naccneur is not None else 9

    def _create_naccmicr(self) -> int:
        """Create the NACCMICR variable.

        Microinfarcts
        """
        formver = self.__np.get_value("formver")
        npold = self.__np.get_value("npold")
        npmicro = self.__np.get_value("npmicro")

        naccmicr = npold
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccmicr = self._map_v9(npmicro)
        elif formver == 1:
            naccmicr = self._map_v9(npmicro) if npmicro else self._map_vasc(naccmicr)

        return naccmicr if naccmicr is not None else 9
  
    def _create_nacchem(self) -> int:
        """Create the NACCHEM variable.

        Hemorrhages and microbleeds
        """
        formver = self.__np.get_value("formver")
        nphem = self.__np.get_value("nphem")
        nacchem = None

        if formver in [10, 11]:
            nphemo = self.__np.get_value("nphemo")
            npoldd = self.__np.get_value("npoldd")

            if nphemo == 1 or npoldd == 1:
                nacchem = 1
            elif nphemo == 0 and npoldd == 0:
                nacchem = 0
            elif nphemo == 8 and npoldd == 8:
                nacchem = 8
            else:
                nacchem = 9
        elif formver in [7, 8, 9]:
            nacchem = nphem
            nacchem = self._map_v9(nphem)
        elif formver == 1:
            nacchem = nphem
            nacchem = self._map_v9(nphem) if nphem else self._map_vasc(nacchem)

        return nacchem if nacchem is not None else 9

    def _create_naccarte(self) -> int:
        """Create the NACCARTE variable.

        Arteriolosclerosis
        """
        formver = self.__np.get_value("formver")
        nparter = self.__np.get_value("nparter")
        naccarte = None

        if formver in [10, 11]:
            naccarte = nparter
        elif formver in [7, 8, 9]:
            naccarte = self._map_sub1(nparter)
        elif formver == 1:
            naccarte = self._map_sub1(nparter) if nparter else self._map_vasc(naccarte)

        return naccarte if naccarte is not None else 9

    def _create_nacclewy(self) -> int:
        """Create the NACCLEWY variable.

        Lewy body disease
        """
        formver = self.__np.get_value("formver")
        nacclewy = None

        if formver in [10, 11]:
            nplbod = self.__np.get_value("nplbod")
            nacclewy = nplbod
            if nplbod == 4:
                nacclewy = 2
            if nplbod == 5:
                nacclewy = 4
        elif formver in [7, 8, 9]:
            nacclewy = self._map_lewy()
        elif formver == 1:
            nplewy = self.__np.get_value("nplewy")
            if nplewy:
                nacclewy = self._map_lewy()
            else:
                nacclewy = nplewy
                nacclewy = self._map_gross(nacclewy)

        return nacclewy if nacclewy is not None else 9

    def _create_np_death_age(self) -> Optional[int]:
        return self.__np.get_value("npdage")

    def _create_np_death_date(self) -> Optional[date]:
        if self.__np.get_value("npdage") is None:
            return None

        year = self.__np.get_value("npdodyr")
        month = self.__np.get_value("npdodmo")
        day = self.__np.get_value("npdoddy")

        return create_death_date(year=year, month=month, day=day)
