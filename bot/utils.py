from datetime import datetime
from pytz import timezone


LOCAL_TZ = timezone('Europe/Moscow')


def localize_time(dt: datetime) -> str:
    """
    Локализует объект datetime по часовому поясу LOCAL_TZ.
    """
    utc_dt = dt.replace(tzinfo=timezone('UTC'))
    loc_dt = utc_dt.astimezone(LOCAL_TZ)
    return loc_dt.strftime('%H:%M %d.%m.%Y')


def get_next_smoking_time(last: datetime, last_but_one: datetime) -> str:
    next_time = last - last_but_one + last
    return localize_time(next_time)
