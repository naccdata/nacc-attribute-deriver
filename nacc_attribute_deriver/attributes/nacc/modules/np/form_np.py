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

from .np_form_wide_evaluator import NPFormWideEvaluator
from .np_mapper import NPMapper


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormNamespace(table)

        module = self.__np.get_value("module")
        if not module or module.upper() != "NP":
            msg = f"Current file is not an NP form: found {module}"
            raise InvalidFieldError(msg)

        self.mapper = NPMapper(self.__np)
        self.form_evaluator = NPFormWideEvaluator(self.__np, self.mapper)

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
            naccamy = self.mapper.map_sub1(npamy)
        elif formver == 1:
            naccamy = (
                self.mapper.map_sub1(npamy) if npamy else self.mapper.map_vasc(naccamy)
            )

        return naccamy if naccamy is not None else 9

    def _create_naccavas(self) -> int:
        """Create the NACCAVAS variable.

        Severity of gross findings — atherosclerosis of the circle of
        Willis
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
            naccavas = (
                self.mapper.map_sub1(npavas)
                if npavas
                else self.mapper.map_vasc(naccavas)
            )

        return naccavas if naccavas is not None else 9

    def _create_naccbrnn(self) -> int:
        """Create the NACCBRNN variable.

        No major neuropathologic change present
        """
        return self.form_evaluator.determine_naccbrnn()

    def _create_nacccbd(self) -> int:
        """Create the NACCCBD variable.

        FTLD-tau subtype — corticobasal degeneration (CBD)

        TODO: QAF does have this as -4 in some cases, but RDD does not say
        it can be -4 - probably best to keep as 9 but flagging
        """
        formver = self.__np.get_value("formver")
        npcort = self.__np.get_value("npcort")
        npftdtau = self.__np.get_value("npftdtau")
        nacc_cbd = None

        if formver in [10, 11]:
            nacc_cbd = self.mapper.map_v10(npcort, npftdtau)
        elif formver in [7, 8, 9]:
            nacc_cbd = self.mapper.map_v9(npcort)
        elif formver == 1:
            nacc_cbd = (
                self.mapper.map_v9(npcort) if npcort else self.mapper.map_vasc(nacc_cbd)
            )

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
            naccdiff = self.mapper.map_sub4(npdiff)
        elif formver == 1:
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
        formver = self.__np.get_value("formver")
        npchrom = self.__np.get_value("npchrom")

        if formver in [10, 11] or formver in [7, 8, 9] or formver == 1:
            np_down = 1 if npchrom == 11 else 7

        return np_down

    # This one has a very complicated description in the rdd-np.
    # This one will definitely need double checking.
    def _create_naccinf(self) -> int:  # noqa: C901
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
            return npinf if npinf is not None else 9

        elif formver in [7, 8, 9]:
            return self.mapper.map_comb2(nplinf, nplac)

        elif formver == 1:
            if nplinf is not None and nplac is not None:
                return self.mapper.map_comb2(nplinf, nplac)

        return 9  # Fallback value

    # additional cases where it should be blank found in the
    # description in the PDF of rdd-np
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
            return self.mapper.map_v10(npnec, nppath)
        elif formver in [7, 8, 9]:
            return self.mapper.map_v9(npnec)

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
        naccothp = None

        if formver in [10, 11]:
            if nppdxr == 1 or nppdxs == 1 or nppdxt == 1:
                return 1
            elif nppdxr == 0 and nppdxs == 0 and nppdxt == 0:
                return 0
            else:
                return 9

        elif formver in [7, 8, 9]:
            return self.mapper.map_v9(self.__np.get_value("npmajor"))

        elif formver == 1:
            if self.__np.get_value("npmajor") is not None:
                naccothp = self.mapper.map_v9(self.__np.get_value("npmajor"))
            else:
                naccothp = self.mapper.map_gross(self.__np.get_value("naccothp"))

        return naccothp if naccothp is not None else 9

    def _create_naccpick(self) -> int:
        """Create the NACCPICK variable.

        FTLD-tau subtype — Pick's (PiD).

        TODO: QAF does have this as -4 in some cases, but RDD does not say
        it can be -4 - probably best to keep as 9 but flagging
        """
        formver = self.__np.get_value("formver")
        npftdtau = self.__np.get_value("npftdtau")
        nppick = self.__np.get_value("nppick")
        naccpick = None

        if formver in [10, 11]:
            return self.mapper.map_v10(nppick, npftdtau)
        elif formver in [7, 8, 9]:
            return self.mapper.map_v9(nppick)

        elif formver == 1:
            npgross = self.__np.get_value("npgross")
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                naccpick = self.mapper.map_gross(nppick)

        return naccpick if naccpick is not None else 9

    def _create_naccprio(self) -> int:
        """Create the NACCPRIO variable.

        Prion disease.
        """
        formver = self.__np.get_value("formver")
        npcj = self.__np.get_value("npcj")
        npprion = self.__np.get_value("npprion")
        nppdxc = self.__np.get_value("nppdxc")
        npgross = self.__np.get_value("npgross")
        naccprio = None

        if formver in [10, 11]:
            return nppdxc if nppdxc is not None else 9
        elif formver in [7, 8, 9]:
            return self.mapper.map_comb2(npcj, npprion)

        elif formver == 1:
            if npcj is not None and npprion is not None:
                return self.mapper.map_comb2(npcj, npprion)

            naccprio = self.mapper.map_gross(naccprio)

        return naccprio if naccprio is not None else 9

    def _create_naccprog(self) -> int:
        """Create the NACCPROG variable.

        FTLD-tau subtype — progressive supranuclear palsy (PSP).
        """
        formver = self.__np.get_value("formver")
        npftdtau = self.__np.get_value("npftdtau")
        npprog = self.__np.get_value("npprog")
        npgross = self.__np.get_value("npgross")
        naccprog = None

        if formver in [10, 11]:
            return self.mapper.map_v10(npprog, npftdtau)
        elif formver in [7, 8, 9]:
            return self.mapper.map_v9(npprog)

        elif formver == 1:
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                naccprog = self.mapper.map_gross(npprog)

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
        formver = self.__np.get_value("formver")
        writein = self.__np.get_value(writein)
        npmpathx = self.__np.get_value(f"npmpath{num}")
        naccwrix = None

        if formver in [10, 11]:
            naccwrix = writein
        elif formver in [1, 7, 8, 9]:
            naccwrix = npmpathx

        # strip whitespace since write-in
        if naccwrix is not None:
            naccwrix = naccwrix.strip()

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
                naccbraa = self.mapper.map_gross(naccbraa)

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
            naccneur = self.mapper.map_sub4(npneur)
        elif formver == 1:
            naccneur = (
                self.mapper.map_sub4(npneur)
                if npneur
                else self.mapper.map_gross(naccneur)
            )

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
            naccmicr = self.mapper.map_v9(npmicro)
        elif formver == 1:
            naccmicr = (
                self.mapper.map_v9(npmicro)
                if npmicro
                else self.mapper.map_vasc(naccmicr)
            )

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
            nacchem = self.mapper.map_v9(nphem)
        elif formver == 1:
            nacchem = nphem
            nacchem = (
                self.mapper.map_v9(nphem) if nphem else self.mapper.map_vasc(nacchem)
            )

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
            naccarte = self.mapper.map_sub1(nparter)
        elif formver == 1:
            naccarte = (
                self.mapper.map_sub1(nparter)
                if nparter
                else self.mapper.map_vasc(naccarte)
            )

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
            nacclewy = self.mapper.map_lewy()
        elif formver == 1:
            nplewy = self.__np.get_value("nplewy")
            if nplewy:
                nacclewy = self.mapper.map_lewy()
            else:
                nacclewy = nplewy
                nacclewy = self.mapper.map_gross(nacclewy)

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
