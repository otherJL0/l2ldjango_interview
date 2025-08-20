from functools import singledispatch
from datetime import datetime

from django import template

register = template.Library()
template.defaultfilters

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"
DISPLAY_FORMAT = "%Y-%m-%d %H:%M:%S"


@register.filter
@singledispatch
def l2l_dt(value: datetime | str) -> str:
    """Convert datetime objects or ISO format strings to display format"""
    return str(value)


@l2l_dt.register
def _(value: datetime) -> str:
    """Format a datetime object to display format"""
    return value.strftime(DISPLAY_FORMAT)


@l2l_dt.register
def _(value: str) -> str:
    """Parse an ISO datetime string and format to display format"""
    try:
        now: datetime = datetime.strptime(value, ISO_FORMAT)
        return now.strftime(DISPLAY_FORMAT)
    except ValueError:
        return f"Incorrectly formatted: {value}"
