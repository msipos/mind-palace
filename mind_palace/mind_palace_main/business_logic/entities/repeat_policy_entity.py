import math
from typing import Optional


class RepeatPolicyType:
    NONE = 'none'
    HOURLY = 'hourly'
    DAILY = 'daily'


class TimeOfDay:
    MORNING = 'morning'
    EVENING = 'evening'


class RepeatPolicyEntity:
    def __init__(self, typ: str, hours: Optional[int] = None, days: Optional[int] = None,
                 time_of_day: Optional[str] = None):
        self.typ = typ
        self.hours = hours
        self.days = days
        self.time_of_day = time_of_day

        if typ == RepeatPolicyType.NONE:
            assert hours is None
            assert days is None
            assert time_of_day is None
        elif typ == RepeatPolicyType.HOURLY:
            assert isinstance(hours, int)
            assert hours > 0
            assert days is None
            assert time_of_day is None
        elif typ == RepeatPolicyType.DAILY:
            assert hours is None
            assert isinstance(days, int)
            assert days > 0
            assert time_of_day in [TimeOfDay.MORNING, TimeOfDay.EVENING]
        else:
            raise ValueError(f'Invalid type="{typ}"')

    def to_json(self) -> dict:
        d = {'type': self.typ}
        if self.hours is not None:
            d['hours'] = self.hours
        if self.days is not None:
            d['days'] = self.days
        if self.time_of_day is not None:
            d['timeOfDay'] = self.time_of_day
        return d

    @staticmethod
    def from_json(d: dict) -> 'RepeatPolicyEntity':
        typ = d['type']

        if typ == RepeatPolicyType.NONE:
            return RepeatPolicyEntity(typ)
        elif typ == RepeatPolicyType.DAILY:
            return RepeatPolicyEntity(typ, days=d['days'], time_of_day=d['timeOfDay'])
        elif typ == RepeatPolicyType.HOURLY:
            return RepeatPolicyEntity(typ, hours=d['hours'])
        else:
            raise ValueError(f'Invalid type="{typ}"')

    def to_human_readable(self) -> str:
        """ Human readable string. """
        if self.typ == RepeatPolicyType.NONE:
            return 'Never'
        elif self.typ == RepeatPolicyType.DAILY:
            if self.days == 1:
                return '1 day'
            else:
                return f'{self.days} days'
        elif self.typ == RepeatPolicyType.HOURLY:
            if self.hours == 1:
                return '1 hour'
            else:
                return f'{self.hours} hours'
        else:
            raise ValueError(f'Invalid type="{typ}"')

    @staticmethod
    def _apply_factor(value: Optional[int], factor: float):
        if value is None:
            return None
        if factor == 1.0:
            return value
        if factor < 1.0:
            if value == 1:
                return value
        return math.floor(value * factor)

    def copy(self, factor: float = 1.0) -> 'RepeatPolicyEntity':
        return RepeatPolicyEntity(
            self.typ,
            self._apply_factor(self.hours, factor),
            self._apply_factor(self.days, factor),
            self.time_of_day
        )
