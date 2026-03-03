"""Tests the A3 Family handler."""

import pytest
import random
from typing import Any, Dict

from nacc_attribute_deriver.attributes.derived.modules.uds.helpers.a3_family_handler import (  # noqa: E501
    A3FamilyHandlerV1,
    A3FamilyHandlerV2,
    A3FamilyHandlerV3,
    A3FamilyHandlerV4,
    A3FamilyHandlerPrevVisit,
    FamilyStatusRecord,
)

from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

VALID_STATUSES = [0, 1, 9]


class TestFamilyStatusRecord:
    """Test the FamilyStatusRecord."""

    def test_status_yes(self) -> None:
        """Test when family status is 1."""
        record = FamilyStatusRecord(
            mom_status=-4,
            dad_status=1,
            sib_status=0,
            kid_status=9
        )
        assert record.family_status() == 1

        record = FamilyStatusRecord(
            mom_status=1,
            dad_status=1,
            sib_status=-4,
            kid_status=-4
        )
        assert record.family_status() == 1

    def test_status_no(self) -> None:
        """Test when family status is 0."""
        record = FamilyStatusRecord(
            mom_status=0,
            dad_status=0,
            sib_status=0,
            kid_status=0
        )
        assert record.family_status() == 0

    def test_status_missing(self) -> None:
        """Test when family status is completely missing."""
        record = FamilyStatusRecord(
            mom_status=INFORMED_MISSINGNESS,
            dad_status=INFORMED_MISSINGNESS,
            sib_status=INFORMED_MISSINGNESS,
            kid_status=INFORMED_MISSINGNESS
        )
        assert record.family_status() == INFORMED_MISSINGNESS

    def test_status_unknown(self) -> None:
        """Test when it's a mix resulting in unknown."""
        record = FamilyStatusRecord(
            mom_status=0,
            dad_status=9,
            sib_status=-4,
            kid_status=-4
        )
        assert record.family_status() == 9

        record = FamilyStatusRecord(
            mom_status=0,
            dad_status=0,
            sib_status=0,
            kid_status=9
        )
        assert record.family_status() == 9

        record = FamilyStatusRecord(
            mom_status=9,
            dad_status=9,
            sib_status=9,
            kid_status=9
        )
        assert record.family_status() == 9


def set_working_family(
    mom: int = INFORMED_MISSINGNESS,
    dad: int = INFORMED_MISSINGNESS,
    sib: int = INFORMED_MISSINGNESS,
    kid: int = INFORMED_MISSINGNESS
) -> SymbolTable:
    """Set the family working data."""
    table = SymbolTable({
        "subject": {
            "info": {
                "working": {
                    "cross-sectional": {
                        "cognitive-status-mom": mom,
                        "cognitive-status-dad": dad,
                        "cognitive-status-sib": sib,
                        "cognitive-status-kid": kid
                    }
                }
            }
        },
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": 3,
                        "birthyr": 1990,
                        "module": "UDS",
                        "packet": "I",
                        "formver": "3.0",
                        "naccid": "NACC123456",
                        "adcid": 0,
                    }
                }
            }
        },
    })
    return table


class TestA3FamilyHandlerPrevVisit:
    """Test the A3FamilyHandlerPrevVisit class."""

    def test_family_record(self) -> None:
        """Test family record is created correctly."""
        # should just return the previous working data if set
        mom = random.choice(VALID_STATUSES)
        dad = random.choice(VALID_STATUSES)
        sib = random.choice(VALID_STATUSES)
        kid = random.choice(VALID_STATUSES)

        table = set_working_family(mom=mom, dad=dad, sib=sib, kid=kid)

        handler = A3FamilyHandlerPrevVisit(table)
        assert handler.record == FamilyStatusRecord(
            mom_status=mom,
            dad_status=dad,
            sib_status=sib,
            kid_status=kid
        )

        # all not set
        handler = A3FamilyHandlerPrevVisit(set_working_family())
        assert handler.record == FamilyStatusRecord(
            mom_status=INFORMED_MISSINGNESS,
            dad_status=INFORMED_MISSINGNESS,
            sib_status=INFORMED_MISSINGNESS,
            kid_status=INFORMED_MISSINGNESS
        )

