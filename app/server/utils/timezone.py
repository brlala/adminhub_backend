from datetime import datetime

from pytz import timezone

from app.server.core.server_config import db_config


def make_timezone_aware(dt: datetime):
    singapore = timezone(db_config.portal.region)
    return singapore.localize(dt)