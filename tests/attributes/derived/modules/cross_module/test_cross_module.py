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

    def test_discontinued_dates(self) -> None:
        """Test discontinued dates are set correctly when only
        one of or neither of discontinued or minimum contact is defined.
        """
        # discontinued defined
        table = create_working_table(
            {
                "milestone-discontinued-date": {
                    "value": "9999-12-21",
                    "date": "2024-01-19",
                }
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 9999
        assert attr._create_naccdsmo() == 12
        assert attr._create_naccdsdy() == 21

        # minimum contact defined
        table = create_working_table(
            {
                "milestone-minimum-contact-date": {
                    "value": "2023-01-18",
                    "date": "2024-01-19",
                },
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 2023
        assert attr._create_naccdsmo() == 1
        assert attr._create_naccdsdy() == 18

        # neither defined
        table = create_working_table({})
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 8888
        assert attr._create_naccdsmo() == 88
        assert attr._create_naccdsdy() == 88

    def test_discontinued_dates_both_defined(self) -> None:
        """Test discontinued dates are set correctly when both
        discontinued AND minimum contact status is defined.
        """
        # set discontinued came later
        table = create_working_table(
            {
                "milestone-discontinued-date": {
                    "value": "2025-04-99",
                    "date": "2025-07-19",
                },
                "milestone-minimum-contact-date": {
                    "value": "2024-02-13",
                    "date": "2024-01-19",
                },
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 2025
        assert attr._create_naccdsmo() == 4
        assert attr._create_naccdsdy() == 99

        # set mlst came later but barely
        table = create_working_table(
            {
                "milestone-discontinued-date": {
                    "value": "2024-02-12",
                    "date": "2024-05-12",
                },
                "milestone-minimum-contact-date": {
                    "value": "2024-02-13",
                    "date": "2024-01-19",
                },
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 2024
        assert attr._create_naccdsmo() == 2
        assert attr._create_naccdsdy() == 13

        # set dates ambiguous, compare on form date, but both
        # are still the same, so use discontinued
        table = create_working_table(
            {
                "milestone-discontinued-date": {
                    "value": "9999-99-99",
                    "date": "2024-01-19",
                },
                "milestone-minimum-contact-date": {
                    "value": "9999-12-15",
                    "date": "2024-01-19",
                },
            }
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsyr() == 9999
        assert attr._create_naccdsmo() == 99
        assert attr._create_naccdsdy() == 99
