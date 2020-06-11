import datetime
from time import time

import pytz
from django.conf import settings

utc = pytz.timezone('UTC')
local_tz = pytz.timezone(settings.TIME_ZONE)
start_time = datetime.datetime(1970, 1, 1, tzinfo=utc)  # tzinfo works for UTC only


def timestamp_now() -> int:
    return int(time())


def localtime_now() -> datetime.datetime:
    return timestamp_to_localtime(timestamp_now())


def timestamp_to_localtime(ts: int) -> datetime.datetime:
    """ Timestamp is proper unix time. Converts it into a local time with correctly assigned tzinfo. """
    utc_datetime = start_time + datetime.timedelta(seconds=ts)
    local_datetime = utc_datetime.astimezone(local_tz)
    return local_datetime


def make_localtime(year: int, month: int, day: int, hour: int, minute=0):
    naive_datetime = datetime.datetime(year, month, day, hour, minute)
    local_datetime = local_tz.localize(naive_datetime)
    return local_datetime


def localtime_to_timestamp(d: datetime.datetime) -> int:
    return int(d.astimezone(utc).timestamp())
