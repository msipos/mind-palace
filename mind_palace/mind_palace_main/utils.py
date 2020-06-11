import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from jinja2.environment import Environment


def jinja_environment(**options):
    if settings.DEBUG is True:
        options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'urlencode': urlencode,
    })
    return env


class AuthorizationError(Exception):
    pass


def pretty_format_hours(hours: int):
    return pretty_format_timedelta(datetime.timedelta(hours=hours))


def pretty_format_timedelta(td: datetime.timedelta):
    seconds = int(td.total_seconds())
    periods = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
    ]

    minus = seconds < 0
    if minus:
        seconds *= -1
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    if minus:
        return '-' + (", ".join(strings))
    else:
        return ", ".join(strings)
