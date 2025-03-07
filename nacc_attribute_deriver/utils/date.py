"""
Helper methods related to dates.
"""
import re
from datetime import datetime, timedelta


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


def calculate_age(date1: datetime, date2: datetime) -> int:
    """Calculate age in years between two dates

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
    date1 = date1.date()
    date2 = date2.date()

    return (date2.year - date1.year) - \
           ((date2.month, date2.day) < (date1.month, date1.day))
