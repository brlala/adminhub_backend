from datetime import datetime, date, time
from typing import Union

from pytz import timezone

from app.server.core.env_variables import local_config


def make_timezone_aware(dt: Union[datetime, date]):
    midnight = dt
    if isinstance(dt, date):
        midnight = datetime.combine(dt, time.min)
    singapore = timezone(local_config.TIMEZONE)
    return singapore.localize(midnight)


def get_local_datetime_now():
    return make_timezone_aware(datetime.now())
