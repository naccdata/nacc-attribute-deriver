"""Derived variables from neuropathology form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date
from nacc_attribute_deriver.utils.errors import InvalidFieldError

from .np_form_wide_evaluator import NPFormWideEvaluator
from .np_mapper import NPMapper


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormNamespace(
            table=table, required=frozenset(["formver", "module"])
        )

        module = self.__np.get_required("module", str)
        if module.upper() != "NP":
            msg = f"Current file is not an NP form: found {module}"
            raise InvalidFieldError(msg)

        self.formver = self.__np.get_required("formver", int)
        self.mapper = NPMapper(self.__np)
        self.form_evaluator = NPFormWideEvaluator(self.__np, self.mapper)

    def _create_naccamy(self) -> int:
        """Create the NACCAMY variable.

        Cerebral amyloid angiopathy
        """
        npamy = self.__np.get_value("npamy", int)
        naccamy = npamy

        if self.formver in [10, 11]:
            pass
        elif self.formver in [7, 8, 9]:
            naccamy = self.mapper.map_sub1(npamy)
        elif self.formver == 1:
            naccamy = (
                self.mapper.map_sub1(npamy) if npamy else self.mapper.map_vasc(naccamy)
            )

        return naccamy if naccamy is not None else 9

    def _create_naccarte(self) -> int:
        """Create the NACCARTE variable.

        Arteriolosclerosis
        """
        nparter = self.__np.get_value("nparter", int)
        naccarte = None

        if self.formver in [10, 11]:
            naccarte = nparter
        elif self.formver in [7, 8, 9]:
            naccarte = self.mapper.map_sub1(nparter)
        elif self.formver == 1:
            naccarte = (
                self.mapper.map_sub1(nparter)
                if nparter
                else self.mapper.map_vasc(naccarte)
            )

        return naccarte if naccarte is not None else 9

    def _create_naccavas(self) -> int:
        """Create the NACCAVAS variable.

        Severity of gross findings — atherosclerosis of the circle of
        Willis
        """
        npavas = self.__np.get_value("npavas", int)
        naccavas = npavas

        if self.formver in [10, 11]:
            pass
        elif self.formver in [7, 8, 9]:
            if not npavas:
                raise InvalidFieldError(
                    "npvas cannot be missing for formver 7, 8, or 9"
                )

            naccavas = npavas - 1
            if npavas == 5:
                naccavas = 8
            elif npavas == 9:
                naccavas = 9
        elif self.formver == 1:
            naccavas = (
                self.mapper.map_sub1(npavas)
                if npavas
                else self.mapper.map_vasc(naccavas)
            )

        return naccavas if naccavas is not None else 9

    def _create_naccbnkf(self) -> Optional[int]:
        """Create the NACCBNKF variable.

        Banked frozen brain. Not in v1-7.
        """
        if self.formver < 8:
            return None

        if self.formver in [10, 11]:
            return self.__np.get_value("npbnka", int)

        npbrfrzn = self.__np.get_value("npbrfrzn", int)
        return self.mapper.banked_v9(npbrfrzn)

    def _create_naccbraa(self) -> int:
        """Create the NACCBRAA variable.

        Braak stage for neurofibrillary degeneration (B score)
        """
        npbraak = self.__np.get_value("npbraak", int)
        naccbraa = npbraak

        if self.formver in [10, 11]:
            pass
        elif self.formver in [7, 8, 9]:
            if npbraak == 7:
                naccbraa = 0
        elif self.formver == 1:
            if npbraak:
                if npbraak == 7:
                    naccbraa = 0
            else:
                naccbraa = self.mapper.map_gross(naccbraa)

        return naccbraa if naccbraa is not None else 9

    def _create_naccbrnn(self) -> int:
        """Create the NACCBRNN variable.

        No major neuropathologic change present
        """
        return self.form_evaluator.determine_naccbrnn()

    def _create_nacccbd(self) -> Optional[int]:
        """Create the NACCCBD variable.

        FTLD-tau subtype — corticobasal degeneration (CBD)
        """
        npcort = self.__np.get_value("npcort", int)
        npftdtau = self.__np.get_value("npftdtau", int)
        nacc_cbd = None

        if self.formver in [10, 11]:
            return self.mapper.map_v10(npcort, npftdtau)
        elif self.formver in [7, 8, 9]:
            nacc_cbd = self.mapper.map_v9(npcort)
        elif self.formver == 1:
            nacc_cbd = (
                self.mapper.map_v9(npcort) if npcort else self.mapper.map_vasc(nacc_cbd)
            )

        return nacc_cbd if nacc_cbd is not None else 9

    def _create_nacccsfp(self) -> Optional[int]:
        """Creates the NACCCSFP variable.

        Banks postmorten CSF. Not in v1-7.
        """
        if self.formver < 8:
            return None

        if self.formver in [10, 11]:
            return self.__np.get_value("npbnke", int)

        npcsfant = self.__np.get_value("npcsfant", int)
        return self.mapper.banked_v9(npcsfant)

    def _create_naccdiff(self) -> int:
        """Create the NACCDIFF variable.

        Density of diffuse plaques (CERAD semi-quantitative score)
        """
        npdiff = self.__np.get_value("npdiff", int)
        naccdiff = None

        if self.formver in [10, 11]:
            naccdiff = npdiff
        elif self.formver in [7, 8, 9]:
            naccdiff = self.mapper.map_sub4(npdiff)
        elif self.formver == 1:
            naccdiff = (
                self.mapper.map_sub4(npdiff)
                if npdiff
                else self.mapper.map_gross(naccdiff)
            )

        return naccdiff if naccdiff is not None else 9

    def _create_naccdown(self) -> int:
        """Create the NACCDOWN variable.

        Down syndrome
        """
        npchrom = self.__np.get_value("npchrom", int)

        if self.formver in [10, 11] or self.formver in [7, 8, 9] or self.formver == 1:
            np_down = 1 if npchrom == 11 else 7

        return np_down

    def _create_naccform(self) -> Optional[int]:
        """Creates the NACCFORM variable.

        Formalin - or paraformaldehyde-fixed brain. Not in v1-7.
        """
        if self.formver < 8:
            return None

        if self.formver in [10, 11]:
            return self.__np.get_value("npbnkc", int)

        npbrfrm = self.__np.get_value("npbrfrm", int)
        return self.mapper.banked_v9(npbrfrm)

    def _create_nacchem(self) -> int:
        """Create the NACCHEM variable.

        Hemorrhages and microbleeds
        """
        nphem = self.__np.get_value("nphem", int)
        nacchem = None

        if self.formver in [10, 11]:
            nphemo = self.__np.get_value("nphemo", int)
            npoldd = self.__np.get_value("npoldd", int)

            if nphemo == 1 or npoldd == 1:
                nacchem = 1
            elif nphemo == 0 and npoldd == 0:
                nacchem = 0
            elif nphemo == 8 and npoldd == 8:
                nacchem = 8
            else:
                nacchem = 9
        elif self.formver in [7, 8, 9]:
            nacchem = nphem
            nacchem = self.mapper.map_v9(nphem)
        elif self.formver == 1:
            nacchem = nphem
            nacchem = (
                self.mapper.map_v9(nphem) if nphem else self.mapper.map_vasc(nacchem)
            )

        return nacchem if nacchem is not None else 9

    def _create_naccinf(self) -> int:
        """Create the NACCINF variable.

        infarcts or lacunes
        """
        npinf = self.__np.get_value("npinf", int)
        nplinf = self.__np.get_value("nplinf", int)
        nplac = self.__np.get_value("nplac", int)

        if self.formver in [10, 11]:
            return npinf if npinf is not None else 9

        if self.formver in [7, 8, 9]:
            return self.mapper.map_comb2(nplinf, nplac)

        if self.formver == 1 and (nplinf is not None and nplac is not None):
            return self.mapper.map_comb2(nplinf, nplac)

        return 9  # Fallback value

    def _create_nacclewy(self) -> int:
        """Create the NACCLEWY variable.

        Lewy body disease
        """
        nacclewy = None

        if self.formver in [10, 11]:
            nplbod = self.__np.get_value("nplbod", int)
            nacclewy = nplbod
            if nplbod == 4:
                nacclewy = 2
            if nplbod == 5:
                nacclewy = 4
        elif self.formver in [7, 8, 9]:
            nacclewy = self.mapper.map_lewy()
        elif self.formver == 1:
            nplewy = self.__np.get_value("nplewy", int)
            if nplewy:
                nacclewy = self.mapper.map_lewy()
            else:
                nacclewy = nplewy
                nacclewy = self.mapper.map_gross(nacclewy)

        return nacclewy if nacclewy is not None else 9

    def _create_naccmicr(self) -> int:
        """Create the NACCMICR variable.

        Microinfarcts
        """
        npold = self.__np.get_value("npold", int)
        npmicro = self.__np.get_value("npmicro", int)

        naccmicr = npold
        if self.formver in [10, 11]:
            pass
        elif self.formver in [7, 8, 9]:
            naccmicr = self.mapper.map_v9(npmicro)
        elif self.formver == 1:
            naccmicr = (
                self.mapper.map_v9(npmicro)
                if npmicro
                else self.mapper.map_vasc(naccmicr)
            )

        return naccmicr if naccmicr is not None else 9

    def _create_naccnec(self) -> Optional[int]:
        """Create the NACCNEC variable.

        Laminar necrosis
        """
        npnec = self.__np.get_value("npnec", int)
        nppath = self.__np.get_value("nppath", int)
        npgross = self.__np.get_value("npgross", int)
        npvasc = self.__np.get_value("npvasc", int)

        if self.formver in [10, 11]:
            return self.mapper.map_v10(npnec, nppath)
        elif self.formver in [7, 8, 9]:
            return self.mapper.map_v9(npnec)

        elif self.formver == 1:
            if npgross == 2 or npvasc == 2:
                return 0
            elif npvasc == 3:
                return 8

        return 9

    def _create_naccneur(self) -> int:
        """Create the NACCNEUR variable.

        Density of neocortical neuritic plaques (CERAD score) (C score)
        """
        npneur = self.__np.get_value("npneur", int)
        naccneur = npneur

        if self.formver in [10, 11]:
            pass
        elif self.formver in [7, 8, 9]:
            naccneur = self.mapper.map_sub4(npneur)
        elif self.formver == 1:
            naccneur = (
                self.mapper.map_sub4(npneur)
                if npneur
                else self.mapper.map_gross(naccneur)
            )

        return naccneur if naccneur is not None else 9

    def _create_naccothp(self) -> int:
        """Create the NACCOTHP variable.

        Other pathologic diagnosis.
        """
        nppdxr = self.__np.get_value("nppdxr", int)
        nppdxs = self.__np.get_value("nppdxs", int)
        nppdxt = self.__np.get_value("nppdxt", int)
        npmajor = self.__np.get_value("npmajor", int)
        naccothp = None

        if self.formver in [10, 11]:
            if nppdxr == 1 or nppdxs == 1 or nppdxt == 1:
                return 1
            elif nppdxr == 0 and nppdxs == 0 and nppdxt == 0:
                return 0
            else:
                return 9

        elif self.formver in [7, 8, 9]:
            return self.mapper.map_v9(npmajor)

        elif self.formver == 1:
            if npmajor is not None:
                naccothp = self.mapper.map_v9(npmajor)
            else:
                naccothp = self.mapper.map_gross(naccothp)

        return naccothp if naccothp is not None else 9

    def _create_naccpara(self) -> Optional[int]:
        """Creates the NACCPARA variable.

        Paraffin-embedded blocks of brain regions. Not in v1-7.
        """
        if self.formver < 8:
            return None

        if self.formver in [10, 11]:
            return self.__np.get_value("npbnkd", int)

        npbparf = self.__np.get_value("npbparf", int)
        return self.mapper.banked_v9(npbparf)

    def _create_naccpick(self) -> Optional[int]:
        """Create the NACCPICK variable.

        FTLD-tau subtype — Pick's (PiD).
        """
        npftdtau = self.__np.get_value("npftdtau", int)
        nppick = self.__np.get_value("nppick", int)
        naccpick = None

        if self.formver in [10, 11]:
            return self.mapper.map_v10(nppick, npftdtau)
        elif self.formver in [7, 8, 9]:
            return self.mapper.map_v9(nppick)

        elif self.formver == 1:
            naccpick = self.mapper.map_gross(nppick)

        return naccpick if naccpick is not None else 9

    def _create_naccprio(self) -> int:
        """Create the NACCPRIO variable.

        Prion disease.
        """
        npcj = self.__np.get_value("npcj", int)
        npprion = self.__np.get_value("npprion", int)
        nppdxc = self.__np.get_value("nppdxc", int)
        naccprio = None

        if self.formver in [10, 11]:
            return nppdxc if nppdxc is not None else 9
        elif self.formver in [7, 8, 9]:
            return self.mapper.map_comb2(npcj, npprion)

        elif self.formver == 1:
            if npcj is not None and npprion is not None:
                return self.mapper.map_comb2(npcj, npprion)

            naccprio = self.mapper.map_gross(naccprio)

        return naccprio if naccprio is not None else 9

    def _create_naccprog(self) -> Optional[int]:
        """Create the NACCPROG variable.

        FTLD-tau subtype — progressive supranuclear palsy (PSP).
        """
        npftdtau = self.__np.get_value("npftdtau", int)
        npprog = self.__np.get_value("npprog", int)
        naccprog = None

        if self.formver in [10, 11]:
            return self.mapper.map_v10(npprog, npftdtau)
        elif self.formver in [7, 8, 9]:
            return self.mapper.map_v9(npprog)

        elif self.formver == 1:
            self.mapper.map_gross(npprog)

        return naccprog if naccprog is not None else 9

    def _create_naccvasc(self) -> int:
        """Create the NACCVASC variable.

        Cerebrovascular disease indicator
        """
        return self.form_evaluator.determine_naccvasc()

    def _handle_naccwrix(self, writein: str, num: int) -> Optional[str]:
        """Handle the NACCWRIX variable.

        Args:
            writein: Writein variable to use
            num: Number of NPMPATHX variable to grab which corresponds
                to the number of the NACCWRIX variable
        """
        value = self.__np.get_value(writein, str)
        npmpathx = self.__np.get_value(f"npmpath{num}", str)
        naccwrix = None

        if self.formver in [10, 11]:
            naccwrix = value
        elif self.formver in [1, 7, 8, 9]:
            naccwrix = npmpathx

        return naccwrix if naccwrix else None

    def _create_naccwri1(self) -> Optional[str]:
        """Create the NACCWRI1 variable.

        First other pathologic diagnosis write-in.
        """
        return self._handle_naccwrix("nppdxrx", 1)

    def _create_naccwri2(self) -> Optional[str]:
        """Create the NACCWRI2 variable.

        Second other pathologic diagnosis write-in.
        """
        return self._handle_naccwrix("nppdxsx", 2)

    def _create_naccwri3(self) -> Optional[str]:
        """Create the NACCWRI3 variable.

        Third other pathologic diagnosis write-in.
        """
        return self._handle_naccwrix("nppdxtx", 3)

    def _create_np_death_age(self) -> Optional[int]:
        """Create NP death age; used to determine a lot of death-related
        variables."""
        return self.__np.get_value("npdage", int)

    def _create_np_death_date(self) -> Optional[date]:
        """Create NP death date; used to determine a lot of death-related
        variables."""
        if self.__np.get_value("npdage", int) is None:
            return None

        year = self.__np.get_value("npdodyr", int)
        month = self.__np.get_value("npdodmo", int)
        day = self.__np.get_value("npdoddy", int)

        return create_death_date(year=year, month=month, day=day)

    def _create_np_form_date(self) -> str:
        """Create NP form date - needed to compare when this was submitted
        relative to other forms like MLST."""
        return self.__np.get_required("visitdate", str)

    def _create_npchrom(self) -> Optional[int]:
        """Keeps track of NPCHROM - required for NACCADMU, NACCFTDM
        in UDS D1.

        V9 and earlier.
        """
        return self.__np.get_value("npchrom", int)

    def _create_nppdxp(self) -> Optional[int]:
        """Keeps track of NPPDXP - required for NACCADMU in UDS D1.

        V10+
        """
        return self.__np.get_value("nppdxp", int)

    def _create_nppdxq(self) -> Optional[int]:
        """Keeps track of NPPDXQ - required for NACCFTDM in UDS D1.

        V10+
        """
        return self.__np.get_value("nppdxq", int)
