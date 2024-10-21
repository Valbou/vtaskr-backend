from datetime import time, timedelta
from unittest import TestCase

from src.libs.utils import time_to_seconds, timedelta_to_time
from src.libs.utils.exceptions import DateUtilConvertionError


class TestTimeToSeconds(TestCase):
    def test_time_hour_minutes_seconds(self):
        btime = time(hour=13, minute=42, second=7)
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 49_327)

    def test_str_hour_minutes_seconds(self):
        btime = "13:42:07"
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 49_327)

    def test_time_minutes_seconds(self):
        btime = time(minute=42, second=7)
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 2_527)

    def test_str_minutes_seconds(self):
        btime = "42:07"
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 2_527)

    def test_time_seconds(self):
        btime = time(second=7)
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 7)

    def test_str_seconds(self):
        btime = "07"
        result = time_to_seconds(to_convert=btime)

        self.assertEqual(result, 7)


class TestTimedeltaToTime(TestCase):
    def test_some_hours_delta(self):
        delta = timedelta(seconds=49_327)
        result = timedelta_to_time(to_convert=delta)

        self.assertIsInstance(result, time)
        self.assertEqual(result.hour, 13)
        self.assertEqual(result.minute, 42)
        self.assertEqual(result.second, 7)

    def test_some_hours_seconds(self):
        seconds = 49_327
        result = timedelta_to_time(to_convert=seconds)

        self.assertIsInstance(result, time)
        self.assertEqual(result.hour, 13)
        self.assertEqual(result.minute, 42)
        self.assertEqual(result.second, 7)

    def test_zero_seconds(self):
        seconds = 0
        result = timedelta_to_time(to_convert=seconds)

        self.assertIsInstance(result, time)
        self.assertEqual(result.hour, 0)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)

    def test_a_day_seconds(self):
        seconds = 86_400
        with self.assertRaises(DateUtilConvertionError):
            timedelta_to_time(to_convert=seconds)

    def test_negative_seconds(self):
        seconds = -1
        with self.assertRaises(DateUtilConvertionError):
            timedelta_to_time(to_convert=seconds)
