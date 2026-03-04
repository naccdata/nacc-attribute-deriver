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


def set_working_family(
    mom: int = INFORMED_MISSINGNESS,
    dad: int = INFORMED_MISSINGNESS,
    sib: int = INFORMED_MISSINGNESS,
    kid: int = INFORMED_MISSINGNESS,
) -> SymbolTable:
    """Set the family working data."""
    table = SymbolTable(
        {
            "subject": {
                "info": {
                    "working": {
                        "cross-sectional": {
                            "cognitive-status-mom": mom,
                            "cognitive-status-dad": dad,
                            "cognitive-status-sib": sib,
                            "cognitive-status-kid": kid,
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
        }
    )
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
            mom_status=mom, dad_status=dad, sib_status=sib, kid_status=kid
        )

        # all not set
        handler = A3FamilyHandlerPrevVisit(set_working_family())
        assert handler.record == FamilyStatusRecord(
            mom_status=INFORMED_MISSINGNESS,
            dad_status=INFORMED_MISSINGNESS,
            sib_status=INFORMED_MISSINGNESS,
            kid_status=INFORMED_MISSINGNESS,
        )


class TestA3FamilyHandlerV1:
    """Test the A3FamilyHandlerV1 class."""

    def test_parent_status_current_visit(self) -> None:
        """Test the parent logic works as expected when evaluating the current
        visit."""
        # starting as IVP, should look at momdem/daddem
        # both are definitively set
        table = set_working_family()
        table["file.info.forms.json"].update({"momdem": 1, "daddem": 0})
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # sanity check family status is 1 because of mom status
        assert handler.record.family_status() == 1

        # test both are unknown/not set, without previous data
        table["file.info.forms.json"].update({"momdem": 9, "daddem": None})
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

        # test both are unknown/not set, but there is previous data
        table = set_working_family(mom=0, dad=1)
        table["file.info.forms.json"].update({"momdem": None, "daddem": 9})
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 1

    def test_parent_status_fvp_visit(self) -> None:
        """Test the parent logic works as expected when evaluating an FVP
        visit."""
        # test parent change and both are newly set
        table = set_working_family(mom=0, dad=0)
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 1, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 1

        # test no parent change denoted; ignore even if something was
        # set and pull from previous working data
        table = set_working_family(mom=0, dad=0)
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 0, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 0

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

        # test no working data; can happen if they basically never
        # submitted this form
        table = set_working_family()
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 0, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.mom_status == INFORMED_MISSINGNESS
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # whole family is unknown
        assert handler.record.family_status() == INFORMED_MISSINGNESS

    def test_sibkid_status_current_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating the current
        visit."""
        # starting as IVP, should look at sibsdem/kidsdem
        # both are definitively set
        table = set_working_family()
        table["file.info.forms.json"].update(
            {"sibs": 2, "kids": 5, "sibsdem": 0, "kidsdem": 3}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 1

        # sanity check family status is 1 because of kid status
        assert handler.record.family_status() == 1

        # sibs/kids = 0 so we assume status is 0,
        # even if something got set
        table["file.info.forms.json"].update(
            {"sibs": 0, "kids": 0, "sibsdem": 1, "kidsdem": 2}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # try the 88/99 cases
        table["file.info.forms.json"].update(
            {
                "sibs": 2,
                "kids": 4,
                "sibsdem": 88,  # should trigger status of 0
                "kidsdem": 99,  # should trigger status of 9
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 9

        # sanity check family status is 9 because we don't know parents
        assert handler.record.family_status() == 9

        # try the no data case (on sibsdem/kidsdem)
        table["file.info.forms.json"].update(
            {"sibs": 2, "kids": 4, "sibsdem": None, "kidsdem": None}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == INFORMED_MISSINGNESS
        assert handler.record.kid_status == INFORMED_MISSINGNESS

        # try the no data case (on sibs/kids)
        table["file.info.forms.json"].update(
            {"sibs": None, "kids": None, "sibsdem": 3, "kidsdem": 0}
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == INFORMED_MISSINGNESS
        assert handler.record.kid_status == INFORMED_MISSINGNESS

        # sanity check family status is missing
        assert handler.record.family_status() == INFORMED_MISSINGNESS

        # test there is no data in current form but there is working data
        table = set_working_family(sib=1, kid=0)
        table["file.info.forms.json"].update(
            {
                "sibchg": 1,
                "kidchg": 1,
                "sibs": 2,
                "kids": 5,
                "sibsdem": 99,
                "kidsdem": 99,
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

    def test_sibkid_status_fvp_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating a FVP
        visit."""
        # set no sib/kid change, so ignore values if set and pull
        # from working data
        table = set_working_family(sib=0, kid=0)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 0,
                "kidchg": None,
                "sibs": 2,
                "kids": 5,
                "sibsdem": 2,
                "kidsdem": 3,
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # yes sib/kid change, but unknown, so pull from working values
        table = set_working_family(sib=0, kid=1)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 1,
                "kidchg": 1,
                "sibs": 2,
                "kids": 5,
                "sibsdem": 99,
                "kidsdem": None,
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 1

        # yes sib/kid change, and overrides with new values
        table = set_working_family(sib=9, kid=1)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 1,
                "kidchg": 1,
                "sibs": 2,
                "kids": 5,
                "sibsdem": 1,
                "kidsdem": 88,
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

    def test_sibkid_status_unknown_num(self) -> None:
        """Test when there is an unknown number of sibs/kids.

        Ultimately doesn't matter for V1 since we just check
        sibsdem/kidsdem anyways.
        """
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 99,
                "kids": 99,
                "sibsdem": 1,
                "kidsdem": 0,
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # not set
        table["file.info.forms.json"].update(
            {
                "sibs": 99,
                "kids": 99,
                "sibsdem": 99,
                "kidsdem": None, # kidsdem is just missing
            }
        )
        handler = A3FamilyHandlerV1(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == 9


class TestA3FamilyHandlerV2:
    """Test the A3FamilyHandlerV2 class.

    The parent tests here are a duplicate of V1, but with the swapped
    parent change code.
    """

    def test_parent_status_current_visit(self) -> None:
        """Test the parent logic works as expected when evaluating the current
        visit."""
        # starting as IVP, should look at momdem/daddem
        # both are definitively set
        table = set_working_family()
        table["file.info.forms.json"].update({"momdem": 1, "daddem": 0})
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # sanity check family status is 1 because of mom status
        assert handler.record.family_status() == 1

        # test both are unknown/not set, without previous data
        table["file.info.forms.json"].update({"momdem": 9, "daddem": None})
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

        # test both are unknown/not set, but there is previous data
        table = set_working_family(mom=0, dad=1)
        table["file.info.forms.json"].update({"momdem": None, "daddem": 9})
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 1

    def test_parent_status_fvp_visit(self) -> None:
        """Test the parent logic works as expected when evaluating an FVP
        visit."""
        # test parent change and both are newly set
        table = set_working_family(mom=0, dad=0)
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 0, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 1

        # test no parent change denoted; ignore even if something was
        # set and pull from previous working data
        table = set_working_family(mom=0, dad=0)
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 1, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 0

        # sanity check that family status is 9 because we don't
        # know the sibs/kids
        assert handler.record.family_status() == 9

        # test no working data; can happen if they basically never
        # submitted this form
        table = set_working_family()
        table["file.info.forms.json"].update(
            {"packet": "F", "parchg": 1, "momdem": 1, "daddem": 1}
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.mom_status == INFORMED_MISSINGNESS
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # whole family is unknown
        assert handler.record.family_status() == INFORMED_MISSINGNESS

    def test_sibkid_status_current_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating the current
        visit and it should be set."""
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 3,
                "kids": 1,
                "sib1dem": 0,
                "sib2dem": 9,
                "sib3dem": 1,  # this should set it
                "kid1dem": 0,
                "kid2dem": 1,  # this should be ignored
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # unknown cases
        table["file.info.forms.json"].update(
            {
                "sibs": 3,
                "kids": 1,
                "sib1dem": 0,
                "sib2dem": 9,
                "sib3dem": 9,
                "kid1dem": None,
                "kid2dem": 1,  # this should be ignored
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == INFORMED_MISSINGNESS

        # unknown cases but we have working values
        table = set_working_family(sib=1, kid=1)
        table["file.info.forms.json"].update(
            {
                "sibs": 3,
                "kids": 1,
                "sib1dem": 9,
                "sib2dem": None,
                "sib3dem": 9,
                "kid1dem": None,
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 1

    def test_sibkid_status_fvp_visit(self) -> None:
        """Test the sib/kid logic works as expected when evaluating an FVP
        visit."""
        # should not be evaluated and pull from working data if
        # sibchg/kidchg is not 0
        table = set_working_family(sib=0, kid=0)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 1,
                "kidchg": None,
                "sibs": 2,
                "kids": 5,
                "sib1dem": 1,
                "sib2dem": 0,
                "sib3dem": 1,
                "kid1dem": 1,
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # data change so should be evaluated, and overrides working data
        table = set_working_family(sib=0, kid=0)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 0,
                "kidchg": 0,
                "sibs": 3,
                "kids": 5,
                "sib1dem": 1,
                "sib2dem": 0,
                "sib3dem": 9,
                "kid1dem": 1,
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 1

        # data changed so should be evaluated, but data does NOT override
        # working data
        table = set_working_family(sib=0, kid=1)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "sibchg": 0,
                "kidchg": 0,
                "sibs": 3,
                "kids": 3,
                "sib1dem": 0,
                "sib2dem": None,
                "kid1dem": 9,
                "kid2dem": 9,
                "kid3dem": None,
            }
        )
        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 1

    def test_sibkid_status_unknown_num(self) -> None:
        """Test when there is an unknown number of sibs/kids.

        Will end up looping through all, so most likely 9
        unless at least 1 is set to 1 or all are set to 0
        """
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 99,
                "kids": 99,
                "sib20dem": 1,  # set the 20th sibling to 1
            }
        )

        # set all kids
        for i in range(1, 16):
            table[f'file.info.forms.json.kid{i}dem'] = 0

        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # more likely case
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 99,
                "kids": 99,
                "sib1dem": 0,
                "sib2dem": 0,
                # set nothing for kids, will still expect 9
            }
        )

        handler = A3FamilyHandlerV2(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == 9


class TestA3FamilyHandlerV3:
    """Test the A3FamilyHandlerV3 class."""

    def test_parent_status_current_visit(self) -> None:
        """Test the parent logic works as expected when evaluating the current
        visit."""
        # case 1 - definite sets to yes/no when neur is 1
        # momneur is 1 AND pdx value in list
        # dadneur is 1 but pdx value NOT in list
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "momneur": 1,
                "momprdx": random.choice(A3FamilyHandlerV3.DXCODES),
                "dadneur": 1,
                "dadprdx": 23,
            }
        )
        handler = A3FamilyHandlerV3(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # case 2 - unknown sets
        # momneur is 1 but pdx if 999 (unknown)
        # dadneur is 9 even if pdf ix in DXCODES
        table["file.info.forms.json"].update(
            {
                "momneur": 1,
                "momprdx": 999,
                "dadneur": 9,
                "dadprdx": random.choice(A3FamilyHandlerV3.DXCODES),
            }
        )
        handler = A3FamilyHandlerV3(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == 9

        # case 3 - definite sets to no when neur is not 1, even with working values
        # momneur is not 1 even if pdx in DXCODES
        # dadneur is not 1 and pdx is not in DXCODES
        table = set_working_family(mom=1, dad=1)
        table["file.info.forms.json"].update(
            {
                "momneur": random.choice([2, 3, 4, 5, 8]),
                "momprdx": random.choice(A3FamilyHandlerV3.DXCODES),
                "dadneur": random.choice([2, 3, 4, 5, 8]),
                "dadprdx": 36,
            }
        )
        handler = A3FamilyHandlerV3(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 0

        # case 4: unknown but working values set it
        table = set_working_family(mom=1, dad=1)
        table["file.info.forms.json"].update(
            {
                "momneur": 1,
                "momprdx": 999,
                "dadneur": 9,
                "dadprdx": random.choice(A3FamilyHandlerV3.DXCODES),
            }
        )
        handler = A3FamilyHandlerV3(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 1

    def test_sibkid_status_unknown_num(self) -> None:
        """Test when there is an unknown number of sibs/kids.

        Will end up looping through all, so most likely 9
        unless at least 1 is set to 1 or all are set to 0
        """
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 77,
                "kids": 77,
                "sib20neu": 1,  # ensure the 20th sibling is set
                "sib20pdx": 43
            }
        )

        # set all kids
        for i in range(1, 16):
            table[f'file.info.forms.json.kid{i}neu'] = 8

        handler = A3FamilyHandlerV3(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # more likely case
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 77,
                "kids": 77,
                "sib1neu": 8,
                "sib2neu": 8,
                # set nothing for kids, will still expect 9
            }
        )

        handler = A3FamilyHandlerV3(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == 9

    # TODO: FVP and sib/kid logic; most of how those work have already
    # been tested above, would still be good to be thorough though


class TestA3FamilyHandlerV4:
    """Test the A3FamilyHandlerV4 class.

    This one is a bit complicated in that it needs to look at the
    previous record for a specific variable, not necessarily the
    previous group status (especially for sibs/kids).
    """

    def test_parent_status_current_visit(self) -> None:
        """Test the parent logic works as expected when evaluating the current
        visit."""
        # case 1 - definite sets to yes/n
        table = set_working_family()
        table["file.info.forms.json"].update({"mometpr": "05", "dadetpr": "00"})
        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # case 2 - definite unknowns
        table["file.info.forms.json"].update({"mometpr": "99", "dadetpr": None})
        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == INFORMED_MISSINGNESS

        # case 3 - previous value set
        table = set_working_family(mom=1, dad=0)
        table["file.info.forms.json"].update(
            {
                "mometpr": "00",  # will override working value
                "dadetpr": "99",  # does not override working value
            }
        )
        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 0
        assert handler.record.dad_status == 0

    def test_parent_status_prev_record(self) -> None:
        """Test the parent logic works as expected when needing to pull from
        the previous record.

        In theory for parents this will be consistent with the working
        status as well, but we need to differentiate anyways for the
        kids/sibs.
        """
        table = set_working_family()
        table["file.info.forms.json"].update({"mometpr": "66", "dadetpr": "66"})
        table["_prev_record"] = {
            "info": {"resolved": {"mometpr": "09", "dadetpr": "99"}}
        }

        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 9

        # pull from raw data + has working values
        table = set_working_family(mom=9, dad=0)
        table["file.info.forms.json"].update(
            {"packet": "F", "nwinfpar": 1, "mometpr": "66", "dadetpr": "66"}
        )
        table["_prev_record"] = {
            "info": {
                "forms": {
                    "json": {
                        "mometpr": "06",  # overrides
                        "dadetpr": "99",  # does not override
                    }
                }
            }
        }

        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 1
        assert handler.record.dad_status == 0

        # nwinfpar != 1 in this case
        table = set_working_family(mom=9, dad=1)
        table["file.info.forms.json"].update(
            {"packet": "F", "nwinfpar": 0, "mometpr": "66", "dadetpr": "66"}
        )
        table["_prev_record"] = {
            "info": {
                "forms": {
                    "json": {
                        "mometpr": "06",  # would have overrode
                        "dadetpr": "00",  # would have overrode
                    }
                }
            }
        }

        handler = A3FamilyHandlerV4(table)
        assert handler.record.mom_status == 9
        assert handler.record.dad_status == 1

    def test_sibkids_status_prev_record(self) -> None:
        """Test the sib/kids logic works as expected when needing to pull from
        the previous record.

        This can get a bit complicated due to the fact that it is
        evaluating over ALL sibs/kids.
        """
        # case 1; updates status
        table = set_working_family(sib=9, kid=1)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "nwinfsib": 1,
                "nwinfkid": 1,
                "sibs": 2,
                "kids": 3,
                "sib1etpr": "66",
                "sib2etpr": "00",  # will cause the whole status to be 0 now
                "sib3etpr": "03",  # should be ignored
                "kid1etpr": "66",
                "kid2etpr": "66",
                "kid3etpr": "00",  # will cause the whole status to be 0 now
                "kid5etpr": "01",  # should be ignored
            }
        )
        table["_prev_record"] = {
            "info": {
                "resolved": {
                    "sib1etpr": "00",
                    "sib2etpr": "99",  # what should have caused it to be 9 last time
                    "kid1etpr": "00",
                    "kid2etpr": "00",
                    "kid3etpr": "01",  # what should have caused it to be 1 last time
                }
            }
        }
        handler = A3FamilyHandlerV4(table)
        assert handler.record.sib_status == 0
        assert handler.record.kid_status == 0

        # case 2: 66s just point to unknowns anyways, so working should
        # override; maybe the 1/0s got set at a far earlier visit
        table = set_working_family(sib=1, kid=0)
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "nwinfsib": 1,
                "nwinfkid": 1,
                "sibs": 2,
                "kids": 3,
                "sib1etpr": "66",
                "sib2etpr": "66",
                "kid1etpr": "66",
                "kid2etpr": "66",
                "kid3etpr": "66",
            }
        )
        table["_prev_record"] = {
            "info": {
                "resolved": {
                    "sib1etpr": "99",
                    "sib2etpr": "99",
                    "kid1etpr": "99",
                    "kid2etpr": "99",
                    "kid3etpr": "99",
                }
            }
        }
        handler = A3FamilyHandlerV4(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # case 3: cases that resultin 99s
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "packet": "F",
                "nwinfsib": 1,
                "nwinfkid": 1,
                "sibs": 2,
                "kids": 3,
                "sib1etpr": "99",  # changed to 99
                "sib2etpr": "66",
                "kid1etpr": "99",  # change to 99
                "kid2etpr": "66",
                "kid3etpr": "66",
            }
        )
        # in theory this kind of record would have set the overall
        # status to 0, which stays instead of 9, but this is just
        # testing the 66 behavior more than anything
        table["_prev_record"] = {
            "info": {
                "resolved": {
                    "sib1etpr": "00",
                    "sib2etpr": "00",
                    "kid1etpr": "00",
                    "kid2etpr": "00",
                    "kid3etpr": "00",
                }
            }
        }
        handler = A3FamilyHandlerV4(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == 9

    def test_sibkid_status_unknown_num(self) -> None:
        """Test when there is an unknown number of sibs/kids.

        Will end up looping through all, so most likely 9
        unless at least 1 is set to 1 or all are set to 0
        """
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 77,
                "kids": 77,
                "sib20etpr": '08',  # ensure the 20th sibling is set
            }
        )

        # set all kids
        for i in range(1, 16):
            table[f'file.info.forms.json.kid{i}etpr'] = '00'

        handler = A3FamilyHandlerV4(table)
        assert handler.record.sib_status == 1
        assert handler.record.kid_status == 0

        # more likely case
        table = set_working_family()
        table["file.info.forms.json"].update(
            {
                "sibs": 77,
                "kids": 77,
                "sib1etpr": '00',
                "sib2etpr": '00',
                # set nothing for kids, will still expect 9
            }
        )

        handler = A3FamilyHandlerV4(table)
        assert handler.record.sib_status == 9
        assert handler.record.kid_status == 9
