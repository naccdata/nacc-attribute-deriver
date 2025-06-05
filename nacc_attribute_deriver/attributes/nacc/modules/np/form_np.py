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

from .np_mapper import NPMapper


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormNamespace(table)

        module = self.__np.get_value("module")
        if not module or module.upper() != "NP":
            msg = f"Current file is not an NP form: found {module}"
            raise InvalidFieldError(msg)

        self.map = NPMapper(table)

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
            naccamy = self.map.map_sub1(npamy)
        elif formver == 1:
            naccamy = self.map.map_sub1(npamy) if npamy else self.map.map_vasc(naccamy)

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
            naccavas = self.map.map_sub1(npavas) if npavas else self.map.map_vasc(naccavas)

        return naccavas if naccavas is not None else 9

    def _create_naccbrnn(self) -> int:
        """Create the NACCBRNN variable.

        No major neuropathologic change present
        """
        formver = self.__np.get_value("formver")
        npbraak = self.__np.get_value('npbraak')
        npneur = self.__np.get_value('nnpneur')
        npdiff = self.__np.get_value('npdiff')
        nplinf = self.__np.get_value('nplinf')
        npmicro = self.__np.get_value('npmicro')
        nplac = self.__np.get_value('nplac')
        nphem = self.__np.get_value('nphem')
        npart = self.__np.get_value('npart')
        npnec = self.__np.get_value('npnec')
        npscl = self.__np.get_value('npscl')
        npavas = self.__np.get_value('npavas')
        nparter = self.__np.get_value('nparter')
        npamy = self.__np.get_value('npamy')
        npoang = self.__np.get_value('npoang')
        npvoth = self.__np.get_value('npvoth')
        nplewy = self.__np.get_value('nplewy')
        nppick = self.__np.get_value('nppick')
        npcort = self.__np.get_value('npcort')
        npprog = self.__np.get_value('npprog')
        npfront = self.__np.get_value('npfront')
        nptau = self.__np.get_value('nptau')
        npftd = self.__np.get_value('npftd')
        npftdno = self.__np.get_value('npftdno')
        npftdspc = self.__np.get_value('npftdspc')
        npcj = self.__np.get_value('npcj')
        npprion = self.__np.get_value('npprion')
        npmajor = self.__np.get_value('npmajor')

        # these could probably be grouped, but type all out for now
        # to match SAS
        if (npbraak in [1, 2, 7] and
            npneur in [4] and
            npdiff in [4] and
            nplinf in [2] and
            npmicro in [2] and
            nplac in [2] and
            nphem in [2] and
            npart in [2] and
            npnec in [2] and
            npscl in [2] and
            npavas in [1, 2] and
            nparter in [1, 2] and
            npamy in [1,24] and
            npoang in [2] and
            npvoth in [2] and
            nplewy in [5] and
            nppick in [2] and
            npcandt in [2] and
            npprog in [2] and
            npfront in [2] and
            nptau in [2] and
            npftd in [3] and
            npftdno in [2] and
            npftdspc in [2] and
            npcj in [2] and
            npprion in [2] and
            npmajand in [2]):
            return 1

        pathnpv9 = 0
        if (npbraak in [3, 4, 5, 6] or
            npneur in [1, 2, 3] or
            npdiff in [1, 2, 3] or
            nplinf in [1] or
            npmicro in [1] or
            nplac in [1] or
            nphem in [1] or
            npart in [1] or
            npnec in [1] or
            npscl in [1] or
            npavas in [3, 4] or
            nparter in [3, 4] or
            npamy in [3, 4] or
            npoang in [1] or
            npvoth in [1] or
            nplewy in [1, 2, 3, 4] or
            nppick in [1] or
            npcort in [1] or
            npprog in [1] or
            npfront in [1] or
            nptau in [1] or
            npftd in [1, 2] or
            npftdno in [1] or
            npftdspc in [1] or
            npcj in [1] or
            npprion in [1] or
            npmajor in [1]):
            pathnpv9 = 1

        if (pathnpv9 != 1 and (npbraak in [8, 9] or
            npneur in [5, 9] or
            npdiff in [5, 9] or
            nplinf in [3, 9] or
            npmicro in [3, 9] or
            nplac in [3, 9] or
            nphem in [3, 9] or
            npart in [3, 9] or
            npnec in [3, 9] or
            npscl in [3, 9] or
            npavas in [5, 9] or
            nparter in [5, 9] or
            npamy in [5, 9] or
            npoang in [3, 9] or
            npvoth in [3, 9] or
            nplewy in [6, 9] or
            nppick in [3, 9] or
            npcort in [3, 9] or
            npprog in [3, 9] or
            npfront in [3, 9] or
            nptau in [3, 9] or
            npftd in [4, 9] or
            npftdno in [3, 9] or
            npftdspc in [3, 9] or
            npcj in [3, 9] or
            npprion in [3, 9] or
            npmajor in [3, 9])):
            return 8

        return 0

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
            nacc_cbd = self.map.map_v10(npcort, npftdtau)
        elif formver in [7, 8, 9]:
            nacc_cbd = self.map.map_v9(npcort)
        elif formver == 1:
            nacc_cbd = self.map.map_v9(npcort) if npcort else self.map.map_vasc(nacc_cbd)

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
            naccdiff = self.map.map_sub4(npdiff)
        elif formver == 1:
            naccdiff = self.map.map_sub4(npdiff) if npdiff else self.map.map_gross(naccdiff)

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
            return self.map.map_comb2(nplinf, nplac)

        elif formver == 1:
            if nplinf is not None and nplac is not None:
                return self.map.map_comb2(nplinf, nplac)

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
            return self.map.map_v10(npnec, nppath)
        elif formver in [7, 8, 9]:
            return self.map.map_v9(npnec)

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
            return self.map.map_v9(self.__np.get_value("npmajor"))

        elif formver == 1:
            if self.__np.get_value("npmajor") is not None:
                naccothp = self.map.map_v9(self.__np.get_value("npmajor"))
            else:
                naccothp = self.map.map_gross(self.__np.get_value("naccothp"))

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
            return self.map.map_v10(nppick, npftdtau)
        elif formver in [7, 8, 9]:
            return self.map.map_v9(nppick)

        elif formver == 1:
            npgross = self.__np.get_value("npgross")
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                naccpick = self.map.map_gross(nppick)

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
            return self.map.map_comb2(npcj, npprion)

        elif formver == 1:
            if npcj is not None and npprion is not None:
                return self.map.map_comb2(npcj, npprion)

            return self.map.map_gross(naccprio)

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
            return self.map.map_v10(npprog, npftdtau)
        elif formver in [7, 8, 9]:
            return self.map.map_v9(npprog)

        elif formver == 1:
            if npgross == 2:
                return 0
            elif npgross == 9:
                return 9
            else:
                naccprog = self.map.map_gross(npprog)

        return naccprog if naccprog is not None else 9

    # Tons of skip patterns, and for all different versions utilizes
    # almost every other variable. Really wasn't sure how to go about this.
    def _create_naccvasc(self) -> int:
        """Create the NACCVASC variable.

        Cerebrovascular disease indicator
        """
        # I think this is the most variables we've needed and I don't
        # think there's any way around that
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
            if (
                npinf == 1
                or nphemo == 1
                or npold == 1
                or npoldd == 1
                or nparter in [1, 2, 3]
                or npwmr in [1, 2, 3]
                or nppath == 1
                or npavas in [1, 2, 3]
                or npamy in [1, 2, 3]
            ):
                naccvasc = 1
            elif (
                npinf == 0
                and nphemo == 0
                and npold == 0
                and npoldd == 0
                and nparter == 0
                and npwmr == 0
                and nppath == 0
                and npavas == 0
                and npamy == 0
            ):
                naccvasc = 0

        elif formver in [7, 8, 9]:
            naccvasc = 9
            if (
                self.__np.get_value("nplinf") == 1
                or self.__np.get_value("npmicro") == 1
                or self.__np.get_value("nplac") == 1
                or nphemo == 1
                or self.__np.get_value("npart") == 1
                or self.__np.get_value("npnec") == 1
                or self.__np.get_value("npscl") == 1
                or npavas in [2, 3, 4]
                or nparter in [2, 3, 4]
                or npamy in [2, 3, 4]
                or self.__np.get_value("npoang") == 1
                or self.__np.get_value("npvoth") == 1
            ):
                naccvasc = 1
            elif (
                self.__np.get_value("nplinf") == 2
                and self.__np.get_value("npmicro") == 2
                and self.__np.get_value("nplac") == 2
                and nphemo == 2
                and self.__np.get_value("npart") == 2
                and self.__np.get_value("npnec") == 2
                and self.__np.get_value("npscl") == 2
                and npavas == 1
                and nparter == 1
                and npamy == 1
                and self.__np.get_value("npoang") == 2
                and self.__np.get_value("npvoth") == 2
            ):
                naccvasc = 0

        elif formver == 1:
            naccvasc = self.map.map_gross(naccvasc)  # type: ignore

        return naccvasc if naccvasc is not None else 9

    def _create_naccwri1(self) -> Optional[str]:
        """Create the NACCWRI1 variable.

        First other pathologic diagnosis write-in.
        """
        formver = self.__np.get_value("formver")
        nppdxrx = self.__np.get_value("nppdxrx")
        npmpath1 = self.__np.get_value("npmpath1")

        if formver in [10, 11]:
            naccwri1 = nppdxrx
        elif formver in [7, 8, 9] or formver == 1:
            naccwri1 = npmpath1

        return naccwri1 if naccwri1 else None

    def _create_naccwri2(self) -> Optional[str]:
        """Create the NACCWRI2 variable.

        Second other pathologic diagnosis write-in.
        """
        formver = self.__np.get_value("formver")
        nppdxsx = self.__np.get_value("nppdxsx")
        npmpath2 = self.__np.get_value("npmpath2")

        if formver in [10, 11]:
            naccwri2 = nppdxsx
        elif formver in [7, 8, 9] or formver == 1:
            naccwri2 = npmpath2

        return naccwri2 if naccwri2 else None

    def _create_naccwri3(self) -> Optional[str]:
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
                naccbraa = self.map.map_gross(naccbraa)

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
            naccneur = self.map.map_sub4(npneur)
        elif formver == 1:
            naccneur = self.map.map_sub4(npneur) if npneur else self.map.map_gross(naccneur)

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
            naccmicr = self.map.map_v9(npmicro)
        elif formver == 1:
            naccmicr = self.map.map_v9(npmicro) if npmicro else self.map.map_vasc(naccmicr)

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
            nacchem = self.map.map_v9(nphem)
        elif formver == 1:
            nacchem = nphem
            nacchem = self.map.map_v9(nphem) if nphem else self.map.map_vasc(nacchem)

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
            naccarte = self.map.map_sub1(nparter)
        elif formver == 1:
            naccarte = self.map.map_sub1(nparter) if nparter else self.map.map_vasc(naccarte)

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
            nacclewy = self.map.map_lewy()
        elif formver == 1:
            nplewy = self.__np.get_value("nplewy")
            if nplewy:
                nacclewy = self.map.map_lewy()
            else:
                nacclewy = nplewy
                nacclewy = self.map.map_gross(nacclewy)

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
