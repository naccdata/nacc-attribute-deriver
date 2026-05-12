"""Tests NCRAD Biomarker attributes."""

import pytest

import datetime
from nacc_attribute_deriver.attributes.derived.genetics.ncrad_biomarker import (
    NCRADBiomarkerAttributeCollection,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "provenance": {
            "file_id": "12345",
            "file_name": "dummy_parent_file.csv",
            "flywheel_path": "fw://some/path/in/fw",
            "modified_date": "2020-01-01T00:00:00.000000+00:00",
        }
    }

    return SymbolTable(data)


class TestNCRADBiomarkerAttributeCollection:
    def test_create_past_ncrad_embargo(self, table):
        """Tests creating whether data is past NCRAD embargo."""
        attr = NCRADBiomarkerAttributeCollection(table)
        assert attr._create_past_ncrad_embargo() == 1

        # make the modified date now so it doesn't pass
        table["provenance"]["modified_date"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        assert attr._create_past_ncrad_embargo() == 0

    def test_create_past_ncrad_embargo_bad_provenance(self, table):
        """Tests create_past_ncrad_embargo with bad data."""
        table["provenance"]["modified_date"] = None
        attr = NCRADBiomarkerAttributeCollection(table)

        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value) == "modified_date not found in biomarker provenance data"

        table["provenance"]["modified_date"] = "hello world"
        attr = NCRADBiomarkerAttributeCollection(table)

        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value) == "Failed to calculate embargo date"
