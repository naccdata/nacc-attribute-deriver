"""Class to handle BDS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class BDSFormMissingness(FormMissingnessCollection):
    def _missingness_bds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for BDS form variables."""
        return self.generic_missingness(field, attr_type)

    def _handle_bdsudsd_gate(
        self, field: str, normal_code: int, unknown_code: int
    ) -> int:
        """Handles variables skipped when BDSUDSD (cognitive status at time of
        death) is 1 (normal cognition) or 9 (unknown).

        A submitted value is kept as-is. Otherwise:
            If BDSUDSD = 1, FIELD = normal_code
            If BDSUDSD = 9, FIELD = unknown_code
            Else generic missingness
        """
        value = self.form.get_value(field, int)
        if value is not None:
            return value

        bdsudsd = self.form.get_value("bdsudsd", int)
        if bdsudsd == 1:
            return normal_code
        if bdsudsd == 9:
            return unknown_code

        return self.generic_missingness(field, int)

    def _missingness_bdstmci(self) -> int:
        """Handles missingness for BDSTMCI.

        A submitted value is kept as-is. Otherwise:
            If BDSUDSD ne 3 (not MCI), BDSTMCI = 8
            Else generic missingness
        """
        value = self.form.get_value("bdstmci", int)
        if value is not None:
            return value

        bdsudsd = self.form.get_value("bdsudsd", int)
        if bdsudsd is not None and bdsudsd != 3:
            return 8

        return self.generic_missingness("bdstmci", int)

    def _missingness_bdsetpr(self) -> int:
        """Handles missingness for BDSETPR."""
        return self._handle_bdsudsd_gate("bdsetpr", 88, 99)

    def _missingness_bdscoalz(self) -> int:
        """Handles missingness for BDSCOALZ."""
        return self._handle_bdsudsd_gate("bdscoalz", 8, 9)

    def _missingness_bdscolbd(self) -> int:
        """Handles missingness for BDSCOLBD."""
        return self._handle_bdsudsd_gate("bdscolbd", 8, 9)

    def _missingness_bdscomsa(self) -> int:
        """Handles missingness for BDSCOMSA."""
        return self._handle_bdsudsd_gate("bdscomsa", 8, 9)

    def _missingness_bdscopsp(self) -> int:
        """Handles missingness for BDSCOPSP."""
        return self._handle_bdsudsd_gate("bdscopsp", 8, 9)

    def _missingness_bdscocbd(self) -> int:
        """Handles missingness for BDSCOCBD."""
        return self._handle_bdsudsd_gate("bdscocbd", 8, 9)

    def _missingness_bdscofmo(self) -> int:
        """Handles missingness for BDSCOFMO."""
        return self._handle_bdsudsd_gate("bdscofmo", 8, 9)

    def _missingness_bdscofot(self) -> int:
        """Handles missingness for BDSCOFOT."""
        return self._handle_bdsudsd_gate("bdscofot", 8, 9)

    def _missingness_bdscovas(self) -> int:
        """Handles missingness for BDSCOVAS."""
        return self._handle_bdsudsd_gate("bdscovas", 8, 9)

    def _missingness_bdscotbi(self) -> int:
        """Handles missingness for BDSCOTBI."""
        return self._handle_bdsudsd_gate("bdscotbi", 8, 9)

    def _missingness_bdscodwn(self) -> int:
        """Handles missingness for BDSCODWN."""
        return self._handle_bdsudsd_gate("bdscodwn", 8, 9)

    def _missingness_bdscoo1f(self) -> int:
        """Handles missingness for BDSCOO1F."""
        return self._handle_bdsudsd_gate("bdscoo1f", 8, 9)

    def _missingness_bdscoo2f(self) -> int:
        """Handles missingness for BDSCOO2F."""
        return self._handle_bdsudsd_gate("bdscoo2f", 8, 9)

    def _missingness_bdscoo3f(self) -> int:
        """Handles missingness for BDSCOO3F."""
        return self._handle_bdsudsd_gate("bdscoo3f", 8, 9)
