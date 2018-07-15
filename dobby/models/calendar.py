import re
from datetime import datetime, timedelta
from enum import Enum, Flag
from typing import Optional, Pattern, Union

__all__ = ["EVERY", "Calendar", "Interval"]

_DEFAULT = object()
RE_PARSER: Pattern = re.compile(r"^(@?\d+|\*)([a-zA-Z])$")


class Interval(Flag):
    START = 0


class ReprMap(Enum):
    year = "y"
    month = "m"
    week = "w"
    day = "d"
    hour = "H"
    minute = "M"
    second = "S"


class EVERY:
    interval: int

    def __init__(self, interval=1):
        self.interval = interval

    def __repr__(self) -> str:
        return "*" if self.interval == 1 else str(self.interval)


IntervalValue = Union[int, Interval]

INTERVALS = ("year", "month", "week", "day", "hour", "minute", "second")

PRESETS = [
    (("yearly", "every_year"), dict(year=Interval.START)),
    (("monthly", "every_month"), dict(month=Interval.START)),
    (("weekly", "every_week"), dict(week=Interval.START)),
    (("daily", "every_day"), dict(day=Interval.START)),
    (("hourly", "every_hour"), dict(hour=Interval.START)),
    (("minutely", "every_minute"), dict(minute=Interval.START)),
    (("secondly", "every_second"), dict(second=Interval.START)),
]


def find_preset(key: str) -> Optional[dict]:
    key = key.lower()
    return next((value for keys, value in PRESETS if key in keys), None)


def set_datetime_prop(dt: datetime, month_anchor: bool, **changes) -> datetime:
    day = changes.pop("day", None)
    if day is not None:
        if month_anchor:
            changes["day"] = day + 1
        else:
            diff = day - dt.weekday()
            dt = dt + timedelta(days=diff)

    month = changes.pop("month", None)
    if month is not None:
        changes["month"] = month + 1

    week = changes.pop("week", None)
    if week is not None:
        diff = week - get_datetime_prop(dt, month_anchor, "week")
        dt = dt + timedelta(weeks=diff)

    return dt.replace(**changes)


def get_datetime_prop(dt: datetime, month_anchor: bool, prop: str) -> int:
    if prop == "week":
        return dt.day // 7 + 1 if month_anchor else dt.isocalendar()[1]
    elif prop == "day":
        return dt.day - 1 if month_anchor else dt.weekday()
    elif prop == "month":
        return dt.month - 1

    return getattr(dt, prop)


class Calendar:
    month_anchor: bool
    year: IntervalValue
    month: Optional[IntervalValue]
    week: Optional[IntervalValue]
    day: IntervalValue
    hour: IntervalValue
    minute: IntervalValue
    second: IntervalValue

    def __init__(self, **kwargs):
        _found_value = False
        _found_start = False

        intervals = {key: value for key, value in kwargs.items() if key in INTERVALS}

        for interval in INTERVALS:
            value = 0

            if not _found_start:
                val = intervals.pop(interval, _DEFAULT)
                if val is not _DEFAULT:
                    if interval == "week":
                        self.month = None

                    if val == Interval.START:
                        _found_start = True
                        value = EVERY()
                    else:
                        if not intervals:
                            _found_value = True
                        value = val
                elif interval == "week":
                    value = None
                elif not _found_value:
                    value = EVERY()
            setattr(self, interval, value)

        self.month_anchor = self.month is not None

    def __repr__(self) -> str:
        int_details = []
        for interval in INTERVALS:
            val = getattr(self, interval)
            if not val:
                continue

            if isinstance(val, Interval):
                val = str(val.value)
            elif isinstance(val, EVERY):
                val = str(val)
            else:
                val = "@" + str(val)

            int_details.append(val + ReprMap[interval].value)

        return "[" + " ".join(int_details) + "]"

    @classmethod
    def from_config(cls, config: Union[str, dict]) -> "Calendar":
        if isinstance(config, str):
            preset = find_preset(config.lower().replace(" ", "_"))

            if not preset:
                preset = Calendar.parse_repr(config)

            if preset:
                return cls(**preset)

        raise NotImplementedError

    @staticmethod
    def parse_repr(rep: str) -> dict:
        rep = rep.strip("[] ")
        parts = rep.split()
        data = {}

        for part in parts:
            match = RE_PARSER.match(part)
            if not match:
                raise Exception(f"Couldn't parse part {part} of {rep}")

            spec, field_name = match.groups()
            if spec == "*":
                val = EVERY()
            elif spec.startswith("@"):
                val = int(spec[1:])
            elif spec.isnumeric():
                val = EVERY(int(spec))
            else:
                raise Exception(f"Couldn't interpret {spec} in {part} of {rep}")

            field = ReprMap(field_name).name
            data[field] = val

        return data

    def next_event(self, current: datetime) -> datetime:
        next_time = current.replace(microsecond=0)

        for interval in reversed(INTERVALS):
            value = getattr(self, interval)
            if isinstance(value, EVERY):
                current_value = get_datetime_prop(next_time, self.month_anchor, interval)
                last_value = value.interval * (current_value // value.interval)
                try:
                    next_time = set_datetime_prop(next_time, self.month_anchor, **{interval: last_value + value.interval})
                except ValueError:
                    next_time = set_datetime_prop(next_time, self.month_anchor, **{interval: value.interval})
                else:
                    break
            elif value is not None:
                next_time = set_datetime_prop(next_time, self.month_anchor, **{interval: value})
                if next_time > current:
                    break

        return next_time
