"""Tests NCRAD Biomarker attributes."""

import random
import pytest

import datetime
from nacc_attribute_deriver.attributes.derived.genetics.ncrad_biomarker import (
    NCRADBiomarkerAttributeCollection,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    MissingRequiredError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "provenance": {
                    "file_id": "12345",
                    "file_name": "0_ncrad-biomarker-dummy-return-15_identifiers.csv",
                    "flywheel_path": "fw://some/path/in/fw",
                    "created_date": "2020-01-01T00:00:00.000000+00:00",
                    "modified_date": "2025-01-01T00:00:00.000000+00:00",
                }
            }
        }
    }

    return SymbolTable(data)


class TestNCRADBiomarkerAttributeCollection:
    def test_create_past_ncrad_embargo(self, table):
        """Tests creating whether data is past NCRAD embargo."""
        attr = NCRADBiomarkerAttributeCollection(table)
        assert attr._create_past_ncrad_embargo() == 1

        # make the modified date now so it doesn't pass
        table["file.info.provenance.created_date"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        assert attr._create_past_ncrad_embargo() == 0

    def test_legacy_return_passes_embargo(self, table):
        """Test that legacy returns automatically pass embargo.

        Also tests regex works even with extra stuff in the filename.
        """
        return_round = random.choice(range(1, 15))
        file_name = (
            f"0_ncrad-biomarker-dummy-legacy-return-{return_round}"
            + "-other-text_identifiers.csv"
        )

        table["file.info.provenance"].update(
            {
                "file_name": file_name,
                "created_date": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
            }
        )

        attr = NCRADBiomarkerAttributeCollection(table)
        assert attr._create_past_ncrad_embargo() == 1

    def test_early_express_round_does_not_pass_embargo(self, table):
        """Test that an old legacy return does NOT pass embargo.

        Also tests regex works even with extra stuff in the filename.
        """
        return_round = random.choice(range(1, 15))
        file_name = (
            "0_ncrad-biomarker-abeta-42-adcfb-express-return-"
            + f"{return_round}_identifiers.csv"
        )

        table["file.info.provenance"].update(
            {
                "file_name": file_name,
                "created_date": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
            }
        )

        attr = NCRADBiomarkerAttributeCollection(table)
        assert attr._create_past_ncrad_embargo() == 0

    def test_bad_created_date(self, table):
        """Tests create_past_ncrad_embargo with bad created date."""
        table["file.info.provenance.created_date"] = None
        with pytest.raises(MissingRequiredError) as e:
            NCRADBiomarkerAttributeCollection(table)

        assert (
            str(e.value)
            == "missing required attributes: file.info.provenance.created_date"
        )

        table["file.info.provenance.created_date"] = "hello world"
        attr = NCRADBiomarkerAttributeCollection(table)
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value) == "Failed to convert created_date to datetime object"

    def test_bad_file_name(self, table):
        """Tests create_past_ncrad_embargo with bad file name."""
        table["file.info.provenance.file_name"] = ""
        with pytest.raises(MissingRequiredError) as e:
            NCRADBiomarkerAttributeCollection(table)

        assert (
            str(e.value)
            == "missing required attributes: file.info.provenance.file_name"
        )

        # missing leading number
        table["file.info.provenance.file_name"] = (
            "ncrad-biomarker-return-5_identifiers.csv"
        )
        attr = NCRADBiomarkerAttributeCollection(table)
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value).startswith(
            "Biomarker filename does not match expected regex"
        )

        # missing ncrad-biomarker
        table["file.info.provenance.file_name"] = "0_-return-5_identifiers.csv"
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value).startswith(
            "Biomarker filename does not match expected regex"
        )

        # missing _identifiers
        table["file.info.provenance.file_name"] = "0_ncrad-biomarker-n2pb-return-5.csv"
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value).startswith(
            "Biomarker filename does not match expected regex"
        )

        # something after the _identifiers
        table["file.info.provenance.file_name"] = (
            "0_ncrad-biomarker-n2pb-return-5_identifiers_other.csv"
        )
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value).startswith(
            "Biomarker filename does not match expected regex"
        )

        # missing round
        table["file.info.provenance.file_name"] = (
            "0_ncrad-biomarker-n2pb-return-_identifiers.csv"
        )
        with pytest.raises(AttributeDeriverError) as e:
            assert attr._create_past_ncrad_embargo()

        assert str(e.value).startswith(
            "Biomarker filename does not match expected regex"
        )

    def test_weird_but_okay_file_name(self, table):
        """Tests create_past_ncrad_embargo with a filename that is unexpected
        but otherwise acceptable."""
        table["file.info.provenance.file_name"] = (
            "089237832490_ncrad-biomarker-a-lot-of-text---describing the-return-"
            + "return-899999-and-things-after-too!!! xyz_identifiers.csv"
        )
        attr = NCRADBiomarkerAttributeCollection(table)
        assert attr._create_past_ncrad_embargo() == 1
