from datetime import datetime

from pytz import timezone

from app.server.core.env_variables import local_config
from app.server.core.server_config import db_config


def make_timezone_aware(dt: datetime):
    singapore = timezone(local_config.TIMEZONE)
    return singapore.localize(dt)
