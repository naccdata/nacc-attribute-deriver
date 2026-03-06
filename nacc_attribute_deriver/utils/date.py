"""Helper methods related to dates."""

import re
from datetime import date, datetime
from typing import List, Optional, Set, Tuple

from .errors import AttributeDeriverError

# compile
DATE_FMT_YEAR_FIRST_DASH = re.compile(r"\d{4}-\d{2}-\d{2}")
DATE_FMT_YEAR_FIRST_SLASH = re.compile(r"\d{4}/\d{2}/\d{2}")
DATE_FMT_YEAR_LAST_DASH = re.compile(r"\d{2}-\d{2}-\d{4}")
DATE_FMT_YEAR_LAST_SLASH = re.compile(r"\d{2}/\d{2}/\d{4}")


def datetime_from_form_date(date_string: Optional[str]) -> Optional[datetime]:
    """Converts date string to datetime based on format.

    Args:
      date_string: the date string
    Returns:
      the date as datetime
    """
    if not date_string:
        return None

    try:
        # YYYY-MM-DD format
        if DATE_FMT_YEAR_FIRST_DASH.match(date_string):
            return datetime.strptime(date_string, "%Y-%m-%d")

        # YYYY/MM/DD format
        elif DATE_FMT_YEAR_FIRST_SLASH.match(date_string):
            return datetime.strptime(date_string, "%Y/%m/%d")

        # MM-DD-YYYY
        elif DATE_FMT_YEAR_LAST_DASH.match(date_string):
            return datetime.strptime(date_string, "%m-%d-%Y")

        # MM/DD/YYYY
        elif DATE_FMT_YEAR_LAST_SLASH.match(date_string):
            return datetime.strptime(date_string, "%m/%d/%Y")

        raise AttributeDeriverError(f"Invalid date format: {date_string}")

    except ValueError as e:
        raise AttributeDeriverError(f"Failed to parse date {date_string}: {e}") from e


def date_from_form_date(date_string: Optional[str]) -> Optional[date]:
    result = datetime_from_form_date(date_string)
    if result:
        return result.date()

    return None


def parse_date_parts(
    date_string: Optional[str],
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Parse dates even if parts are unknown, e.g. 9999-99-99.

    Return year, month, day
    """
    if date_string is None:
        return None, None, None

    # get dates parts in the correct order
    date_parts = None

    # YYYY-MM-DD format
    if DATE_FMT_YEAR_FIRST_DASH.match(date_string):
        date_parts = date_string.split("-")

    # YYYY/MM/DD format
    elif DATE_FMT_YEAR_FIRST_SLASH.match(date_string):
        date_parts = date_string.split("/")

    # MM-DD-YYYY
    elif DATE_FMT_YEAR_LAST_DASH.match(date_string):
        date_parts = date_string.split("-")
        date_parts = [date_parts[2], date_parts[0], date_parts[1]]

    # MM/DD/YYYY
    elif DATE_FMT_YEAR_LAST_SLASH.match(date_string):
        date_parts = date_string.split("/")
        date_parts = [date_parts[2], date_parts[0], date_parts[1]]

    if not date_parts:
        raise AttributeDeriverError(f"Unparsable date string: {date_string}")

    return int(date_parts[0]), int(date_parts[1]), int(date_parts[2])


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
    years = [date_from_form_date(x) for x in dates]
    return set(x.year for x in years if x is not None)


def standardize_date(date_value: Optional[str | date]) -> Optional[str]:
    """Standardize date to YYYY-MM-DD format, if provided."""
    if not isinstance(date_value, date):
        date_value = date_from_form_date(date_value)

    if not date_value:
        return None

    return str(date_value)


def find_closest_date(
    raw_dates: List[str], raw_target_date: str, as_date: bool = False
) -> Tuple[str | date, int]:
    """Find the value and index of the closet date in the list of dates to the
    given target date."""
    if not raw_dates:
        raise AttributeDeriverError("Dates list is empty; cannot find closet date")

    # convert all to datetime objects
    target = date_from_form_date(raw_target_date)
    dates = [date_from_form_date(x) for x in raw_dates]

    if not target or any(x is None for x in dates):
        raise AttributeDeriverError(
            "Failed to convert all dates to datetime objects; cannot "
            + "find closest date"
        )

    index = min(range(len(dates)), key=lambda i: abs(dates[i] - target))  # type: ignore
    result = standardize_date(raw_dates[index])

    if not result:
        raise AttributeDeriverError(f"Failed to standardize {raw_dates[index]}")

    if as_date:
        return (dates[index], index)  # type: ignore

    return (result, index)


def make_date_from_parts(
    year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None
) -> Optional[str]:
    """Make date from part variables.

    If all are missing, returns None. Else, if only some parts are
    missing, set missing parts to 9999-99-99. Return as a string in
    YYYY-MM-DD format.
    """
    # if none are set, return None
    if all(x is None for x in [year, month, day]):
        return None

    # otherwise build the date; set anything missing to 9999-99-99
    if not year:
        year = 9999
    if not month:
        month = 99
    if not day:
        day = 99

    # return in YYYY-MM-DD format
    return f"{year:04d}-{month:02d}-{day:02d}"


def approximate_date(date_string: Optional[str]) -> Optional[str]:
    """Approximate a date if the day is unknown.

    If only the day is unknown (e.g. 2025-05-99), approximate by setting the
    day value to 15. Done to estimate time differences.

    Returns the approximate date if it is created, otherwise just returns
    the date as-is.
    """
    if not date_string:
        return None

    if date_string.endswith("-99") or date_string.endswith("-88"):
        year, month, day = parse_date_parts(date_string)
        if year not in [8888, 9999] and month not in [88, 99] and day in [88, 99]:
            return f"{year:4d}-{month:02d}-15"

    return date_string
