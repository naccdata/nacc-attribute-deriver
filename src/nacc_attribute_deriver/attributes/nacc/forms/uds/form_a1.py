"""
Derived variables from form D1.
"""
from typing import List
from nacc_attribute_deriver.attributes.utils.utils import (
    is_int_value,
    datetime_from_form_date,
    generate_dob
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from .form_a1_helpers import generate_naccnihr


def _create_naccage(table: SymbolTable) -> str:
    """Creates DOB from BIRTHMO and BIRTHYR and
    compares to form date.

    Location:
        file.info.derived.naccage
    Event:
        update
    Type:
        longitudinal
    Description:
        Subject's age at visit
    """
    dob = generate_dob(table)
    visitdate = table.get('file.info.forms.json.visitdate', None)

    if not dob or not visitdate:
        return None

    visitdate = datetime_from_form_date(visitdate)

    # .25 is due to leap year/how we defined it for error checks
    # not sure if we want to do the same here
    return (formdate - dob) // timedelta(days=365.25)


def _create_naccnihr(table: SymbolTable) -> int:
    """Creates NACCNIHR (race)

    Location:
        file.info.derived.naccnihr
    Event:
        update
    Type:
        longitudinal
    Description:
        Subject's age at visit
    """
    return generate_naccnihr(
        race=table.get('file.info.forms.json.race'),
        racex=table.get('file.info.forms.json.racex'),
        racesec=table.get('file.info.forms.json.racesec'),
        racesecx=table.get('file.info.forms.json.racesecx'),
        raceter=table.get('file.info.forms.json.raceter'),
        raceterx=table.get('file.info.forms.json.raceterx')
    )
