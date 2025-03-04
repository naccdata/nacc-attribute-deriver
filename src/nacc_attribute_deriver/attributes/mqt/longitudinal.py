"""
All longtitudinal MQT derived variables.
Assumes NACC-derived variables are already set
"""
from nacc_attribute_deriver.symbol_table import SymbolTable

def _create_total_uds_visits(table: SymbolTable) -> int:
    """Total number of UDS visits.

    This is an accumulative variable, assumes its called
    for each form

    Location:
        subject.info.longitudinal-data.uds.count.latest
    Event:
        latest
    Type:
        mqt-longitudinal
    Description:
        Total number of UDS visits
    """
    count = table.get('subject.info.longitudinal-data.uds.count.latest.value', 0)
    module = table.get('file.info.forms.json.module')
    if module and module.lower() == 'uds':
        count += 1

    return count


def _create_years_of_uds(table: SymbolTable) -> int:
    """Creates subject.info.longitudinal-data.uds.year-count.latest
    
    TODO Not clear how this is supposed to be calculated.

    Location:
        TODO
    Event:
        update
    Type:
        mqt-longitudinal
    Description:
        Number of years of UDS visits available
    """
    pass
