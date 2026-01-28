"""Tests form A4."""

import pytest
import random
from typing import Any, Dict
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a4 import (
    UDSFormA4Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table(uds_table) -> Dict[str, Any]:
    uds_table["file.info.forms.json"].update({"a4sub": 1, "frmdatea4": "2025-01-01"})
    return uds_table


@pytest.fixture(scope="function")
def table1(table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    table.update(
        {
            "subject": {
                "info": {
                    "working": {
                        "longitudinal": {
                            "drugs-list": [
                                {
                                    "date": "2025-01-01",
                                    "value": [
                                        "d00131",  # triggers NACCAAAS
                                        "d00171",  # triggers NACCAANX
                                        "d00252",  # triggers NACCAC
                                        "d00006",  # triggers NACCACEI
                                    ],
                                }
                            ]
                        }
                    }
                }
            },
        }
    )

    return SymbolTable(table)


@pytest.fixture(scope="function")
def table2(table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable.

    Badly formed.
    """
    table.update(
        {
            "subject": {
                "info": {
                    "working": {
                        "longitudinal": {
                            "drugs-list": [
                                {
                                    "date": "2025-01-01",
                                    "value": [
                                        "d00132     ",  # triggers NACCVASD
                                        "     d00175",  # triggers NACCPDMD,
                                        "D07768",  # triggers NACCNSD
                                        "d00179",  # triggers NACCDIUR,
                                        "d03180",  # triggers NACCAPSY
                                        "unknown drug",  # unknown write-in
                                    ],
                                }
                            ]
                        }
                    }
                }
            },
        }
    )

    table["file"]["info"]["forms"]["json"]["formver"] = "1.0"

    return SymbolTable(table)


class TestUDSFormA4Attribute:
    def test_drugs_1(self, table1):
        """Tests A4 derived variables, well formed."""
        attr = UDSFormA4Attribute(table1)
        assert attr._create_naccamd() == 4
        assert attr._create_naccaaas() == 1
        assert attr._create_naccaanx() == 1
        assert attr._create_naccac() == 1
        assert attr._create_naccacei() == 1

        assert attr._create_naccahtn() == 1  # based on others
        assert attr._create_naccvasd() == 0

    def test_drugs_2(self, table2):
        """Tests A4 derived variables, badly formed from V1."""
        attr = UDSFormA4Attribute(table2)
        assert attr._create_naccamd() == 6
        assert attr._create_naccvasd() == 1
        assert attr._create_naccpdmd() == 1
        assert attr._create_naccnsd() == 1
        assert attr._create_naccdiur() == 1
        assert attr._create_naccapsy() == 1

        assert attr._create_naccahtn() == 1  # based on others
        assert attr._create_naccadmd() == 0

    def __check_derived_values(
        self, attr: UDSFormA4Attribute, expected_value: int
    ) -> None:
        """Check all derived values return the expected value based on the
        submitted property."""
        assert attr._create_naccamd() == expected_value
        assert attr._create_naccaaas() == expected_value
        assert attr._create_naccaanx() == expected_value
        assert attr._create_naccac() == expected_value
        assert attr._create_naccacei() == expected_value
        assert attr._create_naccadep() == expected_value
        assert attr._create_naccadmd() == expected_value
        assert attr._create_naccahtn() == expected_value
        assert attr._create_naccacei() == expected_value
        assert attr._create_naccaaas() == expected_value
        assert attr._create_naccbeta() == expected_value
        assert attr._create_naccccbs() == expected_value
        assert attr._create_naccdiur() == expected_value
        assert attr._create_naccvasd() == expected_value
        assert attr._create_nacchtnc() == expected_value
        assert attr._create_naccangi() == expected_value
        assert attr._create_naccangi() == expected_value
        assert attr._create_naccapsy() == expected_value
        assert attr._create_naccbeta() == expected_value
        assert attr._create_naccccbs() == expected_value
        assert attr._create_naccdbmd() == expected_value
        assert attr._create_naccdiur() == expected_value
        assert attr._create_naccemd() == expected_value
        assert attr._create_naccepmd() == expected_value
        assert attr._create_nacchtnc() == expected_value
        assert attr._create_nacclipl() == expected_value
        assert attr._create_naccnsd() == expected_value
        assert attr._create_naccpdmd() == expected_value
        assert attr._create_naccvasd() == expected_value

    def test_submitted_property(self, uds_table):
        """Test the submitted property works as expected."""
        # For V1 - V3, use anysub, for V4 use anymeds
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice([1.0, 2.0, 3.0, 3.2]), "a4sub": 1}
        )
        attr = UDSFormA4Attribute(uds_table)

        # submitted, but no drugs, so should all return 0
        assert attr.submitted
        self.__check_derived_values(attr, 0)

        # NOT submitted, should return -4
        uds_table["file.info.forms.json.a4sub"] = 0
        assert not attr.submitted
        self.__check_derived_values(attr, -4)

        # For V4, use ANYMEDS. Only -4 if ANYMEDS is missing
        uds_table["file.info.forms.json"].update({"formver": 4.0, "anymeds": 0})
        attr = UDSFormA4Attribute(uds_table)

        assert attr.submitted
        self.__check_derived_values(attr, 0)

        uds_table["file.info.forms.json.anymeds"] = 1
        assert attr.submitted
        self.__check_derived_values(attr, 0)

        uds_table["file.info.forms.json.anymeds"] = None
        assert not attr.submitted
        self.__check_derived_values(attr, -4)

    def test_naccamd_range_enforced(self, table1):
        """Ensure range is enforced for NACCAMD."""
        table1["subject.info.working.longitudinal"].update(
            {
                "drugs-list": [
                    {"date": "2025-01-01", "value": [str(i) for i in range(43)]}
                ]
            }
        )
        attr = UDSFormA4Attribute(table1)
        assert attr._create_naccamd() == 40

        table1["subject.info.working.longitudinal"].update(
            {
                "drugs-list": [
                    {"date": "2025-01-01", "value": [str(i) for i in range(39)]}
                ]
            }
        )
        attr = UDSFormA4Attribute(table1)
        assert attr._create_naccamd() == 39
