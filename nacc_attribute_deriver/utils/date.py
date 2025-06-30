"""Helper methods related to dates."""

import re
from datetime import date, datetime
from typing import List, Optional, Set, Union


def datetime_from_form_date(date_string: Optional[str]) -> Optional[datetime]:
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


def calculate_age(date1: date | None, date2: date | None) -> Optional[int]:
    """Calculate age in years between two dates.

    Args:
        date1: The earlier date
        date2: The later date
    Returns:
        The age between the two dates in years
    """
    if not date1 or not date2:
        return None

    # use date objects, not doing division with leap year
    # since it's not always precise when visitdate == birthdate

    return abs(
        (date2.year - date1.year)
        - ((date2.month, date2.day) < (date1.month, date1.day))
    )


def calculate_months(date1: date | None, date2: date | None) -> Optional[int]:
    """Calculates the interval in months between two dates.

    Args:
        date1: The earlier date
        date2: The later date
    Returns:
        The interval in months between the two dates
    """
    if not date1 or not date2:
        return None

    return abs((date2.year - date1.year) * 12 + date2.month - date1.month)


def calculate_days(date1: date | None, date2: date | None) -> Optional[int]:
    """Calculates the interval in days between two dates.

    Args:
        date1: The earlier date
        date2: The later date
    Returns:
        The interval in days between the two dates
    """
    if not date1 or not date2:
        return None

    return abs((date2 - date1).days)


def get_unique_years(dates: List[str]) -> Set[int]:
    """Gets unique years from list of string dates.

    Args:
        dates: List of dates to get unique years from
    """
    years = [datetime_from_form_date(x) for x in dates]
    return set(x.year for x in years if x is not None)


def create_death_date(
    *,
    year: Optional[Union[str, int]],
    month: Optional[Union[str, int]],
    day: Optional[Union[str, int]],
) -> Optional[date]:
    """Creates the death date, handling conventions for unknown dates."""

    if not year:
        return None
    if not month:
        month = "7"
    if not day:
        day = "1"

    try:
        dyr = int(year)
        dmo = int(month)
        ddy = int(day)
    except (TypeError, ValueError):
        return None

    if dyr == 9999:
        return None

    if dmo > 12:
        dmo = 7
    if ddy > 31:
        ddy = 1

    date_value = datetime_from_form_date(f"{dyr}-{dmo:02d}-{ddy:02d}")
    if not date_value:
        return None

    return date_value.date()
