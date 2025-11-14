"""Keeps track of global constants."""

INVALID_TEXT = ["", ".", "`", "--", "-"]
INFORMED_MISSINGNESS = -4
INFORMED_MISSINGNESS_FLOAT = -4.4
INFORMED_BLANK = "blank"  # will be translated to an overriding None

CURATION_TYPE = ["create", "missingness"]

# For form B6
GDS_VARS = [
    "satis",
    "dropact",
    "empty",
    "bored",
    "spirits",
    "afraid",
    "happy",
    "helpless",
    "stayhome",
    "memprob",
    "wondrful",
    "wrthless",
    "energy",
    "hopeless",
    "better",
]

# For form A4 derived variables
COMBINATION_RX_CLASSES = [
    "C02L",
    "C07B",
    "C07C",
    "C09B",
    "C09D",
    "G03F",
]

NON_COMBINATION_RX_CLASSES = [
    "A10",
    "B01",
    "C01D",
    "C02A",
    "C02B",
    "C02C",
    "C02D",
    "C02L",
    "C03",
    "C07A",
    "C07B",
    "C07C",
    "C08",
    "C09A",
    "C09B",
    "C09C",
    "C09D",
    "C10",
    "G03C",
    "G03F",
    "N04",
    "N05A",
    "N05B",
    "N05C",
    "N06A",
    "N06D",
    "M01A",
]

ALL_RX_CLASSES = COMBINATION_RX_CLASSES + NON_COMBINATION_RX_CLASSES


# REGRESSION: let these go through and evaluate missingness logic
# these are variables that ideally should be -4 if they are not
# applicable to the version, but the SAS code does set them to
# something, so for now we let them through
REGRESSION_VARIABLES = [
    "diabtype",
    "height",
    "trailarr",
    "trailali",
    "trailbrr",
    "trailbli",
    "cogoth2f",
    "cogoth3f",
]
