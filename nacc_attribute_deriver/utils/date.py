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


def date_from_form_date(date_string: Optional[str]) -> Optional[date]:
    result = datetime_from_form_date(date_string)
    if result:
        return result.date()

    return None


def date_came_after(date1: date | None, date2: date | None) -> bool:
    """Compare relativity of two dates.
        If date1 came AFTER date2, or date2 is None returns True
        If date1 came BEFORE date2, or date1 is None returns False
        If dates are equal/both none, return False
    """
    if date1 == date2:
        return False

    return date2 is None or (date1 is not None and date1 > date2)


def date_came_after_sparse(
        date1: date | None,
        sparse_year = Optional[int],
        sparse_month = Optional[int],
        sparse_day = Optional[int]) -> bool:
    """Compare relativity of two dates, where date2 is sparse (e.g.
    some parts can be 99 or None.
        If date1 came AFTER date2, or date2 is None returns True
        If date1 came BEFORE date2, or date1 is None returns False
        If dates are equal/both none, return False

    """
    all_parts = [sparse_year, sparse_month, sparse_day]

    # if all sparse parts are None, this is not meaningful so just return
    # whether or not date1 is valid
    not_meaningful = [88, 99, 8888, 9999, None]
    if all(x in not_meaningful for x in all_parts):
        return date1 is not None

    # if date1 is None, but some sparse part is meaningful (which is true if we
    # got to this point), return True
    if date1 is None:
        return True

    # if ALL parts are valid, can check directly with date_came_after
    if all(x not in not_meaningful for x in all_parts):
        built_date = date(sparse_year, sparse_month, sparse_day)
        return date_came_after(date1, built_date)

    # finally check parts individual parts; need year to be defined to
    # be meaningful
    if sparse_year is not None and sparse_year != 9999:
        if date1.year > sparse_year:
            return True
        if date1.year < sparse_year:
            return False

        # If year tied, check month. if tied again, assume sparse date came later
        # and return False (kind of arbitrary but far more likely for our use cases,
        # e.g. in MLST they really did discontinue instead of suddenly rejoined within
        # a few days via another form)
        #   - don't check further if month is 99 as well; for the same reason
        #     that it's kind of arbitrary to check the day
        if (sparse_month is not None and (1 <= sparse_month <= 12)):
            if date1.month > sparse_month:
                return True
            return False

    # assume true by default (by date2 not being meaningful enough to decide)
    return True


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

    return date_from_form_date(f"{dyr}-{dmo:02d}-{ddy:02d}")
