"""
Attribute utils
"""
import re
from datetime import datetime
from typing import Any, Dict, List, Union

from nacc_attribute_deriver.symbol_table import SymbolTable

def generate_dob(table: SymbolTable) -> datetime:
    """Creates DOB, which is used to calculate ages."""
    birthmo = table.get('file.info.forms.json.birthmo')
    birthyr = table.get('file.info.forms.json.birthyr')
    formdate = table.get('file.info.forms.json.visitdate')
    if None in [birthmo, birthyr, formdate]:
        return None

    return datetime(int(birthyr), int(birthmo), 1)


def datetime_from_form_date(date_string: str) -> datetime:
    """Converts date string to datetime based on format.

    Expects either `%Y-%m-%d` or `%m/%d/%Y`.

    Args:
      date_string: the date string
    Returns:
      the date as datetime
    """
    if not date_string:
        return None

    if re.match(r"\d{4}-\d{2}-\d{2}", date_string):
        return datetime.strptime(date_string, "%Y-%m-%d")

    return datetime.strptime(date_string, "%m/%d/%Y")


def is_int_value(value: Union[int, str], target: int) -> bool:
    """Check whether the value is the specified target int.
    This might be overkill but I wanted it to handle str/int comparisons.

    Args:
        value: Field to check
        target: Target to check against
    """
    if not value:
        return False

    try:
        return int(value) == target
    except ValueError as e:
        return False

    return False


def aggregate_variables(mapping: Dict[str, Any],
                        table: SymbolTable,
                        default: Any = None) -> Dict[str, Any]:
    """Aggregates all the variables defined in the mapping.

    Args:
        mapping: Mapping to iterate over. Grabs the field and sets it
                 to the found/derived value.
        table: Table with FW metadata
        default: Default value to set aggregation to if not found
    Returns:
        The aggregated variables
    """
    result = {}
    for field, label in mapping.items():
        result[field] = table.get(field, default)

    return result


def assert_required(source: str, required: List[str], table: SymbolTable) -> Dict[str, Any]:
    """Asserts that the given fields in required are in the
    table for the source

    Args:
        source: Source function that requires variables
        required: The required fields
        table: The table the fields should be set in
    Returns:
        The found required variables, flattened out from the table
    """
    found = {}
    for r in required:
        full_field = f'file.info.derived.{r}'  # TODO: will NACC derived variables always be in file.info.derived?
        if full_field not in table:            # TODO: maybe can implicitly derive even if schema didn't define it?
            raise ValueError(f"{full_field} must be derived before {source} can run")

        found[r] = table[full_field]

    return found