class TestA3FamilyHandlerV1:
    """Test the A3FamilyHandlerV1 class."""

    def test_parent_status_current_visit(self) -> None:
        """Test the parent logic works as expected when
        evaluating the current visit."""
        # starting as IVP, should look at momdem/daddem
        # both are definitively set
        table = set_working_family()
        table['file.info.forms.json'].update({
            'momdem': 1,
            'daddem': 0
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # sanity check family status is 1 because of mom status
        assert handler.record.family_status() == 1

        # test both are unknown/not set, without previous data
        table['file.info.forms.json'].update({
            'momdem': 9,
            'daddem': None
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

    def test_parent_status_fvp_visit(self) -> None:
        """Test the parent logic works as expected when
        evaluating an FVP visit."""
        # test both are unknown/not set, but there is previous data
        table = set_working_family(mom=0, dad=1)
        table['file.info.forms.json'].update({
            'momdem': None,
            'daddem': 9
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 1

        # test parent change and both are newly set
        table = set_working_family(mom=0, dad=0)
        table['file.info.forms.json'].update({
            'packet': 'F',
            'parchg': 1,
            'momdem': 1,
            'daddem': 1
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 1

        # test no parent change denoted; ignore even if something was
        # set and pull from previous working data
        table = set_working_family(mom=0, dad=0)
        table['file.info.forms.json'].update({
            'packet': 'F',
            'parchg': 0,
            'momdem': 1,
            'daddem': 1
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 0

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

        # test no working data; can happen if they basically never
        # submitted this form
        table = set_working_family()
        table['file.info.forms.json'].update({
            'packet': 'F',
            'parchg': 0,
            'momdem': 1,
            'daddem': 1
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == INFORMED_MISSINGNESS
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # whole family is unknown
        assert handler.record.family_status() == INFORMED_MISSINGNESS

    def test_kidsib_status_current_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating
        the current visit."""
        # starting as IVP, should look at sibsdem/kidsdem
        # both are definitively set
        table = set_working_family()
        table['file.info.forms.json'].update({
            'sibs': 2,
            'kids': 5,
            'sibsdem': 0,
            'kidsdem': 3
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 1

        # sanity check family status is 1 because of kid status
        assert handler.record.family_status() == 1

        # sibs/kids = 0 so we assume status is 0,
        # even if something got set
        table['file.info.forms.json'].update({
            'sibs': 0,
            'kids': 0,
            'sibsdem': 1,
            'kidsdem': 2
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # try the 88/99 cases
        table['file.info.forms.json'].update({
            'sibs': 2,
            'kids': 4,
            'sibsdem': 88,  # should trigger status of 0
            'kidsdem': 99   # should trigger status of 9
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 9

        # sanity check family status is 9 because we don't know parents
        assert handler.record.family_status() == 9

        # try the no data case (on sibsdem/kidsdem)
        table['file.info.forms.json'].update({
            'sibs': 2,
            'kids': 4,
            'sibsdem': None,
            'kidsdem': None
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == INFORMED_MISSINGNESS
        assert handler.record.kid_status == INFORMED_MISSINGNESS

        # try the no data case (on sibs/kids)
        table['file.info.forms.json'].update({
            'sibs': None,
            'kids': None,
            'sibsdem': 3,
            'kidsdem': 0
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == INFORMED_MISSINGNESS
        assert handler.record.kid_status == INFORMED_MISSINGNESS

        # sanity check family status is missing
        assert handler.record.family_status() == INFORMED_MISSINGNESS

    def test_kidsib_status_fvp_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating
        a FVP visit."""
        # set no sib/kid change, so ignore values if set and pull
        # from working data
        table = set_working_family(sib=0, kid=0)
        table['file.info.forms.json'].update({
            'packet': 'F',
            'sibchg': 0,
            'kidchg': None,
            'sibs': 2,
            'kids': 5,
            'sibsdem': 2,
            'kidsdem': 3
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # yes sib/kid change, but unknown, so pull from working values
        table = set_working_family(sib=0, kid=1)
        table['file.info.forms.json'].update({
            'packet': 'F',
            'sibchg': 1,
            'kidchg': 1,
            'sibs': 2,
            'kids': 5,
            'sibsdem': 99,
            'kidsdem': None
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 1

        # yes sib/kid change, and overrides with new values
        table = set_working_family(sib=9, kid=1)
        table['file.info.forms.json'].update({
            'packet': 'F',
            'sibchg': 1,
            'kidchg': 1,
            'sibs': 2,
            'kids': 5,
            'sibsdem': 1,
            'kidsdem': 88
        })
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0
