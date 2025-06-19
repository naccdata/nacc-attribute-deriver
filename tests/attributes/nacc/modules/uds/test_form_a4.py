"""Tests form A4."""

import pytest
from typing import Any, Dict
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a4 import (
    UDSFormA4Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


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
                    }
                }
            }
        },
    }


@pytest.fixture(scope="function")
def meds_table(table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    table.update(
        {
            "subject": {
                "info": {
                    "derived": {
                        "drugs_list": {
                            "2025-01-01": [
                                "d00131",  # triggers NACCAAAS
                                "d00171",  # triggers NACCAANX
                                "d00252",  # triggers NACCAC
                                "d00006",  # triggers NACCACEI
                            ]
                        }
                    }
                }
            },
        }
    )

    return SymbolTable(table)


@pytest.fixture(scope="function")
def udsmeds_table(table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    table.update(
        {
            "subject": {
                "info": {
                    "derived": {
                        "drugs_list": {
                            "2025-01-01": [
                                "hydrALAZINE     ",  # triggers NACCVASD
                                "Benztropine Mesylate",  # triggers NACCPDMD,
                                "acetaminophen/magnesium salicylate/pamabrom",  # triggers NACCNSD
                                "BUMETAMIDE",  # known typo/alternative, triggers NACCDIUR,
                                "   RISPERADONE",  # known typo/alternative, triggers NACCAPSY
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
    def test_drugs_from_meds_file(self, meds_table):
        """Tests A4 derived variables when using MEDS file."""
        attr = UDSFormA4Attribute(meds_table)
        assert attr._create_naccamd() == 4
        assert attr._create_naccaaas() == 1
        assert attr._create_naccaanx() == 1
        assert attr._create_naccac() == 1
        assert attr._create_naccacei() == 1

        assert attr._create_naccahtn() == 1  # based on others
        assert attr._create_naccvasd() == 0

    def test_drugs_from_udsmeds_table(self, udsmeds_table):
        """Tests A4 derived variables when using UDSMEDS table."""
        attr = UDSFormA4Attribute(udsmeds_table)
        assert attr._create_naccamd() == 5
        assert attr._create_naccvasd() == 1
        assert attr._create_naccpdmd() == 1
        assert attr._create_naccnsd() == 1
        assert attr._create_naccdiur() == 1
        assert attr._create_naccapsy() == 1

        assert attr._create_naccahtn() == 1  # based on others
        assert attr._create_naccadmd() == 0
