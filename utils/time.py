from datetime import datetime, timezone


API_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DISPLAY_FORMAT = "%m/%d/%Y %H:%M:%S"


def convert_dt(dt: str) -> int:
    """ Convert API datetime format to unix timestamp """
    dt_utc = datetime.strptime(dt, API_FORMAT).replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(tz=None)  # Discord expects local time
    return int(dt_local.timestamp())


def now() -> int:
    """ Return current time as Unix timestamp """
    return int(datetime.now().timestamp())


def now_str() -> str:
    """ Return current time as formatted string """
    return datetime.now().strftime(DISPLAY_FORMAT)
