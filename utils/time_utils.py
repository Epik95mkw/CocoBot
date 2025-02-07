from datetime import datetime, timezone


def to_timestamp(dt: str) -> int:
    """ Convert API datetime format to unix timestamp """
    dt_utc = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(tz=None)  # Discord expects local time
    return int(dt_local.timestamp())

def now() -> int:
    """ Return current time as Unix timestamp """
    return int(datetime.now().timestamp())
