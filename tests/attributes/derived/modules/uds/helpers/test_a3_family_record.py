"""Tests the A3 Family record."""

from nacc_attribute_deriver.attributes.derived.modules.uds.helpers.a3_family_handler import (  # noqa: E501
    FamilyStatusRecord,
)

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class TestFamilyStatusRecord:
    """Test the FamilyStatusRecord."""

    def test_status_yes(self) -> None:
        """Test when family status is 1."""
        record = FamilyStatusRecord(
            mom_status=-4, dad_status=1, sib_status=0, kid_status=9
        )
        assert record.family_status() == 1

        record = FamilyStatusRecord(
            mom_status=1, dad_status=1, sib_status=-4, kid_status=-4
        )
        assert record.family_status() == 1

    def test_status_no(self) -> None:
        """Test when family status is 0."""
        record = FamilyStatusRecord(
            mom_status=0, dad_status=0, sib_status=0, kid_status=0
        )
        assert record.family_status() == 0

    def test_status_missing(self) -> None:
        """Test when family status is completely missing."""
        record = FamilyStatusRecord(
            mom_status=INFORMED_MISSINGNESS,
            dad_status=INFORMED_MISSINGNESS,
            sib_status=INFORMED_MISSINGNESS,
            kid_status=INFORMED_MISSINGNESS,
        )
        assert record.family_status() == INFORMED_MISSINGNESS

    def test_status_unknown(self) -> None:
        """Test when it's a mix resulting in unknown."""
        record = FamilyStatusRecord(
            mom_status=0, dad_status=9, sib_status=-4, kid_status=-4
        )
        assert record.family_status() == 9

        record = FamilyStatusRecord(
            mom_status=0, dad_status=0, sib_status=0, kid_status=9
        )
        assert record.family_status() == 9

        record = FamilyStatusRecord(
            mom_status=9, dad_status=9, sib_status=9, kid_status=9
        )
        assert record.family_status() == 9
