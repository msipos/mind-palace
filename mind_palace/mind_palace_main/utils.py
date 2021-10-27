import datetime
import logging
import time
from typing import Optional, Tuple, Dict, Set
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse
from jinja2.environment import Environment
from geoip import geolite2

logger = logging.getLogger(__name__)


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


def get_client_ip(request: HttpRequest) -> Optional[str]:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class GeoIp:
    def __init__(self, country: str, timezone: str, last_date: Optional[datetime.date] = None):
        self.country = country
        self.timezone = timezone
        if last_date is None:
            self.last_date = datetime.date.today()
        else:
            self.last_date = last_date

    @staticmethod
    def from_ip(ip: str) -> 'GeoIp':
        match = geolite2.lookup(ip)
        country = 'Unknown'
        timezone = 'Unknown'
        if match is not None:
            country = match.country
            timezone = match.timezone
        return GeoIp(country, timezone)

    def to_tuple(self) -> Tuple[str, str, str]:
        return self.country, self.timezone, self.last_date.strftime('%Y-%m-%d')

    @staticmethod
    def from_tuple(t: Tuple[str, str, str]) -> 'GeoIp':
        return GeoIp(t[0], t[1], datetime.datetime.strptime(t[2], '%Y-%m-%d').date())


class IpRecord:
    def __init__(self, current_ip, username):
        self.current_ip = current_ip
        self.username = username
        logger.info(f'Username: {self.username} IP: {self.current_ip}')

        if self.current_ip is None:
            logger.warning(f'No IP for user: {username}')

        self.ip_map: Dict[str, GeoIp] = {}

    @staticmethod
    def on_request(request):
        return IpRecord(get_client_ip(request), username=request.user.username)

    def _get_cache_key(self) -> str:
        return f'ip_record_{self.username}'

    def cache_update(self, today: Optional[datetime.date] = None):
        """ Read from cache and update ip_map. """
        current_cache_dict = cache.get(self._get_cache_key(), default={})

        if today is None:
            today = datetime.date.today()

        for ip, t in current_cache_dict.items():
            self.ip_map[ip] = GeoIp.from_tuple(t)

        # Do we need to update the cache
        needs_updating = False
        if self.current_ip is not None:
            # Existing ip
            if self.current_ip in self.ip_map:
                if self.ip_map[self.current_ip].last_date < today:
                    self.ip_map[self.current_ip].last_date = today
                    needs_updating = True
            else:
                self.ip_map[self.current_ip] = GeoIp.from_ip(self.current_ip)
                needs_updating = True

        # Do we need to evict the cache?
        ips_to_remove: Set[str] = set()
        eviction_date = today - datetime.timedelta(days=7)
        for ip, geoip in self.ip_map.items():
            if geoip.last_date <= eviction_date:
                ips_to_remove.add(ip)
        if len(ips_to_remove) > 0:
            needs_updating = True
            for ip in ips_to_remove:
                del self.ip_map[ip]

        # Do we need to update the cache?
        if needs_updating:
            cache_value = {}
            for ip, geoip in self.ip_map.items():
                cache_value[ip] = geoip.to_tuple()
            cache.set(self._get_cache_key(), cache_value, timeout=7*24*60*60)


def update_ip_record(request) -> dict:
    """ Updates the IP record for this user and returns it.  """
    ip = get_client_ip(request)
    username = request.user.username



