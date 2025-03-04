"""
Derived variables that rely on other forms.
"""
from datetime import datetime, timedelta

from nacc_attribute_deriver.attributes.utils.utils import (
    datetime_from_form_date,
    generate_dob,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


def _create_naccdage(table: SymbolTable) -> int:
    """From derive.sas and derivenew.sas

    Grabs data from NP -> MDS -> UDS forms. This might not be totally correct.

    Location:
        file.info.derived.naccdage
    Event:
        update
    Type:
        cross-sectional
    Description:
        Age at death
    """
    dod = None
    # NP
    npdage = table.get('np.info.forms.json.npdage')
    if npdage:
        dod = npdage

    # milestone
    if not dod and table.get('mds.info.forms.json.deceased') == 1:
        dyr = table.get('mds.info.forms.json.deathyr')
        dmo = table.get('mds.info.forms.json.deathmo')
        ddy = table.get('mds.info.forms.json.deathdy')
        dod = '/'.join([dyr, dmo, ddy])

    # UDS
    # looks like looking at UDS is just for NACCINT?

    if not dod:
        return 999

    dob = generate_dob(table)  # from UDS
    dod = datetime_from_form_date(dod)

    return dod - dob // timedelta(days=365.25)
