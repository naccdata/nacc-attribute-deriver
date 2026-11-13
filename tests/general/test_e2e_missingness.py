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
        "cdrglob": -4.0,
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


def test_file_sanity_check():
    """Sanity check for the file and subject levels just to make sure they
    run."""
    MissingnessDeriver(missingness_level="file")
    MissingnessDeriver(missingness_level="subject")


def test_bds_form():
    """Test BDS gated missingness through the file-level rules."""
    table = SymbolTable(
        {
            "file": {
                "info": {
                    "forms": {
                        "json": {
                            "module": "BDS",
                            "visitdate": "2025-01-01",
                            "formver": "1.0",
                            "adcid": "1",
                            "bdsudsd": "1",
                        }
                    }
                }
            }
        }
    )
    MissingnessDeriver(missingness_level="file").curate(table, "bds")

    resolved = table["file.info.resolved"]
    assert resolved["bdstmci"] == 8
    assert resolved["bdsetpr"] == 88
    assert resolved["bdscoalz"] == 8
    assert resolved["bdscoo3f"] == 8


def test_ds_form():
    """Test DS A1D and B1D missingness through the file-level rules."""
    table = SymbolTable(
        {
            "file": {
                "info": {
                    "forms": {
                        "json": {
                            "module": "DS",
                            "visitdate": "2025-01-01",
                            "formver": "1.0",
                            "adcid": "1",
                            "dsmomage": "777",
                            "dshrtrpr": "0",
                            "dscrdsrg": "1",
                            "dscrdsyr": "7777",
                            "dsdxhs_no": "1",
                        }
                    }
                },
            },
            "_prev_record": {"info": {"resolved": {"dsmomage": 30}}},
        }
    )
    MissingnessDeriver(missingness_level="file").curate(table, "ds")

    resolved = table["file.info.resolved"]
    assert resolved["dsmomage"] == 30
    assert resolved["dsmnsage"] == -4
    assert resolved["dshrtryr"] == 8888
    assert resolved["dscrdsyr"] == 9999

    # B1D: no MCI/dementia diagnosis, no repeat recommendation
    assert resolved["dsdxhs_mci"] == 0
    assert resolved["dsdxhs_dem"] == 0
    assert resolved["dsmcimo"] == 88
    assert resolved["dsmciyr"] == 8888
    assert resolved["dsdemmo"] == 88
    assert resolved["dsdemyr"] == 8888
    assert resolved["dsdxby"] == 8
    assert resolved["dsonstmo"] == 88
    assert resolved["dsonstyr"] == 8888
    assert resolved["dsrepmo"] == 888
