"""Tests MEDS form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.meds.form_meds import (
    MEDSFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4g": "2011-08-10",
                        "drugs_list": "d00004,d00170,d00269,d00321,d00732",
                        "module": "MEDS",
                        "formver": 2.0,
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def v1_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4": "2011-08-10",
                        "module": "MEDS",
                        "formver": 1.0,
                        "pma": "atenoLOL",
                        "pmb": "     ampicillin",
                        "pmc": "unknown drug",  # unknown
                        "pmf": "hctz",  # abbreviation
                        "pmt": "hydrochlorathiazide",  # misspelled
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def empty_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4": "2011-08-10",
                        "module": "MEDS",
                        "formver": 1.0,
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestMEDSFormAttributeCollection:
    def test_create_drugs_list(self, table):
        meds = MEDSFormAttributeCollection(table)
        assert meds._create_drugs_list() == [
            "d00004",
            "d00170",
            "d00269",
            "d00321",
            "d00732",
        ]

    def test_create_drugs_list_v1(self, v1_table):
        meds = MEDSFormAttributeCollection(v1_table)
        assert meds._create_drugs_list() == [
            "d00003",
            "d00004",
            "d00253",
            "d00253",
            "xxxxxx",  # unknowns are set to xxxxxx
        ]

    def test_create_drugs_list_v1_case2(self, v1_table):
        """This is how it usually actually appears in the form, with the large
        spacing."""
        v1_table["file.info.forms.json"].update(
            {
                "pma": "                        Zoloft",
                "pmb": "                        Toprol",
                "pmc": "                         Actos",
                "pmd": "                   Pravastatin",
                "pme": "                    Lisinopril",
                "pmf": "                         Zetia",
                "pmg": "                     Metformin",
                "pmh": "                       namenda",
            }
        )

        meds = MEDSFormAttributeCollection(v1_table)
        assert meds._create_drugs_list() == [
            "d00134",
            "d00253",
            "d00348",
            "d00732",
            "d00880",
            "d03807",
            "d04442",
            "d04824",
            "d04899",
        ]

    def test_replacement(self, table):
        """Test the two specific S codes get replaced to d04523."""
        table["file.info.forms.json.drugs_list"] = (
            "d00004,s10008,d00170,d00269,d00321,s10136,d00732"
        )
        meds = MEDSFormAttributeCollection(table)

        assert meds._create_drugs_list() == [
            "d00004",
            "d00170",
            "d00269",
            "d00321",
            "d00732",
            "d04523",
            "d04523",
        ]

    def test_meds_date(self, table):
        """Test date comes from _uds_visitdate."""
        table["_uds_visitdate"] = "2025-01-01"
        meds = MEDSFormAttributeCollection(table)
        assert str(meds.get_date()) == "2025-01-01"

        # assert error raised if no date found
        table["_uds_visitdate"] = None
        table["file.info.forms.json.frmdatea4g"] = None
        table["file.info.forms.json.frmdatea4"] = None

        with pytest.raises(AttributeDeriverError) as e:
            MEDSFormAttributeCollection(table)

        assert "Cannot determine MEDS form date" in str(e)

    def test_all_drug_types(self):
        """Test has all of PM/NM/VS drugs."""
        data = {
            "file": {
                "info": {
                    "forms": {
                        "json": {
                            "frmdatea4": "2000-01-01",
                            "module": "MEDS",
                            "formver": 1.0,
                            "nma": "Quinine sulfate",
                            "pma": "Levothyroxine",
                            "pmb": "warfarin",
                            "pmc": "lanoxin",
                            "pmd": "K-lor",
                            "pme": "Torsemide",
                            "vsa": "glucosamine",
                            "vsb": "chondroitin",
                            "vsc": "multivitamins",
                        }
                    }
                }
            }
        }

        meds = MEDSFormAttributeCollection(SymbolTable(data))

        assert meds._create_drugs_list() == [
            "d00022",
            "d00210",
            "d00278",
            "d00345",
            "d00366",
            "d03140",
            "d03189",
            "d04418",
            "d04419",
        ]
