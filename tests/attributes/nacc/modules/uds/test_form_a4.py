"""Tests form A4."""

import pytest
from typing import Any, Dict
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a4 import (
    UDSFormA4Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> Dict[str, Any]:
    return {
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
                        "anymeds": 1,
                        "naccid": "NACC123456",
                        "adcid": 0,
                    }
                }
            }
        },
    }


@pytest.fixture(scope="function")
def table1(table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    table.update(
        {
            "subject": {
                "info": {
                    "working": {
                        "cross-sectional": {
                            "drugs-list": {
                                "2025-01-01": [
                                    "d00131",  # triggers NACCAAAS
                                    "d00171",  # triggers NACCAANX
                                    "d00252",  # triggers NACCAC
                                    "d00006",  # triggers NACCACEI
                                ]
                            }
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
                        "cross-sectional": {
                            "drugs-list": {
                                "2025-01-01": [
                                    "d00132     ",  # triggers NACCVASD
                                    "     d00175",  # triggers NACCPDMD,
                                    "D07768",  # triggers NACCNSD
                                    "d00179",  # triggers NACCDIUR,
                                    "d03180",  # triggers NACCAPSY
                                    "unknown drug",  # unknown write-in, possible in V1
                                ]
                            }
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
