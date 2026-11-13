"""Tests BDS form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.bds.form_bds import (
    BDSFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "BDS",
                    }
                }
            }
        },
        "subject": {"info": {"working": {"cross-sectional": {"np-death-age": "86"}}}},
    }
    return SymbolTable(data)


def set_uds(table: SymbolTable) -> None:
    """Mark the subject as having UDS visits."""
    table["subject.info.working.cross-sectional.uds-visitdates"] = ["2020-01-01"]


class TestBDSFormAttributeCollection:
    def test_create_bds_naccdage(self, table):
        """Tests _create_bds_naccdage."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_naccdage() == 86

        # when not there
        table.pop("subject")
        assert attr._create_bds_naccdage() == 999

    def test_create_bds_naccsex(self, table):
        """Tests _create_bds_naccsex."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_naccsex() == INFORMED_MISSINGNESS

        table["file.info.forms.json.sex"] = "2"
        assert attr._create_bds_naccsex() == 2

        set_uds(table)
        assert BDSFormAttributeCollection(table)._create_bds_naccsex() is None

    def test_create_bds_nacchisp(self, table):
        """Tests _create_bds_nacchisp."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_nacchisp() == INFORMED_MISSINGNESS

        for value in [0, 1, 9]:
            table["file.info.forms.json.hispanic"] = value
            assert attr._create_bds_nacchisp() == value

        set_uds(table)
        assert BDSFormAttributeCollection(table)._create_bds_nacchisp() is None

    def test_create_bds_nacclang(self, table):
        """Tests _create_bds_nacclang."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_nacclang() == INFORMED_MISSINGNESS

        expected = {1: 1, 2: 2, 3: 3, 4: 3, 5: 5, 6: 6, 8: 8, 9: 9}
        for primlang, nacclang in expected.items():
            table["file.info.forms.json.primlang"] = primlang
            assert attr._create_bds_nacclang() == nacclang

        table["file.info.forms.json.primlang"] = 7
        with pytest.raises(AttributeDeriverError):
            attr._create_bds_nacclang()

        set_uds(table)
        assert BDSFormAttributeCollection(table)._create_bds_nacclang() is None

    def test_create_bds_nacclangx(self, table):
        """Tests _create_bds_nacclangx."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_nacclangx() == INFORMED_BLANK

        table["file.info.forms.json.primlang"] = 8
        table["file.info.forms.json.primlanx"] = "Klingon"
        assert attr._create_bds_nacclangx() == "Klingon"

        set_uds(table)
        assert BDSFormAttributeCollection(table)._create_bds_nacclangx() is None

    def test_create_bds_naccnihr(self, table):
        """Tests _create_bds_naccnihr."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_naccnihr() == INFORMED_MISSINGNESS

        for bdsrace in range(1, 7):
            table["file.info.forms.json.bdsrace"] = bdsrace
            assert attr._create_bds_naccnihr() == bdsrace

        table["file.info.forms.json.bdsrace"] = 9
        assert attr._create_bds_naccnihr() == 99

        table["file.info.forms.json.bdsrace"] = 7
        with pytest.raises(AttributeDeriverError):
            attr._create_bds_naccnihr()

        set_uds(table)
        assert BDSFormAttributeCollection(table)._create_bds_naccnihr() is None
