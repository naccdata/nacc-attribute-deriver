"""Tests cross-module attributes."""

import pytest
from typing import Any, Dict

from nacc_attribute_deriver.attributes.derived.modules.cross_module import (
    CrossModuleAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


def create_working_table(data: Dict[str, Any]) -> SymbolTable:
    """Create dummy working data, add the specified data under working.cross-
    sectional, and return the table."""
    table = SymbolTable({"subject": {"info": {"working": {"cross-sectional": data}}}})
    return table


class TestCrossModuleAttribute:
    def test_create_naccint(self):
        """Tests _create_naccint."""
        # NP death date available, but day unknown; approximate
        table = create_working_table(
            {
                "np-death-date": {
                    "value": "2025-11-99",
                    "date": "2025-07-19",
                },
                "np-death-age": 73,
                "uds-visitdates": ["2025-01-01"],
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 10

        # set UDS so approximation calculates 11, also add other UDS visitdates
        # just as a sanity check it uses the latest one
        table["subject.info.working.cross-sectional.uds-visitdates"] = [
            "2024-12-15",
            "2023-02-14",
            "2021-12-23",
        ]
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 11

        # Milestone death date available, but day and month unknown,
        # so should return 999
        table = create_working_table(
            {
                "milestone-death-date": {
                    "value": "2025-99-99",
                    "date": "2025-07-19",
                },
                "uds-visitdates": ["2025-01-01"],
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 999

        # sanity check, make it known with full date
        table = create_working_table(
            {
                "milestone-death-date": {
                    "value": "2025-04-21",
                    "date": "2025-07-19",
                },
                "uds-visitdates": ["2025-01-01"],
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 3

        # and when they're not dead, but say, discontinued
        table = create_working_table(
            {
                "milestone-discontinued-date": {
                    "value": "2025-04-21",
                    "date": "2025-07-19",
                },
                "uds-visitdates": ["2025-01-01"],
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 888
