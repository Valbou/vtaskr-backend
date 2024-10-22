from datetime import time, timedelta

from .exceptions import DateUtilConvertionError


def time_to_seconds(to_convert: time | str) -> int:
    """
    Convert a time to seconds.

    Handle formats like:
    - %H:%M:%S
    - %M:%S
    - %S
    """

    if isinstance(to_convert, time):
        to_convert = str(to_convert)

    to_convert = to_convert.split(".")[0]

    return sum(
        [
            j * (60**i)
            for i, j in enumerate(reversed([int(i) for i in to_convert.split(":")]))
        ]
    )


def seconds_to_time(to_convert: int) -> time:
    """
    Time delta to duration conversion.
    Convert a small timedelta (< 86 400 seconds) to a time object.
    """

    if isinstance(to_convert, timedelta):
        to_convert = int(to_convert.total_seconds())

    if to_convert >= 86_400:
        raise DateUtilConvertionError(
            f"seconds_to_time cannot convert values over 24h: {to_convert}s given"
        )
    elif to_convert < 0:
        raise DateUtilConvertionError(
            "seconds_to_time cannot convert values under 0s"
            f"(negative values not admitted): {to_convert}s given"
        )

    def split_parts(total_seconds: int) -> tuple[int, int, int]:
        hours = total_seconds // 3600
        hours_rest = total_seconds / 3600 % 1
        minutes = hours_rest * 60 // 1
        minutes_rest = hours_rest * 60 % 1
        seconds = minutes_rest * 60

        return int(hours), int(minutes), int(seconds)

    hours, minutes, seconds = split_parts(to_convert)
    return time(hour=hours, minute=minutes, second=seconds)
