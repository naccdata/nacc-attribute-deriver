"""Class to handle NACCBRNN and NACCVASC due to their complexity of involving
almost the entire form.

The SAS code currently checks every single variable individually.
This could probably be refactored some, but for now follow SAS.

NOTE: These seeemed to have been redefined multiple times, and it seems
like the QAF value may be set to older iterations of this implementation.
Will need to determine what behavior we want.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
)

from .np_mapper import NPMapper


class NPFormWideEvaluator:
    def __init__(self, np: FormNamespace, mapper: NPMapper, formver: int) -> None:
        """Initializer; assumes np is correct form."""
        self.np = np
        self.mapper = mapper
        self.formver = formver

    def get(self, attr: str) -> Optional[int]:
        """Get attribute."""
        return self.np.get_value(attr, int)

    """
    NACCBRNN
    """

    def determine_naccbrnn(self) -> int:
        """Determine NACCBRNN.

        Depends on form version.
        """
        if self.formver == 11:
            return self._naccbrnn_v11()
        if self.formver == 10:
            return self._naccbrnn_v10()

        return self._naccbrnn_v19()

    def _naccbrnn_v11(self) -> int:
        """Runs the NACCBRNN v11 definition."""
        if (
            self.get("npbraak") in [0, 1, 2]
            and self.get("npneur") == 0
            and self.get("npdiff") == 0
            and self.get("npthal") == 0
            and self.get("npamy") in [0, 1]
            and self.get("npinf") == 0
            and self.get("nphemo") == 0
            and self.get("npold") == 0
            and self.get("npoldd") == 0
            and self.get("nparter") in [0, 1]
            and self.get("npwmr") in [0, 1]
            and self.get("nppath") == 0
            and self.get("nplbod") == 0
            and self.get("npnloss") in [0, 1]
            and self.get("nphipscl") == 0
            and self.get("nptdpa") == 0
            and self.get("nptdpb") == 0
            and self.get("nptdpc") == 0
            and self.get("nptdpd") == 0
            and self.get("nptdpe") == 0
            and self.get("npftdtau") == 0
            and self.get("npftdtdp") == 0
            and self.get("npalsmnd") == 0
            and self.get("npoftd") == 0
            and self.get("nppdxa") == 0
            and self.get("nppdxb") == 0
            and self.get("nppdxc") == 0
            and self.get("nppdxd") == 0
            and self.get("nppdxe") == 0
            and self.get("nppdxf") == 0
            and self.get("nppdxg") == 0
            and self.get("nppdxh") == 0
            and self.get("nppdxi") == 0
            and self.get("nppdxj") == 0
            and self.get("nppdxk") == 0
            and self.get("nppdxl") == 0
            and self.get("nppdxm") == 0
            and self.get("nppdxn") == 0
            and self.get("nppdxr") == 0
            and self.get("nppdxs") == 0
            and self.get("nppdxt") == 0
            and self.get("npartag") == 0
        ):
            return 1

        pathnpv11 = (
            self.get("npbraak") in [3, 4, 5, 6, 7]
            or self.get("npneur") in [1, 2, 3]
            or self.get("npdiff") in [1, 2, 3]
            or self.get("npthal") in [1, 2, 3, 4, 5]
            or self.get("npamy") in [2, 3]
            or self.get("npinf") == 1
            or self.get("nphemo") == 1
            or self.get("npold") == 1
            or self.get("npoldd") == 1
            or self.get("nparter") in [2, 3]
            or self.get("npwmr") in [2, 3]
            or self.get("nppath") == 1
            or self.get("nplbod") in [1, 2, 3, 4, 5]
            or self.get("npnloss") in [2, 3]
            or self.get("nphipscl") in [1, 2, 3]
            or self.get("nptdpa") == 1
            or self.get("nptdpb") == 1
            or self.get("nptdpc") == 1
            or self.get("nptdpd") == 1
            or self.get("nptdpe") == 1
            or self.get("npftdtau") == 1
            or self.get("npftdtdp") == 1
            or self.get("npalsmnd") in [1, 2, 3, 4, 5]
            or self.get("npoftd") == 1
            or self.get("nppdxa") == 1
            or self.get("nppdxb") == 1
            or self.get("nppdxc") == 1
            or self.get("nppdxd") == 1
            or self.get("nppdxe") == 1
            or self.get("nppdxf") == 1
            or self.get("nppdxg") == 1
            or self.get("nppdxh") == 1
            or self.get("nppdxi") == 1
            or self.get("nppdxj") == 1
            or self.get("nppdxk") == 1
            or self.get("nppdxl") == 1
            or self.get("nppdxm") == 1
            or self.get("nppdxn") == 1
            or self.get("nppdxr") == 1
            or self.get("nppdxs") == 1
            or self.get("nppdxt") == 1
            or self.get("npartag") == 1
        )

        if not pathnpv11 and (
            self.get("npbraak") in [8, 9]
            or self.get("npneur") in [8, 9]
            or self.get("npdiff") in [8, 9]
            or self.get("npthal") in [8, 9]
            or self.get("npamy") in [8, 9]
            or self.get("npinf") in [8, 9]
            or self.get("nphemo") in [8, 9]
            or self.get("npold") in [8, 9]
            or self.get("nparter") in [8, 9]
            or self.get("npwmr") in [8, 9]
            or self.get("nppath") in [8, 9]
            or self.get("nplbod") in [8, 9]
            or self.get("npnloss") in [8, 9]
            or self.get("nphipscl") in [8, 9]
            or self.get("nptdpa") in [8, 9]
            or self.get("nptdpb") in [8, 9]
            or self.get("nptdpc") in [8, 9]
            or self.get("nptdpd") in [8, 9]
            or self.get("nptdpe") in [8, 9]
            or self.get("npftdtau") in [8, 9]
            or self.get("npftdtdp") in [8, 9]
            or self.get("npalsmnd") in [8, 9]
            or self.get("npoftd") in [8, 9]
            or self.get("nppdxa") in [8, 9]
            or self.get("nppdxb") in [8, 9]
            or self.get("nppdxc") in [8, 9]
            or self.get("nppdxd") in [8, 9]
            or self.get("nppdxe") in [8, 9]
            or self.get("nppdxf") in [8, 9]
            or self.get("nppdxg") in [8, 9]
            or self.get("nppdxh") in [8, 9]
            or self.get("nppdxi") in [8, 9]
            or self.get("nppdxj") in [8, 9]
            or self.get("nppdxk") in [8, 9]
            or self.get("nppdxl") in [8, 9]
            or self.get("nppdxm") in [8, 9]
            or self.get("nppdxn") in [8, 9]
            or self.get("nppdxr") in [8, 9]
            or self.get("nppdxs") in [8, 9]
            or self.get("nppdxt") in [8, 9]
            or self.get("npartag") in [8, 9]
        ):
            return 9

        return 0

    def _naccbrnn_v10(self) -> int:
        """Runs the NACCBRNN v10 definition."""
        if (
            self.get("npbraak") in [0, 1, 2]
            and self.get("npneur") == 0
            and self.get("npdiff") == 0
            and self.get("npthal") == 0
            and self.get("npamy") in [0, 1]
            and self.get("npinf") == 0
            and self.get("nphemo") == 0
            and self.get("npold") == 0
            and self.get("npoldd") == 0
            and self.get("nparter") in [0, 1]
            and self.get("npwmr") in [0, 1]
            and self.get("nppath") == 0
            and self.get("nplbod") == 0
            and self.get("npnloss") in [0, 1]
            and self.get("nphipscl") == 0
            and self.get("nptdpa") == 0
            and self.get("nptdpb") == 0
            and self.get("nptdpc") == 0
            and self.get("nptdpd") == 0
            and self.get("nptdpe") == 0
            and self.get("npftdtau") == 0
            and self.get("npftdtdp") == 0
            and self.get("npalsmnd") == 0
            and self.get("npoftd") == 0
            and self.get("nppdxa") == 0
            and self.get("nppdxb") == 0
            and self.get("nppdxc") == 0
            and self.get("nppdxd") == 0
            and self.get("nppdxe") == 0
            and self.get("nppdxf") == 0
            and self.get("nppdxg") == 0
            and self.get("nppdxh") == 0
            and self.get("nppdxi") == 0
            and self.get("nppdxj") == 0
            and self.get("nppdxk") == 0
            and self.get("nppdxl") == 0
            and self.get("nppdxm") == 0
            and self.get("nppdxn") == 0
            and self.get("nppdxr") == 0
            and self.get("nppdxs") == 0
            and self.get("nppdxt") == 0
        ):
            return 1

        pathnpv10 = (
            self.get("npbraak") in [3, 4, 5, 6, 7]
            or self.get("npneur") in [1, 2, 3]
            or self.get("npdiff") in [1, 2, 3]
            or self.get("npthal") in [1, 2, 3, 4, 5]
            or self.get("npamy") in [2, 3]
            or self.get("npinf") == 1
            or self.get("nphemo") == 1
            or self.get("npold") == 1
            or self.get("npoldd") == 1
            or self.get("nparter") in [2, 3]
            or self.get("npwmr") in [2, 3]
            or self.get("nppath") == 1
            or self.get("nplbod") in [1, 2, 3, 4, 5]
            or self.get("npnloss") in [2, 3]
            or self.get("nphipscl") in [1, 2, 3]
            or self.get("nptdpa") == 1
            or self.get("nptdpb") == 1
            or self.get("nptdpc") == 1
            or self.get("nptdpd") == 1
            or self.get("nptdpe") == 1
            or self.get("npftdtau") == 1
            or self.get("npftdtdp") == 1
            or self.get("npalsmnd") in [1, 2, 3, 4, 5]
            or self.get("npoftd") == 1
            or self.get("nppdxa") == 1
            or self.get("nppdxb") == 1
            or self.get("nppdxc") == 1
            or self.get("nppdxd") == 1
            or self.get("nppdxe") == 1
            or self.get("nppdxf") == 1
            or self.get("nppdxg") == 1
            or self.get("nppdxh") == 1
            or self.get("nppdxi") == 1
            or self.get("nppdxj") == 1
            or self.get("nppdxk") == 1
            or self.get("nppdxl") == 1
            or self.get("nppdxm") == 1
            or self.get("nppdxn") == 1
            or self.get("nppdxr") == 1
            or self.get("nppdxs") == 1
            or self.get("nppdxt") == 1
        )

        if not pathnpv10 and (
            self.get("npbraak") in [8, 9]
            or self.get("npneur") in [8, 9]
            or self.get("npdiff") in [8, 9]
            or self.get("npthal") in [8, 9]
            or self.get("npamy") in [8, 9]
            or self.get("npinf") in [8, 9]
            or self.get("nphemo") in [8, 9]
            or self.get("npold") in [8, 9]
            or self.get("nparter") in [8, 9]
            or self.get("npwmr") in [8, 9]
            or self.get("nppath") in [8, 9]
            or self.get("nplbod") in [8, 9]
            or self.get("npnloss") in [8, 9]
            or self.get("nphipscl") in [8, 9]
            or self.get("nptdpa") in [8, 9]
            or self.get("nptdpb") in [8, 9]
            or self.get("nptdpc") in [8, 9]
            or self.get("nptdpd") in [8, 9]
            or self.get("nptdpe") in [8, 9]
            or self.get("npftdtau") in [8, 9]
            or self.get("npftdtdp") in [8, 9]
            or self.get("npalsmnd") in [8, 9]
            or self.get("npoftd") in [8, 9]
            or self.get("nppdxa") in [8, 9]
            or self.get("nppdxb") in [8, 9]
            or self.get("nppdxc") in [8, 9]
            or self.get("nppdxd") in [8, 9]
            or self.get("nppdxe") in [8, 9]
            or self.get("nppdxf") in [8, 9]
            or self.get("nppdxg") in [8, 9]
            or self.get("nppdxh") in [8, 9]
            or self.get("nppdxi") in [8, 9]
            or self.get("nppdxj") in [8, 9]
            or self.get("nppdxk") in [8, 9]
            or self.get("nppdxl") in [8, 9]
            or self.get("nppdxm") in [8, 9]
            or self.get("nppdxn") in [8, 9]
            or self.get("nppdxr") in [8, 9]
            or self.get("nppdxs") in [8, 9]
            or self.get("nppdxt") in [8, 9]
        ):
            return 9

        return 0

    def _naccbrnn_v19(self):
        """Runs the NACCBRNN v1 - v9 definition."""
        if (
            self.get("npbraak") in [1, 2, 7]
            and self.get("npneur") == 4
            and self.get("npdiff") == 4
            and self.get("nplinf") == 2
            and self.get("npmicro") == 2
            and self.get("nplac") == 2
            and self.get("nphem") == 2
            and self.get("npart") == 2
            and self.get("npnec") == 2
            and self.get("npscl") == 2
            and self.get("npavas") in [1, 2]
            and self.get("nparter") in [1, 2]
            and self.get("npamy") in [1, 2]
            and self.get("npoang") == 2
            and self.get("npvoth") == 2
            and self.get("nplewy") == 5
            and self.get("nppick") == 2
            and self.get("npcort") == 2
            and self.get("npprog") == 2
            and self.get("npfront") == 2
            and self.get("nptau") == 2
            and self.get("npftd") == 3
            and self.get("npftdno") == 2
            and self.get("npftdspc") == 2
            and self.get("npcj") == 2
            and self.get("npprion") == 2
            and self.get("npmajor") == 2
        ):
            return 1

        # pathnpv9
        pathnpv9 = (
            self.get("npbraak") in [3, 4, 5, 6]
            or self.get("npneur") in [1, 2, 3]
            or self.get("npdiff") in [1, 2, 3]
            or self.get("nplinf") == 1
            or self.get("npmicro") == 1
            or self.get("nplac") == 1
            or self.get("nphem") == 1
            or self.get("npart") == 1
            or self.get("npnec") == 1
            or self.get("npscl") == 1
            or self.get("npavas") in [3, 4]
            or self.get("nparter") in [3, 4]
            or self.get("npamy") in [3, 4]
            or self.get("npoang") == 1
            or self.get("npvoth") == 1
            or self.get("nplewy") in [1, 2, 3, 4]
            or self.get("nppick") == 1
            or self.get("npcor") == 1
            or self.get("npprog") == 1
            or self.get("npfront") == 1
            or self.get("nptau") == 1
            or self.get("npftd") in [1, 2]
            or self.get("npftdno") == 1
            or self.get("npftdspc") == 1
            or self.get("npcj") == 1
            or self.get("npprion") == 1
            or self.get("npmajor") == 1
        )

        if not pathnpv9 and (
            self.get("npbraak") in [8, 9]
            or self.get("npneur") in [5, 9]
            or self.get("npdiff") in [5, 9]
            or self.get("nplinf") in [3, 9]
            or self.get("npmicro") in [3, 9]
            or self.get("nplac") in [3, 9]
            or self.get("nphem") in [3, 9]
            or self.get("npart") in [3, 9]
            or self.get("npnec") in [3, 9]
            or self.get("npscl") in [3, 9]
            or self.get("npavas") in [5, 9]
            or self.get("nparter") in [5, 9]
            or self.get("npamy") in [5, 9]
            or self.get("npoang") in [3, 9]
            or self.get("npvoth") in [3, 9]
            or self.get("nplewy") in [6, 9]
            or self.get("nppick") in [3, 9]
            or self.get("npcor") in [3, 9]
            or self.get("npprog") in [3, 9]
            or self.get("npfront") in [3, 9]
            or self.get("nptau") in [3, 9]
            or self.get("npftd") in [4, 9]
            or self.get("npftdno") in [3, 9]
            or self.get("npftdspc") in [3, 9]
            or self.get("npcj") in [3, 9]
            or self.get("npprion") in [3, 9]
            or self.get("npmajor") in [3, 9]
        ):
            return 8

        return 0

    """
    NACCVASC
    """

    def determine_naccvasc(self) -> int:
        """Determine NACCVASC.

        Depends on form version.
        """
        if self.formver in [10, 11]:
            return self._naccvasc_v1011()
        if self.formver in [7, 8, 9]:
            return self._naccvasc_v789()
        if self.formver in [1]:
            return self._naccvasc_v1()

        return 9

    def _naccvasc_v1011(self) -> int:
        """Runs the NACCVASC v10 - v11 definition."""
        if (
            self.get("npinf") == 1
            or self.get("nphemo") == 1
            or self.get("npold") == 1
            or self.get("npoldd") == 1
            or self.get("nparter") in [1, 2, 3]
            or self.get("npwmr") in [1, 2, 3]
            or self.get("nppath") == 1
            or self.get("npavas") in [1, 2, 3]
            or self.get("npamy") in [1, 2, 3]
        ):
            return 1

        if (
            self.get("npinf") == 0
            and self.get("nphemo") == 0
            and self.get("npold") == 0
            and self.get("npoldd") == 0
            and self.get("nparter") == 0
            and self.get("npwmr") == 0
            and self.get("nppath") == 0
            and self.get("npavas") == 0
            and self.get("npamy") == 0
        ):
            return 0

        return 9

    def _naccvasc_v789(self) -> int:
        """Runs the NACCVASC v7 - v9 definition."""
        if (
            self.get("nplinf") == 1
            or self.get("npmicro") == 1
            or self.get("nplac") == 1
            or self.get("nphem") == 1
            or self.get("npart") == 1
            or self.get("npnec") == 1
            or self.get("npscl") == 1
            or self.get("npavas") in (2, 3, 4)
            or self.get("nparter") in (2, 3, 4)
            or self.get("npamy") in (2, 3, 4)
            or self.get("npoang") == 1
            or self.get("npvoth") == 1
        ):
            return 1

        if (
            self.get("nplinf") == 2
            and self.get("npmicro") == 2
            and self.get("nplac") == 2
            and self.get("nphem") == 2
            and self.get("npart") == 2
            and self.get("npnec") == 2
            and self.get("npscl") == 2
            and self.get("npavas") == 1
            and self.get("nparter") == 1
            and self.get("npamy") == 1
            and self.get("npoang") == 2
            and self.get("npvoth") == 2
        ):
            return 0

        return 9

    def _naccvasc_v1(self) -> int:
        """Runs the NACCVASC v1 definition."""
        if (
            self.get("nplinf") == 1
            or self.get("npmicro") == 1
            or self.get("nplac") == 1
            or self.get("nphem") == 1
            or self.get("npart") == 1
            or self.get("npnec") == 1
            or self.get("npscl") == 1
            or self.get("npavas") in [2, 3, 4]
            or self.get("nparter") in [2, 3, 4]
            or self.get("npamy") in [2, 3, 4]
            or self.get("npoang") == 1
            or self.get("npvoth") == 1
        ):
            return 1

        if (
            self.get("nplinf") == 2
            and self.get("npmicro") == 2
            and self.get("nplac") == 2
            and self.get("nphem") == 2
            and self.get("npart") == 2
            and self.get("npnec") == 2
            and self.get("npscl") == 2
            and self.get("npavas") == 1
            and self.get("nparter") == 1
            and self.get("npamy") == 1
            and self.get("npoang") == 2
            and self.get("npvoth") == 2
        ):
            return 0

        naccvasc = self.mapper.map_gross(None)
        return naccvasc if naccvasc is not None else 9
