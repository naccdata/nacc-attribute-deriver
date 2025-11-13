"""Class to handle B3-specific missingness values."""

from typing import ClassVar, List, Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormB3Missingness(UDSMissingness):
    ALL_B3_FIELDS: ClassVar[List[str]] = [
        "speech",
        "facexp",
        "trestfac",
        "trestrhd",
        "trestlhd",
        "trestrft",
        "trestlft",
        "tractrhd",
        "tractlhd",
        "rigdneck",
        "rigduprt",
        "rigduplf",
        "rigdlort",
        "rigdlolf",
        "tapsrt",
        "tapslf",
        "handmovr",
        "handmovl",
        "handaltr",
        "handaltl",
        "legrt",
        "leglf",
        "arising",
        "posture",
        "gait",
        "posstab",
        "bradykin",
    ]

    def _missingness_pdnormal(self) -> Optional[int]:
        """Handles missingness for PDNORMAL for if PDNORMAL is blank.

        - If at least 1 FIELD is 1-4, then PDNORMAL should be 0
        - If all fields are 0 or 8, then PDNORMAL should be 8

        REGRESSION/LEGACY:
            - If they're ALL 0, PDNORMAL = 1. I think in V4, error
                checks ensure this = 1 so this situation doesn't
                happen
        """
        # V4 checks this and it should be right, but I think in older
        # versions we can't really trust this
        # if self.uds.get_value("pdnormal", int) is not None:
        #     return None

        all_values = [self.uds.get_value(x, int) for x in self.ALL_B3_FIELDS]
        if any(x in [1, 2, 3, 4] for x in all_values):
            return 0

        if all(x == 0 for x in all_values):
            return 1

        # if all blank, likely form was not filled out
        if all(x is None for x in all_values):
            return INFORMED_MISSINGNESS

        # all values are mix of 0, 8, or blank at this point
        # return 8 = unknown
        return 8

    def _handle_pdnormal_gate(self, field: str) -> Optional[int]:
        """Handle PDNORMAL gate:

        If PDNORMAL = 1, then FIELD must be 0.
        """
        if self.uds.get_value("pdnormal", int) == 1:
            return 0

        return self.generic_missingness(field, int)

    # technically these could all have the rules CSV call a single
    # _missingness_pdnormal_gate rule; however doing this for
    # explicity since it's confusing to track down what's defined
    # and what's not otherwise

    def _missingness_speech(self) -> Optional[int]:
        """Handles missingness for SPEECH."""
        return self._handle_pdnormal_gate("speech")

    def _missingness_facexp(self) -> Optional[int]:
        """Handles missingness for FACEXP."""
        return self._handle_pdnormal_gate("facexp")

    def _missingness_trestfac(self) -> Optional[int]:
        """Handles missingness for TRESTFAC."""
        return self._handle_pdnormal_gate("trestfac")

    def _missingness_trestrhd(self) -> Optional[int]:
        """Handles missingness for TRESTRHD."""
        return self._handle_pdnormal_gate("trestrhd")

    def _missingness_trestlhd(self) -> Optional[int]:
        """Handles missingness for TRESTLHD."""
        return self._handle_pdnormal_gate("trestlhd")

    def _missingness_trestrft(self) -> Optional[int]:
        """Handles missingness for TRESTRFT."""
        return self._handle_pdnormal_gate("trestrft")

    def _missingness_trestlft(self) -> Optional[int]:
        """Handles missingness for TRESTLFT."""
        return self._handle_pdnormal_gate("trestlft")

    def _missingness_tractrhd(self) -> Optional[int]:
        """Handles missingness for TRACTRHD."""
        return self._handle_pdnormal_gate("tractrhd")

    def _missingness_tractlhd(self) -> Optional[int]:
        """Handles missingness for TRACTLHD."""
        return self._handle_pdnormal_gate("tractlhd")

    def _missingness_rigdneck(self) -> Optional[int]:
        """Handles missingness for RIGDNECK."""
        return self._handle_pdnormal_gate("rigdneck")

    def _missingness_rigduprt(self) -> Optional[int]:
        """Handles missingness for RIGDUPRT."""
        return self._handle_pdnormal_gate("rigduprt")

    def _missingness_rigduplf(self) -> Optional[int]:
        """Handles missingness for RIGDUPLF."""
        return self._handle_pdnormal_gate("rigduplf")

    def _missingness_rigdlort(self) -> Optional[int]:
        """Handles missingness for RIGDLORT."""
        return self._handle_pdnormal_gate("rigdlort")

    def _missingness_rigdlolf(self) -> Optional[int]:
        """Handles missingness for RIGDLOLF."""
        return self._handle_pdnormal_gate("rigdlolf")

    def _missingness_tapsrt(self) -> Optional[int]:
        """Handles missingness for TAPSRT."""
        return self._handle_pdnormal_gate("tapsrt")

    def _missingness_tapslf(self) -> Optional[int]:
        """Handles missingness for TAPSLF."""
        return self._handle_pdnormal_gate("tapslf")

    def _missingness_handmovr(self) -> Optional[int]:
        """Handles missingness for HANDMOVR."""
        return self._handle_pdnormal_gate("handmovr")

    def _missingness_handmovl(self) -> Optional[int]:
        """Handles missingness for HANDMOVL."""
        return self._handle_pdnormal_gate("handmovl")

    def _missingness_handaltr(self) -> Optional[int]:
        """Handles missingness for HANDALTR."""
        return self._handle_pdnormal_gate("handaltr")

    def _missingness_handaltl(self) -> Optional[int]:
        """Handles missingness for HANDALTL."""
        return self._handle_pdnormal_gate("handaltl")

    def _missingness_legrt(self) -> Optional[int]:
        """Handles missingness for LEGRT."""
        return self._handle_pdnormal_gate("legrt")

    def _missingness_leglf(self) -> Optional[int]:
        """Handles missingness for LEGLF."""
        return self._handle_pdnormal_gate("leglf")

    def _missingness_arising(self) -> Optional[int]:
        """Handles missingness for ARISING."""
        return self._handle_pdnormal_gate("arising")

    def _missingness_posture(self) -> Optional[int]:
        """Handles missingness for POSTURE."""
        return self._handle_pdnormal_gate("posture")

    def _missingness_gait(self) -> Optional[int]:
        """Handles missingness for GAIT."""
        return self._handle_pdnormal_gate("gait")

    def _missingness_posstab(self) -> Optional[int]:
        """Handles missingness for POSSTAB."""
        return self._handle_pdnormal_gate("posstab")

    def _missingness_bradykin(self) -> Optional[int]:
        """Handles missingness for BRADYKIN."""
        return self._handle_pdnormal_gate("bradykin")

    def _missingness_totalupdrs(self) -> Optional[int]:
        """Handles missingness for TOTALUPDRS."""
        return self._handle_pdnormal_gate("totalupdrs")
