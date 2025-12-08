"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all.
"""

from nacc_attribute_deriver.attribute_deriver import MissingnessDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form(uds_table):
    """Test UDS."""
    deriver = MissingnessDeriver(missingness_level="test")

    uds_table["file.info.forms.json"].update(
        {"height": "53.1", "heigdec": "5", "trailb": "996"}
    )

    deriver.curate(uds_table, "uds")

    assert uds_table["file.info.resolved"] == {
        "npiqinf": -4,
        "npiqinfx": None,
        "height": 53.6,
        "trailbrr": 96,
    }


def test_np_form():
    """Test NP."""
    np_table = SymbolTable(
        {
            "file": {
                "info": {"forms": {"json": {"visitdate": "2020-01-01", "formver": 11}}}
            }
        }
    )
    deriver = MissingnessDeriver(missingness_level="test")
    deriver.curate(np_table, "np")

    assert np_table["file.info.resolved"] == {"npsex": -4, "nppmih": -4.4}


def test_csf_subject():
    """Test CSF missingness at the subject level."""
    form = SymbolTable()
    form["subject.info.derived.cross-sectional"] = {
        "naccacsf": 1,
        "naccpcsf": 0,
        #  NACCTCSF should be filled in by missingness
    }

    deriver = MissingnessDeriver(missingness_level="subject")
    deriver.curate(form, "csf")

    assert form.to_dict() == {
        "subject": {
            "info": {
                "derived": {
                    "cross-sectional": {"naccacsf": 1, "naccpcsf": 0, "nacctcsf": 0}
                }
            }
        },
    }


def test_mds_form():
    """Test MDS."""
    mds_table = SymbolTable(
        {
            "file": {
                "info": {
                    "forms": {
                        "json": {"visitdate": "2020-01-01", "formver": 11, "agedem": 75}
                    }
                }
            }
        }
    )
    deriver = MissingnessDeriver(missingness_level="test")
    deriver.curate(mds_table, "mds")

    # only apoe is set since agedem exists
    assert mds_table["file.info.resolved"] == {"agedem": 75, "apoe": -4}
