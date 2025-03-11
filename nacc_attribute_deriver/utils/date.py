"""Helper methods related to dates."""
import re
from datetime import datetime
from typing import Optional


def datetime_from_form_date(date_string: str) -> Optional[datetime]:
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


def calculate_age(d1: datetime, d2: datetime) -> Optional[int]:
    """Calculate age in years between two dates.

    Args:
        date1: The earlier date
        date2: The later date
    Returns:
        The age between the two dates in years
    """
    if not d1 or not d2:
        return None

    # use date objects, not doing division with leap year
    # since it's not always precise when visitdate == birthdate
    date1 = d1.date()
    date2 = d2.date()

    return (date2.year - date1.year) - \
           ((date2.month, date2.day) < (date1.month, date1.day))
