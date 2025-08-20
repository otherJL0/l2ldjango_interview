from datetime import datetime
from typing import Literal, get_args

from django.test import TestCase

from l2l.templatetags.l2l_extras import DISPLAY_FORMAT, ISO_FORMAT, l2l_dt


class DatetimeTestCase(TestCase):
    """
    Custom TestCase class for datetime comparison
    """

    DatetimeResolution = Literal[
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
    ]

    def assertDtEqual(
        self,
        expected: datetime,
        actual: datetime,
        resolution: DatetimeResolution = "second",
    ):
        """Assert two datetime objects are equal up to a certain resolution"""
        for unit in get_args(self.DatetimeResolution):
            self.assertEqual(
                getattr(expected, unit),
                getattr(actual, unit),
                f"{expected} {actual} do not match at {unit} resolution",
            )
            if unit == resolution:
                break


class DisplayFormatTestCase(DatetimeTestCase):
    """l2l_dt test suite"""

    def test_datetime_now(self):
        """Test datetime objects are formatted correctly"""
        now = datetime.now()
        displayed = l2l_dt(now)
        displayed_dt = datetime.strptime(displayed, DISPLAY_FORMAT)
        self.assertDtEqual(now, displayed_dt)

    def test_isoformatted_string(self):
        """Test ISO formatted strings are convertted correctly"""
        now = datetime.now()
        now_iso = now.strftime(ISO_FORMAT)
        displayed = l2l_dt(now_iso)
        displayed_dt = datetime.strptime(displayed, DISPLAY_FORMAT)
        self.assertDtEqual(now, displayed_dt)

    def test_incorrectly_formatted_string(self):
        """Test incorrectly formatted strings return `Incorrectly formatted` prefix"""
        now = datetime.now()
        invaid_format = "%Y-%m-%d"
        now_iso = now.strftime(invaid_format)
        displayed = l2l_dt(now_iso)
        self.assertTrue(displayed.startswith("Incorrectly formatted"))

    def test_consistency(self):
        """Test datetime objects and ISO formatted strings return the same format"""
        now = datetime.now()
        now_iso = now.strftime(ISO_FORMAT)
        self.assertEqual(l2l_dt(now), l2l_dt(now_iso))
