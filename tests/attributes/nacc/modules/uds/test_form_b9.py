"""Tests UDS Form B9 attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b9 import (
    UDSFormB9Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    data = {
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
                        "b9chg": 1,
                        "befpred": 0,
                    }
                }
            }
        },
        "subject": {
            "info": {
                "working": {
                    # "longitudinal": {
                    #     "decclin": [{"date": "2024-12-01", "value": 0}],
                    #     "befrst": [
                    #         {"date": "2024-01-01", "value": 88},
                    #         {"date": "2025-01-01", "value": 0},
                    #     ],
                    "cross-sectional": {
                        "decclin": {
                            "initial": {
                                "date": "2024-01-01",
                                "value": 0
                            }
                        },
                        "befrst": {
                            "initial": {
                                "date": "2024-01-01",
                                "value": 0
                            }
                        },
                        "mofrst": {
                            "initial": {
                                "date": "2024-01-01",
                                "value": 3
                            }
                        }
                    },
                    "longitudinal": {
                        "mofrst": [
                            {
                                "date": "2024-01-01",
                                "value": 3
                            },
                            {
                                "date": "2024-05-01",
                                "value": 0
                            }
                        ]
                    }
                }
            }
        },
    }

    return SymbolTable(data)


class TestUDSFormB9Attribute:

    def test_determine_carryover(self):
        """Test determining the carryover value, where 0 == look at previous record."""
        table = SymbolTable({
            "file": {
                "info": {
                    "forms": {
                        "json": {
                            "visitdate": "2025-01-01",
                            "birthmo": 3,
                            "birthyr": 1990,
                            "module": "UDS",
                            "packet": "F",
                            "formver": "3.0",
                            "var": 0,
                            "null_var": 0
                        }
                    }
                }
            },
            "subject": {
                "info": {
                    "working": {
                        "longitudinal": {
                            "var": [
                                {
                                    "date": "2023-01-01",
                                    "value": 6
                                },
                                {
                                    "date": "2024-01-01",
                                    "value": 2
                                }
                            ]
                        }
                    }
                }
            }
        })

        attr = UDSFormB9Attribute(table)
        assert attr.determine_carryover("var") == 2

        # when there is no previous value - return as-is
        assert attr.determine_carryover("null_var") == 0

    # def test_grab_prev(self, table):
    #     """Test the grab_prev method.

    #     Need to get around name mangling just for this test.
    #     """
    #     attr = UDSFormB9Attribute(table)
    #     assert attr.grab_prev("decclin", attr._UDSFormB9Attribute__working_derived) == 0

    #     # this should ignore the second record since it has the
    #     # same visitdate as the current record
    #     assert attr.grab_prev("befrst", attr._UDSFormB9Attribute__working_derived) == 88

    #     # no previous record
    #     assert attr.grab_prev("cogfrst", attr._UDSFormB9Attribute__working_derived) is None

    # def test_create_naccbehf(self, table, working_derived_prefix):
    #     """Tests create NACCBEHF."""
    #     attr = UDSFormB9Attribute(table)
    #     assert attr._create_naccbehf() == 0

    #     # p_befpred drives value when formver >= 3
    #     set_attribute(
    #         table,
    #         working_derived_prefix,
    #         "cross-sectional.befpred.initial",
    #         {"date": "2024-01-01", "value": "3"},
    #     )
    #     assert attr._create_naccbehf() == 3
    #     set_attribute(
    #         table,
    #         working_derived_prefix,
    #         "cross-sectional.befpred.initial",
    #         {"date": "2024-01-01", "value": "0"},
    #     )
    #     assert attr._create_naccbehf() == 99
